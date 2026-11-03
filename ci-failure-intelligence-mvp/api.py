from fastapi import FastAPI
from pydantic import BaseModel
from app.analyzer import detect_signatures
from app.llm import analyze_log, chat_about_failure, general_chat

app = FastAPI(title="CI Failure Intelligence API", version="0.2.0")

class AnalysisRequest(BaseModel):
    log:str

class ChatRequest(BaseModel):
    analysis:dict
    question:str

class GeneralChatRequest(BaseModel):
    question:str

@app.post("/analyze")
def analyze(req:AnalysisRequest):
    findings=detect_signatures(req.log)
    return analyze_log(req.log, findings)

@app.post('/chat')
def chat(req:ChatRequest):
    return {"answer": chat_about_failure(req.analysis, req.question)}

@app.post('/general-chat')
def general(req:GeneralChatRequest):
    return {"answer": general_chat(req.question)}
