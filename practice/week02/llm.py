"""
Goi OpenAI de doc meeting notes -> JSON.

Neu OpenAI loi (timeout, 429, 500, JSON hong)
thi nem LLMError(status_code, message) cho main.py tra HTTP.
"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import APIStatusError, APITimeoutError, OpenAI, RateLimitError
from pydantic import ValidationError

from schemas import MeetingAnalysis

WEEK02 = Path(__file__).resolve().parent
ROOT = WEEK02.parent.parent  # practice/week02 -> kit root
PROMPT_FILE = WEEK02 / "prompts.md"


class LLMError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def read_prompt() -> str:
    text = PROMPT_FILE.read_text(encoding="utf-8")
    match = re.search(r"```text\n(.*?)```", text, flags=re.DOTALL)
    if not match:
        raise LLMError(500, "Khong doc duoc prompts.md")
    return match.group(1).strip()


def get_client() -> tuple[OpenAI, str]:
    load_dotenv(ROOT / ".env")
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    model = (os.getenv("OPENAI_MODEL") or "").strip()
    base_url = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").strip()

    if not api_key or api_key.startswith("replace_"):
        raise LLMError(500, "Thieu OPENAI_API_KEY trong .env")
    if not model or model.startswith("choose_"):
        raise LLMError(500, "Thieu OPENAI_MODEL trong .env")

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=30.0)
    return client, model


def parse_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            raise ValueError("Khong co JSON")
        return json.loads(text[start : end + 1])


def analyze_meeting_text(meeting_text: str) -> MeetingAnalysis:
    """Buoc: doc .env -> goi model -> parse JSON -> kiem tra schema."""
    client, model = get_client()

    try:
        # gpt-6-luna (va mot so model moi) chi chap nhan temperature mac dinh
        kwargs = {
            "model": model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": read_prompt()},
                {"role": "user", "content": f"Meeting notes:\n{meeting_text}"},
            ],
        }
        if not model.startswith("gpt-6"):
            kwargs["temperature"] = 0
        reply = client.chat.completions.create(**kwargs)
        raw = reply.choices[0].message.content or ""
        return MeetingAnalysis.model_validate(parse_json(raw))

    except APITimeoutError as e:
        raise LLMError(504, "Upstream model timeout") from e
    except RateLimitError as e:
        raise LLMError(429, "Upstream model rate limited") from e
    except APIStatusError as e:
        detail = getattr(e, "message", None) or str(e)
        raise LLMError(502, f"Upstream model error: {e.status_code} — {detail}") from e
    except (ValidationError, ValueError, json.JSONDecodeError) as e:
        raise LLMError(502, f"Malformed model response: {e}") from e

analyze_fn = analyze_meeting_text
