import os
from pathlib import Path
from typing import Any

def ensure_dir(path_str: str):
    """Ensure that a directory exists, creating it if necessary."""
    path = Path(path_str)
    path.mkdir(parents=True, exist_ok=True)

def safe_float(val: Any, default: float = 0.0) -> float:
    """Safely convert to float."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def safe_int(val: Any, default: int = 0) -> int:
    """Safely convert to int."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return default
