"""
Simple class scheduler
Aidan Heinle

3/24/2026
"""

from classSection import ClassSection
import scheduler
import writer
import scorer
import re


def get_yes_no(prompt):
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def get_time(prompt):
    while True:
        time_input = input(prompt + " (HH:MM-HH:MM, 24-hour format): ").strip()
        if re.match(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}$", time_input):
            start, end = time_input.split("-")
            try:
                sh, sm = map(int, start.split(":"))
                eh, em = map(int, end.split(":"))
                if 0 <= sh < 24 and 0 <= eh < 24 and 0 <= sm < 60 and 0 <= em < 60:
                    return time_input
            except ValueError:
                pass
        print("Invalid time. Please try again in HH:MM-HH:MM format.")

def get_days(prompt):
    valid_days = {"M", "T", "W", "Th", "F"}
    while True:
        days_input = input(prompt + " (e.g., M,W,F): ").strip()
        if not days_input:
            print("You must enter at least one day.")
            continue
        days_list = [d.strip() for d in days_input.split(",")]
        if all(d in valid_days for d in days_list):
            return ",".join(days_list)
        print("Invalid day(s). Use only M,T,W,Th,F separated by commas.")

def main():
    classes = []

    print("Welcome to the Class Scheduler.\n")
    
    while True:
        command = input("What would you like to do? (add/list/remove/generate/quit): ").strip().lower()

        if command == "quit":
            print("Goodbye!")
            break

        elif command == "add":
            print("\nAdding a new course:")
            name = input("Course name: ").strip()
            code = input("Course code (e.g., MAT100): ").strip()
            
            while True:
                try:
                    num_sections = int(input("Number of sections for this course: ").strip())
                    if num_sections > 0:
                        break
                    print("Please enter a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            for i in range(1, num_sections + 1):
                section_num = f"{i:03}"  # formats 1 -> "001"
                print(f"\nEntering info for section {section_num}")
                online = get_yes_no(f"Is section {section_num} online?")

                if online:
                    cls = ClassSection(code, section_num, name, online=True)
                else:
                    time = get_time(f"Enter meeting time for section {section_num}")
                    days = get_days(f"Enter meeting days for section {section_num}")
                    cls = ClassSection(code, section_num, name, time, days)

                classes.append(cls)
                print(f"Section added: {cls}")

            print("Finished adding all sections for this course.\n")

        elif command == "list":
            if not classes:
                print("No classes added yet.\n")
            else:
                print("Classes added so far:")
                for index in range(len(classes)):
                    print(f"{index+1}. {classes[index]}")
                print("")

        elif command == "remove":
            if not classes:
                print("No classes to remove.\n")
                continue
            code_to_remove = input("Enter course code to remove: ").strip()
            before_count = len(classes)
            classes = [c for c in classes if c.get_code() != code_to_remove]
            removed_count = before_count - len(classes)
            if removed_count > 0:
                print(f"Removed {removed_count} section(s) of {code_to_remove}.\n")
            else:
                print(f"No sections found with code {code_to_remove}.\n")

        elif command == "generate":
            if not classes:
                print("No classes to schedule. Add some first.\n")
                continue

            print("\nGenerating schedules... please wait.\n")
            groups = scheduler.group_courses(classes)
            unsorted_schedules = scheduler.generate_schedules(groups)
            sorted_schedules = scheduler.sort_schedules(unsorted_schedules)

            scored_schedules = []
            for schedule in sorted_schedules:
                score = scorer.score_schedule(schedule)
                scored_schedules.append((score, schedule))

            scored_schedules.sort(key=lambda x: x[0], reverse=True)

            print(f"Generated {len(sorted_schedules)} schedules.\n")
            top_n = min(5, len(scored_schedules))
            print(f"Showing the top {top_n} schedules:\n")

            for schedule_index in range(top_n):
                score, schedule = scored_schedules[schedule_index]
                print(f"Schedule {schedule_index+1} | Score: {score}")
                for course in schedule:
                    print("  " + str(course))
                print("")

            # Always write to files
            writer.write_scored_to_file(scored_schedules)
            print("All schedules written to output files.\n")

        else:
            print("Unknown command. Please enter add/list/remove/generate/quit.\n")

if __name__ == "__main__":
    main()