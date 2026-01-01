"""
Procedural texture generation for blocks
Creates Minecraft-style pixel art textures
"""

import pygame
import random
from constants import BLOCK_SIZE, BLOCK_COLORS

class TextureGenerator:
    """Generates procedural pixel textures for blocks"""
    
    def __init__(self):
        self.texture_cache = {}
        
    def generate_block_texture(self, block_type):
        """
        Generate a 16x16 pixel texture for a block type
        Returns a pygame Surface
        """
        if block_type in self.texture_cache:
            return self.texture_cache[block_type]
        
        surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        base_color = BLOCK_COLORS.get(block_type, (255, 0, 255))
        
        if base_color is None:  # Air
            surface.set_colorkey((0, 0, 0))
            self.texture_cache[block_type] = surface
            return surface
        
        # Generate texture based on block type
        if block_type == 'grass':
            self._generate_grass_texture(surface, base_color)
        elif block_type == 'dirt':
            self._generate_dirt_texture(surface, base_color)
        elif block_type == 'stone':
            self._generate_stone_texture(surface, base_color)
        elif block_type in ['coal', 'iron', 'gold', 'diamond', 'mythic_ore']:
            self._generate_ore_texture(surface, base_color)
        elif block_type == 'water':
            self._generate_water_texture(surface, base_color)
        elif block_type == 'lava':
            self._generate_lava_texture(surface, base_color)
        elif block_type == 'bedrock':
            self._generate_bedrock_texture(surface, base_color)
        elif block_type == 'tnt':
            self._generate_tnt_texture(surface, base_color)
        elif block_type == 'super_tnt':
            self._generate_super_tnt_texture(surface, base_color)
        elif block_type == 'mythic_tnt':
            self._generate_mythic_tnt_texture(surface, base_color)
        else:
            self._generate_basic_texture(surface, base_color)
        
        self.texture_cache[block_type] = surface
        return surface
    
    def _generate_basic_texture(self, surface, base_color):
        """Generate basic noisy texture"""
        r, g, b = base_color
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Add random noise
                noise = random.randint(-20, 20)
                pixel_color = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
                surface.set_at((x, y), pixel_color)
    
    def _generate_grass_texture(self, surface, base_color):
        """Generate grass texture with darker bottom"""
        dirt_color = (150, 111, 51)
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Top 3 pixels are grass, rest is dirt
                if y < 3:
                    # Grass layer
                    noise = random.randint(-15, 15)
                    r, g, b = base_color
                    pixel_color = (
                        max(0, min(255, r + noise)),
                        max(0, min(255, g + noise)),
                        max(0, min(255, b + noise))
                    )
                else:
                    # Dirt layer
                    noise = random.randint(-20, 20)
                    r, g, b = dirt_color
                    pixel_color = (
                        max(0, min(255, r + noise)),
                        max(0, min(255, g + noise)),
                        max(0, min(255, b + noise))
                    )
                surface.set_at((x, y), pixel_color)
    
    def _generate_dirt_texture(self, surface, base_color):
        """Generate dirt texture with spots"""
        r, g, b = base_color
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                noise = random.randint(-25, 25)
                
                # Add darker spots
                if random.random() < 0.1:
                    noise -= 30
                
                pixel_color = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
                surface.set_at((x, y), pixel_color)
    
    def _generate_stone_texture(self, surface, base_color):
        """Generate stone texture with cracks"""
        r, g, b = base_color
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                noise = random.randint(-15, 15)
                
                # Add occasional dark crack pixels
                if random.random() < 0.05:
                    noise -= 40
                
                pixel_color = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
                surface.set_at((x, y), pixel_color)
    
    def _generate_ore_texture(self, surface, base_color):
        """Generate ore texture with sparkles on stone background"""
        stone_color = (125, 125, 125)
        r_ore, g_ore, b_ore = base_color
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Base stone texture
                noise = random.randint(-15, 15)
                r, g, b = stone_color
                
                # Add ore sparkles (20% of pixels)
                if random.random() < 0.2:
                    r, g, b = r_ore, g_ore, b_ore
                    noise = random.randint(-10, 30)  # Brighter ore pixels
                
                pixel_color = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
                surface.set_at((x, y), pixel_color)
    
    def _generate_water_texture(self, surface, base_color):
        """Generate semi-transparent water texture"""
        r, g, b = base_color
        surface.set_alpha(180)  # Semi-transparent
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Wavy pattern
                wave = int(10 * ((x + y) % 4) / 4)
                noise = random.randint(-10, 10) + wave
                
                pixel_color = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
                surface.set_at((x, y), pixel_color)
    
    def _generate_lava_texture(self, surface, base_color):
        """Generate animated lava texture"""
        r, g, b = base_color
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Hot spots
                if random.random() < 0.15:
                    noise = random.randint(20, 60)
                else:
                    noise = random.randint(-30, 10)
                
                pixel_color = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
                surface.set_at((x, y), pixel_color)
    
    def _generate_bedrock_texture(self, surface, base_color):
        """Generate dark, unbreakable bedrock texture"""
        r, g, b = base_color
        
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                noise = random.randint(-5, 5)
                
                # Very dark with rare slightly lighter spots
                if random.random() < 0.02:
                    noise += 20
                
                pixel_color = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
                surface.set_at((x, y), pixel_color)
    
    def _generate_tnt_texture(self, surface, base_color):
        """Generate TNT texture with red and white pattern"""
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Create striped pattern
                if (x + y) % 4 < 2:
                    # Red stripes
                    noise = random.randint(-10, 10)
                    pixel_color = (
                        max(0, min(255, 255 + noise)),
                        max(0, min(255, 0 + noise)),
                        max(0, min(255, 0 + noise))
                    )
                else:
                    # White stripes
                    noise = random.randint(-10, 10)
                    pixel_color = (
                        max(0, min(255, 255 + noise)),
                        max(0, min(255, 255 + noise)),
                        max(0, min(255, 255 + noise))
                    )
                surface.set_at((x, y), pixel_color)
        
        # Add "TNT" text in center
        center_pixels = [(7, 6), (8, 6), (7, 7), (7, 8), (7, 9)]
        for px, py in center_pixels:
            surface.set_at((px, py), (0, 0, 0))
    
    def _generate_super_tnt_texture(self, surface, base_color):
        """Generate purple Super TNT texture"""
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Create striped pattern with purple
                if (x + y) % 4 < 2:
                    # Purple stripes
                    noise = random.randint(-10, 10)
                    pixel_color = (
                        max(0, min(255, 150 + noise)),
                        max(0, min(255, 0 + noise)),
                        max(0, min(255, 255 + noise))
                    )
                else:
                    # Light purple stripes
                    noise = random.randint(-10, 10)
                    pixel_color = (
                        max(0, min(255, 200 + noise)),
                        max(0, min(255, 150 + noise)),
                        max(0, min(255, 255 + noise))
                    )
                surface.set_at((x, y), pixel_color)
        
        # Add "TNT" text in center
        center_pixels = [(7, 6), (8, 6), (7, 7), (7, 8), (7, 9)]
        for px, py in center_pixels:
            surface.set_at((px, py), (0, 0, 0))
    
    def _generate_mythic_tnt_texture(self, surface, base_color):
        """Generate pink/purple Mythic TNT texture"""
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                # Create striped pattern with pink/purple
                if (x + y) % 4 < 2:
                    # Pink stripes
                    noise = random.randint(-10, 10)
                    pixel_color = (
                        max(0, min(255, 255 + noise)),
                        max(0, min(255, 100 + noise)),
                        max(0, min(255, 255 + noise))
                    )
                else:
                    # Purple stripes
                    noise = random.randint(-10, 10)
                    pixel_color = (
                        max(0, min(255, 200 + noise)),
                        max(0, min(255, 0 + noise)),
                        max(0, min(255, 255 + noise))
                    )
                surface.set_at((x, y), pixel_color)
        
        # Add "TNT" text in center with glow effect
        center_pixels = [(7, 6), (8, 6), (7, 7), (7, 8), (7, 9)]
        for px, py in center_pixels:
            surface.set_at((px, py), (255, 255, 0))  # Yellow text

# Global texture generator instance
texture_gen = TextureGenerator()
