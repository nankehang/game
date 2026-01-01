"""
Explosion animation for TNT
Generates procedural pixel art explosion frames
"""

import pygame
import random
import math
from constants import BLOCK_SIZE

class Explosion:
    """Animated explosion effect"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        
        # Randomly choose explosion variation (A, B, or C)
        self.variation = random.choice(['A', 'B', 'C'])
        
        # Different timings for each variation
        if self.variation == 'A':
            self.max_frames = 12
            self.frame_duration = 0.04  # Standard speed
        elif self.variation == 'B':
            self.max_frames = 14
            self.frame_duration = 0.035  # Faster
        else:  # C
            self.max_frames = 13
            self.frame_duration = 0.042  # Slightly slower
        
        self.frame_timer = 0
        self.finished = False
        
        # Generate all frames
        self.frames = self._generate_frames()
    
    def _generate_frames(self):
        """Generate all explosion animation frames"""
        frames = []
        max_radius = BLOCK_SIZE * 4.0  # HUGE explosion - 4 blocks radius!
        
        for frame_num in range(self.max_frames):
            # Calculate expansion progress (0.0 to 1.0)
            progress = frame_num / (self.max_frames - 1)
            
            # Create surface for this frame
            size = int(max_radius * 2 + 40)
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            center_x = size // 2
            center_y = size // 2
            
            if frame_num == 0:  # WHITE FLASH FRAME
                self._draw_white_flash(surface, center_x, center_y, max_radius)
            elif frame_num < 8:  # Expanding phase
                self._draw_explosion_expanding(surface, center_x, center_y, progress, max_radius)
            else:  # Fading phase
                fade_progress = (frame_num - 7) / 4
                self._draw_explosion_fading(surface, center_x, center_y, fade_progress, max_radius)
            
            frames.append(surface)
        
        return frames
    
    def _draw_white_flash(self, surface, cx, cy, max_radius):
        """Draw initial white flash frame for maximum impact"""
        flash_radius = max_radius * 1.5
        
        # Outer glow ring (yellow-white)
        for ring in range(5):
            radius = flash_radius - ring * 8
            alpha = 255 - ring * 40
            color = (255, 255, 200 + ring * 10, alpha)
            pygame.draw.circle(surface, color, (cx, cy), int(radius), 4)
        
        # Bright white core with starburst effect
        core_radius = int(flash_radius * 0.7)
        pygame.draw.circle(surface, (255, 255, 255, 255), (cx, cy), core_radius)
        
        # Starburst rays
        num_rays = 16
        for i in range(num_rays):
            angle = (i / num_rays) * 2 * math.pi
            # Long ray
            x1 = cx + int(math.cos(angle) * core_radius * 0.3)
            y1 = cy + int(math.sin(angle) * core_radius * 0.3)
            x2 = cx + int(math.cos(angle) * flash_radius * 1.2)
            y2 = cy + int(math.sin(angle) * flash_radius * 1.2)
            
            ray_color = (255, 255, 255, 200) if i % 2 == 0 else (255, 255, 100, 180)
            pygame.draw.line(surface, ray_color, (x1, y1), (x2, y2), 6 - (i % 3) * 2)
    
    def _draw_explosion_expanding(self, surface, cx, cy, progress, max_radius):
        """Draw expanding explosion - different variations"""
        current_radius = max_radius * (0.2 + progress * 0.8)
        
        # MASSIVE shockwave ring (triple layer for drama)
        if progress > 0.1:
            for layer in range(3):
                ring_radius = current_radius * (1.15 - layer * 0.05)
                ring_thickness = max(3, int(8 * (1 - progress))) - layer
                ring_alpha = int(255 * (1 - progress) * (1 - layer * 0.3))
                
                if layer == 0:
                    color = (255, 255, 255, ring_alpha)  # White outer ring
                elif layer == 1:
                    color = (255, 255, 100, ring_alpha)  # Yellow middle
                else:
                    color = (255, 150, 0, ring_alpha)  # Orange inner
                
                self._draw_circle_outline(surface, cx, cy, ring_radius, ring_thickness, color)
        
        # Energy distortion waves (multiple expanding rings)
        if progress > 0.15:
            for wave in range(4):
                wave_progress = (progress - 0.15) + wave * 0.1
                if wave_progress > 0 and wave_progress < 1:
                    wave_radius = current_radius * (0.5 + wave_progress * 0.7)
                    wave_alpha = int(150 * (1 - wave_progress))
                    wave_color = (255, 200, 0, wave_alpha)
                    self._draw_circle_outline(surface, cx, cy, wave_radius, 2, wave_color)
        
        # Draw flames based on variation
        if self.variation == 'A':
            self._draw_circular_flames(surface, cx, cy, current_radius, progress)
        elif self.variation == 'B':
            self._draw_upward_burst(surface, cx, cy, current_radius, progress)
        else:  # C
            self._draw_cross_pattern(surface, cx, cy, current_radius, progress)
        
        # Core and debris also vary by type
        self._draw_core(surface, cx, cy, current_radius, progress)
        self._draw_debris(surface, cx, cy, current_radius, progress)
    
    def _draw_circular_flames(self, surface, cx, cy, current_radius, progress):
        """Variation A: Classic circular explosion"""
        flame_count = 32 + int(progress * 16)
        for i in range(flame_count):
            angle = (i / flame_count) * 2 * math.pi + progress * 0.5
            
            # Wavy distortion
            wave_offset = math.sin(angle * 3 + progress * 5) * 10
            dist = current_radius * random.uniform(0.75, 1.05) + wave_offset
            
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            color = self._get_flame_color()
            pixel_size = random.randint(3, 7)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
        
        # Middle layer
        mid_radius = current_radius * 0.65
        for i in range(40):
            angle = (i / 40) * 2 * math.pi - progress * 0.5
            spiral_offset = math.sin(angle * 2) * 8
            dist = mid_radius * random.uniform(0.4, 1.0) + spiral_offset
            
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            color = self._get_hot_color()
            pixel_size = random.randint(3, 6)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
    
    def _draw_upward_burst(self, surface, cx, cy, current_radius, progress):
        """Variation B: Vertical geyser-like explosion"""
        flame_count = 28 + int(progress * 12)
        for i in range(flame_count):
            angle = (i / flame_count) * 2 * math.pi + progress * 0.3
            
            # Emphasize vertical direction
            vertical_bias = -0.7 if math.sin(angle) < 0 else 0.3
            dist = current_radius * random.uniform(0.7, 1.0)
            
            x = cx + int(math.cos(angle) * dist * 0.7)  # Narrower horizontally
            y = cy + int(math.sin(angle) * dist * 1.3 + vertical_bias * current_radius)  # Taller vertically
            
            color = self._get_flame_color()
            pixel_size = random.randint(3, 8)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
        
        # Upward plume in middle
        for i in range(35):
            angle = random.uniform(-math.pi/3, math.pi/3) - math.pi/2  # Upward cone
            dist = current_radius * random.uniform(0.4, 0.9)
            
            x = cx + int(math.cos(angle) * dist * 0.5)
            y = cy + int(math.sin(angle) * dist * 1.2)
            
            color = self._get_hot_color()
            pixel_size = random.randint(4, 7)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
    
    def _draw_cross_pattern(self, surface, cx, cy, current_radius, progress):
        """Variation C: X-shaped diagonal explosion"""
        # Draw 4 diagonal arms
        flame_count = 36 + int(progress * 14)
        for i in range(flame_count):
            angle = (i / flame_count) * 2 * math.pi + progress * 0.4
            
            # Emphasize diagonal directions (45, 135, 225, 315 degrees)
            diagonal_emphasis = abs(math.cos(angle * 2))  # High at 45° angles
            dist = current_radius * random.uniform(0.7, 1.0) * (0.8 + diagonal_emphasis * 0.4)
            
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            color = self._get_flame_color()
            pixel_size = random.randint(3, 7) if diagonal_emphasis > 0.5 else random.randint(2, 5)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
        
        # Cross arms with extra particles
        for arm in range(4):
            base_angle = arm * math.pi / 2 + math.pi / 4  # 45, 135, 225, 315
            for j in range(15):
                dist = current_radius * random.uniform(0.5, 1.1)
                angle_offset = random.uniform(-0.2, 0.2)
                
                x = cx + int(math.cos(base_angle + angle_offset) * dist)
                y = cy + int(math.sin(base_angle + angle_offset) * dist)
                
                color = self._get_hot_color()
                pixel_size = random.randint(4, 7)
                pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
    
    def _get_flame_color(self):
        """Get random flame color"""
        color_mix = random.random()
        if color_mix < 0.25:
            return (255, 0, 0, 255)  # Pure red
        elif color_mix < 0.5:
            return (255, 100, 0, 240)  # Red-orange
        elif color_mix < 0.75:
            return (255, 180, 0, 220)  # Orange
        else:
            return (255, 255, 50, 200)  # Bright yellow
    
    def _get_hot_color(self):
        """Get random hot center color"""
        if random.random() < 0.4:
            return (255, 220, 0, 250)  # Bright orange
        elif random.random() < 0.7:
            return (255, 255, 150, 240)  # Yellow
        else:
            return (255, 255, 255, 230)  # White hot
    
    def _draw_core(self, surface, cx, cy, current_radius, progress):
        """Draw bright core (same for all variations)"""
        core_radius = current_radius * (0.45 - progress * 0.15)
        
        for i in range(35):
            angle = random.random() * 2 * math.pi
            dist = core_radius * random.random()
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            if random.random() < 0.7:
                color = (255, 255, 255, 255)  # Pure white
            else:
                color = (255, 255, 220, 255)  # Slight yellow tint
            
            pixel_size = random.randint(3, 6)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
    
    def _draw_debris(self, surface, cx, cy, current_radius, progress):
        """Draw debris - direction varies by explosion type"""
        debris_count = int(30 * (1 + progress))
        
        for i in range(debris_count):
            if self.variation == 'A':
                # Circular - debris goes in all directions evenly
                angle = (i / debris_count) * 2 * math.pi + random.uniform(-0.5, 0.5)
            elif self.variation == 'B':
                # Upward - most debris goes up and to sides
                if i < debris_count * 0.7:
                    angle = random.uniform(-math.pi*0.75, -math.pi*0.25)  # Upward
                else:
                    angle = random.uniform(0, 2 * math.pi)  # Some go everywhere
            else:  # C
                # Cross - debris follows diagonal paths
                quadrant = i % 4
                base = quadrant * math.pi / 2 + math.pi / 4
                angle = base + random.uniform(-0.4, 0.4)
            
            dist = current_radius * (1.3 + progress * 0.8)
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            # Varied debris types
            debris_type = random.random()
            if debris_type < 0.4:
                color = (120, 120, 120, 240)  # Gray block
                size = random.randint(4, 8)  # CHUNKY
            elif debris_type < 0.7:
                color = (255, 180, 0, 250)  # Orange ember
                size = random.randint(3, 6)
            else:
                color = (255, 100, 0, 255)  # Red hot fragment
                size = random.randint(2, 5)
            
            pygame.draw.rect(surface, color, (x, y, size, size))
            
            # Add glow to hot debris
            if debris_type >= 0.4:
                glow_surface = pygame.Surface((size + 4, size + 4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*color[:3], 100), 
                                 (size // 2 + 2, size // 2 + 2), size // 2 + 2)
                surface.blit(glow_surface, (x - 2, y - 2))
    
    def _draw_explosion_fading(self, surface, cx, cy, fade_progress, max_radius):
        """Draw fading explosion with THICC smoke (frames 8-11)"""
        alpha_mult = 1.0 - fade_progress
        smoke_radius = max_radius * 1.3
        
        # MASSIVE smoke clouds (dark gray/brown)
        for i in range(50):  # More smoke!
            angle = (i / 50) * 2 * math.pi + random.uniform(-0.3, 0.3)
            dist = smoke_radius * random.uniform(0.5, 1.1)
            
            # Smoke rises and expands
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist - fade_progress * 20)
            
            smoke_alpha = int(180 * alpha_mult * random.uniform(0.4, 1.0))
            
            # Varied smoke colors (more dramatic)
            if random.random() < 0.3:
                gray_value = random.randint(20, 40)  # Dark smoke
            elif random.random() < 0.6:
                gray_value = random.randint(40, 70)  # Medium smoke
            else:
                gray_value = random.randint(70, 100)  # Light smoke
            
            pixel_size = random.randint(5, 10)  # CHUNKY smoke
            
            # Create small surface with alpha for smoke particle
            smoke_surf = pygame.Surface((pixel_size, pixel_size))
            smoke_surf.fill((gray_value, gray_value, gray_value))
            smoke_surf.set_alpha(smoke_alpha)
            surface.blit(smoke_surf, (x, y), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Lots of fading embers
        for i in range(30):
            angle = random.random() * 2 * math.pi
            dist = smoke_radius * random.uniform(0.3, 0.9)
            
            # Embers drift outward and down
            x = cx + int(math.cos(angle) * dist * (1 + fade_progress * 0.3))
            y = cy + int(math.sin(angle) * dist + fade_progress * 15)
            
            ember_alpha = int(240 * alpha_mult * random.uniform(0.2, 1.0))
            
            # Hot ember colors
            ember_type = random.random()
            if ember_type < 0.3:
                ember_color = (255, 50, 0)  # Red hot
            elif ember_type < 0.6:
                ember_color = (255, 120, 0)  # Orange
            else:
                ember_color = (255, 200, 0)  # Yellow
            
            pixel_size = random.randint(2, 5)
            
            # Create ember particle with alpha
            ember_surf = pygame.Surface((pixel_size, pixel_size))
            ember_surf.fill(ember_color)
            ember_surf.set_alpha(ember_alpha)
            surface.blit(ember_surf, (x, y), special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Ember glow
            if ember_alpha > 100:
                glow_alpha = min(100, ember_alpha // 2)
                glow_surf = pygame.Surface((pixel_size * 3, pixel_size * 3), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*ember_color, glow_alpha), 
                                 (pixel_size * 3 // 2, pixel_size * 3 // 2), 
                                 pixel_size + 2)
                surface.blit(glow_surf, (x - pixel_size, y - pixel_size))
        
        # Residual fire flickers
        if fade_progress < 0.5:
            flicker_count = int(20 * (1 - fade_progress * 2))
            for i in range(flicker_count):
                angle = random.random() * 2 * math.pi
                dist = smoke_radius * random.uniform(0.2, 0.6)
                x = cx + int(math.cos(angle) * dist)
                y = cy + int(math.sin(angle) * dist)
                
                flicker_alpha = int(200 * alpha_mult * random.random())
                flicker_color = (255, random.randint(150, 255), 0)
                
                pixel_size = random.randint(3, 6)
                
                # Create flicker particle with alpha
                flicker_surf = pygame.Surface((pixel_size, pixel_size))
                flicker_surf.fill(flicker_color)
                flicker_surf.set_alpha(flicker_alpha)
                surface.blit(flicker_surf, (x, y), special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_circle_outline(self, surface, cx, cy, radius, thickness, color):
        """Draw pixelated circle outline"""
        points = []
        steps = int(radius * 2)
        for i in range(steps):
            angle = (i / steps) * 2 * math.pi
            x = cx + int(math.cos(angle) * radius)
            y = cy + int(math.sin(angle) * radius)
            points.append((x, y))
        
        # Draw thick line
        if len(points) > 1:
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                pygame.draw.line(surface, color, p1, p2, thickness)
    
    def update(self, dt):
        """Update animation frame"""
        if self.finished:
            return
        
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame += 1
            
            if self.frame >= self.max_frames:
                self.finished = True
                self.frame = self.max_frames - 1
    
    def is_finished(self):
        """Check if animation is complete"""
        return self.finished
    
    def get_current_frame(self):
        """Get current animation frame surface"""
        return self.frames[self.frame]
    
    def get_position(self):
        """Get explosion center position for rendering"""
        frame_surface = self.frames[0]
        offset_x = frame_surface.get_width() // 2
        offset_y = frame_surface.get_height() // 2
        return (self.x - offset_x, self.y - offset_y)
