# MCM Partner Growth OS - Review Tech & Map Case Study ZeremAI

> Mục đích: map công thức case study ZeremAI sang dự án MCM/Hermes, so sánh tech họ dùng với tech MCM đã có, và đưa ra phương án cải thiện để bán nội bộ công ty hoặc nhân bản sang ngành khác.
> Nguồn tham chiếu: `zeremai-10-cases-to-oss-stack.html`, workflow 5 agents MCM, vendor-package playbooks, ADR-002, ADR-004.
> Cập nhật: 2026-06-25

---

## 1. Tóm tắt điều hành

ZeremAI không thật sự bán SaaS. Họ bán một công thức agency retainer:

**CRM/board + automation + AI personalization + dashboard realtime + nhịp họp KPI**

Họ áp cùng một công thức này cho nhiều ngành, đóng gói thành hệ điều hành tăng trưởng, rồi thu khoảng **$5,000-15,000/tháng**. Tiền thật nằm ở phần vận hành/agency retainer, không nằm ở tiền phần mềm. Stack SaaS thường chỉ tốn khoảng **$150-600/tháng**, còn bản OSS/self-host trên VPS có thể kéo xuống khoảng **$50-150/tháng**.

MCM/Hermes có công thức tương đương:

**Tuyển người bán bên ngoài -> qualify -> kích hoạt 7 ngày -> track hành động/lead -> AI coaching -> xếp hạng/trả thưởng hằng tuần -> sync lead nóng cho sales nội bộ**

Vì vậy MCM không nên được định vị là bot, agent project, hay dashboard. MCM nên được định vị là:

**Partner Growth Operating System**

Câu bán hàng một dòng:

> MCM giúp công ty biến affiliate, vendor, partner, referrer hoặc thành viên cộng đồng thành một đội sales bên ngoài có onboarding, daily action, coaching, ranking, payout và CRM sync.

---

## 2. Công thức ZeremAI vs công thức MCM

| Công thức ZeremAI | Vai trò thật | Tương đương trong MCM/Hermes |
|---|---|---|
| CRM/board | Một nguồn sự thật cho lead, deal, stage, owner | EspoCRM + Google Sheet `Affiliate Master` |
| Zapier/Make automation | Chuyển dữ liệu giữa form, CRM, message, dashboard | Agent1-5 webhook, cron, Python scripts |
| AI personalization | Gửi message tốt hơn theo segment/status/context | Agent1 score, Agent2 onboarding, Agent3 coaching/report |
| Dashboard realtime | Cho thấy bottleneck và next action | Dashboard `:3003`, Sheet, Agent3/5 reports |
| Nhịp họp KPI | Biến data thành nhịp vận hành | Checklist 7AM, coaching 2PM, report 8PM/9PM, weekly payout/rank |
| Agency retainer | Bán vận hành, không bán quyền dùng phần mềm | MCM có thể bán managed partner/vendor growth ops |

Công thức MCM:

```text
Recruit -> Qualify -> Activate -> Track -> Coach -> Rank -> Pay -> Scale
```

Dịch sang thương mại:

> Xây và vận hành một kênh sales phân tán cho công ty. Thay vì tuyển thêm sales full-time trước, công ty tuyển partner/vendor/affiliate bên ngoài và đưa họ vào một hệ vận hành có tracking, coaching, KPI và payout.

---

## 3. So sánh tech stack

| ZeremAI / paid stack | Vai trò trong case study | MCM đã có gì | Review / quyết định cải thiện |
|---|---|---|---|
| Monday.com / Attio / HubSpot / GoHighLevel | CRM, pipeline, lifecycle board, dashboard vận hành | EspoCRM Docker + Google Sheet ledger | Giữ EspoCRM làm CRM duy nhất. Không thêm Twenty/Chatwoot/CRM khác nếu không bỏ cái cũ. |
| Zapier / Make | Automation bridge giữa các SaaS | 5 Python agents, webhook servers, cron jobs | Giữ Hermes agents. Chỉ thêm n8n ở phase Bundle/client khi workflow đủ phức tạp. |
| AI personalization / Copilot / Claude | Personalized outreach, scoring, content, coaching | 9Router + LLM calls trong Agent1/2/3/5 + fallback templates | Ổn định LLM trước. Personalization là đòn bẩy doanh thu, không phải trang trí. |
| Monday/HubSpot dashboards / BI | Founder/team thấy bottleneck | Dashboard `:3003`, Google Sheet, Agent3/5 reports | Cải thiện câu hỏi KPI trước khi thêm BI nặng. Tránh Metabase/Superset lúc này. |
| Slack / email / SMS / Twilio | Channel gửi thông báo và follow-up | Telegram Bot / Telegram DM/group | Giữ Telegram-first. Email/SMS chỉ thêm khi ngành bắt buộc. |
| Clay / Apollo | Prospecting và enrichment waterfall | Chưa cần cho affiliate core | Để phase B2B outbound hoặc SOP Bundle sales engine. |
| DocuSign / SignNow | Ký hợp đồng | Chưa có | Thêm Docuseal khi bắt đầu bán Bundle/retainer thật. |
| Fireflies / meeting AI | Meeting transcript -> action items | Chưa cần trong flow MCM hiện tại | Optional cho agency/client ops, không phải core affiliate system. |
| Snowflake / data warehouse / BI nặng | Finance/analytics layer lớn | Sheet + reports | Defer tới khi Sheet thật sự thành bottleneck. |
| SaaS ngách như Carta/Ramp/LandInsight | Vận hành đặc thù từng ngành | Không liên quan core MCM | Xóa khỏi scope trừ khi ngành mục tiêu thật sự cần. |

Kết luận delete-first:

- Không chạy theo tool parity với ZeremAI.
- Copy hình dạng operating system của họ, không copy subscription SaaS.
- MCM đã có đủ tech để đóng gói core offer.

---

## 4. MCM đã có tech gì rồi

### Core automation

