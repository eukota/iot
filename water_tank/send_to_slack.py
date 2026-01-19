'''
Send data to Slack
'''
import argparse
import logging

from config_loader import ConfigLoader
from slack_client import SlackClient
from tank_message import build_tank_message

# Parse Inputs
def main():
    parser = argparse.ArgumentParser(description='Send a message to Slack')
    parser.add_argument('--endpoint', type=str, help='Slack endpoint with token included', required=False)
    parser.add_argument('--config', type=str, help='Path to config.json', required=False)
    parser.add_argument('--secrets', type=str, help='Path to secrets.json', required=False)
    parser.add_argument('--rawread', type=str, help='Single data read entry in format "2023-09-23 17:46:07.048532: 18.84 in"', required=True)
    parser.add_argument('--dryrun', help='Set to do work but do not log to slack', action='store_true', required=False)
    args = parser.parse_args()
    if args.dryrun:
        logging.getLogger().setLevel('INFO')

    config_path = args.config or ConfigLoader.default_config_path()
    secrets_path = args.secrets or ConfigLoader.default_secrets_path()
    loader = ConfigLoader(config_path=config_path, secrets_path=secrets_path)
    config = loader.load_config()
    secrets = loader.load_secrets()

    slack_secrets = secrets.get('slack') or {}
    endpoint = args.endpoint or slack_secrets.get('webhook_endpoint')
    if not endpoint:
        raise SystemExit("Missing Slack webhook endpoint. Use --endpoint or set secrets.json.")

    tank_config = config.get('tank') or {}
    message, meter_read, water_height, gallons_remaining = build_tank_message(args.rawread, tank_config)
    if args.dryrun:
        logging.info(args.rawread)
        logging.info(meter_read)
        logging.info(water_height)
        logging.info(gallons_remaining)

    client = SlackClient(webhook_endpoint=endpoint)
    client.post_message(message, dryrun=args.dryrun)


if __name__ == "__main__":
    main()
