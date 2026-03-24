"""
scheduler.py

finds all possible course schedules for each specificed course and section.
schedule is only possible if there are no meeting time/constraints
"""


from classSection import ClassSection

def group_courses(sections):
    grouped = {}
    for s in sections:
        code = s.get_code()
        if code not in grouped:
            grouped[code] = []
        grouped[code].append(s)

    return grouped

def generate_schedules(groups):
    course_groups = list(groups.values()) # list of lists of every value from groups dictionary
    course_groups.sort(key=len)

    results = []
    _backtrack_sections(course_groups, 0, [], results)



    return results

def _backtrack_sections(course_groups, index, current, results):
    # base case
    if index == len(course_groups):
        results.append(current.copy())
        return
    
    # try all sections for one course
    for section in course_groups[index]:
        conflict = False
        for chosen_section in current:
            if section._is_conflicting(chosen_section):
                conflict = True
                break

        if conflict:
            continue

        current.append(section)

        _backtrack_sections(course_groups, index+1, current, results)

        current.pop()


def sort_schedules(schedules):
    day_order = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4}

    def section_key(section):
        if section.is_online():
            return (999, 9999)  # push online classes to end

        days = section.get_meeting_days().split(",")
        earliest_day = min(day_order[d] for d in days)
        start_time = section._time_tokenized[0]
        return (earliest_day, start_time)

    # sort classes inside each schedule
    for sched in schedules:
        sched.sort(key=section_key)

    # find earliest class
    def schedule_key(schedule):
        earliest = None

        for section in schedule:
            key = section_key(section)

            if earliest is None or key < earliest:
                earliest = key

        return earliest

    # sort schedules themselves
    schedules.sort(key=schedule_key)

    return schedules


