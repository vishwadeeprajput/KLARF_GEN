import json
from pathlib import Path
from typing import Dict, Any

from logger import logger

DEFAULT_CONFIG = {
    "classification_mappings": {
        "1": "Particle",
        "2": "Scratch"
    },
    "timestamp_format": "%m-%d-%y %H:%M:%S",
    "coordinate_precision": 2,
    "default_min_defects": 0,
    "default_max_defects": 2000
}

class Config:
    def __init__(self, config_path: str = None):
        self.settings: Dict[str, Any] = DEFAULT_CONFIG.copy()
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        path = Path(config_path)
        if not path.exists():
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return

        try:
            with open(path, 'r') as f:
                user_config = json.load(f)
                self._update_recursive(self.settings, user_config)
            logger.info(f"Loaded configuration from {config_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file {config_path}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading config: {e}")

    def _update_recursive(self, d: dict, u: dict):
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._update_recursive(d[k], v)
            else:
                d[k] = v

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)
