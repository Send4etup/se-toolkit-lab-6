import sys
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env.agent.secret")

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from the project repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path from project root."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories at a given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative directory path from project root."}
                },
                "required": ["path"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a documentation assistant. To answer questions:
1. Use list_files to discover files in the wiki directory.
2. Use read_file to read relevant files.
3. Answer based on the file contents.
4. Always include the source as a file path and section anchor, e.g. wiki/git-workflow.md#resolving-merge-conflicts.
Return your final answer as plain text. End your response with: SOURCE: <path#anchor>"""


def safe_path(relative_path):
    full = os.path.realpath(os.path.join(PROJECT_ROOT, relative_path))
    if not full.startswith(PROJECT_ROOT):
        raise ValueError(f"Access denied: {relative_path}")
    return full


def read_file(path):
    try:
        full = safe_path(path)
        with open(full, "r", encoding="utf-8") as f:
            return f.read()
    except ValueError as e:
        return str(e)
    except FileNotFoundError:
        return f"File not found: {path}"


def list_files(path):
    try:
        full = safe_path(path)
        entries = os.listdir(full)
        return "\n".join(sorted(entries))
    except ValueError as e:
        return str(e)
    except FileNotFoundError:
        return f"Directory not found: {path}"


def execute_tool(name, args):
    if name == "read_file":
        return read_file(args["path"])
    elif name == "list_files":
        return list_files(args["path"])
    return "Unknown tool"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No question provided"}))
        sys.exit(1)

    question = sys.argv[1]
    client = OpenAI(
        api_key=os.environ["LLM_API_KEY"],
        base_url=os.environ["LLM_API_BASE"],
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    all_tool_calls = []
    answer = ""
    source = ""

    for _ in range(10):
        print("Calling LLM...", file=sys.stderr)
        response = client.chat.completions.create(
            model=os.environ["LLM_MODEL"],
            messages=messages,
            tools=TOOLS,
            timeout=60,
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append({"role": "assistant", "content": None, "tool_calls": [
                {"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ]})
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = execute_tool(tc.function.name, args)
                print(f"Tool: {tc.function.name} {args}", file=sys.stderr)
                all_tool_calls.append({"tool": tc.function.name, "args": args, "result": result})
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        else:
            answer_text = msg.content or ""
            if "SOURCE:" in answer_text:
                parts = answer_text.rsplit("SOURCE:", 1)
                answer = parts[0].strip()
                source = parts[1].strip()
            else:
                answer = answer_text.strip()
                source = ""
            break

    print(json.dumps({"answer": answer, "source": source, "tool_calls": all_tool_calls}))


if __name__ == "__main__":
    main()