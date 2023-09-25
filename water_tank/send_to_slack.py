'''
Send data to Slack
'''
import requests
import json
import argparse
import logging
import math
from watertank import WaterTank

# Parse Inputs
parser = argparse.ArgumentParser(description='Send a message to Slack')
parser.add_argument('--endpoint', type=str, help='Slack endpoint with token included', required=True)
parser.add_argument('--rawread', type=str, help='Single data read entry in format "2023-09-23 17:46:07.048532: 18.84 in"', required=True)
parser.add_argument('--dryrun', help='Set to do work but do not log to slack', action='store_true', required=False)
args = parser.parse_args()
if args.dryrun:
    logging.getLogger().setLevel('INFO')

def send_message_to_slack(endpoint, message) -> None:
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": message
    }
    logging.info(payload)
    if args.dryrun:
        return
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        logging.debug("Message sent successfully to Slack!")
    else:
        logging.debug("Failed to send message to Slack. Status code:", response.status_code)
        logging.debug("Response:", response.text)

WATER_TANK_MAXIMUM = 3000
TANK_HEIGHT = 75.0
TANK_RADIUS = 54.23
METER_HEIGHT = 4.0 # inches above max water height
tank = WaterTank(TANK_RADIUS, TANK_HEIGHT)

# Data
data_entry = args.rawread
meter_read = float(data_entry.split(' ')[2])
water_height = (TANK_HEIGHT + METER_HEIGHT) - meter_read 
gallons_remaining = tank.gallons_at_height(water_height)
if args.dryrun:
    logging.info(data_entry)
    logging.info(meter_read)
    logging.info(water_height)
    logging.info(gallons_remaining)
message = "Distance: {}\n    Estimated: {:,.0f} gallons".format(data_entry, gallons_remaining)
send_message_to_slack(args.endpoint, message)
