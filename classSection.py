class ClassSection:
    """
    classSection.py
    
    class for course section creation.

    """
    
    
    def __init__(self, code, section_number, name, time, days, online=False):
        self._name = name # course name
        self._section_number = section_number # unique identifier per code, "001"
        self._code = code # course code, "IT300"
        self._time = time # time of class in 24hr, "14:00-15:15"
        self._meeting_days = days # comma seperated days, "M,W"
        self._online = online # is online. Assume all async for now

        self._time_tokenized = ClassSection.tokenize(time)
  

    def get_name(self):
        return self._name
    
    def get_section_number(self):
        return self._section_number

    def get_code(self):
        return self._code
    
    def get_time(self):
        return self._time
    
    def is_online(self):
        return self._online
    
    def get_meeting_days(self):
        return self._meeting_days
    
    def __repr__(self):
        return f"{self._code}-{self._section_number}: \"{self._name}\", {self._time}, meets {self._meeting_days}."
    
    def __eq__(self, other):
        if not isinstance(other, ClassSection):
            return False
        return (
            self._name == other._name and
            self._code == other._code and
            self._section_number == other._section_number
        )
    
    @staticmethod
    def _to_minutes(time_str):
        hour, minute = map(int, time_str.split(":"))
        return hour * 60 + minute

    @staticmethod
    def tokenize(time_range):
        start, end = time_range.split("-")
        return (ClassSection._to_minutes(start), ClassSection._to_minutes(end))
    
    
    def _is_conflicting(self, other):

        #overlap if max(S1, O1) <= min(S2, O2)

        def day_conflict(a, b):
            return not set(a.split(',')).isdisjoint(b.split(','))

        d1 = self._meeting_days
        d2 = other._meeting_days

        if not day_conflict(d1, d2):
            return False

        start_max = max(self._time_tokenized[0], other._time_tokenized[0])
        end_min = min(self._time_tokenized[1], other._time_tokenized[1])

        # < and not <= to allow back to back
        return start_max < end_min
            




