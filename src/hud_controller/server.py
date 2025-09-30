import sys
import logging

from datasets import load_dataset
from hud.server import MCPServer


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)

mcp = MCPServer(name="hud-humanevalplus")

@mcp.tool
async def setup():
    logging.info("Mock tool.")

@mcp.initialize()
async def initialize_environment(session=None, progress_token=None):
    logging.info("Loading HF dataset.")
    logging.info("TEST HOT RELOAD.")
    dataset = load_dataset("evalplus/humanevalplus")
    logging.info(f"Loaded {len(dataset)} tasks.")


if __name__ == "__main__":
    
    mcp.run()
