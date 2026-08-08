import logging
import sys
from pathlib import Path

def setup_logger(log_file: str = "generation.log") -> logging.Logger:
    """Sets up the application logger."""
    logger = logging.getLogger("KLARF_Generator")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler (INFO level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(ch)

    # File Handler (DEBUG level)
    if log_file:
        try:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except IOError:
            logger.warning(f"Could not open log file {log_file} for writing.")

    return logger

logger = setup_logger()
