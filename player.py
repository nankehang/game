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
        self.width = 26  # Hitbox smaller than sprite (32x32)
        self.height = 28
        
        # Game reference (for statistics)
        self.game = None
        
        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        
        # Acceleration-based movement
        self.max_speed_x = 180  # Max horizontal speed
        self.acceleration = 1200  # Acceleration rate
        self.deceleration = 1600  # Deceleration rate
        self.move_direction = 0  # -1 = left, 0 = none, 1 = right
        
        # Jump state for variable jump
        self.is_jumping = False
        self.jump_released = False
        
        # Mining
        self.is_mining = False
        self.mining_damage_accumulator = 0
        
        # Animation
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.animation_timer = 0
        self.facing_right = True
        
        # Knockback timer
        self.knockback_timer = 0
        self.knockback_spin_angle = 0  # For spin animation
        self.knockback_resistance = 0  # Temporary resistance after being hit
        self.hurt_state = False
        self.hurt_timer = 0
        self.control_locked = False
        
        # Squash and stretch
        self.squash_timer = 0
        self.stretch_amount = 0
        
        # Ground state buffer (prevent flickering)
        self.ground_timer = 0
        self.was_on_ground = False
        
        # Death/respawn flag
        self.fell_to_bedrock = False
        
        # Mining level system
        self.mining_level = 0
        self.mining_speed_bonus = 0.0  # Percentage bonus (0.0 to 2.0 = 0% to 200%)
        self.level_up_flash = 0  # Visual feedback timer
        
        # Health system
        self.max_hp = 3
        self.current_hp = 3
        self.hp_regen_timer = 0
        self.hp_regen_delay = 5.0  # Regen after 5 seconds without damage
        self.last_damage_time = 0
        self.death_flash = 0
        
        # TNT upgrade system
        self.tnt_power_level = 0  # Each level increases TNT damage/radius
        self.tnt_power_bonus = 0.0  # Percentage bonus (10% per level)
        
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
        
        # Jumping texture (stretched upward)
        jumping = pygame.Surface((32, 40))  # Taller for stretch
        jumping.set_colorkey((0, 0, 0))
        self._draw_player_jumping(jumping)
        textures['jumping'] = jumping
        
        # Landing squash texture
        landing = pygame.Surface((32, 28))  # Shorter for squash
        landing.set_colorkey((0, 0, 0))
        self._draw_player_landing(landing)
        textures['landing'] = landing
        
        # Knockback spin frames (4 frames for 360° rotation)
        for i in range(4):
            spin = pygame.Surface((40, 40))  # Larger for rotation
            spin.set_colorkey((0, 0, 0))
            self._draw_player_spin(spin, i * 90)
            textures[f'spin_{i}'] = spin
        
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
    
    def _draw_player_jumping(self, surface):
        """Draw stretched jumping pose"""
        # Head (slightly stretched)
        for y in range(3, 9):
            for x in range(12, 20):
                surface.set_at((x, y), (255, 220, 177))
        
        # Hair (dark brown)
        for y in range(3, 6):
            for x in range(12, 20):
                surface.set_at((x, y), (101, 67, 33))
        
        # Eyes (determined)
        surface.set_at((14, 6), (0, 0, 0))
        surface.set_at((17, 6), (0, 0, 0))
        
        # Body (stretched - blue shirt)
        for y in range(9, 20):  # Taller body
            for x in range(12, 20):
                surface.set_at((x, y), (50, 100, 200))
        
        # Arms reaching up
        # Left arm (up)
        for y in range(7, 11):
            for x in range(9, 12):
                surface.set_at((x, y), (255, 220, 177))
        # Right arm (up)
        for y in range(7, 11):
            for x in range(20, 23):
                surface.set_at((x, y), (255, 220, 177))
        
        # Legs (compressed together)
        for y in range(20, 35):
            for x in range(13, 19):
                surface.set_at((x, y), (40, 60, 100))
        
        # Shoes (together)
        for y in range(35, 38):
            for x in range(13, 19):
                surface.set_at((x, y), (101, 67, 33))
    
    def _draw_player_landing(self, surface):
        """Draw squashed landing pose"""
        # Head (squashed wider)
        for y in range(2, 7):
            for x in range(10, 22):  # Wider
                surface.set_at((x, y), (255, 220, 177))
        
        # Hair
        for y in range(2, 4):
            for x in range(10, 22):
                surface.set_at((x, y), (101, 67, 33))
        
        # Eyes (wide)
        surface.set_at((13, 5), (0, 0, 0))
        surface.set_at((18, 5), (0, 0, 0))
        
        # Body (squashed - very short and wide)
        for y in range(7, 14):  # Short body
            for x in range(10, 22):  # Wide body
                surface.set_at((x, y), (50, 100, 200))
        
        # Arms spread out
        # Left arm
        for y in range(9, 12):
            for x in range(6, 10):
                surface.set_at((x, y), (255, 220, 177))
        # Right arm
        for y in range(9, 12):
            for x in range(22, 26):
                surface.set_at((x, y), (255, 220, 177))
        
        # Legs (wide stance, short)
        for y in range(14, 22):
            for x in range(10, 14):
                surface.set_at((x, y), (40, 60, 100))
        for y in range(14, 22):
            for x in range(18, 22):
                surface.set_at((x, y), (40, 60, 100))
        
        # Shoes (wide)
        for y in range(22, 26):
            for x in range(9, 15):
                surface.set_at((x, y), (101, 67, 33))
        for y in range(22, 26):
            for x in range(17, 23):
                surface.set_at((x, y), (101, 67, 33))
    
    def _draw_player_spin(self, surface, angle):
        """Draw spinning knockback pose at given angle"""
        # Draw simplified sprite rotated
        # Create temp surface with character
        temp = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Simple blocky character for spin
        # Head
        for y in range(6, 12):
            for x in range(13, 19):
                temp.set_at((x, y), (255, 220, 177))
        
        # Hair
        for y in range(6, 8):
            for x in range(13, 19):
                temp.set_at((x, y), (101, 67, 33))
        
        # Eyes
        temp.set_at((14, 9), (0, 0, 0))
        temp.set_at((17, 9), (0, 0, 0))
        
        # Body (tucked)
        for y in range(12, 20):
            for x in range(13, 19):
                temp.set_at((x, y), (50, 100, 200))
        
        # Arms crossed
        for y in range(13, 18):
            for x in range(10, 13):
                temp.set_at((x, y), (255, 220, 177))
        for y in range(13, 18):
            for x in range(19, 22):
                temp.set_at((x, y), (255, 220, 177))
        
        # Legs curled
        for y in range(20, 26):
            for x in range(14, 18):
                temp.set_at((x, y), (40, 60, 100))
        
        # Rotate the sprite
        rotated = pygame.transform.rotate(temp, angle)
        
        # Blit to center of surface
        rect = rotated.get_rect(center=(20, 20))
        surface.blit(rotated, rect)
    
    def move_left(self):
        """Move player left"""
        if not self.control_locked:
            self.move_direction = -1
            self.facing_right = False
    
    def move_right(self):
        """Move player right"""
        if not self.control_locked:
            self.move_direction = 1
            self.facing_right = True
    
    def jump(self):
        """Make player jump"""
        # Use buffered ground state (coyote time) for more responsive jumping
        if not self.control_locked and self.was_on_ground and not self.is_jumping:
            self.velocity_y = -400  # Jump force
            self.was_on_ground = False  # Prevent double jump
            self.is_jumping = True
            self.jump_released = False
            print("[PLAYER] Jump!")
    
    def release_jump(self):
        """Called when jump button is released (for variable jump height)"""
        self.jump_released = True
    
    def update(self, dt, world):
        """Update player state"""
        # Apply acceleration-based horizontal movement
        if self.move_direction != 0:
            # Accelerate in move direction
            self.velocity_x += self.move_direction * self.acceleration * dt
            # Clamp to max speed
            if abs(self.velocity_x) > self.max_speed_x:
                self.velocity_x = self.move_direction * self.max_speed_x
        else:
            # Decelerate when no input
            if abs(self.velocity_x) > 0:
                decel = self.deceleration * dt
                if abs(self.velocity_x) <= decel:
                    self.velocity_x = 0
                else:
                    self.velocity_x -= decel if self.velocity_x > 0 else -decel
        
        # Reset move direction (will be set again by move_left/right if held)
        self.move_direction = 0
        
        # Decay knockback resistance over time
        if self.knockback_resistance > 0:
            self.knockback_resistance -= dt
            if self.knockback_resistance < 0:
                self.knockback_resistance = 0
        
        # Update level up flash effect
        if self.level_up_flash > 0:
            self.level_up_flash -= dt
            if self.level_up_flash < 0:
                self.level_up_flash = 0
        
        # Calculate mining speed bonus from level (10% per level, max 200%)
        old_bonus = self.mining_speed_bonus
        self.mining_speed_bonus = min(2.0, self.mining_level * 0.10)
        if old_bonus != self.mining_speed_bonus:
            print(f"[DEBUG] Mining bonus updated: Level={self.mining_level}, Bonus={self.mining_speed_bonus:.2f} ({int(self.mining_speed_bonus*100)}%)")
        
        # Calculate TNT power bonus (10% per level)
        self.tnt_power_bonus = self.tnt_power_level * 0.10
        
        # HP regeneration (heal 1 HP every 5 seconds if not damaged)
        self.last_damage_time += dt
        if self.last_damage_time >= self.hp_regen_delay and self.current_hp < self.max_hp:
            self.current_hp += 1
            self.last_damage_time = 0
            print(f"[HP] HP Regenerated! Current HP: {self.current_hp}/{self.max_hp}")
        
        # Update death flash
        if self.death_flash > 0:
            self.death_flash -= dt
        
        # Update hurt state
        if self.hurt_timer > 0:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.hurt_state = False
                self.control_locked = False
        
        # Apply gravity
        self.velocity_y += GRAVITY * dt
        
        # Variable jump height - cut jump short if button released early
        if self.is_jumping and self.jump_released and self.velocity_y < 0:
            self.velocity_y *= 0.5  # Cut upward velocity in half
            self.is_jumping = False  # Stop variable jump
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
        
        # Bounds check - prevent falling through world
        if self.x < 0:
            self.x = 0
        if self.x > world.width * BLOCK_SIZE:
            self.x = world.width * BLOCK_SIZE
        
        # Prevent falling below bedrock (death zone)
        bedrock_top = BEDROCK_START * BLOCK_SIZE
        if self.y > bedrock_top:
            # Don't just stop - flag for respawn instead
            self.fell_to_bedrock = True
            self.y = bedrock_top - 10  # Slightly above for detection
            self.velocity_y = 0
    
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
                                self.x -= overlap_x + 0.1  # Add small buffer
                            else:
                                self.x += overlap_x + 0.1
                            self.velocity_x = 0
                        else:
                            # Push vertically
                            if player_rect.centery < block_rect.centery:
                                self.y -= overlap_y + 0.1  # Add small buffer
                                if self.velocity_y >= 0:  # Only set ground if falling down
                                    self.velocity_y = 0
                                    self.on_ground = True
                            else:
                                self.y += overlap_y + 0.1
                                if self.velocity_y <= 0:  # Hit ceiling
                                    self.velocity_y = 0
    
    def _auto_mine(self, dt, world):
        """Automatically mine blocks directly below player"""
        # Get blocks below player feet (including center)
        left_foot = int(self.x // BLOCK_SIZE)
        right_foot = int((self.x + self.width) // BLOCK_SIZE)
        foot_y = int((self.y + self.height + 1) // BLOCK_SIZE)
        
        self.is_mining = False
        
        # Try to mine all blocks below player (from left to right)
        for bx in range(left_foot, right_foot + 1):
            if 0 <= bx < CHUNK_WIDTH:  # Check bounds
                block = world.get_block(bx, foot_y)
                if block and block.is_mineable():
                    self.is_mining = True
                    # Apply mining speed bonus from level
                    speed_multiplier = 1.0 + self.mining_speed_bonus
                    base_damage = AUTO_DIG_DAMAGE * dt
                    damage = base_damage * speed_multiplier
                    if world.mine_block_at(bx, foot_y, damage, self.game):
                        # Block was destroyed
                        print(f"[DEBUG] Block broken! Base dmg={base_damage:.2f}, Multiplier={speed_multiplier:.2f}x, Final={damage:.2f}")
                        pass
    
    def _update_animation(self, dt):
        """Update animation state and frame"""
        # Update knockback timer and spin
        if self.knockback_timer > 0:
            self.knockback_timer -= dt
            # Spin during knockback
            self.knockback_spin_angle += dt * 720  # 2 rotations per second
            if self.knockback_spin_angle >= 360:
                self.knockback_spin_angle -= 360
        
        # Update squash timer (for landing)
        if self.squash_timer > 0:
            self.squash_timer -= dt
        
        # Detect landing (for squash effect)
        if not self.was_on_ground and self.on_ground and abs(self.velocity_y) > 100:
            self.squash_timer = 0.15  # Squash for 150ms
        
        # Update ground state buffer to prevent flickering (coyote time)
        if self.on_ground:
            self.ground_timer = 0.15  # 150ms buffer for better jump feel
            self.was_on_ground = True
            self.is_jumping = False  # Reset jump state on landing
            self.is_jumping = False  # Reset jump state on landing
        else:
            self.ground_timer -= dt
            if self.ground_timer <= 0:
                self.was_on_ground = False
        
        # Store previous state for debug
        prev_state = self.animation_state
        prev_frame = self.animation_frame
        
        # Determine animation state (use buffered ground state)
        if self.knockback_timer > 0:
            # Spinning knockback
            self.animation_state = 'knockback_spin'
            # Determine which spin frame based on angle
            self.animation_frame = int(self.knockback_spin_angle / 90) % 4
        elif self.squash_timer > 0:
            # Landing squash
            self.animation_state = 'landing'
            self.animation_frame = 0
        elif not self.was_on_ground:  # Use buffered ground state
            # Jumping vs Falling (based on velocity direction)
            if self.velocity_y < -100:  # Moving upward (more threshold for smoother transition)
                self.animation_state = 'jumping'
            else:  # Moving downward
                self.animation_state = 'falling'
            self.animation_frame = 0
        elif self.is_mining:
            # Reset frame when entering mining from another state
            if prev_state != 'mining':
                self.animation_frame = 0
                self.animation_timer = 0
            self.animation_state = 'mining'
            # Animate mining (2 frames)
            self.animation_timer += dt
            if self.animation_timer > 0.15:  # Fast mining animation
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
        elif abs(self.velocity_x) > 0.5:  # Moving
            # Reset frame when entering walk from another state
            if prev_state != 'walk':
                self.animation_frame = 0
                self.animation_timer = 0
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
    
    def apply_knockback(self, force_x, force_y, hurt_duration=0.7, damage=1):
        """Apply knockback force to player (e.g., from explosions)"""
        # Play hit sound
        from sound_generator import sound_gen, SOUND_ENABLED
        if SOUND_ENABLED:
            sound_gen.play_player_hit()
        
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
        
        # Take HP damage from explosion (scaled by damage parameter)
        self.current_hp -= damage
        self.last_damage_time = 0  # Reset regen timer
        print(f"[HP] Took {damage} damage! Current HP: {self.current_hp}/{self.max_hp}")
        
        # Check for death
        if self.current_hp <= 0:
            self.current_hp = 0
            self.death_flash = 1.0
            if self.mining_level > 0:
                print(f"[DEATH] Lost all progress - Level {self.mining_level} reset!")
                self.mining_level = 0
                self.mining_speed_bonus = 0.0
                self.tnt_power_level = 0
                self.tnt_power_bonus = 0.0
            # Player will be respawned by game system
    
    def get_texture(self, debug=False):
        """Get current animation texture"""
        texture_key = None
        
        if self.animation_state == 'mining':
            texture_key = f'mining_{self.animation_frame + 1}'
            texture = self.textures[texture_key]
        elif self.animation_state == 'walk':
            texture_key = f'walk_{self.animation_frame + 1}'
            texture = self.textures[texture_key]
        elif self.animation_state == 'jumping':
            texture_key = 'jumping'
            texture = self.textures[texture_key]
        elif self.animation_state == 'falling':
            texture_key = 'falling'
            texture = self.textures[texture_key]
        elif self.animation_state == 'landing':
            texture_key = 'landing'
            texture = self.textures[texture_key]
        elif self.animation_state == 'knockback_spin':
            texture_key = f'spin_{self.animation_frame}'
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
