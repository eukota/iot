#!/usr/bin/env bash

SLACK_TOKEN=$(cat /opt/iot/slack_endpoint.txt)
RESPONSE=$(curl 'https://api.ipify.org?format=json')
IP=$(echo "${RESPONSE}" | jq ".ip" -r)
PAYLOAD="{\"text\":\"External IP: $IP\"}"
echo $PAYLOAD
COMMAND="curl --insecure -X POST -H 'Content-type: application/json' --data '${PAYLOAD}' ${SLACK_TOKEN}"
#echo "COMMAND: ${COMMAND}"
eval $COMMAND
