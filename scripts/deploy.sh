#!/bin/bash
# Deploy MCM Vendor Agent to VPS
# Usage: bash scripts/deploy.sh
set -e

cd /root/hermes-vendor-agent
git pull origin master
systemctl restart mcm-agent1
sleep 2
curl -s http://localhost:3000/health
echo ""
echo "Deploy done."