| Layer | Asset hiện tại | Vai trò |
|---|---|---|
| Capture | Agent1 | Webhook/form capture, Telegram Q1/Q2, lead scoring, ghi Sheet |
| Activation | Agent2 | Onboarding D1-D7, `onboard_day`, progression status |
| Daily operations | Agent3 | Checklist, coaching, report, rank/gap message |
| CRM sync | Agent4 | EspoCRM webhook, opportunity/commission/rank sync |
| Monitor | Agent5 | System report, weekly summary, Sheet -> CRM sync |

### Infra

| Asset | Vai trò |
|---|---|
| EspoCRM + MySQL Docker | CRM và source of truth cho sales |
| Google Sheet | Operational ledger cho affiliate, activity, onboarding, commission |
| Telegram Bot | Kênh giao tiếp lead, affiliate, admin |
| 9Router | LLM proxy, là điểm rủi ro nếu quota chết |
| Dashboard `:3003` | View/report layer nhẹ |
| systemd + cron | Runtime và nhịp vận hành |

### Playbook / SOP assets

| Asset | Vai trò |
|---|---|
| `AGENTS.md` | Lifecycle và branch logic của 5 agents |
| `playbook/vendor-package/*` | Daily/weekly/monthly vendor operations |
| `knowledge/VENDOR-GROWTH-PLAN.md` | Gap về tuyển vendor, activation, rank, offer |
| `docs/adr/002-single-crm-delete-first.md` | Quyết định giữ 1 CRM: EspoCRM |
| `docs/adr/004-llm-fallback-and-quota.md` | Xác định LLM reliability là binding constraint |

MCM đã có khoảng **70-80% technical operating system**. Phần thiếu là đóng gói thành offer bán được, đo được, và nhân bản được sang ngành khác.

---

## 5. Gap hiện tại

### 5.1 Gap định vị

Rủi ro hiện tại: MCM bị nhìn như bot/agent/scripts.

Định vị đúng:

**Hermes Partner Growth OS**

Bán outcome:

- tuyển thêm người bán bên ngoài
- kích hoạt nhanh trong D7
- có lead tracking
- giảm cost per lead
- có weekly payout/rank discipline
- sync lead nóng về sales nội bộ

### 5.2 Gap đo lường

MCM track affiliate/referral được, nhưng chưa có **Social Performance Tracker** sạch.

Các field tối thiểu cần có:

| Field | Ý nghĩa |
|---|---|
| `date` | Ngày post |
| `affiliate_username` | Match với Affiliate Master |
| `post_url` | Link post X/Twitter |
| `channel` | X, Telegram, Facebook, v.v. |
| `source` | Nguồn signal/content |
| `views` | Reach |
| `replies` | Engagement |
| `clicks` | Click nếu có |
| `leads` | Lead attributed |
| `refer_count` | Referral attributed |
| `notes` | Hook/source/comment |

Đây là bài học từ Studio B: hệ thống phải biết content/source/vendor nào thắng.

### 5.3 Gap LLM reliability

Đòn bẩy Landhold/One Golden Thread là personalization và scoring. Khi LLM quota chết, hệ vẫn chạy bằng fallback cứng, nhưng mất đòn bẩy tạo tiền.

Cần cải thiện:

- Giữ hardcoded fallback.
- Khôi phục paid LLM capacity.
- Thêm gateway/budget layer như LiteLLM.
- Alert admin trước khi quota fail âm thầm.

### 5.4 Gap sales kit

MCM cần artifact để bán nội bộ và bán ra ngoài:

- one-page offer
- deck 8-10 slide
- ROI calculator
- case study nội bộ
- demo dashboard
- timeline triển khai 30 ngày
- SOW/contract template
- pitch template theo ngành

### 5.5 Gap cadence

Cron/report đã có, nhưng packaging kinh doanh chưa rõ.

Cần bán cả nhịp vận hành:

- daily 10 phút action review
- weekly rank/payout review
- monthly source/channel strategy review

Đây là một phần của sản phẩm, không phải việc admin phụ.

---

## 6. Phương án cải thiện cho MCM

### Phase 1 - Đóng gói offer

Tạo ngôn ngữ bán hàng:

```text
Hermes Partner Growth OS giúp công ty tuyển, kích hoạt, track, coach, xếp hạng và trả thưởng cho external sellers để sales nội bộ nhận được nhiều qualified leads hơn mà chưa cần tuyển thêm full-time sales team.
```

Định nghĩa pitch nội bộ:

```text
Đây không phải bot project. Đây là distributed sales operating system.
```

Buyer outcomes:

- nhiều partner được tuyển hơn
- D7 activation cao hơn
- nhiều post/action mỗi tuần hơn
- nhiều tracked leads hơn
- cost per qualified lead thấp hơn
- sales follow-up nhanh hơn
- payout/rank rõ hơn

### Phase 2 - Làm measurement thành thật

Build Social Performance Tracker nhẹ trên Google Sheet trước.

Report phải trả lời:

- Affiliate/vendor nào tạo nhiều lead nhất?
- Post nào tạo nhiều lead nhất?
- Source/channel nào nên scale?
- Affiliate nào inactive hoặc tụt hiệu suất?
- Ngày mai từng người cần làm gì?

Chỉ cân nhắc NocoDB khi nhập liệu bằng Sheet bắt đầu đau.

### Phase 3 - Ổn định personalization

LLM reliability phải được xem là revenue infrastructure.

Tiêu chuẩn tối thiểu:

- primary model
- fallback model
- hardcoded template
- 402/429 short-circuit
- cost/budget tracking
- Telegram quota alert

Không build thêm feature personalization mới khi reliability chưa ổn.

### Phase 4 - Biến report thành KPI meeting

Daily:

- ai cần post hôm nay
- ai cần coaching
- lead nào cần follow-up

Weekly:

- top vendor/affiliate
- payout
- rank movement
- best post/source
- inactive list

Monthly:

- cost per valid lead
- sales conversion
- partner quality
- quyết định source/channel: scale, fix, hoặc cut

### Phase 5 - Build template theo ngành

Mỗi ngành chỉ đổi 5 biến:

1. Partner là ai?
2. Họ làm hành động gì mỗi ngày?
3. Lead event được track là gì?
4. Reward/payout là gì?
5. Sales nội bộ nhận lead ở đâu?

