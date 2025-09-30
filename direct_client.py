#!/usr/bin/env python3
"""Direct access to HumanEvalEnvironment without MCP."""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from hud_controller.context import HumanEvalEnvironment

def process_task(task_data):
    """Process a single task."""
    print(f"Processing {task_data['task_id']}: {task_data['entry_point']}")
    # Your task processing logic here
    pass

def iterate_sequentially():
    """Iterate through all tasks sequentially."""
    print("🔄 Sequential Iteration")
    print("=" * 40)
    
    env = HumanEvalEnvironment()
    env.load_dataset()
    
    print(f"Total tasks: {len(env)}")
    
    # Method 1: For loop (cleanest)
    print("\nMethod 1: For loop")
    count = 0
    for task in env:
        if count >= 5:  # Stop after 5 for demo
            break
        process_task(task)
        count += 1
    
    # Method 2: Manual iteration
    print("\nMethod 2: Manual iteration")
    iterator = iter(env)
    count = 0
    while count < 5:  # Stop after 5 for demo
        try:
            task = next(iterator)
            process_task(task)
            count += 1
        except StopIteration:
            print("No more tasks")
            break

def iterate_in_batches():
    """Iterate through tasks in batches."""
    print("\n🔄 Batch Iteration")
    print("=" * 40)
    
    env = HumanEvalEnvironment()
    env.load_dataset()
    
    batch_size = 10
    total_tasks = len(env)
    
    print(f"Total tasks: {total_tasks}, Batch size: {batch_size}")
    
    # Process in batches
    for start_idx in range(0, total_tasks, batch_size):
        batch = env.get_batch(start_idx, batch_size)
        print(f"\nBatch {start_idx//batch_size + 1}: {len(batch)} tasks")
        
        for task in batch:
            process_task(task)
        
        # Stop after 2 batches for demo
        if start_idx + batch_size >= 20:
            break

def multithreading_example():
    """Example of how to use batches for multithreading."""
    print("\n🔄 Multithreading Example")
    print("=" * 40)
    
    import threading
    import time
    
    env = HumanEvalEnvironment()
    env.load_dataset()
    
    def worker_thread(thread_id, start_idx, batch_size):
        """Worker function for a thread."""
        batch = env.get_batch(start_idx, batch_size)
        print(f"Thread {thread_id}: Processing {len(batch)} tasks starting from {start_idx}")
        
        for task in batch:
            print(f"Thread {thread_id}: {task['task_id']}")
            time.sleep(0.1)  # Simulate work
        
        print(f"Thread {thread_id}: Completed")
    
    # Create 3 threads, each processing 5 tasks
    threads = []
    batch_size = 5
    
    for i in range(3):
        start_idx = i * batch_size
        thread = threading.Thread(
            target=worker_thread,
            args=(i, start_idx, batch_size)
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("All threads completed!")

def main():
    """Run all examples."""
    print("🚀 HumanEval+ Iteration Examples")
    print("=" * 50)
    
    try:
        iterate_sequentially()
        iterate_in_batches()
        multithreading_example()
        
        print("\n✅ All examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
