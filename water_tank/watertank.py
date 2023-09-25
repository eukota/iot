
import math

CUBIC_INCHES_PER_GALLON = 231.0

class WaterTank:
    '''The water tank is known to hold 3000 gallons with a depth of 75 inches'''

    def __init__(self, radius=54.23, height=75) -> None:
        self.radius_in_inches = radius
        self.height_in_inches = height
        base_area = math.pi * self.radius_in_inches * self.radius_in_inches
        self.volume_in_gallons = base_area * self.height_in_inches/CUBIC_INCHES_PER_GALLON
        self.gallons_per_inch = self.volume_in_gallons/self.height_in_inches

    def gallons_at_height(self, height) -> float:
        '''Remaining gallons at given height'''
        return height * self.gallons_per_inch

    def rate_change(self, from_height, to_height, window) -> float:
        '''Return gallons per minute'''
        gallons_from = self.gallons_at_height(from_height)
        gallons_to = self.gallons_at_height(to_height)
        return (gallons_to-gallons_from)/window