Giữ core engine giống nhau.

---

## 7. Template map sang ngành khác

| Ngành | Partner / external seller | Daily action | Lead event | Payout / reward |
|---|---|---|---|---|
| Trading / Forex | X hoặc Telegram affiliate | Post signal/content, kéo group joins | Group join, qualified lead, VIP sale | Per join / per sale |
| Bất động sản | Broker địa phương, referrer, community contact | Giới thiệu buyer/renter/investor | Booking, viewing, qualified buyer | Per qualified lead / deal |
| Clinic / Spa | Micro-KOL, khách cũ, local partner | Promote booking offer | Appointment booked, treatment paid | Per booking / paid visit |
| Education / Course | Student ambassador, creator, community owner | Review khóa học, mời webinar | Trial, webinar signup, enrollment | Per enrollment |
| SaaS B2B | Consultant, agency partner, community admin | Refer business lead | Demo booked, subscription | Per qualified demo / closed sale |
| Recruitment | Referral partner, employee, niche community owner | Refer candidate | Interview, hire | Per interview / hire |
| Local F&B | Micro-influencer, customer ambassador | Post coupon/menu offer | Coupon use, booking | Per redemption |
| Gym / Fitness | Member ambassador, PT partner | Invite trial | Trial pass, membership | Per trial / member |
| Agency services | Partner agency, freelancer, consultant | Refer client | Discovery call, retainer | Per call / closed retainer |

---

## 8. Logic pricing

Dùng ZeremAI làm anchor, nhưng adapt theo thị trường.

| Tier | Price anchor | Phù hợp với | Deliverable |
|---|---:|---|---|
| Setup Sprint | $1k-3k one-time | Khách muốn pilot đầu tiên | CRM/Sheet, bot, onboarding, tracking, first report |
| Managed Ops | $3k-8k/month | Khách đã có partner/affiliate channel | Weekly operations, coaching, reports, optimization |
| Growth Retainer | $8k-15k/month | Khách muốn scale nhiều source/region | Recruitment, activation, tracking, sales sync, monthly strategy |

Giá local/Vietnam có thể adapt:

| Tier | Local anchor |
|---|---:|
| Setup Sprint | 20-60 triệu VND |
| Managed Ops | 30-120 triệu VND/tháng |
| Growth Retainer | 120-300 triệu VND/tháng |

Giá không phải cho phần mềm. Giá là cho managed growth operations.

---

## 9. Sales narrative nội bộ

Dùng narrative này với founder/sales team:

> Hầu hết công ty muốn tăng doanh thu thì nghĩ tới ads hoặc tuyển thêm sales. Cả hai đều đắt và chậm. Hermes Partner Growth OS tạo kênh tăng trưởng thứ ba: external sellers. Hệ thống tuyển họ, kích hoạt họ trong 7 ngày, giao daily actions, track từng lead, coach người yếu, rank/pay người thắng, và sync lead nóng về sales nội bộ.

Short version:

> Biến partner bên ngoài thành một kênh sales có quản trị.

Sales nội bộ nhận được:

- lead nóng hơn
- biết source nào tạo lead
- biết thời điểm follow-up
- biết context affiliate/vendor
- giảm tracking thủ công
- có weekly view ai tạo revenue

---

## 10. Acceptance criteria

Plan này hữu dụng khi MCM có thể trả lời các câu hỏi này cho chính mình hoặc cho bất kỳ ngành mục tiêu nào:

1. External seller là ai?
2. Họ làm hành động gì mỗi ngày?
3. Lead được track thế nào?
4. Lead tốt được định nghĩa là gì?
5. Ai follow-up nội bộ?
6. Reward/payout tính thế nào?
7. Weekly KPI meeting review số nào?
8. Source/channel nào nên scale, fix, hoặc cut?

Artifact tối thiểu tiếp theo:

- one-page offer cho Hermes Partner Growth OS
- internal sales deck
- Social Performance Tracker sheet
- ROI calculator
- checklist triển khai 30 ngày
- thư viện template theo ngành

---

## 11. Định vị cuối

MCM/Hermes không chỉ là một AI agent project.

Nó là operating system tái sử dụng cho external sales channels:

```text
Recruit external sellers
-> activate them fast
-> give them daily actions
-> track every lead
-> coach by performance
-> rank/pay weekly
-> sync hot leads to internal sales
```

Đó là phiên bản MCM của công thức ZeremAI.

---

## 12. Công thức bán nội bộ & nhân bản sang ngành khác

### 12.1 Bản chất công thức bán được

ZeremAI bán cùng một công thức cho mọi ngành:

```text
CRM/board + automation + AI personalization + dashboard realtime + KPI cadence
-> đóng gói thành hệ điều hành tăng trưởng cho từng ngành
-> bán retainer $5,000-15,000/tháng
```

MCM/Hermes không nên bán "bot", "agent", hay "tool". Công thức bán được của MCM là:

```text
Lead-getter network + activation system + performance tracking + AI coaching + payout/rank cadence
-> biến cộng tác viên/vendor/affiliate thành đội bán hàng phân tán
-> công ty có thêm lead/sales mà không cần tuyển full-time sales team trước
```

Công thức gốc:

```text
Recruit -> Qualify -> Activate -> Track -> Coach -> Rank -> Pay -> Scale
```

Diễn giải thành sản phẩm:

> Chúng tôi dựng cho công ty một hệ thống tuyển, kích hoạt, theo dõi và tối ưu đội cộng tác viên bán hàng/affiliate/vendor. Mỗi người ngoài công ty trở thành một kênh phân phối có tracking, KPI, coaching và payout rõ ràng.

### 12.2 Map tương đương ZeremAI -> MCM

| ZeremAI Formula | MCM/Hermes Formula |
|---|---|
| CRM/board | Affiliate/Vendor Master + EspoCRM |
| Zapier/Make automation | 5 Hermes agents webhook/cron |
| AI personalization | Agent1 score + Agent2 onboarding + Agent3 coaching |
| Realtime dashboard | Sheet/dashboard/report 7AM/2PM/8PM/9PM |
| KPI meeting cadence | Daily checklist, weekly rank/payment, monthly ops review |
| Agency retainer | Managed growth ops retainer |

