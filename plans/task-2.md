# Task 2 Plan

## Tools
- `read_file(path)` — reads file contents, blocks `../` traversal
- `list_files(path)` — lists directory entries, blocks `../` traversal

## Agentic loop
1. Send question + tool schemas to LLM
2. If response has tool_calls → execute tools, append results, repeat
3. If response has text → output JSON and exit
4. Hard limit: 10 tool calls

## Output
JSON with `answer`, `source`, `tool_calls`.

## Security
Resolve path with `os.path.realpath`, check it starts with project root.