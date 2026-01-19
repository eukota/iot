import json
import logging

import requests

SLACK_API_BASE = 'https://slack.com/api'


class SlackClient:
    def __init__(self, webhook_endpoint=None, bot_token=None):
        self.webhook_endpoint = webhook_endpoint
        self.bot_token = bot_token

    def post_message(self, message, endpoint=None, dryrun=False):
        endpoint = endpoint or self.webhook_endpoint
        if not endpoint:
            logging.error("Missing Slack webhook endpoint")
            return False
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "text": message
        }
        logging.info(payload)
        if dryrun:
            return True
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            logging.debug("Message sent successfully to Slack!")
            return True
        logging.debug("Failed to send message to Slack. Status code: %s", response.status_code)
        logging.debug("Response: %s", response.text)
        return False

    def fetch_history(self, channel_id, oldest_ts, limit=50):
        if not self.bot_token:
            logging.error("Missing Slack bot token")
            return None
        url = "{}/conversations.history".format(SLACK_API_BASE)
        headers = {
            "Authorization": "Bearer {}".format(self.bot_token)
        }
        params = {
            "channel": channel_id,
            "oldest": str(oldest_ts),
            "limit": limit
        }

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if not data.get("ok"):
                logging.error("Slack API error: %s", data.get("error", "unknown"))
                return None

            return data.get("messages", [])

        except Exception as exc:
            logging.error("Error fetching Slack messages: %s", exc)
            return None
