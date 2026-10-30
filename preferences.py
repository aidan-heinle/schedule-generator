"""
User-configurable schedule scoring preferences.
"""

class ScoringPreferences:
    #Holds the score weights and time cutoffs selected in the web UI.

    DEFAULTS = {
        "no_friday_bonus": 5,
        "no_morning_bonus": 3,
        "no_late_bonus": 5,
        "short_day_bonus": 3,
        "online_class_bonus": 2,
        "compact_two_day_bonus": 5,
        "compact_three_day_bonus": 3,
        "compact_four_day_bonus": 1,
        "gap_penalty_multiplier": 3,
        "morning_cutoff": "09:30",
        "late_cutoff": "15:30",
        "short_day_minutes": 180,
    }

    def __init__(self, **values):
        for key, default in self.DEFAULTS.items():
            value = values.get(key, default)
            if key in ("morning_cutoff", "late_cutoff"):
                value = self._time_to_minutes(value)
            elif key != "short_day_minutes":
                value = int(value)
            else:
                value = int(value)
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, values):
        return cls(**(values or {}))

    @staticmethod
    def _time_to_minutes(value):
        if isinstance(value, int):
            return value
        hour, minute = str(value).split(":")
        return int(hour) * 60 + int(minute)
