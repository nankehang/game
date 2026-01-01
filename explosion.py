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
        self.max_frames = 10
        self.frame_duration = 0.05  # 50ms per frame
        self.frame_timer = 0
        self.finished = False
        
        # Generate all frames
        self.frames = self._generate_frames()
    
    def _generate_frames(self):
        """Generate all explosion animation frames"""
        frames = []
        max_radius = BLOCK_SIZE * 2.5  # Explosion expands to 2.5 blocks
        
        for frame_num in range(self.max_frames):
            # Calculate expansion progress (0.0 to 1.0)
            progress = frame_num / (self.max_frames - 1)
            
            # Create surface for this frame
            size = int(max_radius * 2 + 20)
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            center_x = size // 2
            center_y = size // 2
            
            if frame_num < 7:  # Expanding phase
                self._draw_explosion_expanding(surface, center_x, center_y, progress, max_radius)
            else:  # Fading phase
                fade_progress = (frame_num - 6) / 3
                self._draw_explosion_fading(surface, center_x, center_y, fade_progress, max_radius)
            
            frames.append(surface)
        
        return frames
    
    def _draw_explosion_expanding(self, surface, cx, cy, progress, max_radius):
        """Draw expanding explosion (frames 0-6)"""
        current_radius = max_radius * (0.3 + progress * 0.7)
        
        # Shockwave ring (outer edge)
        if progress > 0.2:
            ring_radius = current_radius * 1.1
            ring_thickness = max(2, int(4 * (1 - progress)))
            ring_alpha = int(200 * (1 - progress))
            self._draw_circle_outline(surface, cx, cy, ring_radius, ring_thickness, 
                                     (255, 255, 255, ring_alpha))
        
        # Outer flames (red/orange)
        flame_count = 16 + int(progress * 8)
        for i in range(flame_count):
            angle = (i / flame_count) * 2 * math.pi + progress * 0.5
            dist = current_radius * random.uniform(0.7, 1.0)
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            # Red to orange gradient
            color_mix = random.random()
            if color_mix < 0.3:
                color = (255, 50, 0, 220)  # Red
            elif color_mix < 0.7:
                color = (255, 140, 0, 200)  # Orange
            else:
                color = (255, 200, 0, 180)  # Yellow-orange
            
            pixel_size = random.randint(2, 4)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
        
        # Middle layer (orange/yellow)
        mid_radius = current_radius * 0.6
        for i in range(24):
            angle = (i / 24) * 2 * math.pi - progress * 0.3
            dist = mid_radius * random.uniform(0.5, 1.0)
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            if random.random() < 0.5:
                color = (255, 200, 0, 240)  # Orange
            else:
                color = (255, 255, 100, 230)  # Yellow
            
            pixel_size = random.randint(2, 5)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
        
        # Bright core (yellow/white)
        core_radius = current_radius * (0.4 - progress * 0.2)
        for i in range(20):
            angle = random.random() * 2 * math.pi
            dist = core_radius * random.random()
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            if random.random() < 0.6:
                color = (255, 255, 255, 255)  # White
            else:
                color = (255, 255, 200, 250)  # Bright yellow
            
            pixel_size = random.randint(2, 4)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
        
        # Flying debris/sparks
        debris_count = int(15 * progress)
        for i in range(debris_count):
            angle = (i / debris_count) * 2 * math.pi + random.uniform(-0.3, 0.3)
            dist = current_radius * (1.2 + progress * 0.5)
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            # Debris colors (gray blocks or orange embers)
            if random.random() < 0.6:
                color = (100, 100, 100, 200)  # Gray debris
            else:
                color = (255, 150, 0, 220)  # Orange ember
            
            pixel_size = random.randint(1, 3)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
    
    def _draw_explosion_fading(self, surface, cx, cy, fade_progress, max_radius):
        """Draw fading explosion with smoke (frames 7-9)"""
        alpha_mult = 1.0 - fade_progress
        smoke_radius = max_radius * 1.2
        
        # Smoke puffs (dark gray/brown)
        for i in range(30):
            angle = (i / 30) * 2 * math.pi + random.uniform(-0.2, 0.2)
            dist = smoke_radius * random.uniform(0.6, 1.0)
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist - fade_progress * 10)  # Rise upward
            
            smoke_alpha = int(150 * alpha_mult * random.uniform(0.5, 1.0))
            gray_value = random.randint(40, 80)
            color = (gray_value, gray_value, gray_value, smoke_alpha)
            
            pixel_size = random.randint(3, 6)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
        
        # Fading embers
        for i in range(15):
            angle = random.random() * 2 * math.pi
            dist = smoke_radius * random.uniform(0.4, 0.8)
            x = cx + int(math.cos(angle) * dist)
            y = cy + int(math.sin(angle) * dist)
            
            ember_alpha = int(200 * alpha_mult * random.uniform(0.3, 1.0))
            if random.random() < 0.5:
                color = (255, 100, 0, ember_alpha)  # Orange
            else:
                color = (255, 50, 0, ember_alpha)  # Red
            
            pixel_size = random.randint(2, 3)
            pygame.draw.rect(surface, color, (x, y, pixel_size, pixel_size))
    
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
