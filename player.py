"""
Player class with movement, mining, and animations
"""

import pygame
from constants import *

class Player:
    """Player character with mining abilities"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        
        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        
        # Mining
        self.is_mining = False
        self.mining_damage_accumulator = 0
        
        # Animation
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.animation_timer = 0
        self.facing_right = True
        
        # Generate player texture
        self.textures = self._generate_textures()
        
    def _generate_textures(self):
        """Generate pixel art textures for player"""
        textures = {}
        
        # Idle texture
        idle = pygame.Surface((32, 32))
        idle.set_colorkey((0, 0, 0))
        self._draw_player_idle(idle)
        textures['idle'] = idle
        
        # Mining texture
        mining = pygame.Surface((32, 32))
        mining.set_colorkey((0, 0, 0))
        self._draw_player_mining(mining)
        textures['mining'] = mining
        
        # Falling texture
        falling = pygame.Surface((32, 32))
        falling.set_colorkey((0, 0, 0))
        self._draw_player_falling(falling)
        textures['falling'] = falling
        
        return textures
    
    def _draw_player_idle(self, surface):
        """Draw idle player sprite"""
        # Body (blue shirt)
        for y in range(12, 24):
            for x in range(10, 22):
                surface.set_at((x, y), (0, 100, 200))
        
        # Head (skin tone)
        for y in range(4, 12):
            for x in range(10, 22):
                surface.set_at((x, y), (255, 220, 177))
        
        # Legs (brown pants)
        for y in range(24, 32):
            for x in range(12, 20):
                surface.set_at((x, y), (101, 67, 33))
        
        # Eyes
        surface.set_at((13, 8), (0, 0, 0))
        surface.set_at((18, 8), (0, 0, 0))
        
        # Pickaxe
        for i in range(5):
            surface.set_at((24 + i, 14 + i), (150, 150, 150))
    
    def _draw_player_mining(self, surface):
        """Draw mining player sprite"""
        self._draw_player_idle(surface)
        # Move pickaxe down
        for i in range(5):
            surface.set_at((24 + i, 18 + i), (150, 150, 150))
    
    def _draw_player_falling(self, surface):
        """Draw falling player sprite"""
        self._draw_player_idle(surface)
        # Arms up
        surface.set_at((8, 14), (255, 220, 177))
        surface.set_at((23, 14), (255, 220, 177))
    
    def move_left(self):
        """Move player left"""
        self.velocity_x = -PLAYER_SPEED
        self.facing_right = False
    
    def move_right(self):
        """Move player right"""
        self.velocity_x = PLAYER_SPEED
        self.facing_right = True
    
    def update(self, dt, world):
        """Update player state"""
        # Apply gravity
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Apply friction
        self.velocity_x *= 0.8
        
        # Check collisions
        self._check_collisions(world)
        
        # Auto-mining below player
        if self.on_ground:
            self._auto_mine(dt, world)
        
        # Update animation
        self._update_animation(dt)
        
        # Bounds check
        if self.x < 0:
            self.x = 0
        if self.x > world.width * BLOCK_SIZE:
            self.x = world.width * BLOCK_SIZE
    
    def _check_collisions(self, world):
        """Check and resolve collisions with blocks"""
        self.on_ground = False
        
        # Get player grid bounds
        left = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.width) // BLOCK_SIZE)
        top = int(self.y // BLOCK_SIZE)
        bottom = int((self.y + self.height) // BLOCK_SIZE)
        
        # Check surrounding blocks
        for by in range(max(0, top - 1), min(world.height, bottom + 2)):
            for bx in range(max(0, left - 1), min(world.width, right + 2)):
                block = world.get_block(bx, by)
                
                if block and block.is_solid():
                    block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, 
                                            BLOCK_SIZE, BLOCK_SIZE)
                    player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    
                    if player_rect.colliderect(block_rect):
                        # Resolve collision
                        overlap_x = min(player_rect.right - block_rect.left,
                                       block_rect.right - player_rect.left)
                        overlap_y = min(player_rect.bottom - block_rect.top,
                                       block_rect.bottom - player_rect.top)
                        
                        if overlap_x < overlap_y:
                            # Push horizontally
                            if player_rect.centerx < block_rect.centerx:
                                self.x -= overlap_x
                            else:
                                self.x += overlap_x
                            self.velocity_x = 0
                        else:
                            # Push vertically
                            if player_rect.centery < block_rect.centery:
                                self.y -= overlap_y
                                self.velocity_y = 0
                                self.on_ground = True
                            else:
                                self.y += overlap_y
                                self.velocity_y = 0
    
    def _auto_mine(self, dt, world):
        """Automatically mine blocks directly below player"""
        # Get blocks below player feet
        left_foot = int((self.x + 4) // BLOCK_SIZE)
        right_foot = int((self.x + self.width - 4) // BLOCK_SIZE)
        foot_y = int((self.y + self.height + 1) // BLOCK_SIZE)
        
        self.is_mining = False
        
        # Try to mine blocks below
        for bx in [left_foot, right_foot]:
            block = world.get_block(bx, foot_y)
            if block and block.is_mineable():
                self.is_mining = True
                damage = AUTO_DIG_DAMAGE * dt
                if world.mine_block_at(bx, foot_y, damage):
                    # Block was destroyed
                    pass
    
    def _update_animation(self, dt):
        """Update animation state"""
        if not self.on_ground:
            self.animation_state = 'falling'
        elif self.is_mining:
            self.animation_state = 'mining'
        else:
            self.animation_state = 'idle'
        
        # Update animation timer
        self.animation_timer += dt
        if self.animation_timer > 0.2:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2
    
    def get_texture(self):
        """Get current animation texture"""
        return self.textures.get(self.animation_state, self.textures['idle'])
    
    def get_grid_position(self):
        """Get player position in grid coordinates"""
        return (int(self.x // BLOCK_SIZE), int(self.y // BLOCK_SIZE))
