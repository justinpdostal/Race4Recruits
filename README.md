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




State(S):
S = (T, R, C, Y)
Where:
- T = {T₁, T₂, ..., Tₙ} (Set of all teams)
- R = Recruit pool (Set of available swimmers)
- C = Conference meet results history
- Y = Current year ∈ ℕ

Team State (Tᵢ):
Tᵢ = (bᵢ, Pᵢ, Hᵢ, τᵢ)
Where:
- bᵢ = Budget ∈ ℝ⁺
- Pᵢ = Popularity score ∈ [0,1]
- Hᵢ = Historical placements (List of past results)
- τᵢ = {s₁, s₂, ..., sₖ} (Team roster)

Swimmer State (s):
s = (E, t, e, c, p, r, f)
Where:
- E = Events (Set of event codes)
- t = Times (E → ℝ⁺)
- e = Eligibility years remaining ∈ {0,1,2,3,4}
- c = Scholarship cost ∈ [0,1]
- p = Potential ∈ [0.8,1.2]
- r = Injury risk ∈ [0,0.3]
- f = Team fit ∈ [0,1]

Actions (A):
A = {offer_scholarship(s, a), pass, rescind_offer}
Where:
- s = Swimmer ∈ R
- a = Amount ∈ [0, bᵢ]

Transitions (δ):
δ(S, A) → S'
With:
- Recruiting: Tᵢ.budget -= a if successful offer
- Aging: ∀s ∈ τᵢ, s.e -= 1 (remove if s.e = 0)
- Development: ∀s ∈ τᵢ, tₑ *= (1 - η·p) (η = improvement rate)
- Injuries: Pr(s injured) = r

Observations (O):
O = (V, H, P)
Where:
- V = Visible swimmer attributes (times, events)
- H = Hidden attributes (potential, injury risk)
- P = Partial knowledge of other teams' rosters


This was my first idea, as much as I would like to do this highly complicated version, state space is simply too large, like really too large. So I'm going to reduce the problem size in order to make this feasable. This means loosing realism, but with my current tools I can't exactly deal with the estimated 10^6900 state spaces :(. That's using all 8 teams with ~20 swimmers each.

Next Ideas: 
- Cannot model all 8 Teams, too many interactions.
- Simplify state space.
 


Next Implementation: I really pains me to simplify this state space so much but it must be done. These spaces really do blow up fast.
- 4 Teams, all with the same budget, roster limit of 20 swimmers. Popularity in range {low, med, high}
- 12 Recruits present each year, with a given speciality {Sprint, Stroke Distance}, Team fit score of {0,1,2,3}
- Each swimmer has the same specialty.
- Budget is 100k, with offers in 10k increments.
- Trying to limit states by enumerating values into buckets.
- Reduce potentially nonvaluable variables.
Work in progress...


