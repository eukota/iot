from watertank import WaterTank

def parse_distance_in_inches(raw_entry):
    tokens = raw_entry.strip().split()
    if len(tokens) < 2:
        raise ValueError("Unexpected log line format: %r" % raw_entry)
    return float(tokens[-2])


def build_tank_message(raw_entry, tank_config):
    tank_height = float(tank_config.get('height_in', 75.0))
    tank_radius = float(tank_config.get('radius_in', 54.23))
    meter_height = float(tank_config.get('meter_height_in', 4.0))
    tank = WaterTank(tank_radius, tank_height)

    meter_read = parse_distance_in_inches(raw_entry)
    gallons_remaining = gallons_from_distance(meter_read, tank, tank_height, meter_height)
    water_height = (tank_height + meter_height) - meter_read
    message = "Distance: {}\n    Estimated: {:,.0f} gallons".format(raw_entry, gallons_remaining)
    return message, meter_read, water_height, gallons_remaining


def gallons_from_distance(meter_read, tank, tank_height, meter_height):
    water_height = (tank_height + meter_height) - meter_read
    return tank.gallons_at_height(water_height)
