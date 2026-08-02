"""Static exercise catalog for LiftLog.

`exercise_library` is a list of exercise dicts. The Streamlit UI currently
uses only the `name` field for the exercise selectbox. The other fields
(category, movement_pattern, equipment, muscle_group) are metadata kept for
future filtering or analysis features.
"""

exercise_library = [
    {"name": "Back Squat", "category": "Strength",
     "movement_pattern": "Squat", "equipment": "Barbell",
     "muscle_group": "Quads"},
    {"name": "Bench Press", "category": "Strength",
     "movement_pattern": "Horizontal Push", "equipment": "Barbell",
     "muscle_group": "Chest"},
    {"name": "Deadlift", "category": "Strength",
     "movement_pattern": "Hinge", "equipment": "Barbell",
     "muscle_group": "Hamstrings"},
    {"name": "Overhead Press", "category": "Strength",
     "movement_pattern": "Vertical Push", "equipment": "Barbell",
     "muscle_group": "Shoulders"},
    {"name": "Pull-Up", "category": "Bodyweight",
     "movement_pattern": "Vertical Pull", "equipment": "Bodyweight",
     "muscle_group": "Back"},
]