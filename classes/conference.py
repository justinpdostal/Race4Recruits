import random
from team import Team
from recruit_pool import RecruitPool

class Conference:
    EVENT_POINTS = {
        1: 20, 2: 17, 3: 16, 4: 15, 5: 14, 6: 13, 7: 12, 8: 11,  # A final
        9: 9, 10: 7, 11: 6, 12: 5, 13: 4, 14: 3, 15: 2, 16: 1    # B final
    }
    
    def __init__(self, team_names, initial_budgets, pool_size=50):
        """
        Initialize a swimming conference.
        
        Args:
            team_names (list): List of team names
            initial_budgets (list): List of initial budgets for teams
            pool_size (int): Size of recruit pool
        """
        if len(team_names) != 4 or len(initial_budgets) != 4:
            raise ValueError("Conference must have exactly 4 teams")
            
        self.teams = [Team(name, budget) for name, budget in zip(team_names, initial_budgets)]
        self.recruit_pool = RecruitPool(pool_size)
        self.history = []  # Store historical results
        
    def simulate_bidding(self):
        """Simulate the bidding process for recruits."""
        recruits = self.recruit_pool.get_recruits().copy()
        random.shuffle(recruits)  # Randomize order
        
        for swimmer in recruits:
            interested_teams = [team for team in self.teams if team.can_afford(swimmer)]
            
            if not interested_teams:
                continue
                
            # Teams bid based on their budget and popularity
            bids = []
            for team in interested_teams:
                # Base bid is swimmer's request plus some randomness based on popularity
                popularity_bonus = random.randint(0, team.popularity // 10)
                bid = swimmer.scholarship + popularity_bonus
                bids.append((bid, team))
            
            # Sort bids by amount (descending) and team popularity (descending)
            bids.sort(key=lambda x: (-x[0], -x[1].popularity))
            
            winning_bid, winning_team = bids[0]
            if winning_team.make_bid(swimmer, winning_bid):
                self.recruit_pool.remove_recruit(swimmer)
    
    def simulate_conference_meet(self):
        """Simulate the conference meet and calculate scores based on actual times."""
        team_scores = {team.name: 0 for team in self.teams}
    
        # Simulate each event
        for event in RecruitPool.EVENT_TYPES:
            event_results = []
        
            # Collect all swimmers competing in this event
            for team in self.teams:
                for swimmer in team.roster:
                    if event in swimmer.event_placements:
                        # Get the swimmer's time for this event
                        swimmer_time = swimmer.event_times.get(event)
                        if swimmer_time is not None:
                            event_results.append({
                            'time': swimmer_time,
                            'swimmer': swimmer,
                            'team': team
                        })
        
            if not event_results:
                continue
            
            # Sort by time (fastest first)
            event_results.sort(key=lambda x: x['time'])
        
            # Assign placements based on time, with tiebreakers
            placements = []
            current_placement = 1
        
            for i, result in enumerate(event_results):
                if i > 0:
                    # Check if times are equal (within 0.5 seconds considered a tie)
                    if abs(result['time'] - event_results[i-1]['time']) <= 0.5:
                        # Tie - use popularity and randomness as tiebreaker
                        team1_pop = result['team'].popularity
                        team2_pop = event_results[i-1]['team'].popularity
                    
                        # Give advantage to more popular team, but with some randomness
                        if (team1_pop + random.randint(-10, 10)) > (team2_pop + random.randint(-10, 10)):
                            current_placement = placements[-1]['placement']
                        else:
                            current_placement = placements[-1]['placement'] + 1
                    else:
                        current_placement = i + 1
                else:
                    current_placement = 1
                
                placements.append({
                'placement': current_placement,
                'swimmer': result['swimmer'],
                'team': result['team']
            })
        
            # Award points based on placements
            for result in placements:
                placement = result['placement']
                if placement in self.EVENT_POINTS:
                    team_scores[result['team'].name] += self.EVENT_POINTS[placement]
    
        # Record results
        sorted_results = sorted(team_scores.items(), key=lambda x: -x[1])
        self.history.append(sorted_results)
    
        # Update team popularity based on performance
        for i, (name, score) in enumerate(sorted_results):
            team = next(t for t in self.teams if t.name == name)
            # 1st place gets +10 popularity, 2nd +5, 3rd -5, 4th -10
            popularity_change = [10, 5, -5, -10][i]
            team.popularity += popularity_change
            team.popularity = max(0, min(100, team.popularity))
            team.conference_scores.append(score)
    
        return sorted_results
    
    def advance_year(self):
        """Advance to the next year."""
        # Decrement years for all swimmers
        for team in self.teams:
            team.decrement_years()
        
        # Replenish recruit pool
        self.recruit_pool.replenish(50)
        
        # Reset budgets (could also make this dynamic)
        for team in self.teams:
            team.budget += 50  # Add 50k each year
    
    def get_historical_results(self):
        """Return the historical conference results."""
        return self.history
    
    def __str__(self):
        result = "Conference Teams:\n"
        for team in self.teams:
            result += f"  {team}\n"
        return result