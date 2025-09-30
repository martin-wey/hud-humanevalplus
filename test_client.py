import asyncio
import hud
from hud.datasets import Task
from hud.agents import ClaudeAgent
from hud.clients import MCPClient

async def main():
    task = Task(
        prompt="Complete the task",
        mcp_config={
            "local": {
                "command": "docker", 
                "args": ["run", "--rm", "-i", "humanevalplus:dev"]
            }
        }
    )
    client = MCPClient(mcp_config=task.mcp_config)
    await client.initialize()

asyncio.run(main())
