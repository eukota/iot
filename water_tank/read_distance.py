#!/usr/bin/env python3
import argparse
import logging
import time
from sensor import Sensor

# Parse Inputs
parser = argparse.ArgumentParser(description='Read the distance in inches from the distance sensor.')
parser.add_argument('--interval', type=float, help='time interval to poll the sensor in seconds', default=0.25)
args = parser.parse_args()
read_interval = args.interval

# Setup
logging.getLogger().setLevel('DEBUG')

# Begin
logging.info("Distance Read...")
logging.info("Interval: %5.2f" % read_interval )
with Sensor(pin_trigger=7, pin_echo=11) as sensor:
    try:
        while(True):
            logging.info("Distance: %5.2f in" % sensor.distance_in_inches())
            time.sleep(read_interval)
    except KeyboardInterrupt:
        logging.info("Exiting")
        pass

