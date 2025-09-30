import sys
import logging
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

from datasets import load_dataset
from hud.server import MCPServer
from hud.server.context import attach_context

from .context import HumanEvalEnvironment


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)

mcp = MCPServer(name="hud-humanevalplus")
env: Optional[HumanEvalEnvironment] = None


@mcp.tool
async def get_tasks(start_index: int = 0, count: int = 10) -> dict:
    """
    Get tasks from the dataset starting at a specific index.
    Client is responsible for tracking position.
    
    Args:
        start_index: Index to start from (0-based, default: 0)
        count: Number of tasks to retrieve (default: 10)
    """
    global env
    
    if env is None:
        return {"error": "Environment not initialized"}
    
    try:
        total_tasks = env.size()
        start = max(0, min(start_index, total_tasks))
        end = min(start + count, total_tasks)

        tasks_batch = env.get_tasks_slice(start, end)
        
        streamed_tasks = [
            {
                "task_id": task["task_id"],
                "prompt": task["prompt"],
                "test": task["test"],
                "entry_point": task["entry_point"],
                "canonical_solution": task["canonical_solution"]
            }
            for task in tasks_batch
        ]
        
        return {
            "tasks": streamed_tasks,
            "has_more": end < total_tasks,
            "next_index": end
        }
        
    except Exception as e:
        logging.error(f"Get tasks failed: {e}", exc_info=True)
        return {"error": f"Get tasks failed: {str(e)}"}


@mcp.tool
async def get_dataset_info() -> dict:
    """Get information about the dataset."""
    global env
    
    if env is None:
        return {"error": "Environment not initialized"}
    
    total = env.size()
    all_ids = env.get_all_task_ids()
    
    return {
        "total_tasks": int(total),
        "sample_task_ids": all_ids[:10],
        "message": f"Dataset contains {total} tasks"
    }


@mcp.initialize()
async def initialize_environment(session=None, progress_token=None):
    """Initialize the environment."""
    global env
    logging.info("Initializing HumanEval+ environment...")

    socket_path = Path("/tmp/hud_humanevalplus_ctx.sock")

    async def wait_for_socket():
        while not socket_path.exists():
            await asyncio.sleep(0.1)

    try:
        await asyncio.wait_for(wait_for_socket(), timeout=30)
        logging.info("Context server socket ready, connecting...")
        env = attach_context("/tmp/hud_humanevalplus_ctx.sock")
        logging.info("Environment ready!")
    except asyncio.TimeoutError:
        raise RuntimeError(f"Context server socket not ready after 30 seconds")


if __name__ == "__main__":
    mcp.run()
