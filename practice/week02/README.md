# Week 2 – Meeting Notes API (Gate 1)

API đọc ghi chú họp và trả về:

- `summary`
- `decisions`
- `actions` (`owner`, `action`, `due_date`)

Thiếu owner/ngày → `null`. Không bịa.

Model: `OPENAI_MODEL=gpt-6-luna` trong `.env` (không dùng `gpt-4.1`). `llm.py` bỏ `temperature` với model `gpt-6*` vì Luna không hỗ trợ `temperature=0`.

## File

```text
main.py       POST /analyze-meeting
schemas.py    khung request/response
llm.py        goi OpenAI
prompts.md    loi dan cho model
tests/        5 case loi Gate 1
```

## Chạy API

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --app-dir practice/week02 --reload --port 8002
```

Docs: http://127.0.0.1:8002/docs

Ví dụ:

```powershell
curl -X POST http://127.0.0.1:8002/analyze-meeting `
  -H "Content-Type: application/json" `
  -d "{\"meeting_text\":\"Meeting Date: 2026-11-23\\nPhu will fix login by November 25, 2026.\"}"
```

## Test lỗi (5/5)

```powershell
pytest -q practice/week02/tests
```

1. payload sai → 422  
2. timeout → 504  
3. 429 → 429  
4. upstream 500 → 502  
5. JSON hỏng → 502  

## Chấm ≥ 85% trên 20 case

Dùng gold `data/week02/week2_meeting_notes_expected_20_cases.json`:

1. Gọi `POST /analyze-meeting` với từng `input`
2. So với `expected` (owner/`due_date` chính xác; summary/action/decision đúng nghĩa)
3. Ghi Pass/Fail vào evidence (đạt khi ≥ 17/20)

## Đạt Gate 1 khi

- API chạy theo README, có OpenAPI `/docs`
- Output thành công đúng schema
- ≥ 85% trên 20 case
- 5/5 case lỗi đạt
- Không lộ API key trong git/log
