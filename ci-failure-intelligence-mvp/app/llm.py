from dotenv import load_dotenv
from openai import AzureOpenAI

import json
import os

load_dotenv()

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


def analyze_log(log_text, findings):

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a CI RCA expert. Return JSON only."
            },
            {
                "role": "user",
                "content": f"""
Findings:
{findings}

Log:
{log_text}
"""
            }
        ]
    )

    data = json.loads(
        response.choices[0].message.content
    )

    data["token_usage"] = {
        "prompt": response.usage.prompt_tokens,
        "completion": response.usage.completion_tokens,
        "total": response.usage.total_tokens
    }

    return data


def chat_about_failure(analysis, question):

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Answer using RCA context."
            },
            {
                "role": "user",
                "content": f"""
RCA:
{json.dumps(analysis, indent=2)}

Question:
{question}
"""
            }
        ]
    )

    return response.choices[0].message.content


def general_chat(question):

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a CI/CD Copilot assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content