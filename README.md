# HumanEval+ Iterative Coding Environment

A simple, streamlined environment for testing LLM agents on HumanEval+ coding problems with iterative feedback.

## 🎯 **Simple Workflow**

1. **Setup Task**: Load a HumanEval+ task and get its details
2. **Generate Code**: LLM generates code (no file I/O needed)
3. **Extract Code**: Post-process the response to extract clean code
4. **Check Correctness**: Test the code against test cases

## 🚀 **Quick Start**

### 1. Test Tools
```bash
cd /Users/martinweyssow/Documents/hud-python/hud-humanevalplus
uv run test_simple_tools.py
```

### 2. Run Simple Agent
```bash
uv run simple_client.py
```

### 3. Run Multiple Tasks
```bash
uv run simple_client.py multiple
```

## 🛠️ **Available Tools**

### `list_tasks()`
- Lists available HumanEval+ tasks
- Returns task IDs and descriptions

### `setup_task(task_id: str)`
- Loads a specific HumanEval+ task
- Returns task details (prompt, test cases, etc.)
- Sets the current task for testing

### `check_correctness(code: str)`
- Tests generated code against test cases
- Uses temporary directory for isolation
- Returns detailed test results and success rate

## 📊 **Example Output**

```
🚀 Solving task: HumanEval/0
==================================================
🔌 Initializing MCP client...
✅ Client initialized successfully
📋 Step 1: Setting up task HumanEval/0...
✅ Task loaded: Task HumanEval/0 loaded successfully
📝 Prompt: Complete the function has_close_elements...
🤖 Step 2: Generating code with LLM...
✅ Code generated (245 chars)
🔍 Step 3: Extracting code from response...
✅ Code extracted (156 chars)
🧪 Step 4: Checking correctness...
📊 Step 5: Results
✅ Success: True
📈 Success Rate: 100.0%
✅ Passed: 8
❌ Failed: 0
📊 Total: 8
💬 Message: Tests passed: 8/8 (100.0%)
```

## 🎯 **Key Benefits**

- **Simple**: No complex file I/O or workspace management
- **Isolated**: Each test runs in a temporary directory
- **Fast**: Direct code testing without file operations
- **Clean**: Clear separation between generation and testing
- **Extensible**: Easy to add iterative refinement later

## 🔄 **Future Enhancements**

- Add iterative refinement where agent can see test failures
- Add more sophisticated code extraction
- Add support for multiple programming languages
- Add performance metrics and benchmarking

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │    │   MCP Server     │    │  Context Server │
│                 │    │                  │    │                 │
│ • setup_task    │◄───┤ • setup_task     │◄───┤ • HumanEval+    │
│ • check_correct │◄───┤ • check_correct  │    │   Dataset       │
│ • list_tasks    │◄───┤ • list_tasks     │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

This demonstrates the core value of **environment evaluation** - agents can test their solutions and get feedback, enabling iterative improvement! 🚀