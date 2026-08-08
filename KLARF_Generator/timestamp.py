from datetime import datetime, timedelta
import random

class TimestampGenerator:
    def __init__(self, start_date_str: str, format_str: str = "%m-%d-%y %H:%M:%S"):
        self.format_str = format_str
        try:
            # First try parsing assuming the user provided standard formats
            # The sample has "01-14-06 13:18:59" which is %m-%d-%y %H:%M:%S
            self.current_time = datetime.strptime(start_date_str, format_str)
        except ValueError:
            # Fallback for simpler user inputs like just date
            try:
                self.current_time = datetime.strptime(start_date_str, "%Y-%m-%d")
            except ValueError:
                self.current_time = datetime.now()

    def advance_time(self, min_minutes: int = 1, max_minutes: int = 60) -> datetime:
        """Advances time by a random amount between min and max minutes."""
        delta_minutes = random.randint(min_minutes, max_minutes)
        self.current_time += timedelta(minutes=delta_minutes)
        return self.current_time

    def get_current_formatted(self) -> str:
        return self.current_time.strftime(self.format_str)
