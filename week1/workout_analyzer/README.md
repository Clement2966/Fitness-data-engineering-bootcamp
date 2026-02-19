# Workout Performance Analyzer

## Overview

The Workout Performance Analyzer is a Python-based data engineering tool that processes workout data, calculates progression metrics, tracks personal records (PRs), and identifies strength trends over time.

**Week 1 Bootcamp Project** - Data Engineering Fundamentals

---

## Features

✅ **Personal Record Tracking** - Automatically identifies max weight lifted per exercise  
✅ **Progression Analysis** - Tracks strength gains over rolling time windows  
✅ **Volume Calculations** - Compute total volume (reps × weight) per session and exercise  
✅ **Performance Reports** - Generate comprehensive summaries of workout data  
✅ **Time-Series Analysis** - Identify trends and patterns in strength progression  
✅ **JSON Data Loading** - Parse structured workout data from JSON files  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/ClementATH/fitness-data-engineering-bootcamp.git
cd fitness-data-engineering-bootcamp/week1/workout_analyzer
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Running the Analyzer

```bash
python workout_analyzer.py
```

This will:
1. Load sample workout data from `sample_workouts.json`
2. Generate a comprehensive performance report
3. Display progression analysis for each exercise

### Using as a Module

```python
from workout_analyzer import WorkoutPerformanceAnalyzer

# Initialize analyzer
analyzer = WorkoutPerformanceAnalyzer("your_workouts.json")

# Get personal records
prs = analyzer.get_personal_records()
print(prs)  # {'Squat': 265, 'Bench Press': 225, 'Deadlift': 375}

# Calculate progression for specific exercise
progression = analyzer.calculate_progression("Squat", window_days=30)
print(progression)

# Generate full report
report = analyzer.generate_report()
print(report)

# Get recent workouts
recent = analyzer.get_recent_workouts(days=7)
print(recent)
```

---

## Data Format

### Expected JSON Structure

```json
{
  "sessions": [
    {
      "date": "2026-01-15",
      "exercise": "Squat",
      "duration_minutes": 45,
      "sets": [
        {
          "exercise": "Squat",
          "reps": 5,
          "weight": 225,
          "rpe": 7,
          "date": "2026-01-15",
          "notes": "Felt strong today"
        }
      ]
    }
  ]
}
```

### Field Definitions

- **date** (string, YYYY-MM-DD): Date of the workout
- **exercise** (string): Name of the exercise (e.g., "Squat", "Bench Press")
- **duration_minutes** (int): How long the session took
- **sets** (array): List of sets performed
  - **reps** (int): Number of repetitions
  - **weight** (float): Weight lifted in pounds
  - **rpe** (float): Rate of Perceived Exertion (1-10 scale)
  - **notes** (string, optional): Additional notes about the set

---

## API Reference

### `WorkoutPerformanceAnalyzer`

#### Methods

**`__init__(data_file: str = None)`**
- Initialize the analyzer, optionally load data from a JSON file

**`load_data(file_path: str)`**
- Load workout data from a JSON file

**`add_workout(workout: WorkoutSession)`**
- Add a new workout session to the analyzer

**`get_personal_records(exercise: str = None) -> Dict[str, float]`**
- Get max weight lifted per exercise
- Optional: filter by specific exercise

**`calculate_progression(exercise: str, window_days: int = 30) -> Dict`**
- Calculate strength progression over a time window
- Returns volume and max weight progression over time

**`get_volume_by_exercise() -> Dict[str, float]`**
- Calculate total volume lifted per exercise

**`get_session_summary(date: str) -> Dict`**
- Get detailed summary of a specific workout session

**`get_recent_workouts(days: int = 7) -> List[Dict]`**
- Get workouts from the last N days

**`generate_report() -> Dict`**
- Generate comprehensive performance report with all metrics

---

## Example Output

### Performance Report
```json
{
  "total_sessions": 8,
  "exercises_tracked": ["Squat", "Bench Press", "Deadlift"],
  "personal_records": {
    "Squat": 265,
    "Bench Press": 225,
    "Deadlift": 375
  },
  "total_volume_by_exercise": {
    "Squat": 3990,
    "Bench Press": 3240,
    "Deadlift": 2095
  },
  "total_volume_overall": 9325,
  "date_range": {
    "start": "2026-01-15",
    "end": "2026-02-12"
  }
}
```

---

## Project Structure

```
week1/
└── workout_analyzer/
    ├── workout_analyzer.py          # Main analyzer class
    ├── sample_workouts.json         # Sample data for testing
    ├── requirements.txt             # Python dependencies
    └── README.md                    # This file
```

---

## Next Steps (Week 2+)

- **Add database storage** (SQLite/PostgreSQL)
- **Implement data visualization** (matplotlib/plotly)
- **Build REST API** (FastAPI)
- **Add machine learning** (predict future PRs)
- **Cloud deployment** (AWS/GCP)

---

## Skills Covered

✅ Object-oriented Python (classes, dataclasses)  
✅ Data structures (lists, dicts, custom types)  
✅ JSON parsing and data loading  
✅ Time-series data analysis  
✅ Type hints and documentation  
✅ Git workflow and version control  

---

## Author

Built by **Ghost** (Technical Co-Pilot) for **Clement**  
Week 1 Bootcamp - Fitness Data Engineering  
February 2026

---

## License

MIT - Feel free to use and modify

---

**Ready to ship. Ready to scale. Ready to BUILD.** 🚀💪🏾👻
