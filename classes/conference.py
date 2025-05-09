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
        
            
        self.teams = [Team(name, budget) for name, budget in zip(team_names, initial_budgets)]
        self.recruit_pool = RecruitPool(pool_size)
        self.history = []  # Store historical results
        
    def simulate_bidding(self):
        """Simulate a more realistic bidding process for recruits."""
        recruits = self.recruit_pool.get_recruits().copy()

        

        
    
        # Sort recruits by quality (better swimmers get recruited first)
        recruits.sort(
            key=lambda r: sum(t for t in r.event_times.values() if t is not None),
            reverse=False  # Lower times are better
    )
    
        # Add some randomness to the order (not strictly by time)
        random.shuffle(recruits[:10])  # Shuffle top 10 recruits
        random.shuffle(recruits[10:])  # Shuffle remaining recruits
    
        for swimmer in recruits:
            
            # Calculate swimmer's preference for each team (based on team performance)
            team_preferences = {}
            for team in self.teams:
                preference_score = 0
                # Better teams get preference
                if team.conference_scores:
                    preference_score += team.conference_scores[-1] // 10
                # Bonus for teams that need this swimmer's events
                preferred_events = set(swimmer.event_placements.keys())
                current_team_events = set()
                for s, _ in team.roster:
                    current_team_events.update(s.event_placements.keys())
                preference_score += len(preferred_events - current_team_events) * 5
                team_preferences[team] = preference_score
        
            interested_teams = [
                team for team in self.teams 
                if team.can_afford(swimmer) and team.budget > 10  # Need minimum budget
        ]
        
            if not interested_teams:
                continue
            
            # Teams create bids considering multiple factors
            bids = []
            for team in interested_teams:
                # Base bid starts at swimmer's requested scholarship
                base_bid = swimmer.scholarship
            
                # Adjust based on team's need for this swimmer's events
                team_needs = 0
                for event in swimmer.event_placements:
                    if not any(event in s.event_placements for s, _ in team.roster):
                        team_needs += 10  # Bonus for filling empty event
            
                # Adjust based on team's budget situation (save some for later recruits)
                budget_factor = min(team.budget - swimmer.scholarship, 50) / 50
            
                # Popularity influences bidding aggressiveness
                popularity_factor = team.popularity / 100
            
                # Final bid calculation
                bid = base_bid + random.randint(0, 10)  # Base randomness
                bid += int(budget_factor * (0.5 + 0.5 * random.random()))
                bid += int(team_needs * (0.5 + 0.5 * random.random()))
                bid += int(10 * popularity_factor * random.random())
                bid = min(bid, team.budget)  # Can't exceed budget
                bid = max(bid, swimmer.scholarship)  # Must meet minimum
            
            
            
                bids.append((bid, team, team_preferences[team]))
        
            # Sort bids by: 1. Bid amount, 2. Team preference, 3. Team popularity
            bids.sort(key=lambda x: (-x[0], -x[2], -x[1].popularity))
        
            # Swimmer chooses considering both bid and preference
            if bids:
                # Take top 3 bids for consideration
                top_bids = bids[:3]
            
                # Calculate selection probabilities
                total_score = sum(b[0] + b[2] for b in top_bids)
                probabilities = [(b[0] + b[2])/total_score for b in top_bids]
            
                # Select winner weighted by bid quality and preference
                winner_idx = random.choices(range(len(top_bids)), weights=probabilities)[0]
                winning_bid, winning_team, _ = top_bids[winner_idx]
            
                # 20% chance recruit chooses differently (personal factors)
                if random.random() < 0.2:
                    winning_team = random.choice([b[1] for b in top_bids])
                    winning_bid = next(b[0] for b in top_bids if b[1] == winning_team)
            
                if winning_team.make_bid(swimmer, winning_bid):
                    self.recruit_pool.remove_recruit(swimmer)
                
                    # Boost team popularity from successful recruitment
                    winning_team.popularity = min(
                    50, 
                    winning_team.popularity + swimmer.team_fit + random.randint(0, 5)
                )
    
    def simulate_conference_meet(self):
        """Simulate the conference meet using realistic scoring by:
        1. Collecting all swimmer times for each event across all teams
        2. Ranking swimmers in each event (top 16 score points)
        3. Assigning NCAA-standard points (20,17,16... for A final, 9,7,6... for B final)
        4. Breaking ties using team popularity
        """
        event_results = {}
    
        # Collect all swimmer times for each event across all teams
        for team in self.teams:
            for swimmer, _ in team.roster:
                for event, time in swimmer.event_times.items():
                    if time is not None:
                        if event not in event_results:
                            event_results[event] = []
                        event_results[event].append((time, swimmer, team))
    
        # Initialize team scores
        team_scores = {team.name: 0 for team in self.teams}
    
        # Process each event
        for event, entries in event_results.items():
            # Sort by time (ascending - lower times are better)
            entries.sort(key=lambda x: x[0])
        
            # Assign placements, handling ties with popularity
            placements = []
            current_place = 1
            while entries:
                # Find all swimmers with the same time (ties)
                current_time = entries[0][0]
                tied_entries = [e for e in entries if e[0] == current_time]
            
                # Sort tied entries by team popularity (descending)
                tied_entries.sort(key=lambda x: -x[2].popularity)
            
                # Assign placements to tied swimmers
                for entry in tied_entries:
                    placements.append((current_place, entry[1], entry[2]))
                    entries.remove(entry)
            
                current_place += len(tied_entries)
        
            # Assign points based on NCAA scoring
            for placement, swimmer, team in placements:
                if 1 <= placement <= 8:     # A Final
                    points = [20, 17, 16, 15, 14, 13, 12, 11][placement-1]
                elif 9 <= placement <= 16:  # B Final
                    points = [9, 7, 6, 5, 4, 3, 2, 1][placement-9]
                else:
                    continue  # No points for placements beyond 16
            
                team_scores[team.name] += points
    
        # Add some randomness to simulate meet variability (10% variation)
        for team in self.teams:
            team_scores[team.name] *= random.uniform(0.9, 1.1)
            team_scores[team.name] = int(team_scores[team.name])
    
        # Sort results by score (descending)
        sorted_results = sorted(
            team_scores.items(),
            key=lambda x: -x[1]
        )
    
        # Store results in history
        self.history.append(sorted_results)
        return sorted_results
    
    def advance_year(self):
        """Advance to the next year."""
        # Decrement years for all swimmers (scholarships will be returned automatically)
        for team in self.teams:
            team.decrement_years()
        
        # Replenish recruit pool
        self.recruit_pool.replenish(50)
        
    
    
    def get_historical_results(self):
        """Return the historical conference results."""
        return self.history
    
    def __str__(self):
        result = "Conference Teams:\n"
        for team in self.teams:
            result += f"  {team}\n"
        return result