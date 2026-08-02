"""CSV-backed workout log for LiftLog.

Provides the shared schema and helpers used by the Streamlit app, CLI seed
script, and data-vis notebook.

Schema columns: date, exercise_name, set_number, reps, weight, notes.

log_exercise / log_workout build set rows and return a new DataFrame;
save_log / load_log handle CSV I/O.
"""

import pandas as pd


def empty_log():
    """Return an empty log DataFrame with the correct columns and dtypes.
    One home for the schema so it isn't duplicated across files."""
    return pd.DataFrame({
        'date': pd.Series(dtype='datetime64[us]'),
        'exercise_name': pd.Series(dtype='object'),
        'set_number': pd.Series(dtype='int'),
        'reps': pd.Series(dtype='int'),
        'weight': pd.Series(dtype='float'),
        'notes': pd.Series(dtype='object'),
    })



def build_set(date, exercise_name, set_number, reps, weight, notes=""): 
    """Build a single set's row as a dict. The atom the other functions assemble."""
    return {
        "date": date,
        "exercise_name": exercise_name,
        "set_number": set_number,
        "reps": reps,
        "weight": weight,
        "notes": notes,
    }



# log_exercise function to build all rows for one exercise in one day it takes a date, exercise name, and a list of sets and returns a list of rows (dicts) that we will add to the dataframe
def log_exercise(date, exercise_name, sets): 
    """
    Build all rows for one exercise in one day.
    `sets` is a list of (reps, weight, notes) tuples one per set.
    set_number is assigned automatically, starting at 1.
    """

    rows = [] #empty list to store set rows
    set_number = 1 #start at 1
    for this_set in sets: #iterate over the list of sets
        reps, weight, notes = this_set #unpack the tuple
        rows.append(build_set(date, exercise_name, set_number, reps, weight, notes)) #add the row to the list
        set_number = set_number + 1  # add 1 to the counter for the next set
    return rows
 


def log_workout(df, date, exercises): 
    """
    Add a full workout to the log dataframe.
    `exercises` is a list of (exercise_name, sets) pairs.
    Collects every set-dict into one batch, then concats onto dataframe in one go.
    Returns the new, larger dataframe (does not modify df in place).
    """
    # GOTCHA: always appends to the dataframe, logging the same date again creates duplicate rows.
    new_workout = [] #empty list to store new workout rows
    for exercise_name, sets in exercises: #iterate over the list of exercises and sets
        new_workout.extend(log_exercise(date, exercise_name, sets)) #add the rows to the new workout list

    new_rows = pd.DataFrame(new_workout) #create a new dataframe from the new workout list
    return pd.concat([df, new_rows], ignore_index=True) #concatenate the new dataframe to the existing dataframe and return the result
 


def save_log(df, path="workout_log.csv"): 
    """Write the log frame to CSV. index=False keeps pandas' row index out of the file."""
    df.to_csv(path, index=False) #write the dataframe to a csv file



def load_log(path="workout_log.csv"):
    """Read the log CSV back into a typed frame.
    parse_dates rebuilds the datetime type (fixing the logging-time drift)."""
    # GOTCHA: path must already exist or read_csv raises FileNotFoundError.
    return pd.read_csv(path, parse_dates=["date"]) #read the csv file back into a dataframe and parse the date column to a datetime object
