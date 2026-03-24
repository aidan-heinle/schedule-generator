# Class Schedule Generator

A Python program that generates all possible non-conflicting class schedules from a list of course sections and ranks them using customizable scoring rules.

## Features

* Generates every valid schedule from course section data
* Detects time conflicts automatically
* Scores schedules based on preferences such as:

  * No Friday classes
  * Fewer gaps between classes
  * No early morning classes
  * No late classes
  * Shorter daily schedules
* Outputs ranked schedules to a text file

## Example Output

```
==========Schedule 1, Score=6==========
INTRODUCTION TO PHILOSOPHY-001: "PHI101", 09:00-09:50, meets M,W,F.
AMERICAN GOVERNMENT-001: "POL101", 10:00-10:50, meets M,W,F.
GENERAL CHEMISTRY-002: "CHE101", 11:00-11:50, meets M,W,F.
LINEAR ALGEBRA-001: "MAT210", 08:00-09:15, meets T,Th.
DATA STRUCTURES-001: "CSC220", 10:00-11:15, meets T,Th.
```

## How It Works

1. Terminal commands: add, list, remove, generate allow for input of course section data.
2. The program generates all combinations of sections.
3. Conflicting schedules are removed.
4. Remaining schedules are scored based on preference rules.
5. Schedules are sorted and written to an output file.

## Future Improvements

* Calendar style output for scheduling.
* UI or web interface. 
