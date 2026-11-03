#!/usr/bin/env bash

set -e

echo "Creating frontend directory..."
mkdir -p frontend

echo "Updating requirements.txt..."

cat > requirements.txt <<'EOF'
openai>=1.55.0
python-dotenv>=1.0.1
pydantic>=2.9.0
pyyaml>=6.0
pytest>=8.3.0
tiktoken>=0.8.0
fastapi
uvicorn
streamlit
requests
EOF

echo "Creating api.py..."

cat > api.py <<'EOF'
from fastapi import FastAPI
from pydantic import BaseModel

from app.analyzer import detect_signatures
from app.llm import analyze_log

app = FastAPI(title="CI Failure Intelligence API")

class AnalysisRequest(BaseModel):
    log: str

@app.post("/analyze")
def analyze(request: AnalysisRequest):

    findings = detect_signatures(request.log)

    return analyze_log(
        log_text=request.log,
        findings=findings
    )
EOF

echo "Updating app/llm.py..."

cat > app/llm.py <<'EOF'
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
                "content": """
You are a CI Root Cause Analysis expert.

Return valid JSON only.
"""
            },
            {
                "role": "user",
                "content": f"""
Known findings:

{findings}

Log:

{log_text}

Return:

{{
 "failure_category":"",
 "root_cause":"",
 "confidence":0,
 "recommendations":[]
}}
"""
            }
        ]
    )

    result = json.loads(
        response.choices[0].message.content
    )

    result["token_usage"] = {
        "prompt": response.usage.prompt_tokens,
        "completion": response.usage.completion_tokens,
        "total": response.usage.total_tokens
    }

    return result
EOF

echo "Creating frontend/app.py..."

cat > frontend/app.py <<'EOF'
import requests
import streamlit as st

st.set_page_config(
    page_title="CI Failure Intelligence",
    layout="wide"
)

st.title("CI Failure Intelligence")

uploaded = st.file_uploader(
    "Upload failed build log",
    type=["log", "txt"]
)

if uploaded:

    log_text = uploaded.read().decode()

    with st.spinner("Analyzing..."):

        response = requests.post(
            "http://localhost:8000/analyze",
            json={
                "log": log_text
            },
            timeout=120
        )

        result = response.json()

    with st.chat_message("assistant"):

        st.markdown(
            f"""
### Root Cause

{result['root_cause']}

### Category

{result['failure_category']}

### Confidence

{result['confidence']}
"""
        )

    st.subheader("Recommendations")

    for item in result["recommendations"]:
        st.write(f"• {item}")

    st.subheader("Token Usage")

    st.json(result["token_usage"])
EOF

echo "Updating .gitignore..."

cat >> .gitignore <<'EOF'

.env
.venv/
__pycache__/
.pytest_cache/
*.pyc
reports/*.json
EOF

echo "Installing dependencies..."

pip install -r requirements.txt

echo ""
echo "Done."
echo ""
echo "Start backend:"
echo "uvicorn api:app --reload"
echo ""
echo "Start frontend:"
echo "streamlit run frontend/app.py"