"""
Renderer for blocks, player, TNT, and particles
"""

import pygame
from texture_generator import texture_gen
from constants import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Renderer:
    """Handles all rendering operations"""
    
    def __init__(self, screen):
        self.screen = screen
        
    def render_world(self, world, camera_x, camera_y):
        """Render visible blocks"""
        visible_blocks = world.get_visible_blocks(camera_x, camera_y, 
                                                  SCREEN_WIDTH, SCREEN_HEIGHT)
        
        for bx, by, block in visible_blocks:
            screen_x = bx * BLOCK_SIZE - camera_x
            screen_y = by * BLOCK_SIZE - camera_y
            
            # Get texture for this block type
            texture = texture_gen.generate_block_texture(block.type)
            self.screen.blit(texture, (screen_x, screen_y))
            
            # Draw health bar if block is damaged
            if block.health < block.max_health and block.is_mineable():
                self._render_health_bar(screen_x, screen_y, 
                                       block.health / block.max_health)
        
        # Render TNT
        for tnt in world.tnt_list:
            self._render_tnt(tnt, camera_x, camera_y)
        
        # Render particles
        for particle in world.particles:
            self._render_particle(particle, camera_x, camera_y)
    
    def _render_health_bar(self, x, y, health_ratio):
        """Render health bar above damaged block"""
        bar_width = BLOCK_SIZE
        bar_height = 2
        
        # Background
        pygame.draw.rect(self.screen, (255, 0, 0), 
                        (x, y - 4, bar_width, bar_height))
        
        # Health
        pygame.draw.rect(self.screen, (0, 255, 0), 
                        (x, y - 4, int(bar_width * health_ratio), bar_height))
    
    def _render_tnt(self, tnt, camera_x, camera_y):
        """Render TNT with fuse indicator"""
        screen_x = int(tnt.x - camera_x)
        screen_y = int(tnt.y - camera_y)
        
        # Get TNT texture
        texture = texture_gen.generate_block_texture('tnt')
        
        # Flash effect when close to explosion
        fuse_ratio = tnt.get_fuse_ratio()
        if fuse_ratio < 0.3 and int(tnt.fuse_time * 10) % 2 == 0:
            # Create flashing white overlay
            flash_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(100)
            texture = texture.copy()
            texture.blit(flash_surface, (0, 0))
        
        self.screen.blit(texture, (screen_x, screen_y))
        
        # Draw fuse timer
        font = pygame.font.Font(None, 16)
        fuse_text = font.render(f"{tnt.fuse_time:.1f}", True, (255, 255, 0))
        text_rect = fuse_text.get_rect(center=(screen_x + BLOCK_SIZE // 2, 
                                                screen_y - 8))
        self.screen.blit(fuse_text, text_rect)
    
    def _render_particle(self, particle, camera_x, camera_y):
        """Render single particle"""
        screen_x = int(particle.x - camera_x)
        screen_y = int(particle.y - camera_y)
        
        # Only render if on screen
        if (0 <= screen_x < SCREEN_WIDTH and 
            0 <= screen_y < SCREEN_HEIGHT):
            
            # Create surface with alpha
            size = particle.size
            surf = pygame.Surface((size, size))
            surf.fill(particle.color)
            surf.set_alpha(particle.get_alpha())
            
            self.screen.blit(surf, (screen_x, screen_y))
    
    def render_player(self, player, camera_x, camera_y):
        """Render player sprite"""
        screen_x = int(player.x - camera_x)
        screen_y = int(player.y - camera_y)
        
        # Get current animation texture
        texture = player.get_texture()
        
        # Flip texture if facing left
        if not player.facing_right:
            texture = pygame.transform.flip(texture, True, False)
        
        self.screen.blit(texture, (screen_x, screen_y))
        
        # Draw mining indicator
        if player.is_mining:
            pygame.draw.circle(self.screen, (255, 215, 0), 
                             (screen_x + player.width // 2, 
                              screen_y + player.height + 10), 
                             3)
