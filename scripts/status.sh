#!/bin/bash
# MCM Vendor AI Affiliate - Quick Status Check
# Usage: ./scripts/status.sh

set -e

COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_NC='\033[0m' # No Color

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║          MCM VENDOR AI AFFILIATE - SYSTEM STATUS                 ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Services
echo "SERVICES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_service() {
    if systemctl is-active --quiet "$1"; then
        echo -e "${COLOR_GREEN}✅${COLOR_NC} $2"
    else
        echo -e "${COLOR_RED}❌${COLOR_NC} $2 (stopped)"
    fi
}

check_service "mcm-agent1" "Agent 1 (Capture) :3000"
check_service "mcm-agent4" "Agent 4 (CRM Sync) :3001"

# Check processes
if pgrep -f "hermes.*gateway" > /dev/null; then
    echo -e "${COLOR_GREEN}✅${COLOR_NC} Hermes Gateway"
else
    echo -e "${COLOR_RED}❌${COLOR_NC} Hermes Gateway (not running)"
fi

if pgrep -f "9router" > /dev/null; then
    echo -e "${COLOR_GREEN}✅${COLOR_NC} 9Router :20128"
else
    echo -e "${COLOR_RED}❌${COLOR_NC} 9Router (not running)"
fi

echo ""

# Webhooks health
echo "WEBHOOKS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if curl -s -m 2 http://localhost:3000/health > /dev/null 2>&1; then
    echo -e "${COLOR_GREEN}✅${COLOR_NC} Agent 1 health check OK"
else
    echo -e "${COLOR_RED}❌${COLOR_NC} Agent 1 health check failed"
fi

if curl -s -m 2 http://localhost:3001/health > /dev/null 2>&1; then
    echo -e "${COLOR_GREEN}✅${COLOR_NC} Agent 4 health check OK"
else
    echo -e "${COLOR_RED}❌${COLOR_NC} Agent 4 health check failed"
fi

echo ""

# Cron jobs
echo "CRON SCHEDULE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
crontab -l 2>/dev/null | grep -E "agent[2-5]" | while read line; do
    echo "$line"
done
echo ""

# State files
echo "STATE FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for state in agent1 agent2; do
    file="/root/.hermes/${state}_state.json"
    if [ -f "$file" ]; then
        count=$(jq '. | length' "$file" 2>/dev/null || echo "0")
        echo -e "${COLOR_GREEN}✅${COLOR_NC} $state: $count entries"
    else
        echo -e "${COLOR_YELLOW}⚠️${COLOR_NC} $state: file not found"
    fi
done

echo ""

# Recent logs
echo "RECENT ERRORS (last 10 lines)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for log in /var/log/mcm-agent*.log; do
    if [ -f "$log" ]; then
        errors=$(tail -100 "$log" 2>/dev/null | grep -i "error\|exception\|failed" | tail -2)
        if [ -n "$errors" ]; then
            echo -e "${COLOR_RED}$(basename $log):${COLOR_NC}"
            echo "$errors"
        fi
    fi
done

echo ""
echo "Run 'tail -f /var/log/mcm-agent*.log' for live monitoring"
echo ""
