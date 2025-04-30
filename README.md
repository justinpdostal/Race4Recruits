# Race4Recruits, Project by Justin Dostal

Milestone #1
Natural Language Description
The state space represents all possible configurations of the collegiate swimming conference during the simulation. It captures:

Team States: Each team's budget, roster composition, and historical performance

Swimmer Attributes: Individual performance times, eligibility status, and development potential

Conference Context: Current year, meet results, and relative team strengths

Recruiting Pool: Available recruits and their characteristics

Competitive Landscape: Other teams' rosters and strategies

The system evolves annually through recruiting cycles and championship meets, with stochastic elements in swimmer development and recruiting outcomes.




Race4Recruits

State (S) Components:
1. Teams (T) - 4 teams (reduced from 8)
   • Each team state (Tᵢ) = (bᵢ, Pᵢ, Hᵢ, τᵢ)
   • Budget (bᵢ): [0-100] discretized to 10 levels
   • Popularity (Pᵢ): [0-100] discretized to 10 levels
   • History (Hᵢ): Last 3 years' placements
   • Roster (τᵢ): Max 20 swimmers (reduced attributes)

2. Recruit Pool (R): 
   • Size = 50 swimmers (reduced from 100)
   • Each swimmer = (E, t, c, f) git 
     - E: 3 events from 13 types
     - t: Times discretized to 5 levels per event
     - c: Scholarship [0,10,20,30,40,50]
     - f: Team fit [-5 to 5]

3. Conference History (C): 
   • Stores last 5 years' results
   • Each result = ordered list of (team, score) pairs

4. Year (Y): 
   • Current simulation year [1-100]

State Space Size Calculation:
• Teams: 4 × (10 budget × 10 popularity × 4³ history × 20 roster slots)
• Recruits: 50 × (C(13,3) events × 5 time levels × 6 scholarships × 11 fits)
• History: 5 × (4! permutations × 100 score levels)
• Total states: ~10^18 (manageable vs original 10^6900)

Action Space (A):
• offer_scholarship(s, a): 
  - s ∈ [1-50 recruits]
  - a ∈ [0,10,20,30,40,50]
• pass: No action
• rescind_offer: Cancel previous bid

Transition Dynamics (δ):
1. Recruiting:
   • Success if bid ≥ swimmer's request
   • Budget: bᵢ -= a
   • Popularity: Pᵢ += Δ based on recruit quality

2. Aging:
   • ∀s ∈ τᵢ: e -= 1
   • Remove if e = 0

3. Development:
   • Times improve by p% annually (p ∈ [0.8,1.2])
   • Injury risk: 5% chance per swimmer

Observations (O):
1. Visible (V):
   • All swimmer times and events
   • Team budgets and popularity
   • Previous meet results

2. Hidden (H):
   • Swimmer potential (p)
   • Injury risk (r)
   • True team fit (f)

 





