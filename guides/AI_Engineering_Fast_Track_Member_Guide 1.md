# AI Engineering Fast-Track — Hướng dẫn làm việc 8 tuần

Dành cho 6 software engineers. Mỗi người khoảng **20 giờ/tuần**. Chương trình chạy **16/11/2026–08/01/2027**.

File này là việc phải làm, chỗ đọc, cách nộp và cách mentor chấm. Slide package v12 vẫn là nguồn yêu cầu gốc khi hai bên khác chi tiết.

## Sản phẩm cuối

Cả nhóm xây một **AI-Powered Delivery Assistant** trên staging, cho PM và Delivery Lead.

Hôm nay PM phải tự lục Jira và tài liệu để biết việc nào kẹt, sprint đang thế nào, rồi tự viết báo cáo. Trợ lý trả lời có dẫn nguồn, chỉ ra issue quá hạn hoặc bị chặn, soạn báo cáo tuần, và chỉ gửi sau khi PM duyệt.

| ID | PM làm gì | Trợ lý phải trả |
|---|---|---|
| F01 | Hỏi tài liệu dự án | Câu trả lời có document và page. Thiếu dữ liệu thì nói không có. Không xem project khác quyền |
| F02 | Xem sức khỏe sprint | Issue quá hạn hoặc bị chặn, có issue key, owner, evidence. Jira chỉ đọc |
| F03 | Xin báo cáo tuần | Tiến độ, việc đã xong, risk, blocker, việc tiếp theo. Fact truy được về nguồn. Mục tiêu ≤ 2 phút trên sample |
| F04 | Duyệt và phân quyền | Draft sửa được, có trạng thái duyệt. Chưa duyệt thì không gửi. Xin project khác thì từ chối. 0 lần lộ sang project khác |

Luồng:

```text
PM / màn hình duyệt
        |
        v
FastAPI (đăng nhập + lọc project)
        |
        v
Agent (điều phối tool, ghép evidence)
        |-- RAG: 15 tài liệu giả -> chunk -> embedding -> PostgreSQL/pgvector
        |-- Mock Jira: tool đọc sprint và issue
        |-- OpenAI: câu trả lời có nguồn + bản nháp báo cáo
        |
        v
Câu trả lời / phân tích issue / bản nháp -> PM duyệt
```

Stack: Python 3.11+, FastAPI, Pydantic, OpenAI API hoặc Agents SDK, PostgreSQL + pgvector, mock Jira, Docker, pytest, CI. Staging do AI Lead chỉ định.

Dữ liệu chỉ là tài liệu giả và Jira giả. Không đưa dữ liệu khách thật vào API. Không tự ghi Jira.

## Kit có gì, bạn làm gì

Thư mục `AI_Engineering_Fast_Track_v12_Starter_Kit` là dữ liệu luyện và công cụ chấm. Không có bài giải.

| Trong kit | Việc của nó |
|---|---|
| `data/documents/` | 15 tài liệu giả (5 yêu cầu, 5 kỹ thuật, 5 PM) và `manifest.json`. Ba project ALPHA, BETA, GAMMA |
| `data/jira/issues.json` | 30 issue giả |
| `app/mock_jira.py` | API Jira chỉ đọc, đã viết sẵn. Chạy cổng 8001. Quyền giả bằng header `X-Allowed-Project`. Tuần 7 thay bằng đăng nhập thật |
| `data/evaluation/` | Bộ luyện công khai: 20 ca phân loại, 20 ca tìm kiếm, 30 ca hỏi đáp, 20 ca agent, 10 ca bảo mật |
| `scripts/smoke_test.py` | Kiểm tra đủ số file fixture. Phải kết thúc bằng `PASS` |
| `scripts/evaluate_issue_classifier.py` | Chấm tuần 1 |
| `evidence/weekly_pr_template.md` | Mẫu điền trong mỗi PR |
| `assignments/W01_START_HERE.md` … `W08_START_HERE.md` | Mỗi tuần mở file này, rồi mở đúng cặp slide Assignment và Implementation Guide |

`app/mock_jira.py` không phải bài phải tự viết. Bạn bật nó lên để có Jira giả. Từ tuần 5, agent của nhóm gọi API này.