### 12.3 Bán nội bộ công ty

Không pitch với sếp/team là:

> Em build bot.

Pitch đúng là:

> Đây là hệ thống biến người ngoài công ty thành đội sales phụ có kiểm soát. Công ty không phải tuyển thêm sales full-time trước. Mỗi affiliate/vendor được onboard, giao việc, đo kết quả, coach, xếp hạng và trả thưởng theo performance.

Tên offer nội bộ:

**Distributed Sales Ops System**

Offer bao gồm:

- Tuyển nguồn cộng tác viên/vendor/affiliate.
- Qualify tự động bằng form/Telegram.
- Onboarding 3-7 ngày để người mới biết làm gì.
- Daily checklist để họ hành động đều.
- Coaching khi họ không post hoặc tụt hiệu suất.
- Tracking link/source để biết ai tạo lead.
- Rank board để tạo cạnh tranh.
- Weekly payout/report để giữ động lực.
- CRM sync để sales nội bộ xử lý lead nóng.

### 12.4 KPI bán cho công ty

Bán cho công ty bằng số, không bằng tính năng.

| KPI | Ý nghĩa |
|---|---|
| New affiliates/vendors/week | Máy tuyển có chạy không |
| Activation rate D7 | Người mới có hành động không |
| Posts/vendor/week | Đội phân phối có tạo traffic không |
| Leads/source/week | Nguồn nào ra lead |
| Cost per valid lead | Có rẻ hơn ads/sales không |
| First sale / VIP conversion | Lead có ra tiền không |
| Churn/inactive rate | Hệ có giữ người không |
| Payout accuracy | Có giữ niềm tin không |

### 12.5 Nhịp họp KPI bán được

Đây là phần ZeremAI bán rất đắt: họ không chỉ dựng tool, họ dựng operating rhythm.

MCM phải đóng gói nhịp này thành một phần của sản phẩm:

- **Daily 10 phút:** hôm nay ai cần post, ai cần coach, ai có lead nóng.
- **Weekly 30 phút:** top vendor, source thắng, payout, rank up/down.
- **Monthly 60 phút:** CAC, revenue, vendor quality, quyết định scale hay cắt nguồn.

### 12.6 Universal formula để map sang ngành khác

Bất kỳ ngành nào có thể dùng MCM formula nếu thỏa 3 điều kiện:

1. Có sản phẩm/dịch vụ có margin đủ trả commission.
2. Có người ngoài công ty có thể giới thiệu hoặc kéo traffic.
3. Có hành động lặp lại được: post, giới thiệu, mời nhóm, booking, referral, demo.

Công thức ngành:

```text
Audience Holder -> Simple Action -> Tracked Lead -> Sales Follow-up -> Commission/Reward
```

### 12.7 Industry templates

| Ngành | "Vendor/Affiliate" là ai | Hành động chính | Lead được track |
|---|---|---|---|
| Forex/Trading | X/Telegram content vendor | Post tín hiệu, kéo vào group | Join, lead, VIP sale |
| BĐS | Broker/cộng tác viên địa phương | Giới thiệu khách mua/thuê | Booking, viewing, deal |
| Spa/Clinic | KOL nhỏ, khách cũ, cộng tác viên | Giới thiệu khách đặt lịch | Appointment, treatment |
| Education/Course | Student ambassador, creator | Review khóa học, mời webinar | Trial, call, enrollment |
| SaaS B2B | Consultant, agency partner | Giới thiệu business lead | Demo booked, subscription |
| Insurance/Finance | CTV tài chính, community admin | Referral form | Qualified consultation |
| Recruitment | Employee/referral partner | Giới thiệu ứng viên | Interview, hire |
| Local F&B | Micro-influencer, khách thân thiết | Post mã ưu đãi | Coupon use, booking |
| Gym/Fitness | Member ambassador/PT | Mời trial | Trial pass, membership |
| Agency Services | Partner/referrer | Giới thiệu client | Discovery call, retainer |

### 12.8 Productized retainer

Tên offer bán ra ngoài:

**Hermes Partner Growth OS**

Khách không mua code. Khách mua một hệ vận hành.

#### Partner Recruitment Engine

- Pitch tuyển partner.
- Form qualify.
- PASS/SOFT_PASS/FAIL rules.
- Source list/Dream 100.

#### Partner Activation Engine

- D1-D7 onboarding.
- First action checklist.
- Templates/scripts.
- Activation tracking.

#### Performance Tracking Engine

- Partner master.
- Activity log.
- Tracking link/source.
- Lead/opportunity sync.
- Payout ledger.

#### AI Coaching Engine

- Daily checklist.
- Inactive nudge.
- Performance drop coaching.
- Best-practice suggestions.

#### Management Cadence

- Daily ops report.
- Weekly rank/payout.
- Monthly strategy review.
- SOP audit.

### 12.9 Pricing logic

ZeremAI anchor: **$5k-15k/tháng**.

MCM nên đóng gói theo 3 tier:

| Tier | Giá gợi ý | Khách phù hợp | Deliverable |
|---|---:|---|---|
| Setup Sprint | $1k-3k one-time | Công ty muốn thử | Setup workflow + Sheet/CRM + bot cadence |
| Managed Ops | $3k-8k/month | Có partner/affiliate thật | Vận hành weekly, optimize, report |
| Growth Retainer | $8k-15k/month | Muốn scale đa nguồn | Full recruitment + activation + analytics + sales sync |

Nếu bán thị trường Việt Nam, có thể quy đổi mềm:

- Setup: 20-60 triệu VND.
- Managed: 30-120 triệu VND/tháng.
- Growth: 120-300 triệu VND/tháng.

### 12.10 MCM assets hiện có để biến thành sales kit

Dự án đã có phần lớn lõi:

