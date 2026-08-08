from typing import List, Tuple
from logger import logger

class DieMap:
    def __init__(self):
        self.dies: List[Tuple[int, int]] = []
        self.die_pitch_x: float = 0.0
        self.die_pitch_y: float = 0.0
        self.die_origin_x: float = 0.0
        self.die_origin_y: float = 0.0
        self.sample_center_x: float = 0.0
        self.sample_center_y: float = 0.0

    def add_die(self, x: int, y: int):
        self.dies.append((x, y))

    def set_pitch(self, x: float, y: float):
        self.die_pitch_x = x
        self.die_pitch_y = y

    def set_origin(self, x: float, y: float):
        self.die_origin_x = x
        self.die_origin_y = y

    def set_sample_center(self, x: float, y: float):
        self.sample_center_x = x
        self.sample_center_y = y

    @property
    def is_valid(self) -> bool:
        return len(self.dies) > 0 and self.die_pitch_x > 0 and self.die_pitch_y > 0

    def get_valid_dies(self) -> List[Tuple[int, int]]:
        return self.dies
