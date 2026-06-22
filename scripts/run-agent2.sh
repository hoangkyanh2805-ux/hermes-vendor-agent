#!/bin/bash
set -a
source /root/.hermes/.env
[ -f /root/hermes-vendor-agent/.env ] && source /root/hermes-vendor-agent/.env
set +a
exec /usr/local/lib/hermes-agent/venv/bin/python /root/hermes-vendor-agent/scripts/agent2.py
