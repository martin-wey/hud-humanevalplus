#!/usr/bin/env python3
"""Hybrid approach: MCP environment with efficient iteration."""

import asyncio
import hud
from hud.clients import MCPClient

async def iterate_with_mcp():
    """Iterate through tasks using MCP but efficiently."""
    print("🔄 MCP Iteration")
    print("=" * 40)
    
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
        
        # Method 1: Iterate until no more tasks
        print("\nMethod 1: Iterate until completion")
        task_count = 0
        while True:
            task_data = await client.call_tool(name="next_task")
            
            if "error" in task_data:
                print(f"✅ Finished: {task_data['message']}")
                break
                
            print(f"Task {task_count + 1}: {task_data['task_id']} - {task_data['entry_point']}")
            task_count += 1
            
            # Process the task
            await process_task_with_mcp(client, task_data)
            
            # Stop after 5 for demo
            if task_count >= 5:
                print("Stopping after 5 tasks for demo...")
                break
        
        # Method 2: Get specific tasks by ID
        print("\nMethod 2: Get specific tasks")
        specific_tasks = ["HumanEval/0", "HumanEval/1", "HumanEval/2"]
        
        for task_id in specific_tasks:
            task_data = await client.call_tool("get_task", {"task_id": task_id})
            if "error" not in task_data:
                print(f"Got specific task: {task_data['task_id']}")
                await process_task_with_mcp(client, task_data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.shutdown()
        print("\n✅ MCP iteration completed")

async def process_task_with_mcp(client, task_data):
    """Process a task using MCP tools."""
    print(f"  Processing {task_data['task_id']}...")
    
    # Example: Generate some code and test it
    test_code = f'''def {task_data['entry_point']}(numbers, threshold):
    """Simple test implementation."""
    return True  # Placeholder'''
    
    # Test the code
    result = await client.call_tool("check_correctness", {"code": test_code})
    if "error" not in result:
        print(f"    Test result: {result['message']}")
    else:
        print(f"    Test error: {result['error']}")

async def main():
    """Main function."""
    await iterate_with_mcp()

if __name__ == "__main__":
    asyncio.run(main())
