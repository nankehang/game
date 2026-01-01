"""
Block class and block-related functionality
"""

from constants import BLOCK_HARDNESS, BLOCK_COLORS

class Block:
    """Represents a single block in the world"""
    
    def __init__(self, block_type='air', x=0, y=0):
        self.type = block_type
        self.x = x  # Grid position
        self.y = y  # Grid position
        self.hardness = BLOCK_HARDNESS.get(block_type, 1.0)
        self.health = 100.0
        self.max_health = 100.0
        
    def is_solid(self):
        """Check if block prevents movement"""
        return self.type not in ['air', 'water', 'lava']
    
    def is_mineable(self):
        """Check if block can be mined"""
        return self.type != 'air' and self.hardness < float('inf')
    
    def is_liquid(self):
        """Check if block is liquid"""
        return self.type in ['water', 'lava']
    
    def damage(self, amount):
        """
        Apply damage to block
        Returns True if block is destroyed
        """
        if not self.is_mineable():
            return False
        
        # Apply damage scaled by hardness
        actual_damage = amount / self.hardness
        self.health -= actual_damage
        
        if self.health <= 0:
            return True
        return False
    
    def reset_health(self):
        """Reset block health to maximum"""
        self.health = self.max_health
    
    def get_color(self):
        """Get base color for this block type"""
        return BLOCK_COLORS.get(self.type, (255, 0, 255))  # Magenta for unknown
    
    def is_ore(self):
        """Check if block is an ore"""
        return self.type in ['coal', 'iron', 'gold', 'diamond', 'mythic_ore']
    
    def __repr__(self):
        return f"Block({self.type}, hp={self.health:.1f})"
