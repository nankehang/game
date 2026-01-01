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
        
        # Knockback
        self.knockback_timer = 0
        self.knockback_resistance = 0  # Temporary resistance after being hit
        self.hurt_state = False
        self.hurt_timer = 0
        self.control_locked = False
        
        # Ground state buffer (prevent flickering)
        self.ground_timer = 0
        self.was_on_ground = False
        
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
        
        # Walking animation (2 frames)
        walk1 = pygame.Surface((32, 32))
        walk1.set_colorkey((0, 0, 0))
        self._draw_player_walk(walk1, frame=0)
        textures['walk_1'] = walk1
        
        walk2 = pygame.Surface((32, 32))
        walk2.set_colorkey((0, 0, 0))
        self._draw_player_walk(walk2, frame=1)
        textures['walk_2'] = walk2
        
        # Mining animation (2 frames)
        mining1 = pygame.Surface((32, 32))
        mining1.set_colorkey((0, 0, 0))
        self._draw_player_mining(mining1, frame=0)
        textures['mining_1'] = mining1
        
        mining2 = pygame.Surface((32, 32))
        mining2.set_colorkey((0, 0, 0))
        self._draw_player_mining(mining2, frame=1)
        textures['mining_2'] = mining2
        
        # Knockback texture
        knockback = pygame.Surface((32, 32))
        knockback.set_colorkey((0, 0, 0))
        self._draw_player_knockback(knockback)
        textures['knockback'] = knockback
        
        # Falling texture
        falling = pygame.Surface((32, 32))
        falling.set_colorkey((0, 0, 0))
        self._draw_player_falling(falling)
        textures['falling'] = falling
        
        return textures
    
    def _draw_player_idle(self, surface):
        """Draw idle player sprite - blocky Minecraft-inspired design"""
        # Head (square, beige/tan skin tone)
        for y in range(4, 12):
            for x in range(10, 22):
                surface.set_at((x, y), (255, 220, 177))
        
        # Head outline (darker)
        for x in range(10, 22):
            surface.set_at((x, 4), (200, 170, 130))  # Top
            surface.set_at((x, 11), (200, 170, 130))  # Bottom
        for y in range(4, 12):
            surface.set_at((10, y), (200, 170, 130))  # Left
            surface.set_at((21, y), (200, 170, 130))  # Right
        
        # Eyes (square, dark)
        for y in range(7, 9):
            for x in range(13, 15):
                surface.set_at((x, y), (50, 50, 50))
        for y in range(7, 9):
            for x in range(17, 19):
                surface.set_at((x, y), (50, 50, 50))
        
        # Body (blue shirt)
        for y in range(12, 22):
            for x in range(10, 22):
                surface.set_at((x, y), (60, 120, 220))
        
        # Body outline (darker blue)
        for x in range(10, 22):
            surface.set_at((x, 12), (40, 80, 160))  # Top
            surface.set_at((x, 21), (40, 80, 160))  # Bottom
        for y in range(12, 22):
            surface.set_at((10, y), (40, 80, 160))  # Left
            surface.set_at((21, y), (40, 80, 160))  # Right
        
        # Legs (dark blue pants)
        # Left leg
        for y in range(22, 30):
            for x in range(12, 16):
                surface.set_at((x, y), (40, 60, 100))
        # Right leg
        for y in range(22, 30):
            for x in range(16, 20):
                surface.set_at((x, y), (40, 60, 100))
        
        # Shoes (brown)
        for y in range(30, 32):
            for x in range(12, 16):
                surface.set_at((x, y), (101, 67, 33))
        for y in range(30, 32):
            for x in range(16, 20):
                surface.set_at((x, y), (101, 67, 33))
        
        # Arms (skin tone)
        # Left arm
        for y in range(13, 21):
            for x in range(7, 10):
                surface.set_at((x, y), (255, 220, 177))
        # Right arm (will hold pickaxe)
        for y in range(13, 21):
            for x in range(22, 25):
                surface.set_at((x, y), (255, 220, 177))
        
        # Pickaxe (gray handle, brown grip)
        # Handle
        for i in range(6):
            surface.set_at((25, 15 + i), (101, 67, 33))
        # Pickaxe head (gray)
        surface.set_at((24, 14), (120, 120, 120))
        surface.set_at((25, 14), (150, 150, 150))
        surface.set_at((26, 14), (120, 120, 120))
        surface.set_at((27, 14), (100, 100, 100))
    
    def _draw_player_walk(self, surface, frame):
        """Draw walking animation - alternate leg positions"""
        # Head (square, beige/tan skin tone)
        for y in range(4, 12):
            for x in range(10, 22):
                surface.set_at((x, y), (255, 220, 177))
        
        # Head outline (darker)
        for x in range(10, 22):
            surface.set_at((x, 4), (200, 170, 130))
            surface.set_at((x, 11), (200, 170, 130))
        for y in range(4, 12):
            surface.set_at((10, y), (200, 170, 130))
            surface.set_at((21, y), (200, 170, 130))
        
        # Eyes (square, dark)
        for y in range(7, 9):
            for x in range(13, 15):
                surface.set_at((x, y), (50, 50, 50))
        for y in range(7, 9):
            for x in range(17, 19):
                surface.set_at((x, y), (50, 50, 50))
        
        # Body (blue shirt)
        for y in range(12, 22):
            for x in range(10, 22):
                surface.set_at((x, y), (60, 120, 220))
        
        # Body outline (darker blue)
        for x in range(10, 22):
            surface.set_at((x, 12), (40, 80, 160))
            surface.set_at((x, 21), (40, 80, 160))
        for y in range(12, 22):
            surface.set_at((10, y), (40, 80, 160))
            surface.set_at((21, y), (40, 80, 160))
        
        # Walking arms - slightly swinging
        if frame == 0:
            # Left arm forward
            for y in range(14, 21):
                for x in range(7, 10):
                    surface.set_at((x, y), (255, 220, 177))
            # Right arm back
            for y in range(13, 21):
                for x in range(22, 25):
                    surface.set_at((x, y), (255, 220, 177))
        else:
            # Left arm back
            for y in range(13, 21):
                for x in range(7, 10):
                    surface.set_at((x, y), (255, 220, 177))
            # Right arm forward
            for y in range(14, 21):
                for x in range(22, 25):
                    surface.set_at((x, y), (255, 220, 177))
        
        # Pickaxe (stays in same position)
        for i in range(6):
            surface.set_at((25, 15 + i), (101, 67, 33))
        surface.set_at((24, 14), (120, 120, 120))
        surface.set_at((25, 14), (150, 150, 150))
        surface.set_at((26, 14), (120, 120, 120))
        surface.set_at((27, 14), (100, 100, 100))
        
        # Legs in walking position
        if frame == 0:
            # Left leg forward, right leg back
            for y in range(21, 30):
                for x in range(11, 15):
                    surface.set_at((x, y), (40, 60, 100))
            for y in range(23, 31):
                for x in range(17, 21):
                    surface.set_at((x, y), (40, 60, 100))
            # Shoes
            for y in range(30, 32):
                for x in range(11, 15):
                    surface.set_at((x, y), (101, 67, 33))
            for y in range(30, 32):
                for x in range(17, 21):
                    surface.set_at((x, y), (101, 67, 33))
        else:
            # Right leg forward, left leg back
            for y in range(21, 30):
                for x in range(17, 21):
                    surface.set_at((x, y), (40, 60, 100))
            for y in range(23, 31):
                for x in range(11, 15):
                    surface.set_at((x, y), (40, 60, 100))
            # Shoes
            for y in range(30, 32):
                for x in range(17, 21):
                    surface.set_at((x, y), (101, 67, 33))
            for y in range(30, 32):
                for x in range(11, 15):
                    surface.set_at((x, y), (101, 67, 33))
    
    def _draw_player_mining(self, surface, frame):
        """Draw mining animation - pickaxe swinging"""
        # Head
        for y in range(4, 12):
            for x in range(10, 22):
                surface.set_at((x, y), (255, 220, 177))
        
        # Head outline
        for x in range(10, 22):
            surface.set_at((x, 4), (200, 170, 130))
            surface.set_at((x, 11), (200, 170, 130))
        for y in range(4, 12):
            surface.set_at((10, y), (200, 170, 130))
            surface.set_at((21, y), (200, 170, 130))
        
        # Eyes
        for y in range(7, 9):
            for x in range(13, 15):
                surface.set_at((x, y), (50, 50, 50))
        for y in range(7, 9):
            for x in range(17, 19):
                surface.set_at((x, y), (50, 50, 50))
        
        # Body
        for y in range(12, 22):
            for x in range(10, 22):
                surface.set_at((x, y), (60, 120, 220))
        
        # Body outline
        for x in range(10, 22):
            surface.set_at((x, 12), (40, 80, 160))
            surface.set_at((x, 21), (40, 80, 160))
        for y in range(12, 22):
            surface.set_at((10, y), (40, 80, 160))
            surface.set_at((21, y), (40, 80, 160))
        
        # Legs (standing still)
        for y in range(22, 30):
            for x in range(12, 16):
                surface.set_at((x, y), (40, 60, 100))
        for y in range(22, 30):
            for x in range(16, 20):
                surface.set_at((x, y), (40, 60, 100))
        
        # Shoes
        for y in range(30, 32):
            for x in range(12, 16):
                surface.set_at((x, y), (101, 67, 33))
        for y in range(30, 32):
            for x in range(16, 20):
                surface.set_at((x, y), (101, 67, 33))
        
        # Arms and pickaxe - different position per frame
        if frame == 0:
            # Pickaxe raised - right arm up
            # Left arm
            for y in range(13, 21):
                for x in range(7, 10):
                    surface.set_at((x, y), (255, 220, 177))
            # Right arm raised
            for y in range(10, 16):
                for x in range(22, 25):
                    surface.set_at((x, y), (255, 220, 177))
            # Pickaxe raised
            for i in range(5):
                surface.set_at((26, 11 + i), (101, 67, 33))
            surface.set_at((25, 10), (120, 120, 120))
            surface.set_at((26, 10), (150, 150, 150))
            surface.set_at((27, 10), (120, 120, 120))
            surface.set_at((28, 10), (100, 100, 100))
        else:
            # Pickaxe lowered - right arm down
            # Left arm
            for y in range(13, 21):
                for x in range(7, 10):
                    surface.set_at((x, y), (255, 220, 177))
            # Right arm lowered
            for y in range(15, 22):
                for x in range(22, 25):
                    surface.set_at((x, y), (255, 220, 177))
            # Pickaxe swinging down
            for i in range(6):
                surface.set_at((24, 17 + i), (101, 67, 33))
            surface.set_at((23, 16), (120, 120, 120))
            surface.set_at((24, 16), (150, 150, 150))
            surface.set_at((25, 16), (120, 120, 120))
            surface.set_at((26, 16), (100, 100, 100))
    
    def _draw_player_knockback(self, surface):
        """Draw knockback/hurt sprite - tilted back with arms up"""
        # Head (tilted, same as idle)
        for y in range(5, 13):
            for x in range(9, 21):
                surface.set_at((x, y), (255, 220, 177))
        
        # Head outline
        for x in range(9, 21):
            surface.set_at((x, 5), (200, 170, 130))
            surface.set_at((x, 12), (200, 170, 130))
        for y in range(5, 13):
            surface.set_at((9, y), (200, 170, 130))
            surface.set_at((20, y), (200, 170, 130))
        
        # Eyes (worried expression)
        surface.set_at((12, 8), (50, 50, 50))
        surface.set_at((13, 8), (50, 50, 50))
        surface.set_at((16, 8), (50, 50, 50))
        surface.set_at((17, 8), (50, 50, 50))
        
        # Body (slightly back)
        for y in range(13, 23):
            for x in range(9, 21):
                surface.set_at((x, y), (60, 120, 220))
        
        # Body outline
        for x in range(9, 21):
            surface.set_at((x, 13), (40, 80, 160))
            surface.set_at((x, 22), (40, 80, 160))
        for y in range(13, 23):
            surface.set_at((9, y), (40, 80, 160))
            surface.set_at((20, y), (40, 80, 160))
        
        # Legs (bent)
        for y in range(23, 30):
            for x in range(11, 15):
                surface.set_at((x, y), (40, 60, 100))
        for y in range(23, 30):
            for x in range(15, 19):
                surface.set_at((x, y), (40, 60, 100))
        
        # Shoes
        for y in range(30, 32):
            for x in range(11, 15):
                surface.set_at((x, y), (101, 67, 33))
        for y in range(30, 32):
            for x in range(15, 19):
                surface.set_at((x, y), (101, 67, 33))
        
        # Arms raised (defensive pose)
        # Left arm
        for y in range(10, 14):
            for x in range(6, 9):
                surface.set_at((x, y), (255, 220, 177))
        # Right arm
        for y in range(10, 14):
            for x in range(21, 24):
                surface.set_at((x, y), (255, 220, 177))
        
        # Pickaxe falling/dropped
        surface.set_at((25, 20), (101, 67, 33))
        surface.set_at((26, 20), (150, 150, 150))
    
    def _draw_player_falling(self, surface):
        """Draw falling sprite - arms up, surprised"""
        # Head
        for y in range(4, 12):
            for x in range(10, 22):
                surface.set_at((x, y), (255, 220, 177))
        
        # Head outline
        for x in range(10, 22):
            surface.set_at((x, 4), (200, 170, 130))
            surface.set_at((x, 11), (200, 170, 130))
        for y in range(4, 12):
            surface.set_at((10, y), (200, 170, 130))
            surface.set_at((21, y), (200, 170, 130))
        
        # Eyes (wider, surprised)
        for y in range(7, 10):
            for x in range(12, 15):
                surface.set_at((x, y), (50, 50, 50))
        for y in range(7, 10):
            for x in range(17, 20):
                surface.set_at((x, y), (50, 50, 50))
        
        # Body
        for y in range(12, 22):
            for x in range(10, 22):
                surface.set_at((x, y), (60, 120, 220))
        
        # Body outline
        for x in range(10, 22):
            surface.set_at((x, 12), (40, 80, 160))
            surface.set_at((x, 21), (40, 80, 160))
        for y in range(12, 22):
            surface.set_at((10, y), (40, 80, 160))
            surface.set_at((21, y), (40, 80, 160))
        
        # Legs (straight down)
        for y in range(22, 30):
            for x in range(12, 16):
                surface.set_at((x, y), (40, 60, 100))
        for y in range(22, 30):
            for x in range(16, 20):
                surface.set_at((x, y), (40, 60, 100))
        
        # Shoes
        for y in range(30, 32):
            for x in range(12, 16):
                surface.set_at((x, y), (101, 67, 33))
        for y in range(30, 32):
            for x in range(16, 20):
                surface.set_at((x, y), (101, 67, 33))
        
        # Arms up (flailing)
        # Left arm raised
        for y in range(9, 13):
            for x in range(6, 10):
                surface.set_at((x, y), (255, 220, 177))
        # Right arm raised
        for y in range(9, 13):
            for x in range(22, 26):
                surface.set_at((x, y), (255, 220, 177))
        
        # Pickaxe in hand (holding tight)
        for i in range(4):
            surface.set_at((27, 10 + i), (101, 67, 33))
        surface.set_at((28, 9), (150, 150, 150))
    
    def move_left(self):
        """Move player left"""
        if not self.control_locked:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
    
    def move_right(self):
        """Move player right"""
        if not self.control_locked:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
    
    def update(self, dt, world):
        """Update player state"""
        # Decay knockback resistance over time
        if self.knockback_resistance > 0:
            self.knockback_resistance -= dt
            if self.knockback_resistance < 0:
                self.knockback_resistance = 0
        
        # Update hurt state
        if self.hurt_timer > 0:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.hurt_state = False
                self.control_locked = False
        
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
        """Update animation state and frame"""
        # Update knockback timer
        if self.knockback_timer > 0:
            self.knockback_timer -= dt
        
        # Update ground state buffer to prevent flickering
        if self.on_ground:
            self.ground_timer = 0.1  # 100ms buffer
            self.was_on_ground = True
        else:
            self.ground_timer -= dt
            if self.ground_timer <= 0:
                self.was_on_ground = False
        
        # Store previous state for debug
        prev_state = self.animation_state
        prev_frame = self.animation_frame
        
        # Determine animation state (use buffered ground state)
        if self.knockback_timer > 0:
            self.animation_state = 'knockback'
            self.animation_frame = 0
        elif not self.was_on_ground:  # Use buffered ground state
            self.animation_state = 'falling'
            self.animation_frame = 0  # Falling has only 1 frame
        elif self.is_mining:
            self.animation_state = 'mining'
            # Animate mining (2 frames)
            self.animation_timer += dt
            if self.animation_timer > 0.15:  # Fast mining animation
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
        elif abs(self.velocity_x) > 0.5:  # Moving
            self.animation_state = 'walk'
            # Animate walking (2 frames)
            self.animation_timer += dt
            if self.animation_timer > 0.2:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
        else:
            self.animation_state = 'idle'
            self.animation_frame = 0  # Idle has only 1 frame
        
        # Debug output when state changes (only major state changes, not frame changes)
        if prev_state != self.animation_state:
            print(f"[ANIM] {prev_state} -> {self.animation_state} | Mining:{self.is_mining} Ground:{self.on_ground}/{self.was_on_ground}")
    
    def apply_knockback(self, force_x, force_y, hurt_duration=0.7):
        """Apply knockback force to player (e.g., from explosions)"""
        # Apply resistance (reduces knockback if hit recently)
        resistance_factor = max(0.2, 1.0 - self.knockback_resistance)
        
        self.velocity_x += force_x * resistance_factor
        self.velocity_y += force_y * resistance_factor
        
        # Cap velocity to prevent flying off screen
        max_knockback_velocity = 400
        self.velocity_x = max(-max_knockback_velocity, min(max_knockback_velocity, self.velocity_x))
        self.velocity_y = max(-max_knockback_velocity, min(max_knockback_velocity, self.velocity_y))
        
        # Set knockback animation
        self.knockback_timer = 0.3
        
        # Enter hurt state and lock controls
        self.hurt_state = True
        self.hurt_timer = hurt_duration
        self.control_locked = True
        
        # Add temporary resistance (prevents multiple TNT from launching player)
        self.knockback_resistance = min(0.8, self.knockback_resistance + 0.3)
    
    def get_texture(self, debug=False):
        """Get current animation texture"""
        texture_key = None
        
        if self.animation_state == 'mining':
            texture_key = f'mining_{self.animation_frame + 1}'
            texture = self.textures[texture_key]
        elif self.animation_state == 'walk':
            texture_key = f'walk_{self.animation_frame + 1}'
            texture = self.textures[texture_key]
        elif self.animation_state == 'falling':
            texture_key = 'falling'
            texture = self.textures[texture_key]
        elif self.animation_state == 'knockback':
            texture_key = 'knockback'
            texture = self.textures[texture_key]
        else:  # idle
            texture_key = 'idle'
            texture = self.textures[texture_key]
        
        if debug:
            print(f"[DEBUG] Animation: {self.animation_state}, Frame: {self.animation_frame}, Texture: {texture_key}")
        
        # Don't flip here - let renderer handle it
        return texture
    
    def get_grid_position(self):
        """Get player position in grid coordinates"""
        return (int(self.x // BLOCK_SIZE), int(self.y // BLOCK_SIZE))
