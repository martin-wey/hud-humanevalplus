import asyncio
import json

import hud
from hud.datasets import Task
from hud.agents import ClaudeAgent
from hud.clients import MCPClient


async def test_environment_manual():
    """Test the HumanEval+ environment step by step."""
    print("🧪 Testing HumanEval+ Environment")
    print("=" * 50)

    mcp_config = {
        "local": {
            "command": "docker",
            "args": ["run", "--rm", "-i", "humanevalplus:dev"],
        }
    }

    client = MCPClient(mcp_config=mcp_config)

    try:
        print("1. Initializing MCP client...")
        await client.initialize()
        print("✅ Client initialized successfully")

        dataset_info = await client.call_tool(name="get_dataset_info")
        dataset_info = json.loads(dataset_info.content[0].text)
        dataset_len = dataset_info["total_tasks"]
        
        for i in range(dataset_len):
            task = await client.call_tool(name="get_tasks", arguments={"start_index": i, "count": 1})
            print(task)
            print("--------------------------------")


    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.shutdown()
        print("\n✅ Test completed")


async def main():
    await test_environment_manual()


if __name__ == "__main__":
    asyncio.run(main())
