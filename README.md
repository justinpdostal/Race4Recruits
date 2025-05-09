# Race4Recruits: AI-Powered Swimming Recruitment Optimization

An intelligent system that uses reinforcement learning to optimize college swimming team recruitment strategies in a competitive environment.

## Table of Contents
- [Problem Overview](#problem-overview)
- [Technical Approach](#technical-approach)
- [State Space](#state-space)
- [Action Space](#action-space)
- [Observations](#observations)
- [Key Features](#key-features)
- [Simulation Parameters](#simulation-parameters)
- [Results Visualization](#results-visualization)
- [Future Enhancements](#future-enhancements)
- [Problems](#problems)

## Problem Overview

College swimming recruitment presents complex challenges:
- Limited scholarship budgets requiring strategic allocation
- Recruits with varying skill levels across 13 swimming events
- Need to balance immediate performance with long-term roster development
- Intense competition from conference rivals
- Dynamic factors like team popularity and swimmer fit

This simulation models these challenges through:
- 4 competing teams with limited budgets
- Annual recruit pools with diverse swimmers
- Multi-year performance tracking
- Conference championship scoring system

## Technical Approach

We implemented a modified SARSA (State-Action-Reward-State-Action) reinforcement learning algorithm with:

### State Representation
9-dimensional state space capturing:
1. Budget tier (0-10)
2. Scholarship ask (0-5)
3. Team popularity (0-10)
4. Swimmer team fit (0-10)
5. Roster size (0-10)
6. Recent performance (0-10)
7. Swimmer's scoring events (count)
8. Team strength (0-20)
9. Eligibility years (1-4)

### Key Algorithm Features
- Budget-constrained action selection
- Experience replay buffer
- Decaying exploration rate
- Multi-factor reward function
- End-of-year performance rewards
- Parallel training capability

## State Space

The state space is a 9-dimensional tuple representing the current situation when making recruitment decisions:

1. **Budget tier** (0-10): Current available budget divided by 10
2. **Scholarship ask** (0-5): Swimmer's requested scholarship divided by 10
3. **Team popularity** (0-10): Team's popularity score divided by 10
4. **Swimmer team fit** (0-10): Swimmer's compatibility with team (from -5 to 5, normalized to 0-10)
5. **Roster size** (0-10): Current number of swimmers on team divided by 2
6. **Recent performance** (0-10): Team's last conference score divided by 100
7. **Scoring events** (count): Number of events the swimmer can score in
8. **Team strength** (0-20): Sum of all swimmers' score contributions divided by 50
9. **Eligibility years** (1-4): Years remaining for the recruit

## Action Space

The action space consists of discrete scholarship amounts that a team can offer:

- Possible actions: [0, 10, 20, 30, 40, 50]
  - 0: No bid (pass on the recruit)
  - 10-50: Scholarship amounts in $10k increments
    - Example: 20 = $20,000 scholarship offer

Actions are constrained by the team's current budget - a team cannot offer more than its available budget.

## Observations

The system observes and tracks several key metrics during the simulation:

1. **Team Performance Metrics**:
   - Annual conference scores
   - Year-over-year ranking changes
   - Performance trends

2. **Financial Metrics**:
   - Budget utilization over time
   - Scholarship allocation patterns
   - Year-end budget balances

3. **Roster Composition**:
   - Number of swimmers per team
   - Class year distribution
   - Event coverage

4. **Recruitment Outcomes**:
   - Bid success rates
   - Scholarship amounts
   - Team preferences

## Key Features

- **Realistic Swimming Simulation**
  - 13 NCAA swimming events with realistic time ranges
  - Championship scoring system (A and B finals)
  - Swimmer graduation and roster turnover

- **Intelligent Bidding System**
  - Dynamic scholarship allocation
  - Team-specific recruitment strategies
  - Budget-aware decision making

- **Comprehensive Tracking**
  - Annual conference results
  - Budget utilization over time
  - Roster composition evolution
  - Team popularity changes

## Simulation Parameters
- **Key adjustable parameters in main.py:**
    - num_years: Number of years to simulate (default: 150)
    - initial_budgets: Starting budgets for each team (default: [500, 500, 500, 500] in $10k units)
    - Key adjustable parameters in SarsaAgent.py:
    - alpha: Learning rate (default: 0.2)
    - gamma: Discount factor (default: 0.95)
    - epsilon: Initial exploration rate (default: 0.3)

## Results Visualization

The system provides three interactive plots to analyze team dynamics over time:

### Team Scores Over Time
- Visualizes total conference points earned each year
- Highlights long-term performance trends and competitiveness

### Team Budgets Over Time
- Tracks scholarship budget usage throughout seasons
- Reveals different financial management strategies across teams

### Roster Sizes Over Time
- Displays how team rosters grow and shrink annually
- Illustrates team-building approaches and class distributions

## Future Enhancements

Planned improvements to the simulation and learning framework include:

### Enhanced Simulation Features
- **Relay Event Scoring**: Add relay events to meet simulations for more realistic scoring.
- **Conference Realignment**: Simulate changes in conference composition over time.
- **Coaching Changes**: Introduce coaching turnover that affects team strategies and swimmer development.
- ** Enhanched Realism**: Ensure all variables are tweaked in order to most closley represent real life swimming.

## Problems
- Teams really love grabbing recruits in waves. I couldn't tweak the logic enough to ensure proper budgeting like in real life. There are safeguards against this but they aren't currently strong enough to require even splitting of recruiting.
- Sarsa logic can be strengthened and improved to ensure smart play is rewarded every time.