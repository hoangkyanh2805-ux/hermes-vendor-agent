# Mapping Output Template

Use this template for a saved plan or project asset.

## Source Inventory

| Source | Type | Role | Confidence | Notes |
|---|---|---|---|---|

## Extracted Mechanisms

| Source | Mechanism | Reusable Principle | Target Use |
|---|---|---|---|

## Agent Contracts

| Agent | Source Pattern | Receives | Produces | Not Responsible For | Metrics |
|---|---|---|---|---|---|

## Harness Loop

```text
Input
  -> node_1
  -> branch/check
  -> node_2
  -> checkpoint
  -> node_3
  -> human gate if needed
  -> final output
```

## State Schema

```json
{
  "workflow_id": "",
  "current_node": "",
  "status": "",
  "inputs": {},
  "outputs": {},
  "errors": [],
  "retry_count": 0,
  "needs_human": false,
  "last_checkpoint": ""
}
```

## Guardrails

| Risk | Guardrail | Stop Condition | Human Gate |
|---|---|---|---|

## Reusable Assets

| Asset | Path | Purpose |
|---|---|---|

## Acceptance Criteria

- Each agent has clear input/output.
- Each loop has state and terminal states.
- Each risky action has a human gate.
- The mapping cites the source repo pattern used.
- The output can be reused in another project without rereading the original source.