- Agent1: capture/qualify/score lead.
- Agent2: onboarding D1-D7.
- Agent3: checklist/coaching/report.
- Agent4: CRM sync, commission/rank.
- Agent5: monitor/SOP audit.
- Playbook vendor-package: daily/weekly/monthly ops.
- Knowledge pack: vendor rules, FAQ, onboarding.
- EspoCRM + Sheet: source of truth.
- Telegram: execution channel.

Thiếu để bán chuyên nghiệp:

- One-page offer.
- Industry-specific pitch template.
- Demo dashboard.
- Case study nội bộ: before/after MCM.
- ROI calculator.
- 30-day implementation timeline.
- Sales deck 8-10 slides.
- Contract/SOW template.

### 12.11 Sales narrative chuẩn

> Hầu hết công ty muốn thêm doanh thu thì nghĩ đến ads hoặc tuyển sales. Cả hai đều đắt và chậm. Hermes Partner Growth OS tạo một lớp phân phối thứ ba: partner/affiliate/vendor bên ngoài. Hệ thống tuyển họ, kích hoạt họ trong 7 ngày, giao việc mỗi ngày, đo kết quả, coach người yếu, thưởng người thắng, và sync lead nóng về CRM cho sales nội bộ chốt.

Short version:

> Chúng tôi giúp công ty biến cộng đồng bên ngoài thành đội sales có tracking, KPI và payout.

### 12.12 30-day rollout plan

#### Week 1: Diagnose + Design

- Chọn một ngành/use case.
- Xác định partner là ai.
- Xác định tracked action: lead, booking, join, demo, sale.
- Thiết kế reward/payout.
- Setup CRM/Sheet schema.

#### Week 2: Build Operating System

- Setup capture form/bot.
- Setup partner master + activity log.
- Setup onboarding D1-D7.
- Setup tracking links/source tags.
- Setup daily/weekly reports.

#### Week 3: Pilot Partners

- Tuyển 10-30 partner đầu tiên.
- Chạy activation 7 ngày.
- Đo first action, first lead.
- Coach inactive partner.
- Fix copy, payout logic, tracking gaps.

#### Week 4: Scale Decision

- Review CAC/lead quality.
- Rank top partners.
- Cut bad sources.
- Double down best channel.
- Chốt retainer tháng tiếp theo.

### 12.13 Acceptance criteria của công thức bán lại

Plan này thành công khi có thể trả lời rõ 6 câu trong bất kỳ ngành nào:

1. Partner là ai?
2. Họ làm hành động gì mỗi ngày?
3. Lead được track bằng gì?
4. Khi nào họ được trả tiền/thưởng?
5. Ai trong công ty nhận lead để chốt?
6. Weekly KPI meeting nhìn số nào để quyết định scale/cut?

### 12.14 Final positioning

MCM/Hermes không phải "AI agent project".

Nó là:

**Partner Growth Operating System**

Áp dụng cho:

- affiliate
- vendor
- cộng tác viên sales
- referral network
- micro-influencer
- ambassador program

Công thức bán lại:

```text
Recruit external sellers
-> activate them fast
-> give them daily actions
-> track every lead
-> coach by performance
-> rank/pay weekly
-> sync hot leads to internal sales
```

---

## 13. Từ prompt sang agent loop cho MCM

### 13.1 Ý chính

Thời prompt engineering hỏi:

```text
Viết prompt thế nào cho hay?
```

Thời agent operating system hỏi:

```text
Đặt mục tiêu, quyền, vòng lặp, tiêu chí kiểm tra và điểm dừng thế nào để agent tự chạy mà không lạc đường?
```

Công thức mới cho MCM:

```text
Goal -> Loop -> Tool -> Check -> Stop -> Human Approval
```

MCM cần đóng gói phần này thành năng lực bán được:

> Chúng tôi không chỉ viết prompt cho AI. Chúng tôi thiết kế agent loop để công việc sales/affiliate/vendor tự chạy theo mục tiêu, có quyền hạn rõ, tự kiểm tra kết quả, biết khi nào phải hỏi người duyệt, và không vượt guardrail.

### 13.2 Prompt vs agent loop

| Tư duy prompt | Tư duy agent loop |
|---|---|
| Viết một lệnh thật dài | Thiết kế mục tiêu + vòng lặp |
| AI trả lời một lần | AI đọc kết quả, sửa plan, làm tiếp |
| Người dùng nhắc từng bước | Agent tự chia việc thành bước nhỏ |
| Output là câu trả lời | Output là trạng thái, log, hành động, report |
| Prompt càng chi tiết càng tốt | Goal, tool, permission, check, stop càng rõ càng tốt |

Prompt vẫn cần, nhưng prompt chỉ là một phần trong vòng lặp. Giá trị lớn hơn nằm ở thiết kế luật chơi.

### 13.3 Agent Contract Layer

Mỗi agent trong MCM nên có một contract rõ ràng:

| Thành phần | Câu hỏi phải trả lời | Ví dụ MCM |
|---|---|---|
| Goal | Mục tiêu cuối cùng là gì? | Biến lead mới thành affiliate đã qualify và nhận onboarding |
| Scope | Agent được xử lý phần nào? | Chỉ capture/qualify, không sửa commission |
| Tools | Được dùng tool nào? | Telegram, Google Sheet, 9Router, EspoCRM webhook |
| Permissions | Được làm gì, cấm gì? | Được gửi DM, không được xóa row, không được payout |
| Checks | Tự kiểm tra bằng gì? | Row có username chưa, score hợp lệ không, Telegram gửi OK không |
| Stop | Khi nào phải dừng? | Thiếu dữ liệu, lỗi 3 lần, hành động nhạy cảm, quota chết |
| Human Approval | Khi nào hỏi admin? | Xóa duplicate, thay payout, suspend affiliate, sửa CRM hàng loạt |
| Output | Kết quả phải để lại ở đâu? | Sheet row, Activity Log, Telegram message, admin report |

### 13.4 Map vào 5 agents hiện có

#### Agent1 - Capture

Goal: nhận lead, hỏi Q1/Q2, score, ghi Sheet, gửi welcome.

Loop:

