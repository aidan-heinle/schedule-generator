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
+ bonus for fewer in person days
gap panealtiy grows quadratically
"""

# BEST possible scores > 14
# WORST possible scores < 1000 lol

from preferences import ScoringPreferences


def score_schedule(schedule, preferences=None):
    preferences = preferences or ScoringPreferences()
    score = 0

    if has_no_friday(schedule):
        score += preferences.no_friday_bonus

    score -= find_gap_penalty(schedule, preferences)

    if not has_early_morning(schedule, preferences):
        score += preferences.no_morning_bonus

    if not has_late_classes(schedule, preferences):
        score += preferences.no_late_bonus

    if has_short_days(schedule, preferences):
        score += preferences.short_day_bonus

    score += online_class_bonus(schedule, preferences)

    score += compact_day_bonus(schedule, preferences)

    return score

def online_class_bonus(schedule, preferences):
    return sum(preferences.online_class_bonus for section in schedule if section.is_online())


def has_no_friday(schedule):
    for section in schedule:
        if section.is_online():
            continue
        if "F" in section.get_meeting_days():
            return False
    return True

def find_gap_penalty(schedule, preferences):
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
                penalty += (gap_hours ** 2) * preferences.gap_penalty_multiplier

    return penalty

def has_early_morning(schedule, preferences):
    for section in schedule:
        if not section.is_online() and section._time_tokenized[0] < preferences.morning_cutoff:
            return True
    return False

def has_late_classes(schedule, preferences):
    for section in schedule:
        if not section.is_online() and section._time_tokenized[1] > preferences.late_cutoff:
            return True
    return False

def has_short_days(schedule, preferences):
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

        if end - start < preferences.short_day_minutes:
            return True

    return False

def compact_day_bonus(schedule, preferences):
    used_days = set()

    for section in schedule:
        if section.is_online():
            continue
        for d in section.get_meeting_days().split(","):
            used_days.add(d)

    day_count = len(used_days)

    if day_count <= 2:
        return preferences.compact_two_day_bonus
    elif day_count == 3:
        return preferences.compact_three_day_bonus
    elif day_count == 4:
        return preferences.compact_four_day_bonus
    else:
        return 0
