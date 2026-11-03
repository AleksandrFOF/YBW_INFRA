from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


def analyze(log_context: str, findings: list):

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are a CI failure RCA expert.

Return valid JSON only.
"""
            },
            {
                "role": "user",
                "content": f"""
Known findings:

{findings}

Log:

{log_context}

Return:

{{
  "failure_category": "",
  "root_cause": "",
  "confidence": 0,
  "recommendations": []
}}
"""
            }
        ]
    )

    return response
