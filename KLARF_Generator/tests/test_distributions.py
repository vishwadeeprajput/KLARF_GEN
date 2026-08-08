import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from distributions import DefectGenerator, Defect
from diemap import DieMap
from coordinates import CoordinateGenerator

class TestDistributions(unittest.TestCase):
    def setUp(self):
        self.dm = DieMap()
        self.dm.add_die(0, 0)
        self.dm.set_pitch(100, 100)
        self.coord_gen = CoordinateGenerator(self.dm)
        self.dg = DefectGenerator(self.dm, self.coord_gen)

    def test_generate_uniform(self):
        defects = self.dg.generate_uniform(10)
        self.assertEqual(len(defects), 10)
        for d in defects:
            self.assertEqual(d.die_x, 0)
            self.assertEqual(d.die_y, 0)

    def test_generate_scratch(self):
        defects = self.dg.generate_scratch(50.0, 5)
        self.assertEqual(len(defects), 5)

    def test_generate_mixed(self):
        defects = self.dg.generate_mixed(100)
        self.assertEqual(len(defects), 100)

if __name__ == '__main__':
    unittest.main()
