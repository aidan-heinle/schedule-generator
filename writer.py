"""
writer.py

writes finished product to either:

output/unscored/unscored.{current_time}.txt
output/scored/scored.{current_time}.txt

"""


from datetime import datetime

"""
def write_to_file(completed_schedule):
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    
    with open(f"output/unscored/unscored.{current_time}.txt", "w") as f:
        
        f.write(f"{len(completed_schedule)} schedules generated!\n")

        for i in range(len(completed_schedule)):
            f.write(f"==========Schedule {i+1}==========\n")
            
            for course in completed_schedule[i]:
                f.write(f"{str(course)}\n")


    print(f"written to output/unscored/unscored.{current_time}.txt!")
"""

def write_scored_to_file(scored_schedule):
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    with open(f"output/scored/scored.{current_time}.txt", "w") as f:

        f.write(f"{len(scored_schedule)} schedules generated!\n")

        for i, (score, schedule) in enumerate(scored_schedule):

            f.write(f"==========Schedule {i+1}, Score={score}==========\n")

            for course in schedule:
                f.write(f"{course}\n")

            f.write("\n")

    print(f"written to output/scored/scored.{current_time}.txt!")
