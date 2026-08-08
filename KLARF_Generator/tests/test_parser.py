import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import KlarfParser

class TestKlarfParser(unittest.TestCase):
    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), '..', 'sample', 'AKAGEN_randomized_01.klarf')

    def test_parse_metadata(self):
        if not os.path.exists(self.sample_path):
            self.skipTest(f"{self.sample_path} not found")

        parser = KlarfParser(self.sample_path)
        parser.parse()

        self.assertTrue(parser.die_map.is_valid)
        self.assertGreater(len(parser.die_map.dies), 0)
        self.assertGreater(len(parser.pre_defect_content), 0)
        self.assertGreater(len(parser.post_defect_content), 0)

if __name__ == '__main__':
    unittest.main()
