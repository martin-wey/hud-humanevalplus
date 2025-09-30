import asyncio
import json

import hud
from hud.datasets import Task
from hud.agents import ClaudeAgent
from hud.clients import MCPClient


async def test_environment_manual():
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

        has_samples = True
        i = 0
        while has_samples:
            tasks = await client.call_tool(
                name="get_tasks", arguments={"start_index": i, "count": 1}
            )
            tasks_data = json.loads(tasks.content[0].text)["tasks"]

            for task in tasks_data:
                print(task["prompt"])
                print("--------------------------------")

                # 1. Prompt storage.
                # 2. Generate a response using Claude Agent.
                # 3. Manually call check_correctness tool (todo: implemented) to evaluate correctness of generated code.

            has_samples = tasks_data["has_more"]
            i = tasks_data["next_index"]

            exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.shutdown()
        print("\n✅ Test completed")


async def main():
    await test_environment_manual()


if __name__ == "__main__":
    asyncio.run(main())
