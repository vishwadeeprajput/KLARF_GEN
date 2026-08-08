import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from diemap import DieMap
from logger import logger

class KlarfParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lines: List[str] = []
        self.pre_defect_content: List[str] = []
        self.post_defect_content: List[str] = []
        self.die_map = DieMap()
        self.metadata: Dict[str, Any] = {}
        self.defect_record_columns: List[str] = []

    def parse(self):
        path = Path(self.filepath)
        if not path.exists():
            raise FileNotFoundError(f"KLARF file {self.filepath} not found.")

        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            self.lines = f.readlines()

        self._extract_metadata_and_diemap()
        self._split_content()
        self._parse_defect_record_spec()

        logger.info(f"Parsed KLARF {self.filepath}: {len(self.die_map.dies)} dies found, DiePitch {self.die_map.die_pitch_x}x{self.die_map.die_pitch_y}")

    def _extract_metadata_and_diemap(self):
        in_sample_test_plan = False
        sample_test_plan_count = 0
        current_count = 0

        for line in self.lines:
            line_stripped = line.strip()

            if line_stripped.startswith("DiePitch"):
                parts = line_stripped.replace(';', '').split()
                if len(parts) >= 3:
                    self.die_map.set_pitch(float(parts[1]), float(parts[2]))
            elif line_stripped.startswith("DieOrigin"):
                parts = line_stripped.replace(';', '').split()
                if len(parts) >= 3:
                    self.die_map.set_origin(float(parts[1]), float(parts[2]))
            elif line_stripped.startswith("SampleCenterLocation"):
                parts = line_stripped.replace(';', '').split()
                if len(parts) >= 3:
                    self.die_map.set_sample_center(float(parts[1]), float(parts[2]))
            elif line_stripped.startswith("SampleTestPlan"):
                in_sample_test_plan = True
                parts = line_stripped.split()
                if len(parts) >= 2:
                    try:
                        sample_test_plan_count = int(parts[1])
                    except ValueError:
                        pass
                continue
            elif in_sample_test_plan:
                if line_stripped.endswith(';'):
                    in_sample_test_plan = False
                    line_stripped = line_stripped[:-1].strip()

                parts = line_stripped.split()
                if len(parts) >= 2:
                    try:
                        x, y = int(parts[0]), int(parts[1])
                        self.die_map.add_die(x, y)
                        current_count += 1
                    except ValueError:
                        pass

                if current_count >= sample_test_plan_count and sample_test_plan_count > 0:
                    in_sample_test_plan = False

    def _split_content(self):
        phase = 0 # 0=pre, 1=defect list, 2=post

        for line in self.lines:
            line_stripped = line.strip()

            if phase == 0:
                if line_stripped.startswith("DefectList"):
                    phase = 1
                self.pre_defect_content.append(line)
            elif phase == 1:
                # Inside defect list, waiting for something that is NOT a defect line
                # A defect line starts with a number. The semicolon means end of defects.
                if line_stripped.startswith("SummarySpec") or line_stripped.startswith("SummaryList") or line_stripped.startswith("EndOfFile"):
                    phase = 2
                    self.post_defect_content.append(line)
                elif line_stripped == ";":
                    # This semicolon ends DefectList. Writer handles it.
                    pass
                elif len(line_stripped) > 0 and line_stripped[0].isalpha():
                    phase = 2
                    self.post_defect_content.append(line)
            elif phase == 2:
                # Post defect, but skip any stray defects that might be dangling
                # Actually, some KLARF files might not have clear boundaries, but if we are in post, we keep it unless it's a raw number
                if line_stripped and line_stripped[0].isdigit() and not line_stripped.startswith("Summary"):
                    pass # ignore stray defects
                else:
                    self.post_defect_content.append(line)

    def _parse_defect_record_spec(self):
        for line in self.lines:
            if line.strip().startswith("DefectRecordSpec"):
                parts = line.strip().replace(';', '').split()
                if len(parts) > 2:
                    self.defect_record_columns = parts[2:]
                break
