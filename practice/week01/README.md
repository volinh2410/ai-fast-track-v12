# Week 1 – Issue Classifier

Phân loại 20 phiếu bằng **OpenAI** + 3 phiên bản prompt.

- **category:** Bug / Feature / Question / Risk  
- **priority:** P1 / P2 / P3  
- **next_action:** model tự viết (mentor đọc; script chấm không chấm)

Gold: `data/evaluation/issue_classification_gold.json` — **không sửa**.  
Script chỉ đưa `text` cho model, không đưa nhãn đúng.

## File trong thư mục này

```text
prompts.md   # V1, V2, V3
schema.py    # Pydantic: category / priority / next_action
classify.py  # goi OpenAI -> validate -> ghi CSV
output/      # predictions_v1.csv ... predictions_v3.csv
```

## Chuẩn bị

1. Activate venv: `.\.venv\Scripts\Activate.ps1`
2. Điền thật trong `.env` ở thư mục gốc:

```env
OPENAI_API_KEY=...
OPENAI_MODEL=...
OPENAI_BASE_URL=https://api.openai.com/v1
```

## Chạy

```powershell
python practice/week01/classify.py --prompt v1
python practice/week01/classify.py --prompt v2
python practice/week01/classify.py --prompt v3

python scripts/evaluate_issue_classifier.py practice/week01/output/predictions_v3.csv
```

## Đạt khi

- Category ≥ 85% (17/20)
- Schema 100%
- Mọi P1 trong gold đều được gán P1
- Giải thích được V3 sửa gì so với V1 (`prompts.md`)