```text
receive lead -> validate -> ask Q1 -> wait -> ask Q2 -> score -> upsert Sheet -> log -> welcome -> trigger Agent2
```

Guardrail:

- Không tạo duplicate username.
- Không ghi đè commission/rank/onboard progress.
- Nếu LLM lỗi thì dùng parser fallback.
- Nếu Sheet lỗi thì giữ state và báo admin.

Stop condition:

- Thiếu `telegram_username`.
- Telegram không gửi được.
- Sheet auth fail.
- Q1/Q2 quá 24h không trả lời.

#### Agent2 - Onboard

Goal: kích hoạt affiliate trong D1-D7.

Loop:

```text
read queue -> chọn next_day -> generate/fallback content -> send Telegram -> update onboard_day -> log
```

Guardrail:

- Mỗi user chỉ nhận một D message/ngày.
- Không promote Active nếu chưa đạt điều kiện.
- Nếu LLM quota lỗi thì dùng fallback, không dừng toàn flow.

Stop condition:

- Telegram fail.
- User không có chat_id/username.
- Sheet row không tìm thấy.

#### Agent3 - Daily Loop

Goal: giữ affiliate hành động đều và biết hôm nay cần làm gì.

Loop:

```text
read Affiliate Master -> detect status/performance -> generate checklist/coaching/report -> send -> log -> update rank
```

Guardrail:

- Chỉ coach khi có trigger: inactive, refer drop, onboarding status.
- Không spam affiliate nhiều lần trong ngày.
- Report phải có next action, không chỉ động viên chung.

Stop condition:

- LLM/fallback đều fail.
- Sheet read fail.
- User inactive quá ngưỡng cần admin review.

#### Agent4 - CRM Sync

Goal: đồng bộ CRM event thành trạng thái affiliate/commission/rank.

Loop:

```text
receive EspoCRM webhook -> validate event -> find affiliate -> update Sheet -> log -> notify/trigger Agent3
```

Guardrail:

- Không tạo row mới nếu username đã tồn tại.
- Commission update phải có event source.
- Rank/VIP thay đổi phải log rõ.

Stop condition:

- Payload thiếu username/lead_id.
- Event không thuộc whitelist.
- Commission bất thường cần admin duyệt.

#### Agent5 - Monitor

Goal: phát hiện hệ thống lệch hướng trước khi hỏng doanh thu.

Loop:

```text
check services -> check cron/report -> check Sheet/CRM sync -> detect errors -> report admin -> audit SOP
```

Guardrail:

- Không tự sửa dữ liệu production.
- Chỉ report hoặc trigger action đã whitelist.
- Lỗi lặp lại 3 lần thì escalate.

Stop condition:

- Service down.
- LLM quota gần hết/hết.
- Duplicate row tăng.
- Cron không chạy.
- CRM sync miss.

### 13.5 Permission matrix

| Action | Agent tự làm | Cần admin duyệt |
|---|---|---|
| Gửi onboarding/checklist/coaching | Có | Không |
| Ghi Activity Log | Có | Không |
| Upsert affiliate row | Có | Không, nếu không đụng payout/rank |
| Xóa row | Không | Có |
| Sửa commission/payout | Không | Có |
| Suspend/churn affiliate | Không | Có |
| Promote VIP theo rule rõ | Có | Admin nhận notification |
| Đổi prompt/fallback template | Không | Có |
| Gửi mass broadcast | Không | Có |
| Tạo tracking link | Có | Không |
| Thay CRM schema | Không | Có |

### 13.6 Test agent loop

- **Goal clarity test:** mỗi agent contract đọc lên phải trả lời được “agent này thắng khi nào?”.
- **Permission test:** case xóa row/sửa payout/mass broadcast phải dừng và yêu cầu admin.
- **Loop test:** lead mới đi qua Agent1 -> Agent2 -> Agent3, mỗi bước có output và log.
- **Fallback test:** tắt LLM, flow vẫn chạy bằng parser/template.
- **Stop test:** lỗi Sheet/Telegram 3 lần, agent không chạy mãi mà escalate.
- **Audit test:** Agent5 report service health, quota, duplicate, inactive, sync miss.

---

## 14. Cấu trúc thư mục AI project cho MCM

### 14.1 Ý chính

Với AI project, không nên bắt đầu bằng prompt rời rạc. Phải bắt đầu bằng **cấu trúc thư mục** để AI biết:

- mục tiêu nằm đâu
- luật nằm đâu
- skill nằm đâu
- reference nằm đâu
- build/deploy nằm đâu
- log/audit nằm đâu

Prompt là lệnh ngắn hạn. Folder structure là **bộ nhớ vận hành dài hạn**.

Công thức:

```text
Folder Structure -> Rules -> Skills -> References -> Actions -> Build/Deploy -> Audit
```

Nếu không có cấu trúc này, AI sẽ phụ thuộc vào prompt mỗi lần chạy. Nếu có cấu trúc, AI biết tự tìm đúng nguồn, đúng luật, đúng skill, đúng output.

### 14.2 Map cấu trúc chuẩn vào MCM hiện tại

| AI Folder Standard | Vai trò | MCM hiện có / nên map |
|---|---|---|
| `agents/` | Agent contract, goal, loop, permission, stop condition | Hiện nằm rải trong `AGENTS.md`, `skills/`, `souls/`; có thể chuẩn hóa sau |
| `skills/` | Skill/action module cho agent dùng | Đã có `skills/agent1-agent5.yaml` |
| `rules/` | Luật vận hành, guardrail, permission matrix | Nên tách từ ADR + AGENTS + docs thành rule files |
| `references/` | Tài liệu nguồn, case study, spec, market research | Hiện có `knowledge/`, `docs/`, HTML case studies |
| `actions/` | Playbook từng workflow: capture, onboard, coach, payout | Hiện có `playbook/vendor-package/` |
| `build/` | Deploy, CI/CD, Docker, service, rollback | Hiện có `docker-compose.yml`, `services/`, `DEPLOYMENT.md` |
| `design/` | UI/dashboard/screen/view spec | Hiện có `web/`, dashboard docs |
| `ops/` | Daily/weekly/monthly operations | Hiện có `playbook/vendor-package/01-02-12...` |
| `security/` | Hardening, secrets, permissions, production gate | Nên bổ sung từ ADR/security checklist |
| `audit/` | Review, QA, evidence, SOP audit, failure log | Hiện có `docs/repo-audit.md`, Agent5 |
| `sales/` | Offer, deck, scripts, pricing, ROI calculator | Nên bổ sung cho Partner Growth OS |
| `screenshots/` | UI evidence, visual QA | Chưa cần nhiều, nhưng nên có nếu dashboard/web phát triển |

