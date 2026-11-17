"""
Week 1 - Issue Classifier (goi OpenAI)
1. Doc 20 cau text tu gold (khong dung nhan dung).
2. Gui prompt V1/V2/V3 + text toi OpenAI.
3. Kiem tra JSON bang Pydantic.
4. Ghi CSV de script chấm cham diem.

Chay (tu thu muc goc, da activate .venv, da dien .env):

  python practice/week01/classify.py --prompt v3
  python scripts/evaluate_issue_classifier.py practice/week01/output/predictions_v3.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from schema import IssuePrediction, parse_prediction

ROOT = HERE.parents[1]
GOLD_PATH = ROOT / "data" / "evaluation" / "issue_classification_gold.json"
PROMPTS_PATH = HERE / "prompts.md"
OUTPUT_DIR = HERE / "output"


def require_env() -> tuple[str, str, str]:
    """Doc key, model, base_url tu .env. Thieu key/model thi dung."""
    load_dotenv(ROOT / ".env")
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    model = (os.getenv("OPENAI_MODEL") or "").strip()
    base_url = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").strip()

    bad_key = (not api_key) or api_key.startswith("replace_")
    bad_model = (not model) or model.startswith("choose_")
    if bad_key or bad_model:
        raise SystemExit(
            "Can dien that OPENAI_API_KEY va OPENAI_MODEL trong file .env "
            "(copy tu .env.example)."
        )
    return api_key, model, base_url


def load_cases() -> list[dict]:
    """Chi lay issue_id + text."""
    rows = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    return [{"issue_id": r["issue_id"], "text": r["text"]} for r in rows]


def load_prompt(version: str) -> str:
    """Doc khoi prompt V1/V2/V3 trong prompts.md."""
    text = PROMPTS_PATH.read_text(encoding="utf-8")
    pattern = rf"## {version.upper()}\b.*?```text\n(.*?)```"
    match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        raise SystemExit(f"Khong tim thay prompt {version} trong {PROMPTS_PATH}")
    return match.group(1).strip()


def extract_json(raw: str) -> dict:
    """Lay object JSON tu cau tra loi cua model."""
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Khong thay JSON trong: {raw[:200]}")
    return json.loads(raw[start : end + 1])


def classify_one(
    client: OpenAI, model: str, system_prompt: str, text: str
) -> IssuePrediction:
    """Goi OpenAI cho 1 phiếu, validate bang Pydantic."""
    # Mot so model (vd gpt-5.x) khong cho temperature=0; dung mac dinh cua API.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Issue text:\n{text}"},
        ],
    )
    content = response.choices[0].message.content or ""
    return parse_prediction(extract_json(content))


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["issue_id", "predicted_category", "predicted_priority"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Week 1 issue classifier")
    parser.add_argument(
        "--prompt",
        choices=["v1", "v2", "v3"],
        default="v3",
        help="Phien ban prompt trong prompts.md",
    )
    args = parser.parse_args()

    api_key, model, base_url = require_env()
    cases = load_cases()
    system_prompt = load_prompt(args.prompt)
    client = OpenAI(api_key=api_key, base_url=base_url)

    print(f"Prompt : {args.prompt}")
    print(f"Model  : {model}")
    print(f"Base   : {base_url}")
    print(f"Cases  : {len(cases)}")

    csv_rows: list[dict] = []
    schema_ok = 0

    for case in cases:
        issue_id = case["issue_id"]
        try:
            pred = classify_one(client, model, system_prompt, case["text"])
            csv_rows.append(
                {
                    "issue_id": issue_id,
                    "predicted_category": pred.category,
                    "predicted_priority": pred.priority,
                }
            )
            schema_ok += 1
            print(f"  {issue_id}: {pred.category}/{pred.priority} | {pred.next_action}")
        except (ValidationError, ValueError, json.JSONDecodeError) as err:
            print(f"  {issue_id}: SCHEMA FAIL -> {err}")

    out_path = OUTPUT_DIR / f"predictions_{args.prompt}.csv"
    if len(csv_rows) != len(cases):
        print(f"\nChi {len(csv_rows)}/{len(cases)} ca hop le. Chua ghi CSV.")
        raise SystemExit(1)

    write_csv(csv_rows, out_path)
    print(f"\nSchema OK: {schema_ok}/{len(cases)}")
    print(f"Wrote    : {out_path}")
    print(
        "\nCham diem:\n"
        f"  python scripts/evaluate_issue_classifier.py {out_path.as_posix()}"
    )


if __name__ == "__main__":
    main()
