#!/usr/bin/env python3
"""
Hermes Account Health v2 — Module 3: 100-Account Health + Risk Scoring

Dynamic account config from JSONL. Tier-aware risk scoring. Cluster health.

Accounts config: /root/hermes-data/accounts/accounts.jsonl
Health DB:       /root/hermes-data/tracking/account-health.json
Suspension log:  /root/hermes-data/tracking/suspensions.jsonl

Usage:
  python3 account-health.py init                              # Generate 100-account starter config
  python3 account-health.py dashboard                         # Cluster → tier → flagged summary
  python3 account-health.py clusters                          # Per-cluster health score
  python3 account-health.py tiers                             # T1/T2/T3 active counts
  python3 account-health.py risk                              # Accounts with risk >= yellow
  python3 account-health.py log --account gulf_t1_01 --posts 4
  python3 account-health.py suspend --account gulf_t2_01 --reason "spam warning"

Deploy: cp account-health.py /root/hermes-bin/vendor-layer/
"""

import argparse, json, os
from datetime import datetime, timedelta
from collections import defaultdict

ACCOUNTS_FILE  = "/root/hermes-data/accounts/accounts.jsonl"
HEALTH_DB      = "/root/hermes-data/tracking/account-health.json"
SUSPENSION_LOG = "/root/hermes-data/tracking/suspensions.jsonl"

CLUSTERS = ["gulf", "europe", "africa", "south_asia", "americas"]
TIERS    = ["T1", "T2", "T3"]

# Risk score thresholds (T1 stricter)
TIER_THRESHOLDS = {
    "T1": {"yellow": 85, "red": 60},
    "T2": {"yellow": 70, "red": 45},
    "T3": {"yellow": 60, "red": 35},
}


