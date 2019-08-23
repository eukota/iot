# iot

My exploration of IoT devices.

# Water Tank Meter

My first IoT device is a Raspberry Pi Zero W hooked up to an Ultrasonic Sensor. The device is deployed inside a water tank in the top of a water tower in Northern California. It connects to the home's WiFi.

## Output

* logs the water height to a file every minute
* logs egress IP address to a Slack channel daily (in case the dynamic IP changes)
* logs the last water height read to the Slack channel hourly

## Next Steps

* Ansible Deployment script for Pi Zero W
* GraphiteDB in the cloud to log results to
* Grafana front end to visualize and explore the data
