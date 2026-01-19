#!/usr/bin/env python3
import argparse
import datetime
import logging
import os

from config_loader import ConfigLoader
from distance_sensor import DistanceSensor


class LogDistance:
    def __init__(self, path, append=True):
        self.path = path
        self.append = append

    def append_reading(self, distance_in_inches, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        entry = ("%s: %5.2f in" % (timestamp, distance_in_inches))
        mode = "a" if self.append else "w+"
        f = open(self.path, mode)
        f.write(entry)
        f.write("\n")
        f.close()
        return entry

    def read_last_line(self):
        if not os.path.exists(self.path):
            return None
        try:
            f = open(self.path, 'rb')
            f.seek(0, os.SEEK_END)
            size = f.tell()
            if size == 0:
                f.close()
                return ""
            read_size = 4096 if size > 4096 else size
            f.seek(-read_size, os.SEEK_END)
            chunk = f.read(read_size)
            f.close()
            lines = chunk.splitlines()
            if not lines:
                return ""
            return lines[-1].decode('utf-8', 'replace').strip()
        except Exception as exc:
            logging.error("Error reading last log line: %s", exc)
            return None

    def read_last_lines(self, count):
        if count <= 0:
            return []
        if not os.path.exists(self.path):
            return []
        try:
            f = open(self.path, 'rb')
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            if file_size == 0:
                f.close()
                return []

            buffer_size = 8192
            data = b""
            offset = 0
            while len(data.splitlines()) <= count and file_size > offset:
                offset = min(file_size, offset + buffer_size)
                f.seek(-offset, os.SEEK_END)
                data = f.read(offset)
                if offset == file_size:
                    break

            f.close()
            lines = data.splitlines()
            tail = lines[-count:] if len(lines) >= count else lines
            return [line.decode('utf-8', 'replace').strip() for line in tail]
        except Exception as exc:
            logging.error("Error reading last log lines: %s", exc)
            return []


def main():
    parser = argparse.ArgumentParser(description='Logs the distance in inches from the distance sensor to input file.')
    parser.add_argument('--output', help='Path to file to write to. Defaults to config.json log_file', default=None)
    parser.add_argument('--config', help='Path to config.json', default=None)
    parser.add_argument('--append', type=bool, help='True = append to file, False = overwrite file, Defaults to True', default=True)
    parser.add_argument('--verbose', type=bool, help='verbose output will also go to log file', default=False)
    args = parser.parse_args()

    config_path = args.config or ConfigLoader.default_config_path()
    loader = ConfigLoader(config_path=config_path)
    config = loader.load_config()

    paths_config = config.get('paths') or {}
    sensor_config = config.get('sensor') or {}

    output_path = args.output or paths_config.get('log_file') or 'out.txt'
    pin_trigger = int(sensor_config.get('pin_trigger', 7))
    pin_echo = int(sensor_config.get('pin_echo', 11))
    sleep_time = float(sensor_config.get('sleep_time', 5))

    if args.verbose:
        logging.getLogger().setLevel('DEBUG')
        logging.debug("Distance Read...")
        logging.debug("Output: %s" % output_path)
        logging.debug("Append: %r" % args.append)
        logging.debug("Verbose: %r" % args.verbose)

    with DistanceSensor(pin_trigger=pin_trigger, pin_echo=pin_echo, sleep_time=sleep_time) as sensor:
        distance = sensor.distance_in_inches()
        logger = LogDistance(output_path, append=args.append)
        logger.append_reading(distance)


if __name__ == "__main__":
    main()
