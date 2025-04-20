from typing import List, Dict
from classes.conference import Conference
from swimmer import Swimmer

class Team:
    def __init__(self, name: str, budget: float = 10.0, popularity: float = 0.5):
        self.name = name
        self.budget = budget
        self.popularity = popularity  # 0.0-1.0 recruit attraction
        self.roster: List[Swimmer] = []
        self.history: List[Dict] = []  # Past meet results

    def add_swimmer(self, swimmer: Swimmer) -> bool:
        """Add swimmer if budget allows, return success status"""
        if self.budget >= swimmer.scholarship_cost:
            self.roster.append(swimmer)
            self.budget -= swimmer.scholarship_cost
            return True
        return False

    def remove_swimmer(self, swimmer: Swimmer) -> None:
        """Remove swimmer from roster"""
        if swimmer in self.roster:
            self.roster.remove(swimmer)
            self.budget += swimmer.scholarship_cost

    def get_swimmers_by_event(self, event: str) -> List[Swimmer]:
        """Return all swimmers who compete in this event"""
        return [s for s in self.roster if event in s.events]

    def update_after_meet(self, placements: Dict[str, int]) -> None:
        """Update team history and popularity based on meet results"""
        self.history.append(placements)
        # Simple popularity adjustment based on placement
        placement_score = sum(17 - p for p in placements.values()) / len(placements)
        self.popularity = min(1.0, max(0.0, self.popularity + (placement_score - 8) * 0.05))


    def projected_points(self, conference_data: Dict) -> Dict[str, float]:
        """
        Calculate projected points for all swimmers by event
        Returns:
            Dictionary of {event: total_points}
        """
        event_points = {event: 0.0 for event in Conference.EVENTS}
        
        for swimmer in self.roster:
            for event in swimmer.events:
                if event not in conference_data.get("conference_times", {}):
                    continue
                    
                swimmer_time = swimmer.times.get(event, float('inf'))
                event_results = conference_data["conference_times"][event]
                
                # Find placement (same logic as swimmer_points)
                placements = [e["time"] for e in event_results]
                placements.sort()
                
                swimmer_place = len(placements)
                for i, time in enumerate(placements):
                    if swimmer_time <= time:
                        swimmer_place = i + 1
                        break
                        
                if swimmer_place <= 3:
                    points = 21 - swimmer_place
                elif swimmer_place <= 16:
                    points = 17 - swimmer_place
                else:
                    points = 0
                    
                event_points[event] += points
                
        return event_points