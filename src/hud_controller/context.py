import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Iterator

from datasets import load_dataset
from hud.server.context import run_context_server

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)


class HumanEvalEnvironment():
    """Simple HumanEval+ environment with iteration and batch support."""

    def __init__(self):
        self.task_cache: Dict[str, Dict[str, Any]] = {}
        self.task_ids: List[str] = []

    def load_dataset(self) -> None:
        """Load the HumanEval+ dataset and cache all tasks."""
        if self.task_cache:
            return

        logging.info("Loading HumanEval+ dataset...")
        dataset = load_dataset("evalplus/humanevalplus")

        # Cache all tasks for quick lookup
        self.task_cache = {task["task_id"]: task for task in dataset["test"]}
        self.task_ids = sorted(self.task_cache.keys())
        
        logging.info(f"Loaded and cached {len(self.task_cache)} tasks from HumanEval+")

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID."""
        return self.task_cache.get(task_id)

    def size(self) -> int:
        """Return the total number of tasks (proxy-safe alternative to __len__)."""
        return len(self.task_ids)
    
    def get_task_by_index(self, index: int) -> Dict[str, Any]:
        """Get a task by index (proxy-safe alternative to __getitem__)."""
        if index < 0:
            index += len(self.task_ids)
        if not 0 <= index < len(self.task_ids):
            raise IndexError(f"Index {index} out of range")
        task_id = self.task_ids[index]
        return self.task_cache[task_id]
    
    def get_tasks_slice(self, start: int, end: int) -> List[Dict[str, Any]]:
        """Get a slice of tasks (proxy-safe alternative to __getitem__ with slice)."""
        end = min(end, len(self.task_ids))
        start = max(0, start)
        return [self.task_cache[tid] for tid in self.task_ids[start:end]]
    
    def get_all_task_ids(self) -> List[str]:
        """Get list of all task IDs."""
        return self.task_ids.copy()


async def main():
    """Main function to start the context server."""
    ctx = HumanEvalEnvironment()
    ctx.load_dataset()

    logging.info("Starting context server...")
    await run_context_server(ctx, "/tmp/hud_humanevalplus_ctx.sock")


if __name__ == "__main__":
    asyncio.run(main())
