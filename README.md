# Race4Recruits: AI-Powered Swimming Recruitment Optimization


An intelligent system that uses reinforcement learning to optimize college swimming team recruitment strategies in a competitive environment.

## Table of Contents
- [Problem Overview](#problem-overview)
- [Technical Approach](#technical-approach)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Simulation Parameters](#simulation-parameters)
- [Results Visualization](#results-visualization)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Race4Recruits.git
cd Race4Recruits