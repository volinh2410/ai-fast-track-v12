"""
Khung du lieu cua API.

Request:  { "meeting_text": "..." }
Response: { "summary": "...", "decisions": [...], "actions": [...] }
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MeetingRequest(BaseModel):
    meeting_text: str = Field(min_length=1)

    @field_validator("meeting_text")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("meeting_text rong")
        return value


class ActionItem(BaseModel):
    owner: Optional[str] = None          # null neu khong ro nguoi lam
    action: str = Field(min_length=1)
    due_date: Optional[str] = None       # YYYY-MM-DD hoac null


class MeetingAnalysis(BaseModel):
    summary: str = Field(min_length=1)
    decisions: list[str] = []
    actions: list[ActionItem] = []
