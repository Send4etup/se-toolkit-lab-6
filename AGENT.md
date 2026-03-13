# AGENT.md

## Overview
CLI agent with an agentic loop. Reads project wiki to answer questions.

## LLM Provider
Qwen Code API — local proxy, OpenAI-compatible, 1000 free requests/day.
Model: qwen3-coder-plus.

## How to run
```bash
uv run agent.py "Your question here"
```

## Output format
```json
{"answer": "...", "source": "wiki/file.md#section", "tool_calls": [...]}
```

## Tools
- `read_file(path)` — reads a file from the project. Blocks path traversal outside project root.
- `list_files(path)` — lists directory contents. Blocks path traversal outside project root.

## Agentic loop
1. Send question + tool schemas to LLM
2. LLM returns tool_calls → execute, feed results back, repeat
3. LLM returns text → parse answer and source, output JSON
4. Hard limit: 10 tool calls

## System prompt strategy
LLM is instructed to use list_files first to discover wiki files, then read_file to find the answer, and end response with SOURCE: path#anchor.

## Configuration
`.env.agent.secret`:
- `LLM_API_KEY`
- `LLM_API_BASE`
- `LLM_MODEL`