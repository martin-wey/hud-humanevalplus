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


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)

mcp = MCPServer(name="hud-humanevalplus")
env = None  # persistent HumanEval+ dataset


@mcp.tool
async def list_tasks() -> dict:
    global env

    # this should never happen
    if env is None:
        return {
            "error": "Environment not initialized. Please wait for initialization to complete."
        }

    tasks = env.get_task_cache()
    # show first 3 tasks as examples
    tasks_info = []
    for task_id, task_data in list(tasks.items())[:3]:
        tasks_info.append(
            {
                "task_id": task_id,
                "description": task_data["prompt"][:100] + "...",
                "entry_point": task_data["entry_point"],
            }
        )

    return {
        "total_tasks": len(tasks),
        "sample_tasks": tasks_info,
        "message": f"Showing first 3 of {len(tasks)} available tasks",
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
