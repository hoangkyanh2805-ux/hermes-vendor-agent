# Doubt-Driven Development — Advisory Board Review

Adversarial review by the MCM Vendor Advisory Board. Each advisor attacks from their domain. Consensus kills the idea or confirms it.

## When to use

- After building something that "seems to work" but you haven't stress-tested
- Before going live with any affiliate-facing flow
- When you're too close to the code and need a fresh perspective
- When the last bug was "obvious in hindsight"

## The Advisory Board

| Advisor | Domain | Attack angle |
|---------|--------|-------------|
| **Gary Vee** | Speed & distribution | "Is this actually moving fast enough? Will affiliates give up before this even loads?" |
| **Alex Hormozi** | Offer & conversion | "What's the ONE thing that makes them stay? Is that thing in the first message?" |
| **Chris Voss** | Negotiation & trust | "Does this message build trust or does it feel like a bot? What's the emotional tone?" |
| **Dan Kennedy** | Direct response copy | "Is there a clear CTA? Does every message earn the next click?" |
| **MrBeast** | Retention & virality | "Would they forward this? Is the hook strong enough in the first 3 words?" |
| **Russell Brunson** | Funnel design | "Where's the upsell path? Does the 7-day sequence move them toward VIP?" |
| **Ali Abdaal** | Learning & habits | "Is the 7-day onboarding building a habit or just delivering information?" |

## Process — 5 steps

### Step 1 — CLAIM
State the specific claim to review in one sentence:
> "Agent2 D1 message will make a new affiliate take action on their first day."

### Step 2 — EXTRACT
List the concrete assumptions behind the claim:
- They have a Telegram account and see the message
- They understand X-first flow from one explanation
- The 3 tasks are actionable without hand-holding
- They'll do it even without a reward yet

### Step 3 — DOUBT
Each advisor attacks one assumption. Each attack must be specific, not generic:

**Gary Vee:** "They got the message at 8AM but they're at work. By evening they forgot. No urgency hook."

**Hormozi:** "3 tasks is too many for day 1 of a cold affiliate. ONE task, done = dopamine hit = they come back tomorrow."

**Chris Voss:** "Starting with 'Mình là bot MCM Vendor 🤖' signals automation. Trust is lower before they even read the offer."

**Dan Kennedy:** "No deadline, no scarcity, no reason to act NOW. A message without urgency is a message ignored."

**MrBeast:** "The hook is a greeting. Worst possible hook. Should open with the result: '$200 in 7 days. Here's day 1.'"

**Brunson:** "D1 has no micro-commitment device. Ask them to reply with ONE thing so you have engagement data."

**Ali Abdaal:** "Installing 3 new habits (bio, follow, screenshot) at once violates habit-stacking. One action per day, compounding."

### Step 4 — RECONCILE
For each attack: accept, modify, or reject with reason.

| Attack | Decision | Change |
|--------|----------|--------|
| Gary Vee: no urgency | Accept | Add "Reply hôm nay để mình gửi tracking link." |
| Hormozi: 3 tasks too many | Modify | Keep 3 but mark Task 1 as "làm ngay trong 5 phút" |
| Chris Voss: bot opener | Accept | Change opener to name-first human tone |
| Dan Kennedy: no deadline | Accept | Add time anchor to Task 1 |
| MrBeast: weak hook | Reject | First message is relationship, not hook — D2 is where hook matters |
| Brunson: no micro-commitment | Accept | Add "Xong task 1 thì reply '✅' cho mình biết nhé" |
| Ali Abdaal: habit stacking | Modify | Sequence tasks 1→2→3 with "sau khi xong cái trên" |

### Step 5 — STOP
Stop when: ≥5 of 7 advisors have no remaining objection to the reconciled version.
Output: the reconciled spec change + commit message using MCM convention.

## Output format

```
CLAIM: [one sentence]
SURVIVING OBJECTIONS: [list any still unresolved]
CHANGES TO MAKE:
  - [file:line] change description
VERDICT: ship / revise / rework
COMMIT: fix: agent2 [description]
```
