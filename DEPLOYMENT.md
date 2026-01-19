# Deployment Steps for Slack Command Checker

## Prerequisites
- Ensure `requests` library is installed: `pip3 install requests`
- Bot token must have `channels:history` or `groups:history` permission (depending on channel type)

## Steps

### 1. Copy the script to the Pi
```bash
# From your local machine, copy to Pi
scp check_slack_commands.py pi@your-pi-ip:/home/eukota/iot/water_tank/
```

### 2. Create the config files on the Pi
SSH into the Pi and create `config_files/config.json` and `config_files/secrets.json`:

```bash
mkdir -p /home/eukota/iot/config_files
nano /home/eukota/iot/config_files/config.json
```

Config content:
```json
{
  "paths": {
    "log_file": "/home/eukota/.water_tank/water_distance.txt",
    "state_file": "/home/eukota/.water_tank/slack_commands_state.json",
    "command_log": "/home/eukota/.water_tank/slack_commands.log"
  },
  "slack": {
    "channel_id": "CHANNEL_ID",
    "allowed_user_ids": ["USER_ID_1", "USER_ID_2"]
  },
  "sensor": {
    "pin_trigger": 7,
    "pin_echo": 11,
    "sleep_time": 5
  },
  "tank": {
    "radius_in": 54.23,
    "height_in": 75.0,
    "meter_height_in": 4.0
  },
  "polling": {
    "lookback_seconds": 300
  }
}
```

Secrets content:
```bash
nano /home/eukota/iot/config_files/secrets.json
```

```json
{
  "slack": {
    "bot_token": "xoxb-your-actual-bot-token-here",
    "webhook_endpoint": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  }
}
```

### 3. Verify bot token permissions
Your bot token needs `conversations.history` scope to read messages. Verify in Slack:
- Go to https://api.slack.com/apps
- Select your app
- Go to "OAuth & Permissions"
- Ensure "channels:history" or "groups:history" scope is added (depending on channel type)

### 4. Make the script executable
```bash
chmod +x /home/eukota/iot/water_tank/check_slack_commands.py
```

### 5. Test the script manually
```bash
# Test it runs without errors
python3 /home/eukota/iot/water_tank/check_slack_commands.py

# Check the log for any errors
tail -f /home/eukota/.water_tank/slack_commands.log
```

### 6. Add cron entry
```bash
crontab -e
```

Add this line:
```
*/1 * * * * python3 /home/eukota/iot/water_tank/check_slack_commands.py
```

### 7. Test the command
In your Slack channel `#water_tank`, type:
```
tank:level
```

Within 1 minute, you should receive a response with the current tank level.

### 8. Verify it's working
```bash
# Check the command log
tail -20 /home/eukota/.water_tank/slack_commands.log

# Check the state file (should have processed message IDs)
cat /home/eukota/.water_tank/slack_commands_state.json
```

## Troubleshooting

- **"Config file not found"**: Ensure `/home/eukota/iot/config_files/config.json` exists and has correct permissions
- **"Slack API error: missing_scope"**: Bot token needs `channels:history` permission
- **"Error fetching Slack messages"**: Check bot token is valid and has access to the channel
- **No response to command**: Check `/var/log/slack_commands.log` for errors