# ── Account config ────────────────────────────────────────────────────────────

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return []
    accounts = []
    with open(ACCOUNTS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    accounts.append(json.loads(line))
                except Exception:
                    pass
    return accounts


def load_health():
    if os.path.exists(HEALTH_DB):
        with open(HEALTH_DB, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_health(data):
    os.makedirs(os.path.dirname(HEALTH_DB), exist_ok=True)
    with open(HEALTH_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ── Risk scoring ──────────────────────────────────────────────────────────────

def calculate_risk(acc, health):
    acc_id = acc["id"]
    tier   = acc.get("tier", "T3")
    history = health.get(acc_id, [])
    reasons = []
    score   = 100

    # Account age
    try:
        age = (datetime.now() - datetime.strptime(acc.get("created", "2026-01-01"), "%Y-%m-%d")).days
    except Exception:
        age = 0

    if age < 7:
        score -= 25
        reasons.append(f"New ({age}d) — warm-up phase")
    elif age < 21:
        score -= 10
        reasons.append(f"Young ({age}d)")

    # 7-day activity
    cutoff    = datetime.now() - timedelta(days=7)
    active_days = 0
    total_posts = 0
    for entry in history:
        try:
            if datetime.strptime(entry["date"], "%Y-%m-%d") >= cutoff:
                active_days += 1
                total_posts += entry.get("posts", 0)
        except Exception:
            pass

    if active_days == 0:
        score -= 35
        reasons.append("0 activity in 7 days — dormant risk")
    elif active_days < 3:
        score -= 15
        reasons.append(f"Low activity ({active_days}/7 days)")
    else:
        score += 5
        reasons.append(f"Active ({active_days}/7 days)")

    # Posting frequency
    if active_days > 0:
        avg = total_posts / active_days
        cap = {"T1": 5, "T2": 4, "T3": 4}.get(tier, 4)
        if avg > cap:
            score -= 15
            reasons.append(f"Over-posting ({avg:.1f}/day > {cap}) — suspend risk")
        elif avg >= 2:
            score += 5

    # Suspension flags
    flags = health.get(f"{acc_id}__flags", [])
    if "suspended" in flags:
        score -= 60
        reasons.append("SUSPENDED")
    if "shadow_banned" in flags:
        score -= 25
        reasons.append("Shadow-banned")
    if "warned" in flags:
        score -= 15
        reasons.append("Has warning")

    # Active flag
    if not acc.get("active", True):
        score = 0
        reasons.append("Marked inactive")

    score = max(0, min(100, score))
    thresh = TIER_THRESHOLDS.get(tier, TIER_THRESHOLDS["T3"])
    level = "green" if score >= thresh["yellow"] else ("yellow" if score >= thresh["red"] else "red")

    return {"level": level, "score": score, "reasons": reasons}


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_init():
    """Generate starter accounts.jsonl with 100 placeholder accounts."""
    os.makedirs(os.path.dirname(ACCOUNTS_FILE), exist_ok=True)

    # Distribution: T1=10, T2=30, T3=60
    # Gulf: 3T1 + 6T2 + 9T3 = 18
    # Europe: 4T1 + 8T2 + 13T3 = 25
    # Africa: 2T1 + 6T2 + 12T3 = 20
    # South Asia: 1T1 + 5T2 + 9T3 = 15
    # Americas: 0T1 + 5T2 + 7T3 = 12 (+ 10 global T3)

    plan = [
        ("gulf",       "T1", 3,  "Dubai, UAE",       "signal_proof"),
        ("gulf",       "T2", 6,  "Dubai, UAE",       "risk"),
        ("gulf",       "T3", 9,  "",                 "macro"),
        ("europe",     "T1", 4,  "London, UK",       "signal_proof"),
        ("europe",     "T2", 8,  "London, UK",       "prop_firm"),
        ("europe",     "T3", 13, "",                 "smc"),
        ("africa",     "T1", 2,  "Nairobi, Kenya",   "signal_proof"),
        ("africa",     "T2", 6,  "Lagos, Nigeria",   "prop_firm"),
        ("africa",     "T3", 12, "",                 "signal_proof"),
        ("south_asia", "T1", 1,  "Karachi, Pakistan","signal_proof"),
        ("south_asia", "T2", 5,  "Karachi, Pakistan","risk"),
        ("south_asia", "T3", 9,  "",                 "smc"),
        ("americas",   "T2", 5,  "Toronto, Canada",  "prop_firm"),
        ("americas",   "T3", 17, "",                 "macro"),   # 7 + 10 global
    ]

    counters = defaultdict(int)
    accounts = []
    for cluster, tier, count, location, niche in plan:
        for _ in range(count):
            counters[(cluster, tier)] += 1
            n   = counters[(cluster, tier)]
            aid = f"{cluster}_{tier.lower()}_{n:02d}"
            accounts.append({
                "id":            aid,
                "handle":        f"@placeholder_{aid}",
                "tier":          tier,
                "cluster":       cluster,
                "location":      location,
                "tracking_link": f"X-{cluster.capitalize()}-{tier}-{n:02d}" if tier == "T1" else "",
                "niche":         niche,
                "active":        True,
                "created":       "2026-06-08",
            })

    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        for a in accounts:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")

    t1 = sum(1 for a in accounts if a["tier"] == "T1")
    t2 = sum(1 for a in accounts if a["tier"] == "T2")
    t3 = sum(1 for a in accounts if a["tier"] == "T3")
    print(f"Generated {len(accounts)} accounts: T1={t1} T2={t2} T3={t3}")
    print(f"Saved to: {ACCOUNTS_FILE}")


def cmd_log(acc_id, posts):
    accounts = {a["id"]: a for a in load_accounts()}
    if acc_id not in accounts:
        print(f"Account not found: {acc_id}. Run `init` first.")
        return
    health = load_health()
    today  = datetime.now().strftime("%Y-%m-%d")
    if acc_id not in health:
        health[acc_id] = []
    updated = False
    for entry in health[acc_id]:
        if entry["date"] == today:
            entry["posts"] = posts
            updated = True
            break
    if not updated:
        health[acc_id].append({"date": today, "posts": posts})
    save_health(health)
    print(f"Logged: {acc_id} — {posts} posts on {today}")


def cmd_suspend(acc_id, reason):
    health = load_health()
    flag_key = f"{acc_id}__flags"
    flags = health.get(flag_key, [])
    if "suspended" not in flags:
        flags.append("suspended")
    health[flag_key] = flags
    save_health(health)

    os.makedirs(os.path.dirname(SUSPENSION_LOG), exist_ok=True)
    with open(SUSPENSION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "account": acc_id, "reason": reason,
            "ts": datetime.now().isoformat()
        }) + "\n")
    print(f"Suspended: {acc_id} — {reason}")


def cmd_tiers():
    accounts = load_accounts()
    health   = load_health()
    print(f"\n  TIER SUMMARY — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  {'─'*40}")
    for tier in TIERS:
        accs  = [a for a in accounts if a["tier"] == tier]
        risks = [calculate_risk(a, health) for a in accs]
        active = sum(1 for a, r in zip(accs, risks) if r["level"] != "red" and a.get("active", True))
        red    = sum(1 for r in risks if r["level"] == "red")
        yellow = sum(1 for r in risks if r["level"] == "yellow")
        print(f"  {tier}: {active}/{len(accs)} active  |  ⚠️ {yellow}  🔴 {red}")
    print()


def cmd_clusters():
    accounts = load_accounts()
    health   = load_health()
    print(f"\n  CLUSTER HEALTH — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  {'Cluster':<14} {'Accounts':>9} {'Active':>7} {'Avg Score':>10} {'Red':>5} {'Yellow':>7}")
    print(f"  {'─'*55}")
    for cl in CLUSTERS:
        accs = [a for a in accounts if a.get("cluster") == cl]
        if not accs:
            continue
        risks  = [calculate_risk(a, health) for a in accs]
        avg    = round(sum(r["score"] for r in risks) / len(risks))
        active = sum(1 for a, r in zip(accs, risks) if a.get("active", True) and r["level"] != "red")
        red    = sum(1 for r in risks if r["level"] == "red")
        yel    = sum(1 for r in risks if r["level"] == "yellow")
        print(f"  {cl:<14} {len(accs):>9} {active:>7} {avg:>10} {red:>5} {yel:>7}")
    print()


def cmd_risk():
    accounts = load_accounts()
    health   = load_health()
    flagged  = []
    for a in accounts:
        r = calculate_risk(a, health)
        if r["level"] in ("yellow", "red"):
            flagged.append((a, r))
    if not flagged:
        print("All accounts healthy. ✅")
        return
    flagged.sort(key=lambda x: x[1]["score"])
    print(f"\n  AT-RISK ACCOUNTS ({len(flagged)})")
    print(f"  {'─'*55}")
    for a, r in flagged:
        icon = "🔴" if r["level"] == "red" else "⚠️"
        print(f"  {icon} {a['id']:<20} [{a['tier']}/{a['cluster']}] score={r['score']} — {r['reasons'][0]}")
    print()


def cmd_dashboard():
    accounts = load_accounts()
    health   = load_health()
    all_risks = [(a, calculate_risk(a, health)) for a in accounts]

    total   = len(accounts)
    active  = sum(1 for a, r in all_risks if a.get("active", True) and r["level"] != "red")
    red_ct  = sum(1 for _, r in all_risks if r["level"] == "red")
    yel_ct  = sum(1 for _, r in all_risks if r["level"] == "yellow")

    print(f"\n{'='*55}")
    print(f"  ACCOUNT HEALTH DASHBOARD — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*55}")
    print(f"  Total: {total} | Active: {active} | ⚠️ {yel_ct} | 🔴 {red_ct}\n")
    cmd_clusters()
    cmd_tiers()

    # Flagged list
    flagged = [(a, r) for a, r in all_risks if r["level"] in ("yellow", "red")]
    if flagged:
        print(f"  FLAGGED ACCOUNTS ({len(flagged)})")
        print(f"  {'─'*50}")
        for a, r in sorted(flagged, key=lambda x: x[1]["score"])[:20]:
            icon = "🔴" if r["level"] == "red" else "⚠️"
            print(f"  {icon} {a['id']:<22} score={r['score']:>3}  {r['reasons'][0]}")
        print()


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap  = argparse.ArgumentParser(description="Hermes Account Health v2")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("init")
    sub.add_parser("dashboard")
    sub.add_parser("clusters")
    sub.add_parser("tiers")
    sub.add_parser("risk")

    lp = sub.add_parser("log")
    lp.add_argument("--account", required=True)
    lp.add_argument("--posts",   type=int, required=True)

    sp = sub.add_parser("suspend")
    sp.add_argument("--account", required=True)
    sp.add_argument("--reason",  default="unspecified")

    args = ap.parse_args()

    if args.cmd == "init":        cmd_init()
    elif args.cmd == "log":       cmd_log(args.account, args.posts)
    elif args.cmd == "suspend":   cmd_suspend(args.account, args.reason)
    elif args.cmd == "clusters":  cmd_clusters()
    elif args.cmd == "tiers":     cmd_tiers()
    elif args.cmd == "risk":      cmd_risk()
    else:                         cmd_dashboard()
