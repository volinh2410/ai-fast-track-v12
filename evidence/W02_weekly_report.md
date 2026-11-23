# Weekly Submission – W2 / vhtlinh

**Feature (F01–F04 or Foundation):** Foundation / Gate 1 — Meeting Notes API (`POST /analyze-meeting`). Chưa phải F01–F04; chưa đụng Jira.

**What I studied (2–3 concepts):**
- FastAPI + Pydantic: validate request trước khi gọi model; payload sai → 422.
- Structured JSON output: ép `summary`, `decisions`, `actions` (owner / action / due_date); thiếu thì `null`, không bịa.
- Map lỗi upstream: timeout → 504, 429 → 429, model 500 / JSON hỏng → 502.

**What I built (summary + key modules):**
API đọc meeting notes và trả về kết quả có schema. Gold: `data/week02/week2_meeting_notes_expected_20_cases.json` (20 case).

- `practice/week02/main.py` — FastAPI `POST /analyze-meeting`
- `practice/week02/schemas.py` — `MeetingRequest`, `MeetingAnalysis`, `ActionItem`
- `practice/week02/llm.py` — gọi OpenAI + `LLMError`
- `practice/week02/prompts.md` — system prompt
- `practice/week02/evaluate.py` — chấm 20 case
- `practice/week02/tests/test_api_errors.py` — 5 lỗi + schema thành công

Model: `gpt-4.1`. Base URL: `https://api.openai.com/v1`. `temperature=0`.

**How to run:**

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --app-dir practice/week02 --reload --port 8002
# docs: http://127.0.0.1:8002/docs

pytest -q practice/week02/tests
python practice/week02/evaluate.py
```

Cần `.env` với `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL`. Không commit `.env`.

**Results:** [test counts, evaluation table, security cases]

| Check | Result |
|---|---|
| pytest (5 lỗi + schema OK) | 6 passed |
| Eval 20 case | 20/20 = 100% (≥ 85%) |
| OpenAPI docs | `/docs` khi chạy uvicorn |
| Secret in git | `.env` bị ignore |

Bảng lỗi Gate 1:

| Case | HTTP |
|---|---|
| Payload sai / rỗng | 422 |
| Timeout | 504 |
| Rate limit | 429 |
| Upstream 500 | 502 |
| Model JSON hỏng | 502 |

Security cases (cross-project / injection): chưa áp dụng ở tuần 2.

**Known failures / trade-offs:**
- Metric eval so owner/due_date chính xác; action/decision so theo nghĩa (token overlap), không byte-for-byte — đúng contract dataset.
- Chưa dùng OpenAI Structured Outputs schema chặt; đang `json_object` + Pydantic.
- Test lỗi dùng hàm fake (`llm.analyze_fn`), không gọi mạng thật.

**Demo link:** Chưa có.

**PR link:** Chưa mở. Code local trong `practice/week02`. Remote: `https://github.com/volinh2410/ai-fast-track-v12.git`.

**Next action:** Mở branch `week02`, push + PR; chuẩn bị Tuần 3 (embeddings / pgvector / scoped search).
