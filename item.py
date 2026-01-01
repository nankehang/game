"""
Collectible items (pickaxes, resources, etc.)
"""

import pygame
import math
from constants import BLOCK_SIZE

class Item:
    """Collectible item in world"""
    
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type  # 'wood_pickaxe', 'stone_pickaxe', etc.
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        
        # Physics
        self.velocity_y = 0
        self.on_ground = False
        
        # Enhanced Animation
        self.float_timer = 0
        self.float_offset = 0
        self.rotation = 0
        self.rotation_speed = 45  # degrees per second
        self.glow_pulse = 0
        self.sparkle_timer = 0
        self.sparkles = []
        self.spawn_timer = 0
        self.scale_pulse = 1.0
        
        # Rare items have special effects
        self.is_rare = item_type in ['magnet', 'double_jump', 'speed_boost', 'shield', 'block_breaker', 'crystal', 'rare_ore', 'heart']
        
        # Lifetime - items disappear after 10 seconds
        self.lifetime = 10.0
        self.lifetime_warning = False  # Flash when about to expire
        
        # Generate texture
        self.texture = self._generate_texture()
    
    def _generate_texture(self):
        """Generate pickaxe sprite based on type"""
        surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        
        # Determine colors based on pickaxe type
        glow_color = (255, 255, 255)  # Default glow color
        
        if self.item_type == 'wood_pickaxe':
            handle_color = (139, 90, 43)
            head_color = (101, 67, 33)
            highlight_color = (160, 110, 60)
            has_glow = False
        elif self.item_type == 'stone_pickaxe':
            handle_color = (139, 90, 43)
            head_color = (100, 100, 100)
            highlight_color = (140, 140, 140)
            has_glow = False
        elif self.item_type == 'iron_pickaxe':
            handle_color = (139, 90, 43)
            head_color = (200, 200, 200)
            highlight_color = (240, 240, 240)
            has_glow = True
            glow_color = (200, 220, 255)
        elif self.item_type == 'diamond_pickaxe':
            handle_color = (139, 90, 43)
            head_color = (0, 200, 200)
            highlight_color = (100, 255, 255)
            has_glow = True
            glow_color = (100, 255, 255)
        elif self.item_type == 'crystal':
            # Beautiful cyan crystal
            handle_color = (150, 220, 255)
            head_color = (80, 200, 255)
            highlight_color = (200, 240, 255)
            has_glow = True
            glow_color = (150, 220, 255)
        elif self.item_type == 'rare_ore':
            # Purple rare ore
            handle_color = (180, 100, 220)
            head_color = (140, 60, 200)
            highlight_color = (220, 140, 255)
            has_glow = True
            glow_color = (180, 100, 220)
        # NEW RARE ITEMS FROM TNT
        elif self.item_type == 'magnet':
            # Cyan magnet effect
            handle_color = (0, 255, 255)
            head_color = (0, 200, 255)
            highlight_color = (100, 255, 255)
            has_glow = True
            glow_color = (0, 255, 255)
        elif self.item_type == 'double_jump':
            # Green wings/feather
            handle_color = (0, 255, 0)
            head_color = (0, 200, 0)
            highlight_color = (100, 255, 100)
            has_glow = True
            glow_color = (0, 255, 0)
        elif self.item_type == 'speed_boost':
            # Yellow lightning
            handle_color = (255, 255, 0)
            head_color = (255, 200, 0)
            highlight_color = (255, 255, 100)
            has_glow = True
            glow_color = (255, 255, 0)
        elif self.item_type == 'shield':
            # Blue shield
            handle_color = (0, 128, 255)
            head_color = (0, 100, 200)
            highlight_color = (100, 180, 255)
            has_glow = True
            glow_color = (0, 128, 255)
        elif self.item_type == 'block_breaker':
            # Red explosive
            handle_color = (255, 0, 0)
            head_color = (200, 0, 0)
            highlight_color = (255, 100, 100)
            has_glow = True
            glow_color = (255, 0, 0)
        elif self.item_type == 'heart':
            # Pink/Red heart
            handle_color = (255, 100, 150)
            head_color = (255, 50, 100)
            highlight_color = (255, 150, 200)
            has_glow = True
            glow_color = (255, 100, 150)
        else:  # Default wood
            handle_color = (139, 90, 43)
            head_color = (101, 67, 33)
            highlight_color = (160, 110, 60)
            has_glow = False
        
        # Generate texture based on item type
        if self.item_type in ['crystal', 'rare_ore', 'heart']:
            self._draw_gem(surface, handle_color, head_color, highlight_color, has_glow, glow_color)
        elif self.item_type in ['magnet', 'double_jump', 'speed_boost', 'shield', 'block_breaker']:
            self._draw_rare_item(surface, handle_color, head_color, highlight_color, has_glow, glow_color)
        else:
            self._draw_pickaxe(surface, handle_color, head_color, highlight_color, has_glow, glow_color)
        
        return surface
    
    def _draw_pickaxe(self, surface, handle_color, head_color, highlight_color, has_glow, glow_color):
        """Draw pickaxe item"""
        # Draw at slight angle (more iconic)
        # Handle (diagonal line 3 pixels wide)
        handle_points = [
            (5, 12), (6, 12), (7, 12),
            (6, 11), (7, 11), (8, 11),
            (7, 10), (8, 10), (9, 10),
            (8, 9), (9, 9), (10, 9),
        ]
        for px, py in handle_points:
            if 0 <= px < BLOCK_SIZE and 0 <= py < BLOCK_SIZE:
                surface.set_at((px, py), handle_color)
        
        # Pickaxe head (stone/metal)
        # Left spike
        head_points = [
            (3, 11), (4, 11),
            (2, 12), (3, 12),
            (1, 13), (2, 13),
        ]
        # Right spike
        head_points += [
            (9, 8), (10, 8),
            (10, 9), (11, 9),
            (11, 10), (12, 10),
        ]
        # Center mass
        head_points += [
            (5, 10), (6, 10),
            (6, 9), (7, 9), (8, 9),
            (7, 8),
        ]
        
        for px, py in head_points:
            if 0 <= px < BLOCK_SIZE and 0 <= py < BLOCK_SIZE:
                surface.set_at((px, py), head_color)
        
        # Highlights on head
        highlights = [(4, 11), (7, 8), (10, 9)]
        for px, py in highlights:
            if 0 <= px < BLOCK_SIZE and 0 <= py < BLOCK_SIZE:
                surface.set_at((px, py), highlight_color)
        
        # Add glow for rare items
        if has_glow:
            glow_surface = pygame.Surface((BLOCK_SIZE + 4, BLOCK_SIZE + 4), pygame.SRCALPHA)
            # Draw glowing outline
            for y in range(BLOCK_SIZE):
                for x in range(BLOCK_SIZE):
                    if surface.get_at((x, y))[3] > 0:  # If pixel is not transparent
                        # Draw glow around it
                        for dy in range(-2, 3):
                            for dx in range(-2, 3):
                                dist = (dx*dx + dy*dy) ** 0.5
                                if dist > 0 and dist <= 2:
                                    glow_x = x + dx + 2
                                    glow_y = y + dy + 2
                                    alpha = int(80 * (1 - dist / 2))
                                    if 0 <= glow_x < BLOCK_SIZE + 4 and 0 <= glow_y < BLOCK_SIZE + 4:
                                        current = glow_surface.get_at((glow_x, glow_y))
                                        new_alpha = min(255, current[3] + alpha)
                                        glow_surface.set_at((glow_x, glow_y), (*glow_color, new_alpha))
            
            # Combine glow with item
            final_surface = pygame.Surface((BLOCK_SIZE + 4, BLOCK_SIZE + 4), pygame.SRCALPHA)
            final_surface.blit(glow_surface, (0, 0))
            final_surface.blit(surface, (2, 2))
            return final_surface
        
        return surface
    
    def _draw_gem(self, surface, handle_color, head_color, highlight_color, has_glow, glow_color):
        """Draw crystal or ore gem"""
        # Diamond/crystal shape
        center_x, center_y = BLOCK_SIZE // 2, BLOCK_SIZE // 2
        
        if self.item_type == 'crystal':
            # Tall crystal shard
            points = [
                (center_x, center_y - 5),  # Top point
                (center_x - 3, center_y),  # Left
                (center_x - 2, center_y + 5),  # Bottom left
                (center_x + 2, center_y + 5),  # Bottom right
                (center_x + 3, center_y),  # Right
            ]
        else:  # rare_ore
            # Chunky ore
            points = [
                (center_x, center_y - 4),  # Top
                (center_x - 4, center_y - 1),  # Left top
                (center_x - 3, center_y + 3),  # Left bottom
                (center_x, center_y + 4),  # Bottom
                (center_x + 3, center_y + 3),  # Right bottom
                (center_x + 4, center_y - 1),  # Right top
            ]
        
        # Fill gem shape
        for y in range(center_y - 6, center_y + 7):
            for x in range(center_x - 5, center_x + 6):
                if self._point_in_polygon(x, y, points):
                    surface.set_at((x, y), head_color)
        
        # Add highlights
        highlight_points = [
            (center_x - 1, center_y - 2),
            (center_x, center_y - 3),
            (center_x + 1, center_y - 2),
        ]
        for px, py in highlight_points:
            if 0 <= px < BLOCK_SIZE and 0 <= py < BLOCK_SIZE:
                surface.set_at((px, py), highlight_color)
    
    def _draw_rare_item(self, surface, handle_color, head_color, highlight_color, has_glow, glow_color):
        """Draw special rare items with unique shapes"""
        center_x, center_y = BLOCK_SIZE // 2, BLOCK_SIZE // 2
        
        if self.item_type == 'magnet':
            # U-shaped magnet
            for y in range(center_y - 4, center_y + 5):
                for x in [center_x - 4, center_x + 4]:  # Left and right bars
                    if 0 <= x < BLOCK_SIZE and 0 <= y < BLOCK_SIZE:
                        surface.set_at((x, y), head_color)
            for x in range(center_x - 4, center_x + 5):  # Bottom bar
                if 0 <= x < BLOCK_SIZE and center_y + 4 < BLOCK_SIZE:
                    surface.set_at((x, center_y + 4), head_color)
            # Highlights
            surface.set_at((center_x - 4, center_y - 3), highlight_color)
            surface.set_at((center_x + 4, center_y - 3), highlight_color)
        
        elif self.item_type == 'double_jump':
            # Wings shape
            wing_points = [
                (center_x - 5, center_y), (center_x - 3, center_y - 3),
                (center_x - 1, center_y), (center_x + 1, center_y),
                (center_x + 3, center_y - 3), (center_x + 5, center_y)
            ]
            for px, py in wing_points:
                if 0 <= px < BLOCK_SIZE and 0 <= py < BLOCK_SIZE:
                    surface.set_at((px, py), head_color)
                    if 0 <= px - 1 < BLOCK_SIZE and 0 <= py + 1 < BLOCK_SIZE:
                        surface.set_at((px - 1, py + 1), head_color)
                        surface.set_at((px, py + 1), head_color)
        
        elif self.item_type == 'speed_boost':
            # Lightning bolt
            bolt_points = [
                (center_x, center_y - 5), (center_x - 1, center_y - 2),
                (center_x + 1, center_y - 2), (center_x, center_y),
                (center_x - 2, center_y), (center_x, center_y + 3),
                (center_x + 1, center_y + 5)
            ]
            for i in range(len(bolt_points) - 1):
                x1, y1 = bolt_points[i]
                x2, y2 = bolt_points[i + 1]
                if 0 <= x1 < BLOCK_SIZE and 0 <= y1 < BLOCK_SIZE:
                    surface.set_at((x1, y1), head_color)
                if 0 <= x2 < BLOCK_SIZE and 0 <= y2 < BLOCK_SIZE:
                    surface.set_at((x2, y2), head_color)
        
        elif self.item_type == 'shield':
            # Shield shape
            for y in range(center_y - 4, center_y + 5):
                width = 5 - abs(y - center_y) // 2
                for x in range(center_x - width, center_x + width + 1):
                    if 0 <= x < BLOCK_SIZE and 0 <= y < BLOCK_SIZE:
                        surface.set_at((x, y), head_color)
            # Cross pattern
            for i in range(-2, 3):
                if 0 <= center_x + i < BLOCK_SIZE and 0 <= center_y < BLOCK_SIZE:
                    surface.set_at((center_x + i, center_y), highlight_color)
                if 0 <= center_x < BLOCK_SIZE and 0 <= center_y + i < BLOCK_SIZE:
                    surface.set_at((center_x, center_y + i), highlight_color)
        
        elif self.item_type == 'block_breaker':
            # Explosive star
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                for dist in range(2, 6):
                    px = center_x + int(math.cos(rad) * dist)
                    py = center_y + int(math.sin(rad) * dist)
                    if 0 <= px < BLOCK_SIZE and 0 <= py < BLOCK_SIZE:
                        color = highlight_color if dist > 4 else head_color
                        surface.set_at((px, py), color)
            # Center
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if 0 <= center_x + dx < BLOCK_SIZE and 0 <= center_y + dy < BLOCK_SIZE:
                        surface.set_at((center_x + dx, center_y + dy), highlight_color)
    
    def _point_in_polygon(self, x, y, polygon):
        """Check if point is inside polygon (ray casting algorithm)"""
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    
    def update(self, dt, world):
        """Update item physics and animation"""
        self.spawn_timer += dt
        
        # Update lifetime
        self.lifetime -= dt
        if self.lifetime <= 2.0 and not self.lifetime_warning:
            self.lifetime_warning = True
            print(f"[ITEM] {self.item_type} will disappear in {self.lifetime:.1f}s!")
        
        # Smooth floating animation with easing
        self.float_timer += dt * 2.5
        self.float_offset = math.sin(self.float_timer) * 4 + math.sin(self.float_timer * 2) * 1
        
        # Rotation animation (rare items spin)
        if self.is_rare:
            self.rotation += self.rotation_speed * dt
            if self.rotation >= 360:
                self.rotation -= 360
        
        # Glow pulse animation
        self.glow_pulse += dt * 3
        glow_intensity = (math.sin(self.glow_pulse) * 0.3 + 0.7)  # 0.4 to 1.0
        
        # Scale pulse for rare items
        if self.is_rare:
            self.scale_pulse = 1.0 + math.sin(self.float_timer * 1.5) * 0.1  # 0.9 to 1.1
        
        # Sparkle effects for rare items
        if self.is_rare:
            self.sparkle_timer += dt
            if self.sparkle_timer >= 0.08:  # Spawn sparkle every 0.08s
                self.sparkle_timer = 0
                self._spawn_sparkle()
        
        # Update sparkles
        for sparkle in self.sparkles[:]:
            sparkle['lifetime'] -= dt
            sparkle['y'] -= sparkle['speed'] * dt
            sparkle['x'] += sparkle['drift'] * dt
            sparkle['alpha'] = int(255 * max(0, sparkle['lifetime'] / sparkle['max_lifetime']))
            
            if sparkle['lifetime'] <= 0:
                self.sparkles.remove(sparkle)
        
        # Gravity if not on ground
        if not self.on_ground:
            self.velocity_y += 800 * dt  # Gravity
            if self.velocity_y > 400:
                self.velocity_y = 400
            
            self.y += self.velocity_y * dt
            
            # Check collision with ground
            grid_x = int(self.x // BLOCK_SIZE)
            grid_y = int((self.y + self.height) // BLOCK_SIZE)
            
            block_below = world.get_block(grid_x, grid_y)
            if block_below and block_below.is_solid():
                self.y = grid_y * BLOCK_SIZE - self.height
                self.velocity_y = 0
                self.on_ground = True
                
                # Bounce effect on landing
                if self.spawn_timer < 1.0:  # Only bounce when first landing
                    self.velocity_y = -150
                    self.on_ground = False
    
    def can_collect(self, player):
        """Check if player is close enough to collect"""
        # Collection radius
        collect_radius = BLOCK_SIZE * 1.5
        
        dx = (player.x + player.width / 2) - (self.x + self.width / 2)
        dy = (player.y + player.height / 2) - (self.y + self.height / 2)
        distance = (dx * dx + dy * dy) ** 0.5
        
        return distance < collect_radius
    
    def _spawn_sparkle(self):
        """Create sparkle particle around item"""
        import random
        
        # Get item color for sparkles
        colors = {
            'magnet': (0, 255, 255),
            'double_jump': (0, 255, 0),
            'speed_boost': (255, 255, 0),
            'shield': (0, 128, 255),
            'block_breaker': (255, 0, 0),
            'crystal': (150, 220, 255),
            'rare_ore': (180, 100, 220),
            'diamond_pickaxe': (0, 255, 255),
            'iron_pickaxe': (200, 220, 255),
            'heart': (255, 100, 150),
        }
        
        color = colors.get(self.item_type, (255, 255, 255))
        
        # Spawn sparkle in circular pattern
        angle = random.uniform(0, math.pi * 2)
        radius = random.uniform(8, 16)
        
        sparkle = {
            'x': self.x + self.width / 2 + math.cos(angle) * radius,
            'y': self.y + self.height / 2 + math.sin(angle) * radius,
            'speed': random.uniform(20, 40),
            'drift': random.uniform(-10, 10),
            'lifetime': random.uniform(0.4, 0.8),
            'max_lifetime': 0.8,
            'alpha': 255,
            'color': color,
            'size': random.randint(1, 3)
        }
        self.sparkles.append(sparkle)
    
    def get_render_y(self):
        """Get Y position with floating offset"""
        return self.y + self.float_offset
    
    def get_glow_alpha(self):
        """Get current glow alpha for pulsing effect"""
        return int((math.sin(self.glow_pulse) * 0.3 + 0.7) * 255)
    
    def get_scale(self):
        """Get current scale for pulsing effect"""
        return self.scale_pulse if self.is_rare else 1.0
    
    def get_rotation(self):
        """Get current rotation angle"""
        return self.rotation if self.is_rare else 0
