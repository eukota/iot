#!/usr/bin/env python3
"""
Check Slack channel for commands and respond.
Runs every minute via cron to check for commands like "tank:level".
Python 3.5-compatible, Pi Zero friendly.
"""

import json
import logging
import time
import os

from config_loader import ConfigLoader
from log_distance import LogDistance
from slack_client import SlackClient
from tank_message import build_tank_message

# Configuration paths
DEFAULT_CONFIG_PATH = ConfigLoader.default_config_path()
DEFAULT_SECRETS_PATH = ConfigLoader.default_secrets_path()


# How far back to look each run (seconds)
DEFAULT_LOOKBACK_SECONDS = 5 * 60

# Allowed Slack user IDs fallback
DEFAULT_ALLOWED_USERS = []  # e.g. ["U012ABCDEF"]

# Setup logging (file handler added after config load)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


def add_file_logger(log_path):
    """Add a file handler if not already present."""
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return
    try:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        root_logger.addHandler(file_handler)
    except Exception as exc:
        logging.error("Failed to set log file %s: %s", log_path, exc)


def load_config_and_secrets(loader):
    """Load configuration and secrets from JSON files"""
    config = loader.load_config()
    secrets = loader.load_secrets()
    if not config:
        logging.error("Config file not found or invalid: %s", loader.config_path)
        return None
    if not secrets:
        logging.error("Secrets file not found or invalid: %s", loader.secrets_path)
        return None
    return config, secrets


def load_state(state_path):
    """Load last processed timestamp state"""
    if not os.path.exists(state_path):
        return {"last_processed_ts": "0"}

    try:
        with open(state_path, 'r') as f:
            state = json.load(f)
        if "last_processed_ts" not in state:
            state["last_processed_ts"] = "0"
        return state
    except Exception as e:
        logging.error("Error loading state file: %s", e)
        return {"last_processed_ts": "0"}


def save_state_atomic(state, state_path):
    """Atomic state save to avoid corruption on power loss"""
    tmp_path = state_path + ".tmp"
    try:
        with open(tmp_path, 'w') as f:
            json.dump(state, f)
        os.rename(tmp_path, state_path)
    except Exception as e:
        logging.error("Error saving state file: %s", e)
        # best effort cleanup
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def handle_tank_level_command(slack_client, log_reader, tank_config, webhook_endpoint):
    """Handle tank:level by posting a tank status message"""
    last_line = log_reader.read_last_line()
    if last_line is None:
        logging.error("Cannot read tank log; not sending response")
        return
    if last_line == "":
        logging.error("Tank log is empty; not sending response")
        return
    message, _, _, _ = build_tank_message(last_line, tank_config)
    ok = slack_client.post_message(message, endpoint=webhook_endpoint)
    if ok:
        logging.info("Sent tank level to Slack")
    else:
        logging.error("Failed to send tank level to Slack")


def is_command(text, command_name):
    """Strict command check: must start with 'tank:level' (case-insensitive)"""
    if not text:
        return False
    t = text.strip().lower()
    return t.startswith(command_name)


class SlackCommandChecker:
    def __init__(self, config, secrets):
        self.config = config
        self.secrets = secrets

    def process_commands(self):
        slack_config = self.config.get('slack') or {}
        slack_secrets = self.secrets.get('slack') or {}

        bot_token = slack_secrets.get('bot_token')
        channel_id = slack_config.get('channel_id')
        webhook_endpoint = slack_secrets.get('webhook_endpoint')
        allowed_users = set(slack_config.get('allowed_user_ids') or DEFAULT_ALLOWED_USERS)

        if not bot_token or not channel_id:
            logging.error("Missing bot_token or channel_id")
            return

        if not webhook_endpoint:
            logging.warning("No webhook_endpoint configured; can't respond")
            return

        paths_config = self.config.get('paths') or {}
        state_path = paths_config.get('state_file', '/home/eukota/.water_tank/slack_commands_state.json')
        log_path = paths_config.get('log_file', '/home/eukota/.water_tank/water_distance.txt')
        command_log_path = paths_config.get('command_log', '/home/eukota/.water_tank/slack_commands.log')
        add_file_logger(command_log_path)

        state = load_state(state_path)
        last_processed_ts = state.get("last_processed_ts", "0")

        now = time.time()
        lookback_seconds = float((self.config.get('polling') or {}).get('lookback_seconds', DEFAULT_LOOKBACK_SECONDS))
        lookback_oldest = now - lookback_seconds

        try:
            last_ts_num = float(last_processed_ts)
        except Exception:
            last_ts_num = 0.0

        oldest = last_ts_num
        if lookback_oldest > oldest:
            oldest = lookback_oldest

        slack_client = SlackClient(bot_token=bot_token)
        messages = slack_client.fetch_history(channel_id, oldest)
        if messages is None:
            return

        if not messages:
            return

        messages.reverse()

        new_last_ts = last_ts_num
        processed_any = False

        log_reader = LogDistance(log_path)
        tank_config = self.config.get('tank') or {}

        for m in messages:
            ts = m.get("ts")
            if not ts:
                continue

            if m.get("subtype") is not None:
                continue

            try:
                ts_num = float(ts)
            except Exception:
                continue

            if ts_num <= last_ts_num:
                continue

            user = m.get("user")
            if allowed_users and user not in allowed_users:
                continue

            text = m.get("text", "")

            if is_command(text, "tank:level"):
                logging.info("Command tank:level from %s ts=%s", user, ts)
                handle_tank_level_command(slack_client, log_reader, tank_config, webhook_endpoint)
                processed_any = True

            if ts_num > new_last_ts:
                new_last_ts = ts_num

        if processed_any:
            state["last_processed_ts"] = str(new_last_ts)
            save_state_atomic(state, state_path)
        else:
            state["last_processed_ts"] = str(new_last_ts)
            save_state_atomic(state, state_path)


def process_commands():
    loader = ConfigLoader(
        config_path=DEFAULT_CONFIG_PATH,
        secrets_path=DEFAULT_SECRETS_PATH
    )
    config_secrets = load_config_and_secrets(loader)
    if not config_secrets:
        return
    config, secrets = config_secrets
    checker = SlackCommandChecker(config, secrets)
    checker.process_commands()


if __name__ == "__main__":
    try:
        process_commands()
    except Exception as e:
        logging.error("Unexpected error: %s", e)
