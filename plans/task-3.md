# Task 3 Plan

## New tool: query_api
- Parameters: method, path, body (optional)
- Auth: LMS_API_KEY from environment variable
- Returns: JSON string with status_code and body

## Environment variables
- LLM_API_KEY, LLM_API_BASE, LLM_MODEL — from .env.agent.secret
- LMS_API_KEY — from .env.docker.secret
- AGENT_API_BASE_URL — defaults to http://localhost:42002

## System prompt update
LLM will be told:
- Use read_file/list_files for wiki and source code questions
- Use query_api for live data and HTTP status questions
- Chain tools when needed (query API error → read source code)

## Benchmark strategy
Run run_eval.py, fix failures one by one.