from typing import Dict
from config import DEFAULT_CONFIG

class ClassificationManager:
    def __init__(self, mappings: Dict[str, str] = None):
        self.mappings = mappings or DEFAULT_CONFIG["classification_mappings"]
        self.reverse_mappings = {v: k for k, v in self.mappings.items()}

    def get_code(self, description: str, default: str = "0") -> str:
        return self.reverse_mappings.get(description, default)

    def get_description(self, code: str, default: str = "unclassified") -> str:
        return self.mappings.get(code, default)