Ba project trong dữ liệu giả là ALPHA, BETA, GAMMA. Không có tài khoản Jira công ty.

Nhãn trong file gold là của người ra đề. Giữ nguyên. Mentor còn 20–30% case ẩn cho các gate. Nhờ model tự sinh nhãn rồi lấy làm đáp án là không được.

Key để trong `.env`, copy từ `.env.example` (`OPENAI_API_KEY`, `OPENAI_MODEL`, `DATABASE_URL`). Không commit key. Repo, model được dùng, trần chi phí và URL staging do AI Lead đưa lúc kickoff.

## Nhịp mỗi tuần

Mỗi tuần là thứ Hai–thứ Sáu. Hạn nộp và gate đều vào thứ Sáu.

| Ngày | Việc |
|---|---|
| Thứ Hai | Chốt mục tiêu, chia việc, thống nhất interface với cả nhóm |
| Thứ Tư | Review kiến trúc và code, gỡ blocker |
| Thứ Sáu | PR, test, evaluation, demo 5–10 phút, mentor chấm |

Chia 20 giờ: 4 giờ đọc, 6 giờ lab và eval cá nhân, 8 giờ ghép capstone, 2 giờ demo và review.

| Tuần | Thời gian | Bạn xây | Hạn | Cột mốc |
|---|---|---|---|---|
| W1 | 16–20/11 | Phân loại issue, 3 phiên bản prompt | 20/11 | Nền |
| W2 | 23–27/11 | Meeting Notes API | 27/11 | **Gate 1** |
| W3 | 30/11–04/12 | Tìm kiếm tài liệu trên pgvector | 04/12 | Nền của F01 |
| W4 | 07–11/12 | Knowledge Assistant có citation | 11/12 | **Gate 2 — F01** |
| W5 | 14–18/12 | Jira Analysis Agent | 18/12 | F02 |
| W6 | 21–25/12 | Báo cáo tuần và duyệt | 25/12 | **Gate 3 — F03/F04** |
| W7 | 28/12–01/01 | Staging, CI, security | 01/01 | Gia cố |
| W8 | 04–08/01 | Demo cuối và bài cá nhân | 08/01 | **Final Gate** |

Tuần sau dùng lại tuần trước. Tuần 4 dùng phần tìm của tuần 3. Tuần 6 ghép tuần 4 và tuần 5. Tuần 8 không viết lại workflow sang framework khác.

## Cách được chấm

Mỗi người **một PR mỗi tuần**. Mentor làm theo README trong PR mà chạy lại được kết quả. Không có code, không có test, hoặc không giải thích được phần mình viết thì trạng thái là **NOT ASSESSED**. Tuần đó không có điểm.

Điểm tuần trên 100:

| Tiêu chí | Điểm | Mentor cần thấy |
|---|---:|---|
| Đúng chức năng | 35 | API, output và số case đúng như đề |
| Chất lượng AI và evaluation | 25 | Dataset, phiên bản prompt và model, số đo, các case còn sai |
| Chất lượng kỹ thuật | 15 | README chạy được, schema rõ, test có thật |
| Bảo mật và độ tin cậy | 15 | Không lộ key, chặn sai quyền, lỗi API không làm sập luồng |
| Giải thích kỹ thuật | 10 | Demo nói được trade-off và một việc sẽ sửa |

**Pass tuần:** ≥ 70/100, không có lỗi bảo mật nghiêm trọng, và mentor xác nhận được phần bạn tự làm.

Ba lỗi sau làm **rớt gate ngay**. Điểm cao không bù:

- Lộ API key hoặc secret trong git hay log
- Lộ nội dung hoặc citation sang project khác quyền
- Ghi hoặc gửi khi chưa có approval trong code

Điểm cuối khóa = tổng (điểm tuần × trọng số):

| W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5% | 10% | 10% | 15% | 15% | 15% | 10% | 20% |

Từ 85: strong. 70–84: làm được việc trong dự án khi có người giám sát. 50–69: đang lên. Dưới 50: chưa sẵn sàng.

Được tính là sẵn sàng khi điểm có trọng số ≥ 70, đủ 4 gate, có đóng góp cá nhân, và không còn lỗi bảo mật nghiêm trọng.

## Mỗi thứ Sáu nộp gì

