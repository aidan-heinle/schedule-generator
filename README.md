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

## To Run
* Install Dependencies:
   * pip install Flask
* cd into /schedule-generator
* run python app.py
