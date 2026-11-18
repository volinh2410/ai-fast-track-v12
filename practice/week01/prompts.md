# Week 1 – Issue Classifier Prompts

Mỗi phiên bản dùng cùng một schema JSON:

```json
{
  "category": "Bug | Feature | Question | Risk",
  "priority": "P1 | P2 | P3",
  "next_action": "one short next step"
}
```

Không được bịa thông tin. Chỉ phân loại từ nội dung phiếu.

---

## V1 – cơ bản (dễ hiểu nhưng còn thiếu)

```text
You classify a Jira-style issue text.

Choose exactly one category:
- Bug: something is broken now
- Feature: a new capability or change request
- Question: the text asks for information
- Risk: not broken yet, but may cause delay or failure later

Choose exactly one priority:
- P1: urgent
- P2: important
- P3: low

Return ONLY valid JSON with keys:
category, priority, next_action
```

Hạn chế của V1:
- “urgent” quá chung, dễ bỏ sót Risk sắp gây sự cố lớn (ví dụ chứng chỉ sắp hết hạn).
- Không nói rõ dấu hiệu của Question (What/How/Where/Who/?).
- Không có ví dụ, model dễ lẫn Feature và Bug.

---

## V2 – làm rõ luật ưu tiên và Risk

```text
You classify a Jira-style issue text.

Categories (choose one):
- Bug: a failure happening now (down, fails, 500, blocks login, unexpected wrong behavior)
- Feature: add/implement/support/change a capability
- Question: asks for information (often starts with What/How/Where/Who/Which or ends with ?)
- Risk: not broken yet, but may delay release or cause a future outage

Priority rules:
- P1: wide user impact now, OR a near-term risk that can break go-live/security/auth
- P2: important but not global outage
- P3: small/nice-to-have work

Return ONLY valid JSON:
{"category":"...","priority":"...","next_action":"..."}
```

V2 cải thiện gì so với V1:
- Risk sắp xảy ra cũng có thể là P1.
- Có dấu hiệu nhận biết Question và Feature rõ hơn.

---

## V3 – luật chặt + few-shot (bản dùng để nộp)

```text
You classify one issue text. Use ONLY the text. Do not invent facts.

Categories:
- Bug: currently broken behavior
- Feature: request to add or change a capability
- Question: information request
- Risk: future/possible problem (may, could, expires, no fallback, single point of delay)

Priority:
- P1 if impact is global/all users OR go-live/security/auth is at near-term risk
- P2 if important delivery impact but not global outage
- P3 if small UI/docs/nice-to-have

Examples:
Input: "Production checkout API down for all users"
Output: {"category":"Bug","priority":"P1","next_action":"Page on-call and restore checkout API"}

Input: "Add download button to sprint chart"
Output: {"category":"Feature","priority":"P3","next_action":"Confirm UI design then implement button"}

Input: "What is the expected UAT deadline?"
Output: {"category":"Question","priority":"P3","next_action":"Check project schedule and reply with date"}

Input: "Security certificate expires before go-live"
Output: {"category":"Risk","priority":"P1","next_action":"Renew certificate before go-live date"}

Return ONLY one JSON object with keys category, priority, next_action.
```

V3 cải thiện gì so với V1:
1. Nói rõ Risk chưa hỏng nhưng sắp gây sự cố lớn → vẫn P1.
2. Có few-shot giúp model bám format JSON và phân biệt 4 loại.
3. next_action phải ngắn và gắn với phiếu.
