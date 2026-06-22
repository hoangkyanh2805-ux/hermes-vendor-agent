#!/bin/bash
VPS_IP=${VPS_IP:-103.97.126.28}
REMOTE_DIR="/root/hermes-vendor-agent"

echo "=== Deploying Agent 5 to $VPS_IP ==="

scp scripts/agent5.py root@$VPS_IP:$REMOTE_DIR/scripts/agent5.py
scp scripts/run-agent5.sh root@$VPS_IP:$REMOTE_DIR/scripts/run-agent5.sh
ssh root@$VPS_IP "chmod +x $REMOTE_DIR/scripts/run-agent5.sh"
echo "Files copied"

# Cron:
# 8PM UTC+7 = 1PM UTC → 0 13 * * *
# 9PM UTC+7 Friday = 2PM UTC Friday → 0 14 * * 5
ssh root@$VPS_IP "crontab -l 2>/dev/null | grep -v 'run-agent5' > /tmp/crontab_new; \
  echo '0 13 * * *   /root/hermes-vendor-agent/scripts/run-agent5.sh report  >> /var/log/mcm-agent5.log 2>&1' >> /tmp/crontab_new; \
  echo '0 14 * * 5   /root/hermes-vendor-agent/scripts/run-agent5.sh weekly  >> /var/log/mcm-agent5.log 2>&1' >> /tmp/crontab_new; \
  crontab /tmp/crontab_new; \
  echo 'Cron updated:'; crontab -l | grep agent5"

echo "=== Agent 5 deployed ==="
echo "Test: ssh root@$VPS_IP '/root/hermes-vendor-agent/scripts/run-agent5.sh report'"
