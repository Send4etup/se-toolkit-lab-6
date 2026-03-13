import sys
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env.agent.secret")

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No question provided"}))
        sys.exit(1)

    question = sys.argv[1]

    client = OpenAI(
        api_key=os.environ["LLM_API_KEY"],
        base_url=os.environ["LLM_API_BASE"],
    )

    print("Calling LLM...", file=sys.stderr)

    response = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=[
            {"role": "system", "content": "Answer the user's question concisely."},
            {"role": "user", "content": question},
        ],
        timeout=60,
    )

    answer = response.choices[0].message.content
    print(json.dumps({"answer": answer, "tool_calls": []}))

if __name__ == "__main__":
    main()