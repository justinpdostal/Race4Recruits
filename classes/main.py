try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except ImportError:
    print("Warning: matplotlib not installed. Graphs will not be displayed.")
    print("Install it with: pip install matplotlib")
    matplotlib_available = False

from conference import Conference
from SarsaAgent import SarsaAgent

def run_simulation(num_years=10):
    # Initialize conference with 4 teams
    team_names = ["Team A", "Team B", "Team C", "Team D"]
    initial_budgets = [2000, 2000, 2000, 2000]  # Each starts with $100k (in 10k increments)
    
    conference = Conference(team_names, initial_budgets)
    agent = SarsaAgent(conference)
    
    print("Starting simulation...")
    agent.train(num_years=num_years)
    
    return conference

def print_results(conference):
    print("\nHistorical Results:")
    for i, year_results in enumerate(conference.get_historical_results()):
        print(f"Year {i + 1}:")
        for team, score in year_results:
            print(f"  {team}: {score} points")

def plot_results(conference):
    if not matplotlib_available:
        print("Skipping plots due to missing matplotlib")
        return

    # Prepare data for plotting
    years = list(range(1, len(conference.history) + 1))
    team_scores = {team.name: [] for team in conference.teams}
    
    # First ensure all teams are in the dictionary
    all_teams = set(team.name for team in conference.teams)
    
    # Initialize score lists for all teams
    for team_name in all_teams:
        team_scores[team_name] = []
    
    # Populate scores year by year
    for year_result in conference.history:
        # Create a temporary dictionary for this year's results
        year_scores = {team: score for team, score in year_result}
        
        # Append scores for each team
        for team_name in all_teams:
            if team_name in year_scores:
                team_scores[team_name].append(year_scores[team_name])
            else:
                # If team didn't compete this year, use 0 or previous score
                if team_scores[team_name]:
                    team_scores[team_name].append(team_scores[team_name][-1])  # Use last year's score
                else:
                    team_scores[team_name].append(0)  # First year with no score

    # Create figure
    plt.figure(figsize=(15, 5))
    
    # Plot Conference Scores
    plt.subplot(1, 2, 1)
    for team_name in sorted(team_scores.keys()):  # Sort to ensure consistent order
        plt.plot(years, team_scores[team_name], label=team_name, marker='o')
    plt.title('Conference Scores Over Years')
    plt.xlabel('Year')
    plt.ylabel('Conference Points')
    plt.grid(True)
    plt.legend()
    
    # Plot Final Year Standings
    plt.subplot(1, 2, 2)
    final_scores = conference.history[-1]
    team_names_final = [team for team, score in final_scores]
    scores_final = [score for team, score in final_scores]
    colors = ['gold', 'silver', 'peru', 'skyblue']
    plt.bar(team_names_final, scores_final, color=colors)
    plt.title('Final Year Standings')
    plt.ylabel('Conference Points')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    num_years = 100
    conference = run_simulation(num_years)
    print_results(conference)
    plot_results(conference)