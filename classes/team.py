import random
from swimmer import Swimmer

class Team:
    def __init__(self, name, budget, popularity=50):
        """
        Initialize a swimming team.
        
        Args:
            name (str): Team name
            budget (int): Budget in 10k increments
            popularity (int): Popularity score (0-100)
        """
        self.name = name
        self.budget = budget
        self.popularity = popularity
        self.roster = []  # List of (swimmer, scholarship_amount) tuples
        self.conference_scores = []  # Track historical performance
        
    def add_swimmer(self, swimmer, scholarship_amount):
        """Add a swimmer to the roster if there's space."""
        if len(self.roster) < 20:
            self.roster.append((swimmer, scholarship_amount))
            self.popularity += swimmer.team_fit
            self.popularity = max(0, min(100, self.popularity))
            return True
        return False
    
    def remove_swimmer(self, swimmer):
        """Remove a swimmer from the roster and return their scholarship to budget."""
        for i, (s, scholarship) in enumerate(self.roster):
            if s == swimmer:
                self.roster.pop(i)
                self.popularity -= swimmer.team_fit
                self.popularity = max(0, min(100, self.popularity))
                self.budget += scholarship  # Return scholarship to budget
                return
        raise ValueError("Swimmer not found in roster")
    
    def decrement_years(self):
        """Properly handle graduation and scholarship returns"""
        swimmers_to_remove = []
        for swimmer, scholarship in self.roster:
            if not swimmer.decrement_year():
                swimmers_to_remove.append((swimmer, scholarship))
    
        for swimmer, scholarship in swimmers_to_remove:
            self.remove_swimmer(swimmer)

        # Small random change to popularity (between -2 and +2)
        self.budget += random.randint(-2, 2) * 10  # Adjust budget by $20k to $20k
        self.popularity += random.randint(-10, 10)
        self.popularity = max(0, min(100, self.popularity))
            
            
    def calculate_team_score(self):
        """Go through all the events and calculate the team's score. Do 
        this by for each swimmers event, compare their times to the other teams and their own team.
        Rank the top 16 scores and assign points based on NCAA scoring. if there exists a tie use team popularity to break it."""
        return 0
    
    
    def can_afford(self, swimmer):
        """Check if team can afford a swimmer's scholarship request."""
        return self.budget >= swimmer.scholarship
    
    def make_bid(self, swimmer, bid_amount):
        """
        Make a bid on a swimmer.
        
        Args:
            swimmer (Swimmer): Swimmer to bid on
            bid_amount (int): Bid amount in 10k increments
            
        Returns:
            bool: True if bid was successful
        """
        if bid_amount > self.budget:
            return False
        
        if bid_amount >= swimmer.scholarship:
            self.budget -= bid_amount
            self.add_swimmer(swimmer, bid_amount)
            return True
        return False
    
    def __str__(self):
        return (f"{self.name} (Budget: ${self.budget * 10000}, Popularity: {self.popularity}, "
                f"Roster Size: {len(self.roster)}, Projected Score: {self.calculate_team_score()})")