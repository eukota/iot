#!/usr/bin/env python3
import argparse
import datetime
import logging
from sensor import Sensor

parser = argparse.ArgumentParser(description='Logs the distance in inches from the distance sensor to input file.')
parser.add_argument('--output', help='Path to file to write to. Defaults to a local file named out.txt', default='out.txt')
parser.add_argument('--append', type=bool, help='True = append to file, False = overwrite file, Defaults to True', default=True)
parser.add_argument('--verbose', type=bool, help='verbose output will also go to log file', default=False)
args = parser.parse_args()

if args.verbose:
        logging.getLogger().setLevel('DEBUG')
        logging.debug("Distance Read...")
        logging.debug("Output: %s" % args.output )
        logging.debug("Append: %r" % args.append )
        logging.debug("Verbose: %r" % args.verbose )

with Sensor(pin_trigger = 7, pin_echo = 11) as sensor:
        distance_in_inches = sensor.distance_in_inches()
        res = ("%s: %5.2f in" % (datetime.datetime.now(), distance_in_inches))
        if not args.append:
                f = open(args.output, "w+")
        else:
                f = open(args.output, "a")
        f.write(res)
        f.write("\n")
        f.close()
