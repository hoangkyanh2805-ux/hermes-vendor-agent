#!/bin/bash
# Deploy Agent 2 to VPS: copy files, install cron
# Run from local: bash scripts/deploy-agent2.sh
# Requires: VPS_IP set in environment or edit below

VPS_IP=${VPS_IP:-103.97.126.28}
REMOTE_DIR="/root/hermes-vendor-agent"

echo "=== Deploying Agent 2 to $VPS_IP ==="

# 1. Copy agent2.py
scp scripts/agent2.py root@$VPS_IP:$REMOTE_DIR/scripts/agent2.py
echo "agent2.py copied"

# 2. Copy prompt files D1-D7
scp prompts/onboard-d{1,2,3,4,5,6,7}.txt root@$VPS_IP:$REMOTE_DIR/prompts/
echo "prompts copied"

# 3. Copy wrapper script
scp scripts/run-agent2.sh root@$VPS_IP:$REMOTE_DIR/scripts/run-agent2.sh
ssh root@$VPS_IP "chmod +x $REMOTE_DIR/scripts/run-agent2.sh"
echo "run-agent2.sh copied"

# 4. Install cron job (8AM daily UTC+7 = 1AM UTC)
ssh root@$VPS_IP "crontab -l 2>/dev/null | grep -v 'run-agent2' > /tmp/crontab_new; \
  echo '0 1 * * * /root/hermes-vendor-agent/scripts/run-agent2.sh >> /var/log/mcm-agent2.log 2>&1' >> /tmp/crontab_new; \
  crontab /tmp/crontab_new; \
  echo 'Cron updated:'; crontab -l | grep agent2"

echo "=== Agent 2 deployed ==="
echo "Test now: ssh root@$VPS_IP '/root/hermes-vendor-agent/scripts/run-agent2.sh'"
