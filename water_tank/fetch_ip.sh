#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECRETS_FILE="${SCRIPT_DIR}/../config_files/secrets.json"

SLACK_TOKEN=$(python3 - "${SECRETS_FILE}" <<'PY'
import json
import sys

path = sys.argv[1]
try:
    with open(path, 'r') as f:
        data = json.load(f)
    print((data.get('slack') or {}).get('webhook_endpoint', ''))
except Exception:
    print('')
PY
)

RESPONSE=$(curl 'https://api.ipify.org?format=json')
IP=$(echo "${RESPONSE}" | jq ".ip" -r)
PAYLOAD="{\"text\":\"External IP: $IP\"}"
echo $PAYLOAD
COMMAND="curl --insecure -X POST -H 'Content-type: application/json' --data '${PAYLOAD}' ${SLACK_TOKEN}"
#echo "COMMAND: ${COMMAND}"
eval $COMMAND
