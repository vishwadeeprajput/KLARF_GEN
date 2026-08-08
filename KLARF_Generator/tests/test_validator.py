import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validator import Validator
from diemap import DieMap
from distributions import Defect

class TestValidator(unittest.TestCase):
    def test_validate_defect_count(self):
        self.assertTrue(Validator.validate_defect_count(500, 0, 2000))
        self.assertFalse(Validator.validate_defect_count(2500, 0, 2000))

    def test_validate_coordinates(self):
        dm = DieMap()
        dm.add_die(1, 1)
        dm.add_die(2, 2)

        d1 = Defect(1, 0, 0, 1, 1)
        d2 = Defect(2, 0, 0, 3, 3)

        self.assertTrue(Validator.validate_coordinates([d1], dm))
        self.assertFalse(Validator.validate_coordinates([d2], dm))

if __name__ == '__main__':
    unittest.main()
