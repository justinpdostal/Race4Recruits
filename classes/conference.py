import json
from pathlib import Path
from typing import Dict, List
from classes.swimmer import Swimmer
from team import Team

class Conference:
    EVENTS = [
        "50 FR", "100 FR", "200 FR", "500 FR", "1650 FR",
        "100 FL", "200 FL", "100 BA", "200 BA", 
        "100 BR", "200 BR", "200 IM", "400 IM"
    ]
    
    # NCAA scoring table (1st through 16th place)
    NCAA_POINTS = [20, 17, 16, 15, 14, 13, 12, 11, 9, 7, 6, 5, 4, 3, 2, 1]

    def __init__(self, name: str, data_file: str = "data/conference_times.json"):
        self.name = name
        self.teams: Dict[str, Team] = {}
        self.current_year = 0
        self._results_file = Path(data_file)
        self._conference_data = None  # Will store loaded JSON data
        self._load_initial_data()

    def _load_initial_data(self) -> None:
        """Initialize teams and swimmers from JSON data"""
        if not self._results_file.exists():
            raise FileNotFoundError(f"Conference data file {self._results_file} not found")
        
        with open(self._results_file, 'r') as f:
            self._conference_data = json.load(f)
        
        # Create all teams first
        for event_results in self._conference_data["conference_times"].values():
            for entry in event_results:
                if entry["team"] not in self.teams:
                    self.teams[entry["team"]] = Team(entry["team"])
        
        # Add swimmers to teams
        swimmers_added = set()
        for event, event_results in self._conference_data["conference_times"].items():
            for entry in event_results:
                swimmer_key = f"{entry['swimmer']}_{entry['team']}"
                if swimmer_key not in swimmers_added:
                    swimmer = Swimmer(
                        name=entry["swimmer"],
                        team=entry["team"],
                        events=[event],  # Will add other events later
                        times={event: entry["time"]}
                    )
                    self.teams[entry["team"]].add_swimmer(swimmer)
                    swimmers_added.add(swimmer_key)
                else:
                    # Add additional event to existing swimmer
                    for swimmer in self.teams[entry["team"]].roster:
                        if swimmer.name == entry["swimmer"]:
                            swimmer.events.append(event)
                            swimmer.times[event] = entry["time"]
                            break

    def get_swimmer_points(self, swimmer: Swimmer) -> float:
        """
        Calculate total potential NCAA points for a swimmer based on conference standards.
        Args:
            swimmer: Swimmer object to evaluate
        Returns:
            Total projected points across all of swimmer's events
        """
        if not self._conference_data:
            return 0.0
            
        total_points = 0.0
        
        for event in swimmer.events:
            if event not in swimmer.times:
                continue
                
            swimmer_time = swimmer.times[event]
            event_results = self._conference_data["conference_times"].get(event, [])
            
            # Get sorted times for this event
            event_times = [e["time"] for e in event_results]
            event_times.sort()
            
            # Find swimmer's placement
            placement = len(event_times) + 1  # Start after last place
            for i, time in enumerate(event_times):
                if swimmer_time <= time:
                    placement = i + 1
                    break
            
            # Assign points if in top 16
            if 1 <= placement <= 16:
                total_points += self.NCAA_POINTS[placement - 1]
                
        return round(total_points, 2)

    def get_event_standards(self, event: str) -> List[Dict]:
        """
        Get sorted results for a specific event
        Args:
            event: Event name (e.g., "50 FR")
        Returns:
            List of results sorted by time, fastest first
        """
        if not self._conference_data:
            return []
        return sorted(
            self._conference_data["conference_times"].get(event, []),
            key=lambda x: x["time"]
        )

    def simulate_meet(self) -> Dict[str, List[Dict]]:
        """Simulate a conference championship meet"""
        results = {event: [] for event in self.EVENTS}
        
        for event in self.EVENTS:
            # Collect all entries for this event
            for team in self.teams.values():
                for swimmer in team.get_swimmers_by_event(event):
                    if event in swimmer.times:
                        results[event].append({
                            "time": swimmer.times[event],
                            "swimmer": swimmer.name,
                            "team": team.name
                        })
            
            # Sort by time and keep top 16
            results[event].sort(key=lambda x: x["time"])
            results[event] = results[event][:16]
        
        # Update team placements
        team_placements = self._calculate_team_scores(results)
        for team in self.teams.values():
            team.update_after_meet(team_placements.get(team.name, {}))
        
        self.current_year += 1
        return results

    def _calculate_team_scores(self, results: Dict) -> Dict[str, Dict[str, int]]:
        """Calculate NCAA-style team scores (1st=20, 2nd=17, ..., 16th=1)"""
        team_scores = {team_name: {} for team_name in self.teams}
        
        for event, entries in results.items():
            for i, entry in enumerate(entries[:16]):
                points = max(17 - i, 1) if i < 3 else max(16 - i, 1)
                team_scores[entry["team"]][event] = points
        
        return team_scores