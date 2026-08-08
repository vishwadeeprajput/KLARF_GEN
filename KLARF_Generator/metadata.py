import random
import string

class MetadataGenerator:
    def __init__(self):
        self.lot_counter = 1

    def generate_lot_id(self) -> str:
        prefix = "".join(random.choices(string.ascii_uppercase, k=3))
        lot_id = f"{prefix}{self.lot_counter:04d}"
        self.lot_counter += 1
        return lot_id

    def generate_wafer_id(self, index: int) -> str:
        # e.g., "01", "02", etc.
        return f"{index:02d}"

    def generate_slot(self, index: int) -> int:
        # Slots are typically 1 to 25
        return ((index - 1) % 25) + 1
