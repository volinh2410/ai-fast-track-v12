"""
Week 2 - Meeting Notes API

Chay:
  uvicorn main:app --app-dir practice/week02 --reload --port 8002

Docs: http://127.0.0.1:8002/docs
"""

from fastapi import FastAPI, HTTPException

import llm
from llm import LLMError
from schemas import MeetingAnalysis, MeetingRequest

app = FastAPI(title="Week 2 Meeting Notes API", version="0.1.0")


@app.post("/analyze-meeting", response_model=MeetingAnalysis)
def analyze_meeting(body: MeetingRequest) -> MeetingAnalysis:
    """Doc meeting_text -> summary, decisions, actions."""
    try:
        # Dung llm.analyze_fn de test co the gan ham fake
        return llm.analyze_fn(body.meeting_text)
    except LLMError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message) from err
