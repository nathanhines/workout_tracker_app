# LiftLog

LiftLog is a personal strength-training tracker. Log each workout—exercises, reps, and weight per set—and save that history to a local CSV file on your computer. Use the Streamlit app to review past sessions with a date filter, and optionally open the data-visualization notebook to explore weight trends over time.

## Requirements

- **Python 3.13.11** (tested on this version)
- No API keys, accounts, or database setup

## Setup

1. Clone this repository and open in IDE (VS Code) .


2. Install dependencies by opening terminal in the project folder and running below:

   ```bash
   pip install -r requirements.txt
   ```

3. Confirm `workout_log.csv` is in the project root. This repo includes a sample log. The app expects that file to exist before you start.

## Run the app

Run in terminal:

```bash
streamlit run app.py
```

Your browser should open the LiftLog home page. This is the main entry point for everyday use.

## Walkthrough

### 1. Home — review history

On the home page you see your logged workouts. Use **From** / **To** to filter by date. Click **Log a workout** when you are ready to add a new session.

<img width="1334" height="680" alt="home" src="https://github.com/user-attachments/assets/cf6f6659-86d4-4f8d-9fcd-a4568cc38962" />

### 2. Add a workout

Choose the date, pick an exercise from the list, enter reps and weight (lbs), and add optional notes.

<img width="1345" height="758" alt="add_workout_form" src="https://github.com/user-attachments/assets/c9fcc739-c76c-48da-a618-c9711328afbf" />

### 3. Build a draft, then save

Click **Add set** for each set. Sets for the same exercise group together in the draft table. When the draft looks right, click **Save workout**. You return to home and the new rows appear in the history.

<img width="1333" height="831" alt="draft" src="https://github.com/user-attachments/assets/20b8af75-aee5-41f4-9433-80a25cfa8c3a" />

## Optional: progress charts

To plot weight history for an exercise:

1. Open [`data-vis.ipynb`](data-vis.ipynb) in Jupyter or VS Code
2. Run all cells (requires `plotly`, which is listed in `requirements.txt`).

Charts live in the notebook, not in the Streamlit UI.

## Common errors

| Problem | What to try |
|--------|-------------|
| `ModuleNotFoundError` (e.g. streamlit, pandas) | Activate your venv and run `pip install -r requirements.txt`. |
| `FileNotFoundError` for `workout_log.csv` | Make sure you are in the project root and the CSV is present. Restore it from git or recreate an empty log with the same columns: `date`, `exercise_name`, `set_number`, `reps`, `weight`, `notes`. |
| Streamlit says the port is already in use | Stop the other Streamlit process, or start with another port: `streamlit run app.py --server.port 8502`. |

## Limitations

- The app will fail to start if `workout_log.csv` is missing.
- Logging another workout on a date that already has entries **appends** new rows (it does not replace that day’s workout), so you can get duplicates.
- The exercise list is fixed in code; you cannot add custom lifts in the UI.
- There is no edit or delete for past workouts in the UI.
- Progress charts are only in `data-vis.ipynb`, not in the Streamlit app.

## Developer documentation

For architecture, code walkthrough, known issues, and future work, see [`docs/devGuide.md`](docs/devGuide.md).
