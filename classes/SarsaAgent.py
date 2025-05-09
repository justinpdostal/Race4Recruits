# SarsaAgent.py
import numpy as np
import random
from collections import deque
import matplotlib.pyplot as plt
from multiprocessing import Pool

class SarsaAgent:
    def __init__(self, conference, alpha=0.2, gamma=0.95, epsilon=0.3):
        """
        Advanced SARSA agent for collegiate swimming recruitment optimization.
        
        Args:
            conference: Conference object containing teams and recruits
            alpha: Initial learning rate (0.1-0.3 recommended)
            gamma: Discount factor (0.9-0.99 recommended)
            epsilon: Initial exploration rate (0.1-0.3 recommended)
        """
        self.conference = conference
        self.initial_alpha = alpha
        self.initial_epsilon = epsilon
        self.gamma = gamma
        self.q_values = {}
        self.actions = [0, 10, 20, 30, 40, 50]  # Scholarship amounts in $10k
        # Experience replay
        self.replay_buffer = deque(maxlen=1000)
        self.batch_size = 32
        
        # Learning tracking
        self.training_year = 0
        self.learning_stats = {
            'years': [],
            'scores': [],
            'budgets': {team.name: [] for team in conference.teams},
            'rosters': {team.name: [] for team in conference.teams}
        }

    def get_state_key(self, team, swimmer):
        """Enhanced 9-dimensional state representation"""
        return (
            min(team.budget // 10, 10),               # Budget tier
            min(swimmer.scholarship // 10, 5),        # Scholarship ask
            min(max(team.popularity // 10, 0), 10),   # Popularity
            min(max(swimmer.team_fit + 5, 0), 10),    # Team fit
            min(len(team.roster) // 2, 10),          # Roster size
            min((team.conference_scores[-1]//100) if team.conference_scores else 0, 10),  # Performance
            sum(1 for e in swimmer.event_placements.values() if e is not None),  # Scoring events
            min(sum(s.get_score_contribution() for s,_ in team.roster)//50, 20),  # Team strength
            swimmer.years_remaining                   # Eligibility years
        )

    def calculate_reward(self, team, swimmer, action, year_results=None):
        """Enhanced reward calculation that considers:
        - Immediate swimmer contribution
        - Budget management
        - End-of-year conference performance
        """
        if action == 0:
            return 0  # No reward for not bidding
        
        # 1. Base reward from swimmer's projected contribution
        base_reward = swimmer.get_score_contribution() * 2  # Increased weight
        
        # 2. Scholarship cost penalty (normalized by team budget)
        cost_penalty = (action / (team.budget + 1)) * 20  # Scale penalty
        
        # 3. Budget reserve penalty (discourage overspending)
        reserve_penalty = max(0, (action - team.budget*0.7) * 0.8)
        # 3. Class balance reward (NEW)
        class_counts = {1:0, 2:0, 3:0, 4:0}
        for s, _ in team.roster:
            class_counts[s.years_remaining] += 1
        
        # Calculate ideal distribution (25% per class)
        target = len(team.roster) / 4
        balance_score = 0
        for year, count in class_counts.items():
            balance_score -= abs(count - target)  # Penalize deviations from ideal
        
        # Add swimmer's year to the calculation
        new_count = class_counts.get(swimmer.years_remaining, 0) + 1
        new_balance_score = balance_score + abs(class_counts[swimmer.years_remaining] - target) - abs(new_count - target)
        balance_reward = new_balance_score * 4  # Weight for class balance
        
        # 4. End-of-year performance bonus (if results are available)
        performance_bonus = 0
        if year_results:
            team_rank = next((i for i, (name, _) in enumerate(year_results) if name == team.name), len(year_results))
            # Rank-based bonus (1st place gets 30, 2nd gets 20, etc.)
            performance_bonus = max(0, (len(year_results) - team_rank)) * 10
        
        # 5. Team fit bonus
        fit_bonus = swimmer.team_fit * 2
        
        total_reward = (base_reward - cost_penalty - reserve_penalty + 
                       performance_bonus + fit_bonus + balance_reward)
        
        return total_reward

    def choose_action(self, state, team, swimmer):
        """Budget-constrained ε-greedy policy"""

    
        if np.random.random() < self.epsilon:
            affordable = [a for a in self.actions if a <= team.budget]
            return random.choice(affordable) if affordable else 0
        
        if state not in self.q_values:
            self.q_values[state] = {a: 0 for a in self.actions}
            
        affordable_q = {a: q for a, q in self.q_values[state].items() 
                       if a <= team.budget}
        
        if not affordable_q:
            return 0
        
        if team.name == "Max Team":
            return max(self.actions) 
        
        if team.name == "Random Team":
            return random.choice(self.actions)
            
        max_q = max(affordable_q.values())
        best_actions = [a for a, q in affordable_q.items() if q == max_q]
        return random.choice(best_actions)

    def update_q_values(self, state, action, reward, next_state, next_action):
        """Experience replay enhanced SARSA update"""
        self.replay_buffer.append((state, action, reward, next_state, next_action))
        
        if len(self.replay_buffer) >= self.batch_size:
            batch = random.sample(self.replay_buffer, self.batch_size)
            
            for s, a, r, ns, na in batch:
                if s not in self.q_values:
                    self.q_values[s] = {act: 0 for act in self.actions}
                if ns not in self.q_values:
                    self.q_values[ns] = {act: 0 for act in self.actions}
                
                current_q = self.q_values[s][a]
                next_q = self.q_values[ns][na]
                td_target = r + self.gamma * next_q
                self.q_values[s][a] += self.alpha * (td_target - current_q)

    def decay_parameters(self):
        """Gradual reduction of exploration/learning rates"""
        self.training_year += 1
        self.epsilon = self.initial_epsilon * (0.99 ** self.training_year)
        self.alpha = self.initial_alpha * (0.995 ** self.training_year)

    def train(self, num_years=10):
        """Enhanced training loop with end-of-year rewards"""
        for year in range(num_years):
            self.decay_parameters()
            
            # Store bids made this year to apply end-of-year rewards
            year_bids = {team.name: [] for team in self.conference.teams}
            
            # Simulate bidding
            recruits = self.conference.recruit_pool.get_recruits().copy()
            random.shuffle(recruits)
            
            for swimmer in recruits:
                for team in self.conference.teams:
                    if team.budget <= 0:
                        continue
                        
                    state = self.get_state_key(team, swimmer)
                    action = self.choose_action(state, team, swimmer)
                    
                    if action >= swimmer.scholarship and team.budget >= action:
                        if team.make_bid(swimmer, action):
                            self.conference.recruit_pool.remove_recruit(swimmer)
                            year_bids[team.name].append((state, action, swimmer))
                            break
                    
                    # Calculate immediate reward (without performance bonus)
                    reward = self.calculate_reward(team, swimmer, action)
                    next_state = self.get_state_key(team, swimmer)
                    next_action = self.choose_action(next_state, team, swimmer)
                    self.update_q_values(state, action, reward, next_state, next_action)
            
            # Conference meet and get results
            results = self.conference.simulate_conference_meet()
            
            # Apply end-of-year rewards for successful bids
            for team in self.conference.teams:
                for state, action, swimmer in year_bids[team.name]:
                    # Recalculate reward with performance results
                    full_reward = self.calculate_reward(team, swimmer, action, results)
                    # Use the same next_state/action as original bid
                    next_state = self.get_state_key(team, swimmer)
                    next_action = self.choose_action(next_state, team, swimmer)
                    self.update_q_values(state, action, full_reward, next_state, next_action)
            
            self.conference.advance_year()
            self.track_progress(year + 1, results)
            self.print_progress(year + 1, results, num_years)


    def track_progress(self, year, results):
        """Record detailed training metrics"""
        self.learning_stats['years'].append(year)
    
        # Convert scores to dict to preserve team associations
        score_dict = {team: score for team, score in results}
        self.learning_stats['scores'].append(score_dict)

        for team in self.conference.teams:
            self.learning_stats['budgets'][team.name].append(team.budget)
            self.learning_stats['rosters'][team.name].append(len(team.roster))

    def print_progress(self, year, results, total_years):
        """report"""
        if year % 10 == 0 or year == 1 or year == total_years or year >0:
            print(f"\nYear {year}/{total_years}")
            print("Standings:", [f"{team}:{score}" for team, score in results])
            print("Roster Sizes:",)
            print(f"ε: {self.epsilon:.3f} α: {self.alpha:.3f}")
            print("Roster Size:", {team.name: len(team.roster) for team in self.conference.teams})
            

    def plot_learning(self):
        """Comprehensive learning visualization"""
        if not plt:
            return
            
        plt.figure(figsize=(15, 10))
        
        # Scores subplot
        plt.subplot(2, 2, 1)
        for team in self.conference.teams:
            scores = [score_dict[team.name] for score_dict in self.learning_stats['scores']]
            plt.plot(self.learning_stats['years'], scores, label=team.name)
        plt.title("Team Scores Over Time")
        plt.xlabel("Year")
        plt.ylabel("Conference Points")
        plt.legend()
        
        # Budgets subplot
        plt.subplot(2, 2, 2)
        for team in self.conference.teams:
            plt.plot(self.learning_stats['years'], 
                    self.learning_stats['budgets'][team.name],
                    label=team.name)
        plt.title("Team Budgets Over Time")
        plt.xlabel("Year")
        plt.ylabel("Budget ($10k)")
        plt.legend()
        
        # Rosters subplot
        plt.subplot(2, 2, 3)
        for team in self.conference.teams:
            plt.plot(self.learning_stats['years'],
                    self.learning_stats['rosters'][team.name],
                    label=team.name)
        plt.title("Roster Sizes Over Time")
        plt.xlabel("Year")
        plt.ylabel("Swimmers")
        plt.legend()
        
        
        # Add final winner annotation
        final_scores = self.learning_stats['scores'][-1]  # A dict of {team_name: score}
        winner_name = max(final_scores, key=final_scores.get)
        winner_score = final_scores[winner_name]
        plt.subplot(2, 2, 1)
        plt.annotate(f"Winner: {winner_name}",
             xy=(self.learning_stats['years'][-1], winner_score),
             xytext=(-120, 30),
             textcoords='offset points',
             arrowprops=dict(arrowstyle="->", lw=1.5),
             fontsize=12, color='green', fontweight='bold')

        
        
        plt.tight_layout()
        plt.show()