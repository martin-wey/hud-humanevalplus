import asyncio
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

        print("\n2. Testing list_tasks tool...")
        tasks_result = await client.call_tool(name="list_tasks")
        print(f"Available tasks: {tasks_result}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.shutdown()
        print("\n✅ Test completed")


async def main():
    await test_environment_manual()


if __name__ == "__main__":
    asyncio.run(main())
