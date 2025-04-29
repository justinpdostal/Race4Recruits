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
        self.roster = []
        self.conference_scores = []  # Track historical performance
        
    def add_swimmer(self, swimmer):
        """Add a swimmer to the roster if there's space."""
        if len(self.roster) < 20:
            self.roster.append(swimmer)
            self.popularity += swimmer.team_fit
            self.popularity = max(0, min(100, self.popularity))  # Keep within bounds
            return True
        return False
    
    def remove_swimmer(self, swimmer):
        """Remove a swimmer from the roster."""
        if swimmer in self.roster:
            self.roster.remove(swimmer)
            self.popularity -= swimmer.team_fit
            self.popularity = max(0, min(100, self.popularity))
    
    def decrement_years(self):
        """Decrement years for all swimmers and remove those with 0 years left."""
        swimmers_to_remove = []
        for swimmer in self.roster:
            if not swimmer.decrement_year():
                swimmers_to_remove.append(swimmer)
        
        for swimmer in swimmers_to_remove:
            self.remove_swimmer(swimmer)
    
    def calculate_team_score(self):
        """Calculate the team's projected conference score."""
        total_score = 0
        for swimmer in self.roster:
            total_score += swimmer.get_score_contribution()
        return total_score
    
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
            self.add_swimmer(swimmer)
            return True
        return False
    
    def __str__(self):
        return (f"{self.name} (Budget: ${self.budget * 10000}, Popularity: {self.popularity}, "
                f"Roster Size: {len(self.roster)}, Projected Score: {self.calculate_team_score()})")