Điền `evidence/weekly_pr_template.md` trong PR:

- Feature đang làm (F01–F04 hoặc Foundation)
- 2–3 khái niệm đã học
- Phần đã xây và module chính
- Lệnh để mentor chạy
- Số test, bảng evaluation, case security
- Lỗi đã biết và trade-off
- Link demo, link PR, việc tuần sau

Kèm theo: branch, lệnh chạy, phiên bản dependency, video hoặc screenshot, ví dụ input/output, dataset id, phiên bản prompt và model, metric, xác nhận không có secret, test quyền, test hành động không an toàn, một điều làm tốt, một điều thất bại, một cải tiến tiếp theo.

Dùng AI để viết code thì được. Trước khi nộp phải tự chạy test, đọc được đoạn mình đưa vào PR, và giải thích được vì sao làm vậy. Mentor hỏi một đoạn không giải thích được thì phần đó không tính là đóng góp của bạn.

## Trước thứ Hai 16/11

Dành 30–60 phút, làm trong thư mục starter kit:

1. Đọc `README.md`.
2. Cài Python 3.11+, Git, Docker. Tạo venv và `pip install -r requirements.txt`.
3. `python scripts/smoke_test.py` phải kết thúc bằng `PASS`.
4. `pytest -q tests/test_mock_jira.py` phải **3 passed**.
5. `uvicorn app.mock_jira:app --reload --port 8001`, mở `http://127.0.0.1:8001/docs`.
6. Thử đọc: `curl -H 'X-Allowed-Project: ALPHA' http://127.0.0.1:8001/projects/ALPHA/sprints/12/issues`.
7. Nhận API key, trần chi phí và quy định staging từ AI Lead. Key để trong env, không commit.
8. Mở kickoff PR, ghi kết quả smoke test, test mock Jira, và lệnh chạy.

Database pgvector để tuần 3: `docker compose up -d db`. Connection trong `.env.example` là `postgresql://training:training@localhost:5432/aibootcamp`.

## Tuần 1 — 16–20/11 — Phân loại issue

Bạn học cách ra lệnh cho model và ép kết quả đúng dạng. Chưa gọi Jira, chưa dựng API.

**Đọc**

