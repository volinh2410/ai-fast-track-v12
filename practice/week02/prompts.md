# Week 2 – Prompt

```text
Extract meeting notes. Use ONLY the given text. Do not invent facts.

Return one JSON object:
{
  "summary": "short summary",
  "decisions": ["approved decisions only"],
  "actions": [{"owner": "Name or null", "action": "task", "due_date": "YYYY-MM-DD or null"}]
}

Rules:
1. Suggestion / maybe / postponed = NOT a decision.
2. Vague talk = NOT an action.
3. Unknown owner -> null. Do not guess from attendees.
4. No deadline -> due_date null. Do not invent dates.
5. due_date must be YYYY-MM-DD or null.
6. Two owners for one task -> two action items.
7. "Team agreed that X" IS a decision, even with no owner.
8. Decision = approved goal. Action = concrete task.
9. Prefer empty lists over guessing.

Example:
"Phu and Hung will implement token refresh by December 4, 2026"
->
[
  {"owner":"Phu","action":"Implement token refresh handling","due_date":"2026-12-04"},
  {"owner":"Hung","action":"Implement token refresh handling","due_date":"2026-12-04"}
]
```
