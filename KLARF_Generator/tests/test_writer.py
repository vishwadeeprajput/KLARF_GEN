import unittest
import sys
import os
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from writer import KlarfWriter
from distributions import Defect
from classification import ClassificationManager

class TestWriter(unittest.TestCase):
    def setUp(self):
        self.output_dir = "test_output"
        self.writer = KlarfWriter(self.output_dir)

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_writer_creates_file(self):
        pre = ["ResultTimestamp 01-01-23 00:00:00;\n", "LotID \"TEST\";\n", "WaferID \"001\";\n", "DefectList\n"]
        defects = [Defect(1, 0, 0, 0, 0, 1, 1.0)]
        post = ["SummaryList\n", "EndOfFile;\n"]

        filepath = self.writer.write(pre, defects, post, "2023", "01", "TEST_LOT", "001", "01-01-23 00:00:00")

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as f:
            content = f.read()
            self.assertIn("LotID \"TEST_LOT\";", content)
            self.assertIn("WaferID \"001\";", content)
            self.assertIn("SummaryList", content)
            self.assertIn("\t1\t1\t0.00\t307\t307;\n", content)

if __name__ == '__main__':
    unittest.main()
