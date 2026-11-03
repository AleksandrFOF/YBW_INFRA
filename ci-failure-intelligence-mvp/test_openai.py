from dotenv import load_dotenv
load_dotenv()

from openai import AzureOpenAI
import os
import json

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    temperature=0,
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": """You are a CI failure RCA expert.
Return valid JSON only."""
        },
        {
            "role": "user",
            "content": """
Analyze this CI failure:

OOMKilled
Container terminated
exit code 137

Return:

{
  "failure_category":"",
  "root_cause":"",
  "confidence":0,
  "recommendations":[]
}
"""
        }
    ]
)

content = response.choices[0].message.content

print("=== MODEL RESPONSE ===")
print(content)

usage = response.usage

print("\n=== TOKEN USAGE ===")
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

json.loads(content)

print("\nJSON validation passed")