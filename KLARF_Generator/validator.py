from typing import List
from logger import logger
from diemap import DieMap
from distributions import Defect

class Validator:
    @staticmethod
    def validate_defect_count(count: int, min_count: int, max_count: int = 2000) -> bool:
        if count < min_count or count > max_count:
            logger.error(f"Defect count {count} is outside allowed range [{min_count}, {max_count}]. Max allowed is 2000.")
            return False
        return True

    @staticmethod
    def validate_coordinates(defects: List[Defect], die_map: DieMap) -> bool:
        valid = True
        for defect in defects:
            if (defect.die_x, defect.die_y) not in die_map.dies:
                logger.error(f"Defect ID {defect.defect_id} is at invalid die ({defect.die_x}, {defect.die_y}).")
                valid = False
        return valid

    @staticmethod
    def validate_klarf_structure(pre_content: List[str], post_content: List[str]) -> bool:
        if not pre_content:
            logger.error("Missing pre-defect content in KLARF template.")
            return False
        return True
