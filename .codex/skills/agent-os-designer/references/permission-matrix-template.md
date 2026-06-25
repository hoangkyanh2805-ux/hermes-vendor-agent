# Permission Matrix Template

Use this to separate autonomous agent actions from human approval gates.

| Action | Agent may do autonomously | Human approval required | Notes/evidence |
|---|---|---|---|
| Read project docs/configs | Yes | No | Prefer read-only exploration first |
| Write draft docs/plans | Yes, if requested | No | Keep changes scoped |
| Send user-facing messages | Depends | Usually yes for mass/external messages | Require preview or approved templates |
| Update operational records | Depends | Yes if money/rank/status risk | Log before/after values |
| Delete records/files | No | Yes | Require backup/explicit target |
| Spend money/use paid API at scale | No | Yes | Include estimated cost |
| Change production schema | No | Yes | Require migration/rollback plan |
| Change payouts/commissions | No | Yes | Include source event and calculation |
| Publish externally | No | Yes | Require final approval |
| Run tests/checks | Yes | No | Safe verification action |
| Restart services/deploy | Depends | Yes for production | Require status and rollback |

Default rule: if an action affects money, customer-facing output, production data, access control, or irreversible state, require human approval.
