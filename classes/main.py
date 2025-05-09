try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except ImportError:
    print("Warning: matplotlib not installed. Graphs will not be displayed.")
    print("Install it with: pip install matplotlib")
    matplotlib_available = False

from conference import Conference
from SarsaAgent import SarsaAgent

def run_simulation(num_years=1000):
    """Enhanced simulation with detailed tracking"""
    team_names = ["Team A", "Team B", "Team C", "Team D"]
    initial_budgets = [200, 200, 200, 200]  # $10k units
    
    conference = Conference(team_names, initial_budgets)
    agent = SarsaAgent(conference, alpha=0.2, gamma=0.95, epsilon=0.3)
    
    #print(f"Starting {num_years} year simulation...")
    agent.train(num_years=num_years)
    
    if matplotlib_available:
       agent.plot_learning()
    
    
    return conference, agent


if __name__ == "__main__":
    num_years = 50
    conference, agent = run_simulation(num_years)
    #print_results(conference)
    #plot_results(conference, agent)