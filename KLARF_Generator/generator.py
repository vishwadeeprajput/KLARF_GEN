import random
from typing import Dict, Any
from logger import logger
from parser import KlarfParser
from timestamp import TimestampGenerator
from metadata import MetadataGenerator
from diemap import DieMap
from coordinates import CoordinateGenerator
from distributions import DefectGenerator
from validator import Validator
from writer import KlarfWriter

class GeneratorEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.parser = None
        self.timestamp_gen = None
        self.metadata_gen = MetadataGenerator()
        self.writer = KlarfWriter(config.get("output_dir", "output"))
        self.defect_gen = None

    def load_template(self, template_path: str):
        self.parser = KlarfParser(template_path)
        self.parser.parse()

        if not Validator.validate_klarf_structure(self.parser.pre_defect_content, self.parser.post_defect_content):
            raise ValueError("Invalid KLARF template structure.")

        coord_gen = CoordinateGenerator(self.parser.die_map)
        self.defect_gen = DefectGenerator(self.parser.die_map, coord_gen, self.parser.defect_record_columns)

    def setup_time(self, start_date: str):
        self.timestamp_gen = TimestampGenerator(start_date)

    def generate(self):
        logger.info("Starting generation process...")

        num_lots = self.config.get("num_lots", 1)
        wafers_per_lot = self.config.get("wafers_per_lot", 1)
        min_defects = self.config.get("min_defects", 0)
        max_defects = self.config.get("max_defects", 2000)
        dist_model = self.config.get("dist_model", "mixed")

        year = self.config.get("year", "2023")
        month = self.config.get("month", "01")

        total_wafers = num_lots * wafers_per_lot
        generated_count = 0

        for _ in range(num_lots):
            lot_id = self.metadata_gen.generate_lot_id()
            logger.info(f"Generating Lot: {lot_id}")

            for w in range(1, wafers_per_lot + 1):
                wafer_id = f"{w:03d}"
                self.timestamp_gen.advance_time(1, 60)
                timestamp_str = self.timestamp_gen.get_current_formatted()

                num_defects = random.randint(min_defects, max_defects)

                if not Validator.validate_defect_count(num_defects, 0, 2000):
                    num_defects = min(num_defects, 2000)

                self.defect_gen.reset_id()

                if dist_model == "uniform":
                    defects = self.defect_gen.generate_uniform(num_defects)
                elif dist_model == "gaussian":
                    defects = self.defect_gen.generate_gaussian(num_defects)
                elif dist_model == "mixed":
                    defects = self.defect_gen.generate_mixed(num_defects)
                else:
                    defects = self.defect_gen.generate_uniform(num_defects)

                if not Validator.validate_coordinates(defects, self.parser.die_map):
                    logger.warning(f"Some coordinates in {wafer_id} are outside valid dies!")

                self.writer.write(
                    self.parser.pre_defect_content,
                    defects,
                    self.parser.post_defect_content,
                    year, month, lot_id, wafer_id, timestamp_str
                )
                generated_count += 1
                logger.info(f"Generated Wafer {wafer_id} in Lot {lot_id} with {len(defects)} defects.")

        logger.info(f"Generation complete. Total wafers generated: {generated_count}")
