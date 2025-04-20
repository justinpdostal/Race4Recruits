from typing import Dict


class Swimmer:
    def __init__(self, name: str, team: str, events: list[str], times: dict[str, float],
                 eligibility: int = 4, scholarship_cost: float = 0.0,
                 potential: float = 1.0, injury_risk: float = 0.1, team_fit: float = 0.5):
        self.name = name
        self.team = team
        self.events = events
        self.times = times  # Format: {"50 FR": 19.20, "100 FR": 43.16}
        self.eligibility = eligibility  # Years remaining (4 = freshman)
        self.scholarship_cost = scholarship_cost
        self.potential = potential  # 0.8-1.2 multiplier for improvement
        self.injury_risk = injury_risk  # 0.0-1.0 probability
        self.team_fit = team_fit  # 0.0-1.0 compatibility score

    def improve_time(self, event: str, improvement_rate: float = 0.02) -> None:
        """Simulate time improvement based on potential"""
        if event in self.times:
            self.times[event] *= (1 - improvement_rate * self.potential)

    def decrement_eligibility(self) -> None:
        """Reduce eligibility by 1 year (call at year end)"""
        self.eligibility = max(0, self.eligibility - 1)

    @property
    def is_injured(self) -> bool:
        """Check if swimmer gets injured this year"""
        import random
        return random.random() < self.injury_risk


       