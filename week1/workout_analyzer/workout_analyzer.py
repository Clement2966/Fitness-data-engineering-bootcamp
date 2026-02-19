"""
Workout Performance Analyzer
Week 1 Bootcamp Project - Fitness Data Engineering

Analyzes workout data to calculate progression metrics, track PRs, 
and identify performance trends over time.

Author: Clement (Ghost)
Date: Feb 2026
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class WorkoutSet:
    """Represents a single set in a workout"""
    exercise: str
    reps: int
    weight: float
    rpe: float  # Rate of Perceived Exertion (1-10)
    date: str
    notes: str = ""


@dataclass
class WorkoutSession:
    """Represents a complete workout session"""
    date: str
    exercise: str
    sets: List[WorkoutSet]
    total_volume: float = 0.0
    duration_minutes: int = 0


class WorkoutPerformanceAnalyzer:
    """Analyzes workout performance data and calculates progression metrics"""
    
    def __init__(self, data_file: str = None):
        """
        Initialize the analyzer
        
        Args:
            data_file: Path to JSON file containing workout data
        """
        self.workouts: List[WorkoutSession] = []
        self.data_file = data_file
        if data_file:
            self.load_data(data_file)
    
    def load_data(self, file_path: str):
        """Load workout data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Parse JSON data into WorkoutSession objects
                for session in data.get('sessions', []):
                    sets = [
                        WorkoutSet(
                            exercise=s['exercise'],
                            reps=s['reps'],
                            weight=s['weight'],
                            rpe=s['rpe'],
                            date=s['date'],
                            notes=s.get('notes', '')
                        )
                        for s in session.get('sets', [])
                    ]
                    workout = WorkoutSession(
                        date=session['date'],
                        exercise=session['exercise'],
                        sets=sets,
                        duration_minutes=session.get('duration_minutes', 0)
                    )
                    workout.total_volume = self.calculate_total_volume(sets)
                    self.workouts.append(workout)
            print(f"✅ Loaded {len(self.workouts)} workout sessions")
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {file_path}")
    
    def add_workout(self, workout: WorkoutSession):
        """Add a new workout session"""
        workout.total_volume = self.calculate_total_volume(workout.sets)
        self.workouts.append(workout)
    
    @staticmethod
    def calculate_total_volume(sets: List[WorkoutSet]) -> float:
        """Calculate total volume (reps × weight) for a workout"""
        return sum(s.reps * s.weight for s in sets)
    
    def get_personal_records(self, exercise: str = None) -> Dict[str, float]:
        """
        Get personal records (max weight lifted) for each exercise
        
        Args:
            exercise: Specific exercise to filter by (optional)
        
        Returns:
            Dict mapping exercise name to max weight
        """
        prs = {}
        for workout in self.workouts:
            if exercise and workout.exercise != exercise:
                continue
            
            max_weight = max((s.weight for s in workout.sets), default=0)
            current_pr = prs.get(workout.exercise, 0)
            prs[workout.exercise] = max(current_pr, max_weight)
        
        return prs if not exercise else {exercise: prs.get(exercise, 0)}
    
    def calculate_progression(self, exercise: str, window_days: int = 30) -> Dict:
        """
        Calculate strength progression over a time window
        
        Args:
            exercise: Exercise to analyze
            window_days: Rolling window in days
        
        Returns:
            Dict with progression metrics
        """
        exercise_workouts = [w for w in self.workouts if w.exercise == exercise]
        
        if not exercise_workouts:
            return {"error": f"No data for {exercise}"}
        
        # Sort by date
        exercise_workouts.sort(key=lambda w: w.date)
        
        progression = {
            "exercise": exercise,
            "total_sessions": len(exercise_workouts),
            "date_range": {
                "start": exercise_workouts[0].date,
                "end": exercise_workouts[-1].date
            },
            "volume_progression": [],
            "max_weight_progression": []
        }
        
        # Track progression by session
        for workout in exercise_workouts:
            max_weight = max((s.weight for s in workout.sets), default=0)
            progression["volume_progression"].append({
                "date": workout.date,
                "volume": workout.total_volume
            })
            progression["max_weight_progression"].append({
                "date": workout.date,
                "weight": max_weight
            })
        
        return progression
    
    def get_volume_by_exercise(self) -> Dict[str, float]:
        """Calculate total volume lifted per exercise"""
        volumes = {}
        for workout in self.workouts:
            if workout.exercise not in volumes:
                volumes[workout.exercise] = 0
            volumes[workout.exercise] += workout.total_volume
        
        return volumes
    
    def get_session_summary(self, date: str) -> Dict:
        """Get summary of a specific workout session"""
        session = next((w for w in self.workouts if w.date == date), None)
        
        if not session:
            return {"error": f"No workout found on {date}"}
        
        return {
            "date": session.date,
            "exercise": session.exercise,
            "total_volume": session.total_volume,
            "sets_count": len(session.sets),
            "max_weight": max((s.weight for s in session.sets), default=0),
            "avg_reps": sum(s.reps for s in session.sets) / len(session.sets) if session.sets else 0,
            "duration_minutes": session.duration_minutes
        }
    
    def get_recent_workouts(self, days: int = 7) -> List[Dict]:
        """Get workouts from the last N days"""
        # Sort by date descending
        sorted_workouts = sorted(self.workouts, key=lambda w: w.date, reverse=True)
        return [asdict(w) for w in sorted_workouts[:days]]
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive performance report"""
        if not self.workouts:
            return {"error": "No workout data available"}
        
        prs = self.get_personal_records()
        volumes = self.get_volume_by_exercise()
        
        report = {
            "total_sessions": len(self.workouts),
            "exercises_tracked": list(prs.keys()),
            "personal_records": prs,
            "total_volume_by_exercise": volumes,
            "total_volume_overall": sum(volumes.values()),
            "date_range": {
                "start": min(w.date for w in self.workouts),
                "end": max(w.date for w in self.workouts)
            },
            "recent_workouts": self.get_recent_workouts(5)
        }
        
        return report


if __name__ == "__main__":
    # Example usage
    analyzer = WorkoutPerformanceAnalyzer("sample_workouts.json")
    
    # Generate report
    report = analyzer.generate_report()
    print("\n" + "="*60)
    print("WORKOUT PERFORMANCE REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))
    
    # Get progression for specific exercise
    print("\n" + "="*60)
    print("SQUAT PROGRESSION ANALYSIS")
    print("="*60)
    squat_progression = analyzer.calculate_progression("Squat")
    print(json.dumps(squat_progression, indent=2))
