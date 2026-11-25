# Weekly Submission – W2 / vhtlinh

**Feature (F01–F04 or Foundation):** Foundation / **Gate 1** — Meeting Notes API (`POST /analyze-meeting`). Chưa phải F01–F04; chưa đụng Jira.

**What I studied (2–3 concepts):**
- FastAPI + Pydantic: validate request trước khi gọi model; payload sai → 422.
- Structured JSON: `summary`, `decisions`, `actions` (`owner`, `action`, `due_date`); thiếu → `null`, không bịa ngày.
- Xử lý lỗi upstream: timeout, 429, 500, response model hỏng — API không sập, trả mã rõ.

**What I built (summary + key modules):**
API trích xuất ghi chú họp theo schema. Dataset công khai: `data/week02/week2_meeting_notes_expected_20_cases.json` (20 case).

- `practice/week02/main.py` — `POST /analyze-meeting`
- `practice/week02/schemas.py` — `MeetingRequest`, `MeetingAnalysis`, `ActionItem`
- `practice/week02/llm.py` — gọi OpenAI + map lỗi HTTP
- `practice/week02/prompts.md` — system prompt
- `practice/week02/tests/test_api_errors.py` — 5 lỗi Gate 1 + schema thành công
- `practice/week02/README.md` — cách chạy / OpenAPI

Model: `gpt-6-luna`. Base URL: `https://api.openai.com/v1`. Model này không hỗ trợ `temperature=0` → dùng temperature mặc định (code bỏ `temperature` với `gpt-6*`).

**How to run:**

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --app-dir practice/week02 --reload --port 8002
# OpenAPI: http://127.0.0.1:8002/docs

pytest -q practice/week02/tests
```

Cần `.env` với `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL`. Không commit `.env`.

**Results:**

| Check | Result |
|---|---|
| pytest (5 lỗi + schema OK) | 6 passed |
| Eval 20 case (gold vs pred) | **20/20 = 100%** (≥ 85%) |
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

### Bản so sánh gold vs pred (20 case)

- Gold: `data/week02/week2_meeting_notes_expected_20_cases.json`
- Pred: `practice/week02/output/eval_results.json` (`passed=20`, `total=20`, `rate=1.0`)
- So: `owner` / `due_date` exact; `action` / `decision` đúng nghĩa

| Case | Group | #actions gold→pred | owner/due khớp | Decisions | Pass |
|---|---|---|---|---|---|
| TC01 | Normal | 3→3 | Yes | OK | Pass |
| TC02 | Normal | 3→3 | Yes | OK | Pass |
| TC03 | Normal | 3→3 | Yes | OK | Pass |
| TC04 | Normal | 3→3 | Yes | OK | Pass |
| TC05 | Normal | 3→3 | Yes | OK | Pass |
| TC06 | Missing info | 2→2 | Yes (`due_date=null`) | OK (rỗng) | Pass |
| TC07 | Missing info | 1→1 | Yes (`owner=null`) | OK | Pass |
| TC08 | Missing info | 2→2 | Yes | OK (rỗng) | Pass |
| TC09 | Missing info | 0→0 | Yes | OK | Pass |
| TC10 | Ambiguous | 0→0 | Yes (không bịa) | OK (rỗng) | Pass |
| TC11 | Ambiguous | 0→0 | Yes | OK (rỗng) | Pass |
| TC12 | Ambiguous | 0→0 | Yes | OK (rỗng) | Pass |
| TC13 | Ambiguous | 1→1 | Yes | OK (rỗng) | Pass |
| TC14 | Complex | 4→4 | Yes | OK | Pass |
| TC15 | Complex | 5→5 | Yes | OK | Pass |
| TC16 | Complex | 3→3 | Yes | OK | Pass |
| TC17 | Complex | 4→4 | Yes | OK | Pass |
| TC18 | Edge | 0→0 | Yes | OK (rỗng) | Pass |
| TC19 | Edge | 0→0 | Yes | OK (rỗng) | Pass |
| TC20 | Edge | 0→0 | Yes | OK (rỗng) | Pass |

Security cases (cross-project / injection): chưa áp dụng ở tuần 2.

**Known failures / trade-offs:**
- Metric eval so owner/due_date chính xác; action/decision so theo nghĩa (token overlap), không byte-for-byte — đúng contract dataset.
- Chưa dùng OpenAI Structured Outputs schema chặt; đang `json_object` + Pydantic.
- Test lỗi dùng hàm fake (`llm.analyze_fn`), không gọi mạng thật.
- `gpt-6-luna` không nhận `temperature=0`; `llm.py` chỉ set `temperature=0` cho model không thuộc `gpt-6*`.

**Demo link:** Chưa có.

**PR link:** Chưa mở. Code local trong `practice/week02`. Remote: `https://github.com/volinh2410/ai-fast-track-v12.git`.

**Next action:** Mở branch `week02`, push + PR; chuẩn bị Tuần 3 (embeddings / pgvector / scoped search).
