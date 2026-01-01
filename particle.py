"""
Particle system for visual effects
"""

import random
from constants import GRAVITY

class Particle:
    """Individual particle for debris effects"""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        
        # Random velocity
        self.velocity_x = random.uniform(-100, 100)
        self.velocity_y = random.uniform(-150, -50)
        
        # Lifetime
        self.lifetime = random.uniform(0.5, 1.5)
        self.max_lifetime = self.lifetime
        
        # Size
        self.size = random.randint(2, 4)
    
    def update(self, dt):
        """Update particle position"""
        # Apply gravity
        self.velocity_y += GRAVITY * dt * 0.5  # Half gravity for particles
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Update lifetime
        self.lifetime -= dt
        
        # Apply drag
        self.velocity_x *= 0.98
        self.velocity_y *= 0.98
    
    def is_dead(self):
        """Check if particle should be removed"""
        return self.lifetime <= 0
    
    def get_alpha(self):
        """Get alpha value based on lifetime"""
        return int(255 * (self.lifetime / self.max_lifetime))
