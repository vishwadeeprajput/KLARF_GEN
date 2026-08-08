import random
from typing import Tuple
from diemap import DieMap
import math

class CoordinateGenerator:
    def __init__(self, die_map: DieMap):
        self.die_map = die_map

    def get_random_die(self) -> Tuple[int, int]:
        if not self.die_map.dies:
            return (0, 0)
        return random.choice(self.die_map.dies)

    def generate_random_in_die(self, die_x: int, die_y: int) -> Tuple[float, float]:
        """Generate random X, Y coordinates relative to the sample center."""
        # Calculate die center
        # Assuming DieOrigin is 0,0 and pitch is die size
        die_center_x = (die_x * self.die_map.die_pitch_x)
        die_center_y = (die_y * self.die_map.die_pitch_y)

        # Add random offset within the die
        offset_x = random.uniform(-self.die_map.die_pitch_x / 2, self.die_map.die_pitch_x / 2)
        offset_y = random.uniform(-self.die_map.die_pitch_y / 2, self.die_map.die_pitch_y / 2)

        x = die_center_x + offset_x
        y = die_center_y + offset_y

        return x, y

    def polar_to_cartesian(self, radius: float, angle: float) -> Tuple[float, float]:
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return x, y

    def map_to_nearest_die(self, x: float, y: float) -> Tuple[int, int]:
        """Given absolute X, Y find the nearest valid die."""
        # This is a simplification. We should ideally find the die that actually contains it.
        die_x = round(x / self.die_map.die_pitch_x)
        die_y = round(y / self.die_map.die_pitch_y)

        # Snap to closest valid die if out of bounds
        if (die_x, die_y) in self.die_map.dies:
            return die_x, die_y

        # Find closest valid die by distance
        min_dist = float('inf')
        closest_die = None
        for dx, dy in self.die_map.dies:
            dist = (dx - die_x)**2 + (dy - die_y)**2
            if dist < min_dist:
                min_dist = dist
                closest_die = (dx, dy)
        return closest_die or (0, 0)
