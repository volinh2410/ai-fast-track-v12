# Week 2 – Meeting Notes API

API đọc ghi chú họp và trả về:

- `summary`
- `decisions`
- `actions` (`owner`, `action`, `due_date`)

Thiếu owner/ngày → `null`. Không bịa.

## File

```text
main.py       POST /analyze-meeting
schemas.py    khung request/response
llm.py        goi OpenAI
prompts.md    loi dan cho model
evaluate.py   cham 20 case
tests/        5 case loi
```

## Chạy API

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --app-dir practice/week02 --reload --port 8002
```

Docs: http://127.0.0.1:8002/docs

## Test + chấm

```powershell
pytest -q practice/week02/tests
python practice/week02/evaluate.py
```

Đạt Gate 1 khi:
- OpenAPI chạy được
- Schema đúng
- ≥ 85% trên 20 case
- 5/5 lỗi: 422, 504, 429, 502, JSON hỏng
- Không lộ API key
