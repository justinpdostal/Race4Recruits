from swimmer import Swimmer

class RecruitPool:
    EVENT_TYPES = [
        "50 FR", "100 FR", "200 FR", "500 FR", "1650 FR",
        "100 FL", "200 FL", "100 BA", "200 BA", 
        "100 BR", "200 BR", "200 IM", "400 IM"
    ]
    
    def __init__(self, pool_size=100):
        """Initialize a pool of recruits."""
        self.pool = []
        self.generate_pool(pool_size)
    
    def generate_pool(self, size):
        """Generate a pool of random swimmers."""
        self.pool = [Swimmer.generate_random_swimmer(self.EVENT_TYPES) for _ in range(size)]
    
    def get_recruits(self):
        """Get the list of available recruits."""
        return self.pool
    
    def remove_recruit(self, swimmer):
        """Remove a recruit from the pool."""
        if swimmer in self.pool:
            self.pool.remove(swimmer)
    
    def replenish(self, size):
        """Replenish the pool with new recruits."""
        self.generate_pool(size)
    
    def __str__(self):
        return f"Recruit Pool with {len(self.pool)} available swimmers"