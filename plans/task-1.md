# Task 1 Plan

## LLM Provider
Qwen Code API (local proxy on VM, port 42005).
Model: qwen3-coder-plus.

## Architecture
1. Parse question from sys.argv[1]
2. Send to LLM via OpenAI-compatible API
3. Print JSON with answer and tool_calls to stdout