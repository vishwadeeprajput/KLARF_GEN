import os
import re
from pathlib import Path
from typing import List
from distributions import Defect
from utils import ensure_dir
from logger import logger
from classification import ClassificationManager

class KlarfWriter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.class_manager = ClassificationManager()

    def write(self, pre_content: List[str], defects: List[Defect], post_content: List[str],
              year: str, month: str, lot_id: str, wafer_id: str, timestamp_str: str) -> str:

        dir_path = Path(self.output_dir) / year / month / lot_id
        ensure_dir(str(dir_path))
        filepath = dir_path / f"Wafer{wafer_id}.klarf"

        with open(filepath, 'w', encoding='utf-8') as f:
            for line in pre_content:
                if line.strip().startswith("ResultTimestamp"):
                    f.write(f"ResultTimestamp {timestamp_str};\n")
                elif line.strip().startswith("LotID"):
                    f.write(f'LotID "{lot_id}";\n')
                elif line.strip().startswith("WaferID"):
                    f.write(f'WaferID "{wafer_id}";\n')
                elif line.strip().startswith("ClassLookup"):
                    f.write("ClassLookup " + str(len(self.class_manager.mappings)) + "\n")
                    for k, v in self.class_manager.mappings.items():
                        f.write(f" {k} \"{v}\";\n")
                elif "unclassified" in line and '0' in line:
                    pass
                elif line.strip().startswith("DefectList"):
                    f.write("DefectList\n")
                else:
                    f.write(line)

            for defect in defects:
                f.write(defect.to_klarf_line() + "\n")

            f.write(";\n")

            in_summary = False
            for line in post_content:
                if line.strip().startswith("SummaryList"):
                    f.write(line)
                    f.write(f"\t1\t{len(defects)}\t0.00\t307\t307;\n")
                    in_summary = True
                elif in_summary and not line.strip().startswith("EndOfFile"):
                    # skip old summary lines
                    pass
                elif line.strip().startswith("EndOfFile"):
                    f.write(line)
                    in_summary = False
                else:
                    f.write(line)

        logger.debug(f"Wrote KLARF file: {filepath}")
        return str(filepath)