### 14.3 Recommended MCM structure

Không cần đổi toàn bộ repo ngay. Nếu chuẩn hóa sau này, dùng cấu trúc như sau:

```text
.ai/
  agents/
    agent1-capture.md
    agent2-onboard.md
    agent3-daily-loop.md
    agent4-crm-sync.md
    agent5-monitor.md
  rules/
    permission-matrix.md
    stop-conditions.md
    data-write-policy.md
    human-approval-gates.md
  references/
    zeremai-case-study-map.md
    agency-agents-map.md
    market-positioning.md
  actions/
    lead-capture-flow.md
    onboarding-d1-d7-flow.md
    daily-coaching-flow.md
    crm-sync-flow.md
    payout-rank-flow.md
  audit/
    agent-loop-audit.md
    sop-audit-checklist.md
    qa-evidence-template.md

docs/
  mcm-partner-growth-os-tech-review.md
  agent-loop-operating-model.md
  ai-project-folder-structure.md

playbook/
  vendor-package/
  sales/
  ops/

scripts/
services/
skills/
souls/
prompts/
web/
knowledge/
```

Không cần tạo hết ngay. Mục tiêu là có **chuẩn để mọi file biết mình thuộc loại nào**.

### 14.4 Folder map theo agent loop

| Thành phần agent loop | Nằm ở đâu |
|---|---|
| Goal/scope | `agents/*.md` |
| Tool/action steps | `skills/*.yaml` + `actions/*.md` |
| Permissions | `rules/permission-matrix.md` |
| Stop condition | `rules/stop-conditions.md` |
| Human approval | `rules/human-approval-gates.md` |
| Knowledge/reference | `references/` hoặc `knowledge/` |
| Build/deploy | `build/`, `services/`, `DEPLOYMENT.md` |
| Audit/QA | `audit/`, Agent5 reports |

### 14.5 Review MCM hiện tại

MCM đã làm đúng:

- Có 5 agent role rõ.
- Có skill YAML cho từng agent.
- Có SOUL/persona.
- Có prompt folder.
- Có playbook vận hành.
- Có ADR quyết định kiến trúc.
- Có deployment docs.
- Có Agent5 audit/monitor.

MCM còn thiếu:

- Chưa có `rules/` riêng cho permission, stop condition, approval gates.
- Chưa có `actions/` chuẩn hóa từng workflow thành reusable playbook.
- Chưa có `sales/` cho Partner Growth OS offer/deck/ROI.
- Chưa có `audit/` chuẩn cho evidence và QA.
- Chưa có file chuẩn “agent contract” cho từng agent.

### 14.6 Implementation order sau này

Khi muốn chuẩn hóa thành template bán lại, làm theo thứ tự nhẹ nhất:

1. Tạo `docs/agent-loop-operating-model.md`.
2. Tạo `docs/ai-project-folder-structure.md`.
3. Tạo `.ai/agents/` cho 5 agent contracts.
4. Tạo `.ai/rules/` cho permission, stop condition, approval gates.
5. Tạo `.ai/actions/` cho lead capture, onboarding, coaching, CRM sync, payout/rank.
6. Chỉ di chuyển production files khi đã chắc không ảnh hưởng deploy.

### 14.7 Acceptance criteria

Người mới đọc repo phải biết:

- agent nào làm gì
- luật nằm đâu
- skill nằm đâu
- reference nằm đâu
- deploy nằm đâu
- audit nằm đâu

Một agent muốn làm task phải tìm được:

- mục tiêu
- quyền
- tool
- checklist tự kiểm tra
- điểm dừng

MCM có thể dùng cấu trúc này để nhân bản sang ngành khác mà không viết lại từ đầu.

---

## 15. AI-Agent-Master: bộ xương thư mục cho AI làm việc như kiến trúc sư

### 15.1 Ý chính

Nếu Section 13 là **agent loop** và Section 14 là **folder structure tổng quát**, thì AI-Agent-Master là cách đóng gói thực dụng cho repo dùng Claude/Codex hằng ngày.

Mục tiêu:

```text
Không để AI làm việc bằng prompt rời rạc.
Đưa AI vào một bộ xương gồm agents, skills, commands, rules, references.
```

Khi có cấu trúc này, AI không cần được giải thích lại từ đầu mỗi lần. Nó biết vai trò nào xử lý việc gì, skill nào cần gọi, lệnh nào là entrypoint, luật nào không được phá, và tài liệu sâu nằm ở đâu.

### 15.2 Năm thành phần chính

| Thành phần | Vai trò | Ví dụ |
|---|---|---|
| `agents/` | Phân công vai trò rõ ràng | project-manager, ui-ux-designer, sales-strategist, infra-maintainer |
| `skills/` | Đóng gói kinh nghiệm và workflow reusable | write-guard, plan, monitoring, payment, production incident, agent-os-designer |
| `commands/` | Lệnh hằng ngày để gọi workflow nhanh | `/build`, `/spec`, `/review`, `/harden`, `/monitoring`, `/seo`, `/deploy` |
| `rules/` | Luật toàn dự án không được phá | naming conventions, project structure, data write policy, permission matrix |
| `references/` | Tài liệu sâu khi AI cần tra cứu | RBAC, auth flow, deploy workflow, Docker, payment integration, backup |

### 15.3 Map với repo MCM hiện tại

MCM đã có một phần AI-Agent-Master:

