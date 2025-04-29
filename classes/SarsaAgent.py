import numpy as np
import random

class SarsaAgent:
    def __init__(self, conference, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.conference = conference
        self.alpha = alpha
        self.gamma = gamma 
        self.epsilon = epsilon
        self.q_values = {}
        self.actions = [0, 10, 20, 30, 40, 50]
    
    def get_state_key(self, team, swimmer):
        """Create a state key based on team and swimmer characteristics."""
        return (
            min(team.budget // 10, 10),  # discretize budget (0-10)
            min(swimmer.scholarship // 10, 5),  # discretize scholarship (0-5)
            min(max(team.popularity // 10, 0), 10),  # discretize popularity (0-10)
            min(max(swimmer.team_fit + 5, 0), 10)  # discretize team_fit (0-10)
        )
    
    def choose_action(self, state, team, swimmer):
        """Choose an action using ε-greedy policy."""
        if np.random.random() < self.epsilon:
            return random.choice(self.actions)
        
        if state not in self.q_values:
            self.q_values[state] = {action: 0 for action in self.actions}
        
        q_values = self.q_values[state]
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)
    
    def update_q_values(self, state, action, reward, next_state, next_action):
        """Update Q-values using SARSA."""
        if state not in self.q_values:
            self.q_values[state] = {a: 0 for a in self.actions}
        if next_state not in self.q_values:
            self.q_values[next_state] = {a: 0 for a in self.actions}
        
        current_q = self.q_values[state][action]
        next_q = self.q_values[next_state][next_action]
        td_target = reward + self.gamma * next_q
        td_error = td_target - current_q
        self.q_values[state][action] += self.alpha * td_error
    
    def train(self, num_years=10):
        """Train the agent over multiple years."""
        for year in range(num_years):
            print(f"\nYear {year + 1}")
            
            # Simulate bidding
            recruits = self.conference.recruit_pool.get_recruits().copy()
            random.shuffle(recruits)
            
            for swimmer in recruits:
                for team in self.conference.teams:
                    if team.budget <= 0:
                        continue
                        
                    state = self.get_state_key(team, swimmer)
                    action = self.choose_action(state, team, swimmer)
                    
                    # Execute action
                    if action > 0 and action >= swimmer.scholarship and team.budget >= action:
                        success = team.make_bid(swimmer, action)
                        if success:
                            self.conference.recruit_pool.remove_recruit(swimmer)
                            break
                    
                    # Calculate reward (handle None placements)
                    try:
                        reward = swimmer.get_score_contribution() - action
                    except TypeError:
                        reward = -action  # If swimmer can't score
                    
                    # Next state and action
                    next_state = self.get_state_key(team, swimmer)
                    next_action = self.choose_action(next_state, team, swimmer)
                    
                    # Update Q-values
                    self.update_q_values(state, action, reward, next_state, next_action)
            
            # Simulate conference and advance year
            results = self.conference.simulate_conference_meet()
            self.conference.advance_year()
            
            # Print yearly results
            print(f"Year {year + 1} results:")
            for i, (team, score) in enumerate(results):
                print(f"  {i+1}. {team}: {score} points")