"""
Meteor entity - Beautiful falling space rocks
"""
import random
import math
from constants import BLOCK_SIZE

class Meteor:
    """A beautiful falling meteor with glowing trail"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 12
        
        # Slow, graceful fall (chill & beautiful)
        self.velocity_x = random.uniform(-15, -5)  # Very slight diagonal
        self.velocity_y = random.uniform(40, 60)  # Extra slow fall (50% slower)
        
        # Visual properties
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-60, 60)
        self.glow_pulse = random.uniform(0, math.pi * 2)
        
        # Trail particles
        self.trail_particles = []
        self.trail_timer = 0
        
        # Meteor color variation (orange to cyan)
        self.color_type = random.choice(['orange', 'cyan', 'purple', 'yellow'])
        
        # State
        self.alive = True
        self.age = 0
        
    def update(self, dt):
        """Update meteor position and effects"""
        if not self.alive:
            return
            
        self.age += dt
        
        # Apply velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Gentle rotation
        self.rotation += self.rotation_speed * dt
        
        # Glow pulse
        self.glow_pulse += dt * 3
        
        # Create trail particles
        self.trail_timer += dt
        if self.trail_timer > 0.05:  # Every 50ms (less frequent for elegance)
            self.trail_timer = 0
            self._create_trail_particle()
        
        # Update trail particles
        for particle in self.trail_particles[:]:
            particle['life'] -= dt
            particle['y'] += particle['vy'] * dt
            particle['x'] += particle['vx'] * dt
            particle['alpha'] = max(0, particle['life'] / particle['max_life'])
            
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
    
    def _create_trail_particle(self):
        """Create a glowing trail particle"""
        particle = {
            'x': self.x + self.width / 2 + random.uniform(-2, 2),
            'y': self.y + self.height / 2 + random.uniform(-2, 2),
            'vx': random.uniform(-10, 10),
            'vy': random.uniform(-20, 0),  # Float up slightly
            'life': random.uniform(0.6, 1.2),  # Longer life for more trails
            'max_life': 1.2,
            'alpha': 1.0,
            'size': random.uniform(3, 6),  # Bigger particles
            'color': self.color_type
        }
        self.trail_particles.append(particle)
    
    def get_block_pos(self):
        """Get meteor's block position"""
        return (int(self.x // BLOCK_SIZE), int(self.y // BLOCK_SIZE))
    
    def should_impact(self, world):
        """Check if meteor should impact with ground"""
        block_x, block_y = self.get_block_pos()
        
        # Check block below
        below_block = world.get_block(block_x, block_y + 1)
        if below_block and below_block.is_solid():
            return True
            
        # Check if out of bounds (bottom of world)
        if block_y >= world.height - 1:
            return True
            
        return False
    
    def create_impact_particles(self):
        """Create beautiful impact particles"""
        particles = []
        
        # More particles for bigger show
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(30, 80)
            
            particle = {
                'x': self.x + self.width / 2,
                'y': self.y + self.height / 2,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed - 50,  # Bias upward
                'life': random.uniform(0.5, 1.2),
                'max_life': 1.2,
                'alpha': 1.0,
                'size': random.uniform(2, 5),
                'color': self.color_type,
                'glow': True
            }
            particles.append(particle)
        
        return particles
    
    def get_glow_intensity(self):
        """Get current glow intensity (0-1)"""
        return 0.5 + 0.5 * math.sin(self.glow_pulse)
    
    def get_color_rgb(self):
        """Get meteor color as RGB tuple"""
        colors = {
            'orange': (255, 140, 50),
            'cyan': (80, 220, 255),
            'purple': (200, 80, 255),
            'yellow': (255, 240, 80)
        }
        return colors.get(self.color_type, (255, 140, 50))