| AI-Agent-Master | MCM hiện có | Review |
|---|---|---|
| `agents/` | `souls/`, `AGENTS.md`, `.agents/` | Có vai trò nhưng chưa đóng thành agent contract chuẩn |
| `skills/` | `skills/agent1-agent5.yaml`, `.claude/skills/*`, `.codex/skills/agent-os-designer` | Đã có skill runtime và skill dev; nên tách rõ runtime skill vs Codex/Claude skill |
| `commands/` | `.claude/commands/spec.md`, `review.md`, `doubt.md` | Mới có 3 command dev; thiếu command ops như `/deploy`, `/monitoring`, `/agent-os`, `/partner-growth` |
| `rules/` | ADR files, `AGENTS.md`, deployment/error handling | Chưa có thư mục rules riêng cho permission, stop condition, naming, data policy |
| `references/` | `docs/`, `knowledge/`, case-study HTML/MD | Có nhiều reference, nhưng cần index rõ để AI không đọc lạc |

### 15.4 Cấu trúc đề xuất cho MCM

Không cần đổi production ngay. Nên thêm một lớp AI operating layer, ưu tiên không phá deploy:

```text
.claude/
  agents/
    project-manager.md
    growth-ops-architect.md
    partner-sales-strategist.md
    ai-agent-architect.md
  skills/
    spec-driven-development/
    code-review-and-quality/
    doubt-driven-development/
  commands/
    spec.md
    review.md
    doubt.md
    agent-os.md
    partner-growth.md

.codex/
  skills/
    agent-os-designer/

.ai/
  agents/
    agent1-capture.md
    agent2-onboard.md
    agent3-daily-loop.md
    agent4-crm-sync.md
    agent5-monitor.md
  rules/
    permission-matrix.md
    stop-conditions.md
    human-approval-gates.md
    data-write-policy.md
  references/
    mcm-partner-growth-os.md
    zeremai-case-study-map.md
    agency-agents-map.md
  actions/
    lead-capture-flow.md
    onboarding-d1-d7-flow.md
    daily-coaching-flow.md
    crm-sync-flow.md
    payout-rank-flow.md
  audit/
    sop-audit-checklist.md
    qa-evidence-template.md
```

### 15.5 Agents: phân vai thay vì một AI làm tất cả

MCM nên có hai lớp agent:

1. **Runtime agents**: Agent1-5 đang chạy thật trong production.
2. **Design/advisory agents**: các vai giúp thiết kế, review, audit, sales, ops.

Ví dụ design/advisory agents:

| Agent | Vai trò |
|---|---|
| `ai-agent-architect` | Thiết kế agent loop, permission, stop condition |
| `growth-ops-architect` | Map MCM thành Partner Growth OS |
| `partner-sales-strategist` | Viết offer, pricing, sales narrative |
| `ops-auditor` | Review daily/weekly/monthly cadence |
| `infra-maintainer` | Review deploy, monitoring, backup, incident |

### 15.6 Skills: đóng gói kinh nghiệm reusable

Skill không phải prompt dài. Skill là một folder có `SKILL.md` và reference đi kèm.

Skill `agent-os-designer` vừa tạo nên là asset dùng lại cho nhiều dự án:

```text
.codex/skills/agent-os-designer/
  SKILL.md
  references/
    agent-contract-template.md
    folder-structure-template.md
    permission-matrix-template.md
    stop-condition-template.md
    project-audit-checklist.md
```

Cách gọi ở repo khác:

```text
Use $agent-os-designer to audit this repo and create an agent operating model.
```

### 15.7 Commands: entrypoint cho công việc hằng ngày

Commands giúp người dùng không phải nhớ prompt dài.

MCM hiện có:

```text
/spec
/review
/doubt
```

Nên bổ sung sau này:

| Command | Mục đích |
|---|---|
| `/agent-os` | Audit repo theo Goal -> Loop -> Tool -> Check -> Stop -> Approval |
| `/partner-growth` | Tạo offer/sales kit/industry template cho Hermes Partner Growth OS |
| `/monitoring` | Review health check, alert, quota, cron, service |
| `/deploy` | Checklist deploy + rollback |
| `/sop-audit` | Review SOP/playbook có đủ owner, cadence, output, metric chưa |

### 15.8 Rules: luật chung cho toàn dự án

Rules là phần AI không được phá, dù task nào.

MCM nên có các rule docs:

```text
.ai/rules/permission-matrix.md
.ai/rules/stop-conditions.md
.ai/rules/human-approval-gates.md
.ai/rules/data-write-policy.md
.ai/rules/naming-conventions.md
.ai/rules/project-structure.md
```

Các rule quan trọng:

- Không xóa row/data production nếu chưa có approval.
- Không sửa payout/commission nếu chưa có evidence và admin duyệt.
- Không mass broadcast nếu chưa có preview và approval.
- Không thêm CRM/tool mới nếu chưa có delete-first/resource-fit review.
- Lỗi lặp 3 lần phải dừng và escalate.

### 15.9 References: thư viện sâu cho AI

References là nơi chứa tài liệu dài, chỉ đọc khi cần.

MCM hiện có:

- `docs/mcm-partner-growth-os-tech-review.md`
- `docs/repo-audit.md`
- `docs/case-study-mapping.md`
- `knowledge/VENDOR-GROWTH-PLAN.md`
- `playbook/vendor-package/*`
- HTML/MD case studies

Cần thêm index sau này:

```text
.ai/references/INDEX.md
```

Index nên trả lời:

- muốn hiểu Partner Growth OS đọc file nào
- muốn hiểu deploy đọc file nào
- muốn hiểu vendor ops đọc file nào
- muốn hiểu case study ZeremAI đọc file nào
- muốn hiểu rule/permission đọc file nào

### 15.10 Kết luận

AI-Agent-Master không phải chỉ là thư mục `.claude`. Nó là hệ thống tổ chức để AI làm việc có vai trò, kỹ năng, lệnh, luật và tài liệu tham khảo.

MCM nên dùng mô hình này để biến dự án từ:

```text
một hệ 5 agents chạy production
```

thành:

```text
một AI-operable business system có thể clone, audit, bán lại và nhân bản sang ngành khác
```
