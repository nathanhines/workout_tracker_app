"""Streamlit UI for LiftLog.

Pages are switched via `st.session_state.page` ("home" or "form").
An in-progress workout is held in `st.session_state.draft` as a list of
(exercise_name, [(reps, weight, notes), ...]) pairs until the user saves.

Run with: streamlit run app.py
"""

from datetime import datetime

import streamlit as st

from exercises import exercise_library
from liftlog import load_log, log_workout, save_log

# to run "streamlit run app.py" in the terminal

# --- session state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if "draft" not in st.session_state:
    st.session_state.draft = []


def show_home():
    """Home page: title, navigation to the form, and date-filtered workout history."""
    # --- header ---
    col1, col2 = st.columns([3, 1], vertical_alignment="center")

    with col1:
        st.title("LiftLog")

    with col2:
        if st.button("Log a workout", type="primary", use_container_width=True):
            st.session_state.page = "form"
            st.rerun()  # refresh UI after navigation state change

    st.divider()

    df = load_log()

    if not df.empty:
       
        # Date filter section
        st.subheader("Filter by Date")
        col1, col2 = st.columns(2)

        # Get min and max dates from the data
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()

        with col1:
            from_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)

        with col2:
            to_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)

        # Filter the dataframe
        filtered_df = df[
            (df['date'].dt.date >= from_date) &
            (df['date'].dt.date <= to_date)
        ]

        

        # --- history table ---
        if not filtered_df.empty:
            st.dataframe(filtered_df, hide_index=True, width='stretch')
        else:
            st.warning("No workouts found in the selected date range.")
    else:
        st.info("No workouts logged yet.")


def show_form():
    """Form page: collect sets into a draft workout, then append and save to CSV."""
    # --- navigation ---
    if st.button("← Back"):
        st.session_state.draft = []
        st.session_state.page = "home"
        st.rerun()  # refresh UI after navigation state change

    st.title("Add workout")

    # --- set inputs ---
    date = st.date_input("Date")
    exercise_names = [e["name"] for e in exercise_library]
    exercise = st.selectbox("Exercise", exercise_names)
    reps = st.number_input("Reps", min_value=1, value=5, step=1)
    weight = st.number_input("Weight (lbs)", min_value=0.0, value=135.0, step=5.0)
    notes = st.text_input("Notes")

    if st.button("Add set"):
        new_set = (int(reps), float(weight), notes)
        draft = st.session_state.draft

        if draft and draft[-1][0] == exercise:
            # same exercise as last entry → append another set
            name, sets = draft[-1]
            sets.append(new_set)
            draft[-1] = (name, sets)
        else:
            # different exercise → start a new (name, [set]) pair
            draft.append((exercise, [new_set]))

        st.rerun()  # refresh UI so the draft table updates

    # --- draft display & save ---
    if st.session_state.draft:
        st.subheader("Draft workout")
        rows = []
        for exercise_name, sets in st.session_state.draft:
            for i, (r, w, n) in enumerate(sets, start=1):
                rows.append({
                    "exercise": exercise_name,
                    "set": i,
                    "reps": r,
                    "weight": w,
                    "notes": n,
                })
        st.dataframe(rows, hide_index=True)

        if st.button("Save workout", type="primary"):
            workout_date = datetime.combine(date, datetime.min.time())
            df = load_log()
            df = log_workout(df, workout_date, st.session_state.draft)
            save_log(df)
            st.session_state.draft = []
            st.session_state.page = "home"
            st.rerun()  # refresh UI after save and return home
    else:
        st.caption("No sets added yet.")


# --- page router ---
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "form":
    show_form()