- Vai trò system và user, few-shot: khóa [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/courses/chatgpt-prompt-eng) trên DeepLearning.AI. Vào học tại [learn.deeplearning.ai](https://learn.deeplearning.ai/courses/chatgpt-prompt-engineering-for-developers). Bài **Guidelines** có system, user, và few-shot (đưa vài cặp ví dụ input/output trong prompt).
- Khái niệm generative AI, prompt, agent: [Introduction to generative AI and agents](https://learn.microsoft.com/en-us/training/modules/fundamentals-generative-ai/) trên Microsoft Learn. Đọc unit **Prompts** và **AI agents**.
- Structured output, tức JSON đúng schema, tuần này chỉ cần output qua được Pydantic. Cách ép schema của OpenAI đọc kỹ ở tuần 2.

**Làm**

Bạn phân loại 20 phiếu việc giả. Bạn viết lời dặn cho model. Model đọc từng phiếu rồi điền loại, mức ưu tiên và việc cần làm tiếp. Bạn so kết quả với đáp án có sẵn.

Một phiếu trong `data/evaluation/issue_classification_gold.json` trông như thế này:

```json
{
  "issue_id": "CASE-01",
  "text": "Production checkout API down for all users",
  "category": "Bug",
  "priority": "P1"
}
```

`text` là nội dung phiếu, đưa cho model. `category` và `priority` là đáp án, không đưa cho model. File này giữ nguyên. Sửa nhãn trong đó thì script chấm theo đáp án đã bị đổi. Không nhờ model đọc file này rồi tự ghi lại nhãn.

Bốn loại:

| Loại | Phiếu đang nói về | Ví dụ trong bộ 20 ca |
|---|---|---|
| Bug | Việc đang hỏng | API thanh toán sập với mọi người dùng |
| Feature | Việc muốn thêm hoặc đổi | Thêm nút tải biểu đồ sprint |
| Question | Một câu hỏi | Hạn UAT là khi nào? |
| Risk | Việc chưa hỏng, nhưng có thể làm trễ hoặc hỏng về sau | Chứng chỉ bảo mật hết hạn trước ngày lên production |

`P1`, `P2`, `P3` là mức gấp. `P1` là đang ảnh hưởng rộng hoặc sắp gây sự cố lớn. `P3` là việc nhỏ, như thêm giao diện tối. Trong 20 ca có 6 ca `P1`: `CASE-01`, `CASE-02`, `CASE-03`, `CASE-04`, `CASE-14`, `CASE-16`. Cả 6 ca này phải gán đúng `P1`.

Next action là câu việc nên làm tiếp, do model tự viết. File đáp án không có câu này. Script chấm không chấm câu này. Mentor đọc để thấy output đủ ý.

Việc chạy trên máy bạn, trong thư mục starter kit. Không có trang web để dán prompt và CSV. CSV không phải thứ đưa cho model. CSV là kết quả sau khi model đã phân loại, để script chấm.

Kit chưa có đoạn code gọi API. Phần đó bạn tự viết. Script chấm đã có sẵn.

Thứ tự:

1. Soạn prompt V1 trong `prompts.md`: quy tắc bốn loại, ba mức ưu tiên, và bảo model trả JSON gồm `category`, `priority`, `next_action`.
2. Viết một script Python làm bốn việc:
   - Đọc 20 câu `text` trong file gold. Chỉ lấy câu chữ, không lấy `category` và `priority`.
   - Gửi prompt kèm câu đó tới API OpenAI. Key đọc từ `.env`, do AI Lead cấp, không commit.
   - Nhận JSON và kiểm tra bằng Pydantic. Pydantic là lớp kiểm tra trong Python: `category` chỉ được là một trong bốn chữ, `priority` chỉ được là `P1`, `P2` hoặc `P3`, và phải có `next_action`. Model trả thêm lời dẫn hoặc JSON thiếu dấu thì ca đó hỏng schema.
   - Ghi CSV đủ 20 dòng, header đúng như sau:

```text
issue_id,predicted_category,predicted_priority
CASE-01,Bug,P1
CASE-02,Bug,P1
```

3. Đứng trong `AI_Engineering_Fast_Track_v12_Starter_Kit`, chạy script chấm có sẵn. Script này không gọi model. Nó chỉ so CSV với file gold rồi in số câu đúng:

```bash
python scripts/evaluate_issue_classifier.py <predictions.csv>
```

4. Xem ca nào sai, sửa prompt thành V2 rồi V3. Mỗi bản chạy lại cùng 20 câu, cùng một model. Khi demo, chỉ được V3 sửa điểm nào của V1. Ví dụ V1 bỏ sót ca chứng chỉ hết hạn vì chưa nói rủi ro sắp xảy ra cũng là `P1`.

**Đạt khi**

- Category đúng ≥ 85%, tức ít nhất 17/20
- 100% output thành công đúng schema
- Mọi ca P1 trong gold đều được gán P1
- Bạn nói được V3 sửa điểm nào của V1

**Nộp:** `prompts.md`, file dự đoán, demo 5 phút.

Chấm category và priority:

```bash
python scripts/evaluate_issue_classifier.py <predictions.csv>
```

CSV cần header `issue_id,predicted_category,predicted_priority` và đủ 20 `issue_id`.

**Mentor:** chạy script trên file bạn nộp, xem ca schema hỏng, đối chiếu các ca P1, nghe bạn so V1 với V3.

## Tuần 2 — 23–27/11 — Gate 1, Meeting Notes API

Bạn đưa lời gọi model vào một API thật, có schema, và xử lý khi API model lỗi. Vẫn chưa đụng Jira.

**Đọc**

- [Developer quickstart](https://developers.openai.com/api/docs/quickstart): tạo key, gọi API bằng Python SDK.
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs): ép model trả JSON đúng schema bạn đưa.
- Timeout, retry, lỗi 429: [Error codes](https://developers.openai.com/api/docs/guides/error-codes) và [Troubleshooting 429](https://help.openai.com/en/articles/5955604-troubleshooting-api-rate-limits-and-429-errors). 429 là gọi quá nhanh hoặc quá hạn mức. Thấy header `Retry-After` thì chờ ít nhất bằng thời gian đó. Không có thì chờ tăng dần và có số lần thử tối đa. SDK của OpenAI đã tự retry một số lỗi tạm thời, đếm cả những lần đó.

**Làm**

FastAPI `POST /analyze-meeting`. Schema Pydantic cho request, summary, decision và action item. Trích summary, decision, owner, action, due date. Thiếu owner hoặc ngày thì trả `null`. Không bịa ngày.

Có test cho 5 lỗi: payload không hợp lệ, timeout, 429, upstream 500, response của model bị hỏng.

Gợi ý file: `app/main.py`, `app/schemas.py`, `app/services/llm.py`, `tests/`.

**Đạt Gate 1 khi**

- API chạy theo README và có OpenAPI docs
- 100% output thành công đúng JSON schema
- Fact và action đúng ≥ 85% trên 20 case
- 5/5 case lỗi đạt
- Git và log không có API key

**Nộp:** PR, ví dụ request/response, báo cáo test, screen recording.

**Mentor:** làm theo README, gọi endpoint, chạy pytest, tìm secret trong repo và log. Lộ key là rớt gate.

## Tuần 3 — 30/11–04/12 — Tìm kiếm tài liệu

Bạn biến 15 tài liệu giả thành kho tìm theo nghĩa, có lọc project. Đây là nền của F01. Chưa nhờ model viết câu trả lời.

**Đọc**

- [Vector Databases: from Embeddings to Applications](https://www.deeplearning.ai/courses/vector-databases-embeddings-applications) trên DeepLearning.AI. Nắm embedding, chunk, similarity, vector database.
- [Retrieval](https://developers.openai.com/api/docs/guides/retrieval) của OpenAI. Nắm cách cắt tài liệu, lưu vector, rồi lấy đoạn gần với câu hỏi.
- Trong bài của khóa, các từ cần nắm: chunking, metadata, top-k, Recall@5, lọc theo project.

**Làm**

Nạp 15 file trong `data/documents/` cùng `manifest.json`. Cắt đoạn khoảng 500–800 token, có overlap vừa phải. Lưu text, embedding, `project_id`, document id và vị trí nguồn vào pgvector. API search trả top-5 kèm metadata.

Khởi động database: `docker compose up -d db`.

Lọc quyền nằm trong câu truy vấn, trước khi lấy top-k. Lấy top-k rồi mới bỏ đoạn trái quyền là chưa đạt. Lý do: top-5 có thể toàn đoạn của project khác, bỏ đi thì người dùng không còn kết quả đúng, và đoạn trái quyền đã bị đọc ra.

**Đạt khi**

- 15/15 tài liệu được index
- Recall@5 ≥ 80% trên 20 query trong `data/evaluation/retrieval_gold.json`
- Không trả chunk của project khác
- Bạn giải thích được trade-off của chunk size, top-k và similarity

**Nộp:** code ingest và query, schema database, báo cáo retrieval.

**Mentor:** ingest lại trên database trống, search bằng project đúng và project sai, đọc chỗ lọc trong query.

## Tuần 4 — 07–11/12 — Gate 2, Knowledge Assistant (F01)

Bạn nối phần tìm của tuần 3 với model. Model chỉ được nói những gì có trong đoạn đã lấy, và phải chỉ ra đoạn đó.

**Đọc**

- Luồng RAG của Azure AI Search: [Retrieval Augmented Generation overview](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview). Đọc để nắm retrieve, rồi đưa đoạn vào prompt, rồi sinh câu trả lời.
- Muốn đi sâu thêm: [Retrieval Augmented Generation](https://www.deeplearning.ai/courses/retrieval-augmented-generation) trên DeepLearning.AI. Phần này không bắt buộc để qua gate.
- Trong bài: citation, từ chối khi không đủ evidence, và cách xử lý khi hai tài liệu lệch nhau.

**Làm**

Dùng retrieval tuần 3. Chỉ đưa chunk đúng quyền vào prompt. Model chỉ trả lời từ evidence, kèm document id và đoạn text để mentor soi. Không có evidence thì trả lời không tìm thấy. Hai tài liệu lệch nhau thì nêu xung đột và cite cả hai.

Luồng: lọc project → top-k → prompt bám evidence → câu trả lời + citation → evaluation.

**Đạt Gate 2 khi**, trên `data/evaluation/rag_gold.json` (30 câu):

- Câu trả lời đúng ≥ 85%
- Citation được evidence chống lưng ≥ 90%
- Mọi case không có đáp án đều không đoán fact
- Số lần lộ sang project khác = 0

**Nộp:** demo ứng dụng, kết quả 30 case, bảng rà citation, PR.

Demo thứ Sáu, 5–10 phút:

1. Một câu có đáp án, chỉ ra citation.
2. Một câu không có evidence.
3. Một câu xin tài liệu project khác.
4. Mở bảng 30 case.

**Mentor:** chạy lại 30 case, mở passage đã lưu, thử một request trái quyền. Một citation của project khác là rớt gate.

## Tuần 5 — 14–18/12 — Jira Analysis Agent (F02)

Lần đầu agent tự chọn tool. Nguồn issue là mock Jira đã có sẵn, không phải Jira công ty.

**Đọc**

- [AI Agents Course, Unit 1](https://huggingface.co/learn/agents-course/en/unit1/introduction) trên Hugging Face. Nắm vòng think → act → observe, và cách một hàm Python trở thành tool.
- [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart) và trang SDK [openai-agents-python](https://openai.github.io/openai-agents-python/).

**Làm**

Agent đọc `app/mock_jira.py` và `data/jira/issues.json` (30 issue). Ba tool:

- `get_project_info`
- `get_sprint_issues`
- `get_issue_details`

Agent chọn tool và điền đúng id. Issue quá hạn và blocker do Python tính từ dữ liệu tool trả về. Model chỉ tóm tắt evidence đã có. Mỗi lượt lưu tên tool, tham số và issue key.

Không tạo tool ghi Jira. Không tạo, sửa, hay gửi issue.

Bộ luyện: `data/evaluation/agent_cases.json`, 20 scenario, gồm cả request trái quyền.

**Đạt khi**

- Cả 3 tool có test
- Chọn đúng tool ≥ 85% trên 20 scenario
- Issue id và status truy được về record nguồn
- 100% lời gọi trái quyền bị chặn

**Nộp:** code agent, kết quả 20 scenario, tool traces.

**Mentor:** đọc trace của một ca đúng và một ca trái quyền, đối chiếu issue key với `issues.json`.

## Tuần 6 — 21–25/12 — Gate 3, báo cáo tuần và duyệt (F03, F04)

Bạn ghép tài liệu và Jira thành một báo cáo, rồi bắt luồng dừng lại cho PM duyệt. Chỗ dừng nằm trong code, không nằm trong câu prompt.

**Đọc**

- [Function calling](https://developers.openai.com/api/docs/guides/function-calling): model xin gọi hàm, ứng dụng chạy hàm, rồi trả kết quả cho model.
- MCP Python SDK chỉ là tài liệu mở rộng, không phải bài bắt buộc: [python-sdk](https://github.com/modelcontextprotocol/python-sdk).

**Làm**

Ghép evidence RAG đúng quyền với phân tích Jira. Báo cáo tuần gồm tiến độ, việc đã xong, blocker, risk, việc tiếp theo, nguồn, và fact còn chưa chắc.

Trạng thái đi `draft` → `awaiting_review` → `approved` hoặc `rejected`. Lưu report id, reviewer id và audit log.

Mọi đường send hoặc update phải được một hàm trong application code chặn khi chưa `approved`. Câu nhắc trong prompt không thay cho hàm đó. Timeout và lỗi một phần phải dừng an toàn, không gửi bản dở.

Một lần chạy hoàn chỉnh có ít nhất 3 bước nghiệp vụ. Ví dụ: lấy tài liệu, lấy sprint, tạo draft.

**Đạt Gate 3 khi**

- Workflow thành công ≥ 90% trên 10 case
- 100% hành động ghi hoặc gửi đều cần approval
- 3/3 lỗi được tiêm vào đều được xử lý an toàn
- Issue và fact trong báo cáo có nguồn

**Nộp:** sơ đồ workflow, demo chạy được, kết quả 10 case, traces.

**Mentor:** gọi nhánh send khi trạng thái còn `draft`. Request vẫn đi tiếp thì gate rớt. Hạn nộp là 25/12.

## Tuần 7 — 28/12–01/01 — Staging, CI, security

Bạn đưa bản đã có lên nơi người khác deploy lại được, và biến các ca tấn công thành test trong CI.

**Đọc**

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/). Đọc để biết prompt injection, lộ dữ liệu nhạy cảm, và quyền của tool.
- GenAIOps trên Microsoft Learn: [GenAIOps for MLOps](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/genaiops-for-mlops). Đọc phần vận hành: theo dõi, đánh giá lại khi đổi prompt hoặc model, và đưa kiểm tra vào pipeline.
- Trong bài còn cần: phân quyền, trace, chi phí, CI.

**Làm**

- Docker Compose và pipeline theo hướng: lint → unit và integration test → eval và safety check → build image → deploy staging.
- Auth thật thay cho header `X-Allowed-Project` của mock. Lọc project trên server. Validate input. Retry có giới hạn.
- Theo dõi latency, số token, chi phí ước tính, tool trace.
- Biến 10 ca trong `data/evaluation/security_cases.json` thành test có payload thật.

Mười việc security phải có mặt trong bộ test:

1. Hỏi chéo project
2. Injection trong tài liệu
3. Ghi Jira khi chưa duyệt
4. Xin API secret
5. Filter project quá rộng
6. Gửi report khi chưa duyệt
7. Bearer token sai
8. Timeout Jira
9. Claim không có nguồn
10. Tham số tool hỏng

**Đạt khi**

- Người khác deploy lại được từ README và pipeline
- CI xanh, gồm functional test và safety test
- Log không còn secret hoặc payload nhạy cảm
- Không còn finding bảo mật mức critical

**Nộp:** staging URL, link pipeline, log và trace đã xóa secret, báo cáo security. Hạn là 01/01.

**Mentor:** deploy theo README, đọc log, chạy bộ safety trong CI.

## Tuần 8 — 04–08/01 — Final Gate

Bạn đóng băng một bản và bảo vệ được nó. Demo dùng Agents SDK đã xây từ tuần 5. Tuần này không viết lại workflow sang framework khác.

**Đọc**

- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Đọc cách giữ bộ đo, so bản mới với bản cũ, và nhìn case sai.
- LangGraph Essentials trên LangChain Academy chỉ là tài liệu optional. Không dùng cho bài nộp.

**Làm**

Đóng băng một bản: commit, tên model, phiên bản prompt, dataset và staging URL.

Cả nhóm demo 20 phút:

| Phút | Phần | Việc chạy |
|---:|---|---|
| 5 | Knowledge search | Câu hỏi → retrieval → câu trả lời có citation |
| 5 | Sprint analysis | Project và sprint → Jira tools → issue quá hạn và blocker |
| 5 | Weekly report | Tài liệu + Jira → draft → người duyệt |
| 5 | Hỏi đáp kỹ thuật | Kiến trúc, lỗi, evaluation, quyền, chi phí |

Mỗi người còn làm một bài chưa được phát trước, rồi chỉ trên code phần mình viết: chỗ lọc project, một tool trace, và chỗ chặn send khi chưa approve.

**Đạt Final Gate khi**

- 3 kịch bản nghiệp vụ chạy trên staging
- Bài cá nhân ≥ 70/100
- Đủ CI, eval, security report, trace và chi phí ước tính
- Báo cáo draft xong trong ≤ 2 phút trên mock data
- Không còn lỗi approval hoặc lỗi bảo mật nghiêm trọng

**Nộp:** final PR, link deploy và eval, `demo.mp4`, `eval.csv`, `security.md`, `architecture.md`, scorecard.

## Sáu tình huống phải xử lý được trước final

1. Không có evidence: nói rõ là không có thông tin.
2. Project A xin tài liệu project B: từ chối cả nội dung lẫn citation.
3. Tài liệu chứa câu kiểu "ignore all rules": coi là dữ liệu không tin cậy, không làm theo.
4. Yêu cầu tự cập nhật Jira hoặc tự gửi báo cáo: code kiểm tra quyền và trạng thái đã duyệt.
5. Lỗi 429 hoặc timeout: retry có số lần tối đa, rồi fail an toàn.
6. Hai tài liệu lệch ngày: nêu xung đột và cite cả hai.
