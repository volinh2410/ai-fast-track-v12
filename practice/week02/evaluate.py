"""
Cham 20 case (data/week02).

Cach cham don gian:
- owner + due_date phai dung
- action/decision chi can giong y (chung nhieu tu)
- Case dat khi action F1 >= 0.8 va decisions ok

Chay: python practice/week02/evaluate.py
"""

import json
import re
import sys
from pathlib import Path

WEEK02 = Path(__file__).resolve().parent
ROOT = WEEK02.parent.parent  # kit root
sys.path.insert(0, str(WEEK02))

from llm import analyze_meeting_text
from schemas import MeetingAnalysis

CASES = ROOT / "data" / "week02" / "week2_meeting_notes_expected_20_cases.json"
OUT = WEEK02 / "output" / "eval_results.json"


def words(text: str) -> set[str]:
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    skip = {"the", "a", "an", "to", "of", "and", "for", "by", "on", "in"}
    return {w for w in text.split() if w and w not in skip}


def similar(a: str, b: str) -> bool:
    """Hai cau giong y neu chung it nhat 35% tu."""
    wa, wb = words(a), words(b)
    if not wa and not wb:
        return True
    if not wa or not wb:
        return False
    inter = len(wa & wb)
    return inter / len(wa | wb) >= 0.35 or inter / min(len(wa), len(wb)) >= 0.5


def score(pred: MeetingAnalysis, expected: dict) -> bool:
    exp_actions = expected.get("actions") or []
    pred_actions = pred.actions

    matched = 0
    used = set()
    for exp in exp_actions:
        for i, got in enumerate(pred_actions):
            if i in used:
                continue
            same_owner = (exp.get("owner") or "") == (got.owner or "")
            same_date = exp.get("due_date") == got.due_date
            if same_owner and same_date and similar(exp.get("action", ""), got.action):
                matched += 1
                used.add(i)
                break

    n_exp, n_pred = len(exp_actions), len(pred_actions)
    precision = matched / n_pred if n_pred else (1.0 if n_exp == 0 else 0.0)
    recall = matched / n_exp if n_exp else (1.0 if n_pred == 0 else 0.0)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)

    exp_dec = expected.get("decisions") or []
    pred_dec = pred.decisions
    if not exp_dec:
        dec_ok = len(pred_dec) == 0
    else:
        hit = sum(
            1
            for ed in exp_dec
            if any(similar(ed, pd) for pd in pred_dec)
        )
        dec_ok = hit / len(exp_dec) >= 0.5 and len(pred_dec) <= len(exp_dec) + 1

    return f1 >= 0.8 and dec_ok


def main() -> None:
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    results = []
    passed = 0

    print(f"Cases: {len(cases)}")
    for case in cases:
        print(f"\n=== {case['id']} {case['title']} ===")
        pred = analyze_meeting_text(case["input"])
        ok = score(pred, case["expected"])
        passed += int(ok)
        print("PASS" if ok else "FAIL")
        print("decisions:", pred.decisions)
        print("actions:", pred.model_dump()["actions"])
        results.append(
            {
                "id": case["id"],
                "passed": ok,
                "pred": pred.model_dump(),
            }
        )

    rate = passed / len(cases)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {"passed": passed, "total": len(cases), "rate": rate, "results": results},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nPassed {passed}/{len(cases)} = {rate:.1%}")
    print(f"Wrote {OUT}")
    if rate < 0.85:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
