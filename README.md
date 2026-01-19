# iot

My exploration of IoT devices.

## Water Tank Meter

My first IoT device is a Raspberry Pi Zero W hooked up to an ultrasonic sensor. The device sits inside a water tank in the top of a water tower in Northern California. It connects to the home's WiFi, logs readings locally, and posts summaries to Slack via cron jobs. Configuration is split into general inputs and secrets to keep deployments consistent across devices.

For deployment steps, see `water_tank/DEPLOYMENT.md`.

### Output

* logs the water height to a file every minute
* logs IP address to a Slack channel daily (in case the dynamic IP changes)
* logs the last water height read to the Slack channel hourly including a remaining gallons estimate
