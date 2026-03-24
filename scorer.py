"""
scorer.py

itemizes generated class schedules into scoring categories. 
"""


"""
Scoring guidelines:
+ 5 for no Friday's
+ 3 for no mornings (before 9:30)
+ 3 for no late clases (after 3:30)
+ 3 for shorter days (< 3 hours)
+ bonus for fewer in person draws
gap panealtiy grows quadratically
"""

# BEST possible scores > 14
# WORST possible scores < 1000 lol

def score_schedule(schedule):
    score = 0

    if has_no_friday(schedule):
        score += 5

    score -= find_gap_penalty(schedule)

    if not has_early_morning(schedule):
        score += 3

    if not has_late_classes(schedule):
        score += 3

    if has_short_days(schedule):
        score += 3

    score += compact_day_bonus(schedule)

    return score

def has_no_friday(schedule):
    for section in schedule:
        if section.is_online():
            continue
        if "F" in section.get_meeting_days():
            return False
    return True

def find_gap_penalty(schedule):
    penalty = 0
    days = {"M": [], "T": [], "W": [], "Th": [], "F": []}

    for section in schedule:
        if section.is_online():
            continue

        for d in section.get_meeting_days().split(","):
            days[d].append(section)

    for day_sections in days.values():
        day_sections.sort(key=lambda s: s._time_tokenized[0])

        for i in range(len(day_sections) - 1):
            end_current = day_sections[i]._time_tokenized[1]
            start_next = day_sections[i+1]._time_tokenized[0]

            gap_minutes = start_next - end_current
            gap_hours = gap_minutes // 60

            if gap_hours > 0:
                penalty += (gap_hours ** 2) * 3

    return penalty

def has_early_morning(schedule):
    for section in schedule:
        if section.is_online():
            continue
        if section._time_tokenized[0] < 570:
            return True
    return False

def has_late_classes(schedule):
    for section in schedule:
        if section.is_online():
            continue
        if section._time_tokenized[1] > 930:
            return True
    return False

def has_short_days(schedule):
    days = {"M": [], "T": [], "W": [], "Th": [], "F": []}

    for section in schedule:
        if section.is_online():
            continue
        for d in section.get_meeting_days().split(","):
            days[d].append(section)

    for day_sections in days.values():
        if len(day_sections) == 0:
            continue

        day_sections.sort(key=lambda s: s._time_tokenized[0])

        start = day_sections[0]._time_tokenized[0]
        end = day_sections[-1]._time_tokenized[1]

        if end - start < 180:
            return True

    return False

def compact_day_bonus(schedule):
    used_days = set()

    for section in schedule:
        if section.is_online():
            continue
        for d in section.get_meeting_days().split(","):
            used_days.add(d)

    day_count = len(used_days)

    if day_count <= 2:
        return 5
    elif day_count == 3:
        return 3
    elif day_count == 4:
        return 1
    else:
        return 0