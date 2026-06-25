# LangGraph Harness Pattern

Use this reference when converting workflows into durable loops, state graphs, and human-in-the-loop execution.

## What To Extract

Map a workflow into:

```text
state -> nodes -> edges -> checkpoints -> interrupts -> retries -> traces
```

Core concepts to preserve:

- Stateful workflow
- Long-running execution
- Durable checkpoint/resume
- Human-in-the-loop interrupt
- Memory
- Branching/routing
- Observability/tracing
- Production deployment boundary

## Harness Template

```text
WORKFLOW:
GOAL:
STATE FIELDS:
NODES:
EDGES:
CHECKPOINTS:
RETRY POLICY:
FALLBACK POLICY:
STOP CONDITIONS:
HUMAN INTERRUPTS:
OBSERVABILITY:
OUTPUT:
```

## Loop Design Rules

- Every node reads and writes explicit state fields.
- Every side-effect node must be idempotent or have a compensation action.
- Every retry loop needs a max attempt count.
- Every graph needs a terminal success state and a terminal failed/escalated state.
- Human approval is required for irreversible, high-blast-radius, money-moving, external publishing, or low-confidence actions.
- Logs must include workflow id, node name, status, latency, error, and state diff summary.

## Common Patterns

Sequential:

```text
capture -> qualify -> onboard -> coach -> sync -> audit
```

Branching:

```text
qualify -> fast_track if Hot
qualify -> nurture if Warm/Cold
```

Evaluator loop:

```text
generate -> evaluate -> revise until pass or max_attempts
```

Escalation:

```text
node fails 3 times -> fallback -> human_review -> resume or stop
```
