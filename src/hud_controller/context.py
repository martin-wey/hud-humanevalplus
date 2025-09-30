import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from datasets import load_dataset
from hud.server.context import run_context_server

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)


class HumanEvalEnvironment:
    """Manages the HumanEval+ environment state."""

    def __init__(self):
        self.dataset: Optional[Dict[str, Any]] = None
        self.current_task: Optional[Dict[str, Any]] = None
        self.task_cache: Dict[str, Dict[str, Any]] = {}

    def load_dataset(self) -> None:
        """Load the HumanEval+ dataset and cache all tasks."""
        if self.dataset is None:
            logging.info("Loading HumanEval+ dataset...")
            self.dataset = load_dataset("evalplus/humanevalplus")

            # Cache all tasks for quick lookup
            for task in self.dataset["test"]:
                self.task_cache[task["task_id"]] = task

            logging.info(
                f"Loaded and cached {len(self.task_cache)} tasks from HumanEval+"
            )

    def get_task_cache(self) -> Dict[str, Dict[str, Any]]:
        """Get the task cache."""
        return self.task_cache

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID."""
        return self.task_cache.get(task_id)

    def set_current_task(self, task: Dict[str, Any]) -> None:
        """Set the current active task."""
        self.current_task = task

    def get_current_task(self) -> Optional[Dict[str, Any]]:
        """Get the current active task."""
        return self.current_task


async def main():
    """Main function to start the context server."""
    ctx = HumanEvalEnvironment()
    ctx.load_dataset()

    logging.info("Starting context server...")
    await run_context_server(ctx, "/tmp/hud_humanevalplus_ctx.sock")


if __name__ == "__main__":
    asyncio.run(main())
