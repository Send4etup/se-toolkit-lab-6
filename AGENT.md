# AGENT.md

## Overview
CLI agent that sends a question to an LLM and returns a JSON answer.

## LLM Provider
Qwen Code API — local proxy, OpenAI-compatible, 1000 free requests/day.
Model: qwen3-coder-plus.

## How to run
```bash
uv run agent.py "Your question here"
```

## Output format
```json
{"answer": "...", "tool_calls": []}
```

## Configuration
Copy `.env.agent.example` to `.env.agent.secret` and fill in:
- `LLM_API_KEY`
- `LLM_API_BASE`
- `LLM_MODEL`