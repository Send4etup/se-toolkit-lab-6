import subprocess
import json

def test_agent_output():
    result = subprocess.run(
        ["uv", "run", "agent.py", "What is 2+2?"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "answer" in data
    assert "tool_calls" in data

def test_agent_uses_read_file_for_merge_conflict():
    result = subprocess.run(
        ["uv", "run", "agent.py", "How do you resolve a merge conflict?"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "answer" in data
    assert "source" in data
    tool_names = [tc["tool"] for tc in data["tool_calls"]]
    assert "read_file" in tool_names
    assert "wiki/git.md" in data["source"]

def test_agent_uses_list_files_for_wiki():
    result = subprocess.run(
        ["uv", "run", "agent.py", "What files are in the wiki?"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "answer" in data
    tool_names = [tc["tool"] for tc in data["tool_calls"]]
    assert "list_files" in tool_names

def test_agent_uses_read_file_for_framework():
    result = subprocess.run(
        ["uv", "run", "agent.py", "What framework does the backend use?"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "answer" in data
    tool_names = [tc["tool"] for tc in data["tool_calls"]]
    assert "read_file" in tool_names


def test_agent_uses_query_api_for_item_count():
    result = subprocess.run(
        ["uv", "run", "agent.py", "How many items are in the database?"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "answer" in data
    tool_names = [tc["tool"] for tc in data["tool_calls"]]
    assert "query_api" in tool_names