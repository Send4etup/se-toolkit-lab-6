# AGENT.md

## Overview
CLI agent with an agentic loop that reads project wiki, source code, and queries the live backend API to answer questions.

## LLM Provider
Qwen Code API — local proxy on VM, OpenAI-compatible, 1000 free requests/day.
Model: qwen3-coder-plus.

## How to run
```bash
uv run agent.py "Your question here"
```

## Output format
```json
{"answer": "...", "source": "wiki/file.md#section", "tool_calls": [...]}
```
`source` is omitted if not applicable.

## Tools

### read_file(path)
Reads a file from the project repository. Used for wiki documentation, source code, config files. Blocks path traversal outside project root using os.path.realpath.

### list_files(path)
Lists directory contents. Used to discover available wiki files or backend modules. Blocks path traversal outside project root.

### query_api(method, path, body?)
Calls the deployed backend API. Used for live data queries (item counts, analytics), HTTP status code checks, and endpoint error diagnosis. Authenticates with LMS_API_KEY from environment variables. Base URL is AGENT_API_BASE_URL (defaults to http://localhost:42002).

## Agentic loop
1. Send question + tool schemas to LLM
2. LLM returns tool_calls → execute each tool, append results as tool messages, repeat
3. LLM returns text → parse answer and source, output JSON
4. Hard limit: 10 tool calls per question

## System prompt strategy
The LLM is instructed with explicit decision rules:
- Wiki and how-to questions → read_file on wiki/
- Source code and architecture → list_files + read_file on backend/
- Live data and HTTP status → query_api
- Bug diagnosis → query_api first to get error, then read_file to find the bug in source

The LLM is asked to end every response with SOURCE: path#anchor so the agent can parse it reliably.

## Environment variables
All configuration is read from environment variables:
- `LLM_API_KEY` — LLM provider API key
- `LLM_API_BASE` — LLM API endpoint URL
- `LLM_MODEL` — model name
- `LMS_API_KEY` — backend API key for query_api authentication
- `AGENT_API_BASE_URL` — backend base URL (default: http://localhost:42002)

## Lessons learned
Tool descriptions must be specific enough for the LLM to choose correctly. Vague descriptions cause the LLM to pick the wrong tool or skip tools entirely. Chaining tools (query API error → read source code) requires the system prompt to explicitly describe the pattern. The SOURCE: marker at the end of LLM responses is a reliable parsing strategy that avoids complex output parsing.