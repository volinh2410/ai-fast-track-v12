# Weekly Submission – W1 / Member volinh2410

**Feature (F01–F04 or Foundation):** Foundation — Issue classifier (prompt V1–V3 + JSON schema). Chưa phải F01–F04.

**What I studied (2–3 concepts):**
- System prompt và user message: luật phân loại nằm ở system, nội dung phiếu nằm ở user.
- Few-shot: V3 đưa ví dụ input/output để model bám category, priority và JSON.
- Structured output: chỉ nhận kết quả khi Pydantic xác nhận `category`, `priority`, `next_action`.

**What I built (summary + key modules):**
Phân loại 20 phiếu trong `data/evaluation/issue_classification_gold.json`. Script chỉ gửi `text`, không gửi nhãn đúng.

- `practice/week01/prompts.md` — prompt V1, V2, V3
- `practice/week01/schema.py` — Pydantic `IssuePrediction`
- `practice/week01/classify.py` — gọi OpenAI, validate, ghi CSV
- `practice/week01/output/predictions_v1.csv` … `predictions_v3.csv`

Model: `gpt-4.1`. Base URL: `https://api.openai.com/v1`. Request gửi `temperature=0` để cùng prompt ra cùng kết quả.

**How to run:**

```powershell
.\.venv\Scripts\Activate.ps1
python practice/week01/classify.py --prompt v1
python practice/week01/classify.py --prompt v2
python practice/week01/classify.py --prompt v3
python scripts/evaluate_issue_classifier.py practice/week01/output/predictions_v3.csv
```

Cần `.env` với `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL`. File `.env` không commit.

**Results:** [test counts, evaluation table, security cases]

Schema: 20/20 cho cả 3 phiên bản (CSV chỉ được ghi khi mọi ca hợp lệ).

| Prompt | Category | Priority | P1 misses | Gate P1 |
|---|---|---|---|---|
| V1 | 20/20 = 100% | 11/20 = 55% | CASE-16 | Fail |
| V2 | 20/20 = 100% | 13/20 = 65% | none | Pass |
| V3 | 20/20 = 100% | 18/20 = 90% | none | Pass |

Tiêu chí tuần 1: category ≥ 85%, schema 100%, mọi P1 đúng. V2 và V3 đạt. V1 không đạt vì bỏ sót Risk sắp gây sự cố (CASE-14 chứng chỉ hết hạn, CASE-16 không có fallback).

V3 sửa V1 bằng cách: Risk chưa hỏng nhưng sắp ảnh hưởng go-live/security/auth vẫn là P1, và có few-shot để giữ đúng JSON.

Security cases: không áp dụng ở tuần 1 (chưa có tool, chưa có quyền project).

**Known failures / trade-offs:**
- Priority của V3 còn sai 2 ca: CASE-07 (Feature P2→P3) và CASE-12 (Question P2→P3).
- V2 bắt đủ P1 nhưng priority chỉ 65%.
- `next_action` không có trong gold và không được script chấm.

**Demo link:** Chưa có.

**PR link:** Chưa mở. Code nằm trên branch local `w1`. Remote đã trỏ `https://github.com/volinh2410/ai-fast-track-v12.git`. Push bị firewall FortiGate trả 403.

**Next action:** Đẩy `w1` khi ra khỏi mạng công ty, mở PR, rồi siết luật priority trong prompt để giảm 5 ca priority còn sai mà không làm mất các ca P1.
