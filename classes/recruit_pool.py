import random
from typing import List
from swimmer import Swimmer
from conference import Conference

class RecruitPool:
    def __init__(self, conference: Conference):
        self.conference = conference
        self.recruits: List[Swimmer] = []
    
    def generate_recruits(self, num_recruits: int) -> None:
        """Generate new recruits based on conference performance"""
        self.recruits.clear()
        
        # Get benchmark times (8th place from last year)
        benchmarks = {
            event: self._get_benchmark_time(event)
            for event in Conference.EVENTS
        }
        
        for _ in range(num_recruits):
            # Pick 3 random events
            events = random.sample(Conference.EVENTS, k=3)
            times = {
                event: self._generate_realistic_time(event, benchmarks[event])
                for event in events
            }
            
            self.recruits.append(
                Swimmer(
                    name=f"Recruit-{random.randint(1000, 9999)}",
                    team="",  # No team assigned yet
                    events=events,
                    times=times,
                    scholarship_cost=random.uniform(0.1, 0.5),
                    potential=random.uniform(0.8, 1.2),
                    injury_risk=random.uniform(0.05, 0.3),
                    team_fit=random.uniform(0.3, 0.8)
                )
            )
    
    def _get_benchmark_time(self, event: str) -> float:
        """Get 8th place time from last year as benchmark"""
        # In a real implementation, this would query historical data
        # For now return a reasonable default
        defaults = {
            "50 FR": 21.0, "100 FR": 46.0, "200 FR": 100.0,
            "500 FR": 270.0, "1650 FR": 950.0,
            "100 FL": 48.0, "200 FL": 110.0,
            "100 BA": 49.0, "200 BA": 110.0,
            "100 BR": 56.0, "200 BR": 125.0,
            "200 IM": 110.0, "400 IM": 240.0
        }
        return defaults.get(event, 60.0)
    
    def _generate_realistic_time(self, event: str, benchmark: float) -> float:
        """Generate time within ±5% of benchmark"""
        return benchmark * random.uniform(0.95, 1.05)