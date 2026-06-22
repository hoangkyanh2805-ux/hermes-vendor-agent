#!/bin/bash
# Deploy Agent 4 + EspoCRM webhook setup
VPS_IP=${VPS_IP:-103.97.126.28}
REMOTE_DIR="/root/hermes-vendor-agent"
ESPO_URL=${ESPO_URL:-http://localhost:8080}
ESPO_USER=${ESPO_USER:-admin}
ESPO_PASS=${ESPO_PASS:-admin}  # change this

echo "=== Deploying Agent 4 to $VPS_IP ==="

scp scripts/agent4.py root@$VPS_IP:$REMOTE_DIR/scripts/agent4.py
scp scripts/run-agent4.sh root@$VPS_IP:$REMOTE_DIR/scripts/run-agent4.sh
scp services/mcm-agent4.service root@$VPS_IP:/etc/systemd/system/mcm-agent4.service
ssh root@$VPS_IP "chmod +x $REMOTE_DIR/scripts/run-agent4.sh"
echo "Files copied"

# Install and start systemd service
ssh root@$VPS_IP "systemctl daemon-reload && \
  systemctl enable mcm-agent4 && \
  systemctl restart mcm-agent4 && \
  systemctl status mcm-agent4 --no-pager"

# Register 4 webhooks in EspoCRM via API
echo ""
echo "=== Registering EspoCRM webhooks ==="
AGENT4_URL="http://localhost:3001"

register_webhook() {
  local event=$1
  local path=$2
  ssh root@$VPS_IP "curl -s -u '$ESPO_USER:$ESPO_PASS' \
    -X POST '$ESPO_URL/api/v1/Webhook' \
    -H 'Content-Type: application/json' \
    -d '{\"event\":\"$event\",\"url\":\"$AGENT4_URL$path\",\"isActive\":true}' \
    | python3 -c 'import sys,json; d=json.load(sys.stdin); print(\"  OK:\", d.get(\"id\",d))'"
}

echo "1. Lead.create"
register_webhook "Lead.create" "/webhook/espo/lead-create"

echo "2. Contact.fieldUpdate.status"
register_webhook "Contact.fieldUpdate.status" "/webhook/espo/status-change"

echo "3. Opportunity.create"
register_webhook "Opportunity.create" "/webhook/espo/opportunity"

echo "4. Contact.fieldUpdate.total_earn"
register_webhook "Contact.fieldUpdate.total_earn" "/webhook/espo/commission"

echo ""
echo "=== Agent 4 deployed ==="
echo "Health check: curl http://$VPS_IP:3001/health"
echo "Logs: journalctl -u mcm-agent4 -f"
