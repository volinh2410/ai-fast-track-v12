"""5 case loi bat buoc cua Gate 1."""

from fastapi.testclient import TestClient

import llm
from llm import LLMError
from main import app
from schemas import ActionItem, MeetingAnalysis

client = TestClient(app)
SAMPLE = {"meeting_text": "Meeting Date: 2026-11-23\nPhu will fix login by 2026-11-25."}


def _fake_error(code: int, message: str):
    def fake(_text: str):
        raise LLMError(code, message)

    return fake


def test_1_invalid_payload_422():
    assert client.post("/analyze-meeting", json={}).status_code == 422
    assert client.post("/analyze-meeting", json={"meeting_text": "  "}).status_code == 422


def test_2_timeout_504():
    llm.analyze_fn = _fake_error(504, "Upstream model timeout")
    try:
        assert client.post("/analyze-meeting", json=SAMPLE).status_code == 504
    finally:
        llm.analyze_fn = llm.analyze_meeting_text


def test_3_rate_limit_429():
    llm.analyze_fn = _fake_error(429, "Upstream model rate limited")
    try:
        assert client.post("/analyze-meeting", json=SAMPLE).status_code == 429
    finally:
        llm.analyze_fn = llm.analyze_meeting_text


def test_4_upstream_500_502():
    llm.analyze_fn = _fake_error(502, "Upstream model error: 500")
    try:
        assert client.post("/analyze-meeting", json=SAMPLE).status_code == 502
    finally:
        llm.analyze_fn = llm.analyze_meeting_text


def test_5_malformed_json_502():
    llm.analyze_fn = _fake_error(502, "Malformed model response: not json")
    try:
        r = client.post("/analyze-meeting", json=SAMPLE)
        assert r.status_code == 502
        assert "malformed" in r.json()["detail"].lower()
    finally:
        llm.analyze_fn = llm.analyze_meeting_text


def test_success_schema():
    def fake(_text: str) -> MeetingAnalysis:
        return MeetingAnalysis(
            summary="Prioritized login bug.",
            decisions=["Prioritize the login bug."],
            actions=[
                ActionItem(owner="Phu", action="Fix login", due_date="2026-11-25"),
                ActionItem(owner="Hung", action="Review PR", due_date=None),
            ],
        )

    llm.analyze_fn = fake
    try:
        r = client.post("/analyze-meeting", json=SAMPLE)
        assert r.status_code == 200
        body = r.json()
        assert body["actions"][0]["due_date"] == "2026-11-25"
        assert body["actions"][1]["due_date"] is None
    finally:
        llm.analyze_fn = llm.analyze_meeting_text
