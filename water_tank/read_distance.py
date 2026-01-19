#!/usr/bin/env python3
import argparse
import logging
import time
from distance_sensor import DistanceSensor
from config_loader import ConfigLoader

# Parse Inputs
parser = argparse.ArgumentParser(description='Read the distance in inches from the distance sensor.')
parser.add_argument('--interval', type=float, help='time interval to poll the sensor in seconds', default=0.25)
parser.add_argument('--config', type=str, help='Path to config.json', required=False)
args = parser.parse_args()
read_interval = float(args.interval)

# Setup
logging.getLogger().setLevel('DEBUG')

# Begin
config_path = args.config or ConfigLoader.default_config_path()
loader = ConfigLoader(config_path=config_path)
config = loader.load_config()
sensor_config = config.get('sensor') or {}
pin_trigger = int(sensor_config.get('pin_trigger', 7))
pin_echo = int(sensor_config.get('pin_echo', 11))
sleep_time = float(sensor_config.get('sleep_time', 5))

logging.info("Distance Read...")
logging.info("Interval: %5.2f" % read_interval )
with DistanceSensor(pin_trigger=pin_trigger, pin_echo=pin_echo, sleep_time=sleep_time) as distance_sensor:
    try:
        while(True):
            logging.info("Distance: %5.2f in" % distance_sensor.distance_in_inches())
            time.sleep(read_interval)
    except KeyboardInterrupt:
        logging.info("Exiting")
        pass
