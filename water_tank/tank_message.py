import math

from watertank import WaterTank

def build_tank_message(raw_entry, tank_config):
    tank_height = float(tank_config.get('height_in', 75.0))
    tank_radius = float(tank_config.get('radius_in', 54.23))
    meter_height = float(tank_config.get('meter_height_in', 4.0))
    tank = WaterTank(tank_radius, tank_height)

    meter_read = float(raw_entry.split(' ')[2])
    water_height = (tank_height + meter_height) - meter_read
    gallons_remaining = tank.gallons_at_height(water_height)
    message = "Distance: {}\n    Estimated: {:,.0f} gallons".format(raw_entry, gallons_remaining)
    return message, meter_read, water_height, gallons_remaining
