import os
import sys
from generator import GeneratorEngine
from config import Config
from logger import logger

def prompt_input(prompt: str, default: str = "") -> str:
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default

def main():
    print("=====================================================")
    print("    KLARF 1.2 Semiconductor Defect Generator")
    print("=====================================================")

    template_file = prompt_input("Sample KLARF 1.2 file path", "sample/AKAGEN_randomized_01.klarf")
    output_dir = prompt_input("Output directory", "output")
    start_date = prompt_input("Start date (MM-DD-YY HH:MM:SS)", "01-01-23 00:00:00")
    end_date = prompt_input("End date (optional, for bounding generation)", "")
    year = prompt_input("Year (for folder structure)", "2023")
    month = prompt_input("Month (for folder structure)", "01")

    try:
        num_lots = int(prompt_input("Number of lots to generate", "1"))
        wafers_per_lot = int(prompt_input("Number of wafers per lot", "1"))
        min_defects = int(prompt_input("Minimum defects per wafer", "50"))
        max_defects = int(prompt_input("Maximum defects per wafer", "200"))
    except ValueError:
        print("Invalid number entered. Exiting.")
        sys.exit(1)

    inspection_steps = prompt_input("Inspection step names (comma separated)", "UNCL")
    dist_model = prompt_input("Defect distribution model (uniform/gaussian/mixed)", "mixed").lower()
    config_file = prompt_input("Configuration file (optional)", "")

    seed_str = prompt_input("Random seed (optional)", "")
    if seed_str:
        import random, numpy
        seed = int(seed_str)
        random.seed(seed)
        numpy.random.seed(seed)
        logger.info(f"Random seed set to {seed}")

    if max_defects > 2000:
        print("Maximum defects per wafer cannot exceed 2000. Capping at 2000.")
        max_defects = 2000

    config = Config(config_file if config_file else None)

    gen_config = {
        "output_dir": output_dir,
        "num_lots": num_lots,
        "wafers_per_lot": wafers_per_lot,
        "min_defects": min_defects,
        "max_defects": max_defects,
        "dist_model": dist_model,
        "year": year,
        "month": month,
        "inspection_steps": inspection_steps.split(",")
    }

    engine = GeneratorEngine(gen_config)

    try:
        engine.load_template(template_file)
        engine.setup_time(start_date)
        engine.generate()
        print(f"\nSuccess! Generated KLARF files are located in: {output_dir}")
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
