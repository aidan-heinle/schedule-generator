"""
Simple class scheduler
Aidan Heinle

3/10/2026
"""



from classSection import ClassSection
import scheduler
import writer
import scorer


classes = []

with open("course_inputs/Test5.txt", "r") as f:
    for line in f:
        items = line.strip().split(";")
        classes.append(ClassSection(*items))

groups = scheduler.group_courses(classes)
unsorted_schedules = scheduler.generate_schedules(groups)
sorted_schedules = scheduler.sort_schedules(unsorted_schedules)

scored_schedules = []
for schedule in sorted_schedules:
    score = scorer.score_schedule(schedule)
    scored_schedules.append((score, schedule))

scored_schedules.sort(key=lambda x: x[0], reverse=True)

writer.write_to_file(sorted_schedules)
writer.write_scored_to_file(scored_schedules)
