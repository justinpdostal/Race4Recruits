import random

class Swimmer:
    def __init__(self, name, events, event_placements, event_times, scholarship, team_fit, years_remaining=4):
        self.name = name
        self.events = events[:3]
        self.event_placements = event_placements
        self.event_times = event_times  # Dictionary mapping events to times
        self.scholarship = scholarship
        self.team_fit = team_fit
        self.years_remaining = years_remaining
        
        
    def decrement_year(self):
        self.years_remaining -= 1
        return self.years_remaining > 0
    
    def get_score_contribution(self, is_relay=False):
        """Calculate realistic points this swimmer would contribute at conference.
    
    Args:
        is_relay (bool): Whether scoring for a relay event
        
    Returns:
        float: Projected points contribution
        """
        total = 0
    
        # Realistic scoring weights based on NCAA championship standards
        scoring_weights = {
        "50 FR": 1.2,   # Sprints are highly competitive
        "100 FR": 1.1,
        "200 FR": 1.0,
        "500 FR": 0.9,   # Distance events typically score slightly less
        "1650 FR": 0.8,
        "100 FL": 1.0,
        "200 FL": 0.95,
        "100 BA": 1.0,
        "200 BA": 0.95,
        "100 BR": 1.1,   # Breaststroke often has fewer top competitors
        "200 BR": 1.0,
        "200 IM": 1.05,
        "400 IM": 1.0
    }
    
        for event, placement in self.event_placements.items():
            if placement is None:
                continue
            
            # Base points
            if 1 <= placement <= 8:     # A Final
                points = (9 - placement) * 2
            elif 9 <= placement <= 16:  # B Final
                points = (17 - placement)
            else:
                continue
            
            # Apply event weight
            weight = scoring_weights.get(event, 1.0)
            weighted_points = points * weight
        
            # Apply bonus for top placements
            if placement == 1:
                weighted_points += 3   # Champion bonus
            elif placement <= 3:
                weighted_points += 1.5 # Medal bonus
            
            # Relay multiplier if applicable
            if is_relay:
                weighted_points *= 1.5
            
            total += weighted_points
    
        # Apply swimmer consistency factor (0.8-1.2)
        consistency = 0.8 + (self.team_fit + 5) * 0.04
        return total * consistency
    
    @classmethod
    def generate_random_swimmer(cls, event_types):
        """Generate a random swimmer for the recruit pool."""
        first_names = ["John", "Michael", "David", "James", "Robert", "William"] 
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller"]
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        events = random.sample(event_types, 3)
        
        event_placements = {}
        event_times = {}
        
        # Generate realistic times based on event
        time_ranges = {
            "50 FR": (19.0, 24.0),
            "100 FR": (43.0, 52.0),
            "200 FR": (93.0, 115.0),
            "500 FR": (255.0, 280.0),
            "1650 FR": (900.0, 1000.0),
            "100 FL": (45.0, 55.0),
            "200 FL": (100.0, 115.0),
            "100 BA": (46.0, 55.0),
            "200 BA": (100.0, 115.0),
            "100 BR": (53.0, 63.0),
            "200 BR": (115.0, 130.0),
            "200 IM": (100.0, 115.0),
            "400 IM": (220.0, 260.0)
        }
        
        for event in events:
            # Generate a random time within the realistic range
            min_time, max_time = time_ranges.get(event, (60.0, 120.0))
            time = random.uniform(min_time, max_time)
            event_times[event] = time
            
            # 60% chance to score, 40% chance to not score
            if random.random() < 0.6:
                placement = random.choices(
                    range(1, 17),
                    weights=[10, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1]
                )[0]
            else:
                placement = None  # Doesn't score
            event_placements[event] = placement
        
        scholarship = random.choice([0, 10, 20, 30, 40, 50])
        team_fit = random.randint(-5, 5)
        
        return cls(name, events, event_placements, event_times, scholarship, team_fit)
    
    def __str__(self):
        return f"{self.name} (${self.scholarship * 1000}, {self.years_remaining}yrs)"