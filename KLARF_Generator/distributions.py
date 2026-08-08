import random
import math
import numpy as np
from typing import List, Dict, Any, Tuple
from coordinates import CoordinateGenerator
from diemap import DieMap
from logger import logger
from parser import KlarfParser

class Defect:
    def __init__(self, defect_id: int, x: float, y: float, die_x: int, die_y: int,
                 class_code: int = 0, size: float = 0.0):
        self.defect_id = defect_id
        self.x = x
        self.y = y
        self.die_x = die_x
        self.die_y = die_y
        self.class_code = class_code
        self.size = size

        self.x_size = size
        self.y_size = size
        self.area = size * size * 0.785

    def to_klarf_line(self, columns: List[str] = None) -> str:
        # We try to use the spec if provided, else fallback to generic 15 col.
        x_str = f"{self.x:.2E}" if abs(self.x) > 1000 else f"{self.x:.2f}"
        y_str = f"{self.y:.2E}" if abs(self.y) > 1000 else f"{self.y:.2f}"

        if not columns:
            return f"{self.defect_id}\t{x_str}\t{y_str}\t{self.die_x}\t{self.die_y}\t{self.x_size:.2f}\t{self.y_size:.2f}\t{self.area:.2f}\t{self.size:.2E}\t0\t1\t{self.class_code}\t0\t1\t{self.defect_id}"

        res = []
        for col in columns:
            col_up = col.upper()
            if col_up == "DEFECTID": res.append(str(self.defect_id))
            elif col_up == "XREL": res.append(x_str)
            elif col_up == "YREL": res.append(y_str)
            elif col_up == "XINDEX": res.append(str(self.die_x))
            elif col_up == "YINDEX": res.append(str(self.die_y))
            elif col_up == "XSIZE": res.append(f"{self.x_size:.2f}")
            elif col_up == "YSIZE": res.append(f"{self.y_size:.2f}")
            elif col_up == "DEFECTAREA": res.append(f"{self.area:.2f}")
            elif col_up == "DSIZE": res.append(f"{self.size:.2E}")
            elif col_up == "CLASSNUMBER": res.append(str(self.class_code))
            elif col_up == "TEST": res.append("1")
            elif col_up == "CLUSTERNUMBER": res.append("0")
            elif col_up == "ROUGHNESS": res.append("1")
            else: res.append("0") # fallback

        return "\t".join(res)

class DefectGenerator:
    def __init__(self, die_map: DieMap, coord_gen: CoordinateGenerator, columns: List[str] = None):
        self.die_map = die_map
        self.coord_gen = coord_gen
        self.current_id = 1
        self.columns = columns

        # Get bounds for edge/center generators
        self.max_x = max([d[0] * self.die_map.die_pitch_x for d in self.die_map.dies]) if self.die_map.dies else 100000
        self.max_y = max([d[1] * self.die_map.die_pitch_y for d in self.die_map.dies]) if self.die_map.dies else 100000
        self.radius_approx = max(self.max_x, self.max_y)

    def _get_random_size(self) -> float:
        return max(0.1, np.random.lognormal(mean=1.0, sigma=1.0))

    def _create_defect(self, x: float, y: float, die_x: int, die_y: int, class_code: int, size: float) -> Defect:
        d = Defect(self.current_id, x, y, die_x, die_y, class_code, size)
        # We override to_klarf_line to use our columns
        d.to_klarf_line = lambda: Defect.to_klarf_line(d, self.columns)
        self.current_id += 1
        return d

    def generate_uniform(self, count: int, class_code: int = 1) -> List[Defect]:
        defects = []
        for _ in range(count):
            die_x, die_y = self.coord_gen.get_random_die()
            x, y = self.coord_gen.generate_random_in_die(die_x, die_y)
            size = self._get_random_size()
            defects.append(self._create_defect(x, y, die_x, die_y, class_code, size))
        return defects

    def generate_gaussian(self, count: int, class_code: int = 1) -> List[Defect]:
        defects = []
        for _ in range(count):
            x = random.gauss(0, self.max_x / 3)
            y = random.gauss(0, self.max_y / 3)
            die_x, die_y = self.coord_gen.map_to_nearest_die(x, y)
            size = self._get_random_size()
            defects.append(self._create_defect(x, y, die_x, die_y, class_code, size))
        return defects

    def generate_scratch(self, length: float, points: int, class_code: int = 2) -> List[Defect]:
        defects = []
        if points <= 0: return defects

        die_x, die_y = self.coord_gen.get_random_die()
        start_x, start_y = self.coord_gen.generate_random_in_die(die_x, die_y)
        angle = random.uniform(0, 2 * math.pi)

        for i in range(points):
            t = i / float(points)
            x = start_x + t * length * math.cos(angle)
            y = start_y + t * length * math.sin(angle)

            d_x, d_y = self.coord_gen.map_to_nearest_die(x, y)
            size = self._get_random_size() * 0.5
            defects.append(self._create_defect(x, y, d_x, d_y, class_code, size))

        return defects

    def generate_ring(self, radius: float, thickness: float, count: int, class_code: int = 1) -> List[Defect]:
        defects = []
        for _ in range(count):
            r = random.gauss(radius, thickness)
            theta = random.uniform(0, 2 * math.pi)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            d_x, d_y = self.coord_gen.map_to_nearest_die(x, y)
            size = self._get_random_size()
            defects.append(self._create_defect(x, y, d_x, d_y, class_code, size))
        return defects

    def generate_cluster(self, count: int, class_code: int = 1) -> List[Defect]:
        defects = []
        if count <= 0: return defects

        die_x, die_y = self.coord_gen.get_random_die()
        center_x, center_y = self.coord_gen.generate_random_in_die(die_x, die_y)
        spread = min(self.die_map.die_pitch_x, self.die_map.die_pitch_y) / 2

        for _ in range(count):
            x = random.gauss(center_x, spread)
            y = random.gauss(center_y, spread)
            d_x, d_y = self.coord_gen.map_to_nearest_die(x, y)
            size = self._get_random_size()
            defects.append(self._create_defect(x, y, d_x, d_y, class_code, size))

        return defects

    def generate_mixed(self, total_count: int) -> List[Defect]:
        defects = []
        remaining = total_count

        num_random = int(remaining * 0.70)
        num_scratch = int(remaining * 0.15)
        num_cluster = remaining - num_random - num_scratch

        defects.extend(self.generate_uniform(num_random, class_code=1))

        if num_scratch > 0:
            points_per_scratch = num_scratch // random.randint(1, 3) if num_scratch > 3 else num_scratch
            while num_scratch > 0:
                pts = min(points_per_scratch, num_scratch)
                defects.extend(self.generate_scratch(length=self.radius_approx/2, points=pts, class_code=2))
                num_scratch -= pts

        if num_cluster > 0:
            defects.extend(self.generate_cluster(num_cluster, class_code=1))

        random.shuffle(defects)
        for i, d in enumerate(defects):
            d.defect_id = i + 1
        self.current_id = total_count + 1

        return defects

    def reset_id(self):
        self.current_id = 1
