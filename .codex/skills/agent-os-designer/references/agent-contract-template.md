# Agent Contract Template

Use this template for every agent or workflow that should run without constant prompting.

```markdown
## <Agent or Workflow Name>

**Goal:**
What final business or technical outcome means this agent succeeded?

**Scope:**
What work belongs to this agent, and what is explicitly out of scope?

**Inputs:**
- Required inputs
- Optional inputs
- Source of truth for each input

**Tools:**
- Tool/API/file/service name
- Purpose
- Required credentials/environment

**Permissions:**
- Autonomous actions
- Human approval required actions
- Forbidden actions

**Loop:**
```text
observe -> plan -> act -> check -> update state -> continue/escalate
```

**Checks:**
- Data validity checks
- Output quality checks
- External system confirmation checks

**Stop Conditions:**
- Missing input
- Repeated failure
- Risky operation
- Conflicting state
- Budget/quota/security threshold

**Human Approval Gates:**
- What must be approved
- Who approves
- What evidence is required

**Outputs:**
- Files/records/messages created
- Logs emitted
- Status updates

**Acceptance Criteria:**
- Observable pass/fail criteria
```
