"""
TNT entity with physics and explosion
"""

import pygame
from sound_generator import sound_gen, SOUND_ENABLED
from constants import *

class TNT:
    """TNT block that falls and explodes"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        
        # Physics
        self.velocity_y = 0
        
        # Explosion
        self.fuse_time = TNT_FUSE_TIME
        self.is_falling = True
        self.last_beep_time = TNT_FUSE_TIME
        
    def update(self, dt, world):
        """Update TNT state"""
        # Update fuse timer
        self.fuse_time -= dt
        
        # Play beep sound every 0.5 seconds
        if SOUND_ENABLED and self.fuse_time < self.last_beep_time - 0.5:
            sound_gen.play_tnt_fuse()
            self.last_beep_time = self.fuse_time
        
        if self.is_falling:
            # Apply gravity
            self.velocity_y += GRAVITY * dt
            if self.velocity_y > TERMINAL_VELOCITY:
                self.velocity_y = TERMINAL_VELOCITY
            
            # Update position
            self.y += self.velocity_y * dt
            
            # Check collision with ground
            grid_x = int(self.x // BLOCK_SIZE)
            grid_y = int((self.y + self.height) // BLOCK_SIZE)
            
            # Check block below
            block_below = world.get_block(grid_x, grid_y)
            if block_below and block_below.is_solid():
                # Land on ground
                self.y = grid_y * BLOCK_SIZE - self.height
                self.velocity_y = 0
                self.is_falling = False
    
    def should_explode(self):
        """Check if TNT should explode"""
        return self.fuse_time <= 0
    
    def get_fuse_ratio(self):
        """Get remaining fuse time as ratio (1.0 to 0.0)"""
        return max(0, self.fuse_time / TNT_FUSE_TIME)
