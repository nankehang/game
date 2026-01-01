"""
TNT entity with physics and explosion
"""

import pygame
import random
from sound_generator import sound_gen, SOUND_ENABLED
from constants import *

class TNT:
    """TNT block that falls and explodes"""
    
    def __init__(self, x, y, fuse_time=None):
        self.x = x
        self.y = y
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        
        # Physics
        self.velocity_y = 0
        
        # Explosion - random fuse time for variety
        if fuse_time is None:
            self.fuse_time = random.uniform(TNT_MIN_FUSE, TNT_MAX_FUSE)
        else:
            self.fuse_time = fuse_time
        self.total_fuse_time = self.fuse_time  # Store original for flash calculation
        self.is_falling = True
        self.last_beep_time = self.fuse_time
        self.has_landed = False
        
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
                if not self.has_landed:
                    self.has_landed = True
                    print(f"[TNT] Landed! Exploding in {self.fuse_time:.1f}s")
    
    def should_explode(self):
        """Check if TNT should explode"""
        return self.fuse_time <= 0
    
    def get_fuse_ratio(self):
        """Get remaining fuse time as ratio (1.0 to 0.0)"""
        return max(0, self.fuse_time / self.total_fuse_time)
    
    def should_flash(self):
        """Check if TNT should flash red (last 30% of fuse)"""
        return self.get_fuse_ratio() < 0.3
        return max(0, self.fuse_time / self.total_fuse_time)
    
    def should_flash(self):
        """Check if TNT should flash red (last 30% of fuse)"""
        return self.get_fuse_ratio() < 0.3
