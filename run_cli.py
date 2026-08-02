"""Developer seed/demo script for LiftLog (not the main user-facing app).

Hardcodes a sample workout, appends it to the CSV via liftlog helpers, and
prints the updated log. Prefer `streamlit run app.py` for normal use.
"""

from liftlog import empty_log, log_workout, save_log, load_log
from exercises import exercise_library
import os


def main():
    """Load the CSV, append a hardcoded sample workout, save, and print the result."""
 
    workout_log = load_log()

    date = "2026-07-07 00:00:00"
    todays_workout = [
        ("Back Squat", [(5, 185.0, "felt strong"), (5, 195.0, ""), (2, 205.0, "very hard")]),
        ("Bench Press", [(10, 135.0, "good speed")]),
        ("Pull-Up", [(10, 0.0, ""), (9, 0.0, "")]),
    ]
    workout_log = log_workout(workout_log, date, todays_workout)


    save_log(workout_log)
    print(f"Saved. Log now has {len(workout_log)} rows.")
    print(workout_log)


if __name__ == "__main__":
    main()
