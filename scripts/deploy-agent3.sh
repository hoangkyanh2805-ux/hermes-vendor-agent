#!/bin/bash
# Deploy Agent 3 to VPS
VPS_IP=${VPS_IP:-103.97.126.28}
REMOTE_DIR="/root/hermes-vendor-agent"

echo "=== Deploying Agent 3 to $VPS_IP ==="

scp scripts/agent3.py root@$VPS_IP:$REMOTE_DIR/scripts/agent3.py
scp scripts/run-agent3.sh root@$VPS_IP:$REMOTE_DIR/scripts/run-agent3.sh
scp prompts/checklist.txt root@$VPS_IP:$REMOTE_DIR/prompts/checklist.txt
scp prompts/coaching.txt root@$VPS_IP:$REMOTE_DIR/prompts/coaching.txt
scp prompts/report-affiliate.txt root@$VPS_IP:$REMOTE_DIR/prompts/report-affiliate.txt
scp prompts/report-pm.txt root@$VPS_IP:$REMOTE_DIR/prompts/report-pm.txt
ssh root@$VPS_IP "chmod +x $REMOTE_DIR/scripts/run-agent3.sh"
echo "Files copied"

# 3 cron entries (UTC times = UTC+7 - 7h):
# 7AM  UTC+7 = 0AM  UTC → 0 0 * * *
# 2PM  UTC+7 = 7AM  UTC → 0 7 * * *
# 9PM  UTC+7 = 2PM  UTC → 0 14 * * *
ssh root@$VPS_IP "crontab -l 2>/dev/null | grep -v 'run-agent3' > /tmp/crontab_new; \
  echo '0 0 * * * /root/hermes-vendor-agent/scripts/run-agent3.sh checklist >> /var/log/mcm-agent3.log 2>&1' >> /tmp/crontab_new; \
  echo '0 7 * * * /root/hermes-vendor-agent/scripts/run-agent3.sh coaching  >> /var/log/mcm-agent3.log 2>&1' >> /tmp/crontab_new; \
  echo '0 14 * * * /root/hermes-vendor-agent/scripts/run-agent3.sh report   >> /var/log/mcm-agent3.log 2>&1' >> /tmp/crontab_new; \
  crontab /tmp/crontab_new; \
  echo 'Cron updated:'; crontab -l | grep agent3"

echo "=== Agent 3 deployed ==="
echo "Test checklist: ssh root@$VPS_IP '/root/hermes-vendor-agent/scripts/run-agent3.sh checklist'"
echo "Test report:    ssh root@$VPS_IP '/root/hermes-vendor-agent/scripts/run-agent3.sh report'"
