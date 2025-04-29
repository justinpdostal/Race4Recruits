import random

class Swimmer:
    def __init__(self, name, events, event_placements, event_times, scholarship, team_fit, years_remaining=4):
        self.name = name
        self.events = events
        self.event_placements = event_placements
        self.event_times = event_times  # Dictionary mapping events to times
        self.scholarship = scholarship
        self.team_fit = team_fit
        self.years_remaining = years_remaining
        
        
    def decrement_year(self):
        self.years_remaining -= 1
        return self.years_remaining > 0
    
    def get_score_contribution(self):
        """Calculate the total points this swimmer would contribute at conference."""
        total = 0
        for event, placement in self.event_placements.items():
            if placement is None:  # Skip if no placement
                continue
            if 1 <= placement <= 8:
                total += (9 - placement) * 2  # A final points
            elif 9 <= placement <= 16:
                total += (17 - placement)      # B final points
        return total
    
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
            "50 FR": (19.0, 22.0),
            "100 FR": (43.0, 48.0),
            "200 FR": (93.0, 105.0),
            "500 FR": (255.0, 280.0),
            "1650 FR": (900.0, 1000.0),
            "100 FL": (45.0, 52.0),
            "200 FL": (100.0, 115.0),
            "100 BA": (46.0, 53.0),
            "200 BA": (100.0, 115.0),
            "100 BR": (53.0, 58.0),
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