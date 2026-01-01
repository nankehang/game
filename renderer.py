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
        """Render TNT with fuse indicator and red flash"""
        screen_x = int(tnt.x - camera_x)
        screen_y = int(tnt.y - camera_y)
        
        # Get TNT texture
        texture = texture_gen.generate_block_texture('tnt')
        texture = texture.copy()  # Make copy for modification
        
        # Red flash effect when close to explosion
        if tnt.should_flash():
            if int(tnt.fuse_time * 8) % 2 == 0:  # Faster flash
                flash_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                flash_surface.fill((255, 0, 0))  # Red flash
                flash_surface.set_alpha(150)
                texture.blit(flash_surface, (0, 0))
        
        self.screen.blit(texture, (screen_x, screen_y))
        
        # Draw fuse timer with color based on urgency
        font = pygame.font.Font(None, 20)
        fuse_ratio = tnt.get_fuse_ratio()
        
        if fuse_ratio < 0.3:
            color = (255, 0, 0)  # Red - danger!
        elif fuse_ratio < 0.6:
            color = (255, 165, 0)  # Orange - warning
        else:
            color = (255, 255, 0)  # Yellow - safe
        
        fuse_text = font.render(f"{tnt.fuse_time:.1f}s", True, color)
        text_rect = fuse_text.get_rect(center=(screen_x + BLOCK_SIZE // 2, 
                                                screen_y - 10))
        # Draw background for better visibility
        bg_rect = text_rect.inflate(4, 2)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
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
    
    def render_player(self, player, camera_x, camera_y, debug=True):
        """Render player sprite"""
        screen_x = int(player.x - camera_x)
        screen_y = int(player.y - camera_y)
        
        # Get current animation texture
        texture = player.get_texture()
        
        # Flip texture if facing left
        if not player.facing_right:
            texture = pygame.transform.flip(texture, True, False)
        
        # Apply hurt flash effect
        if player.hurt_state:
            # Create red tint overlay
            hurt_overlay = pygame.Surface((player.width, player.height))
            hurt_overlay.fill((255, 0, 0))
            # Flashing effect
            if int(player.hurt_timer * 10) % 2 == 0:
                hurt_overlay.set_alpha(80)
            else:
                hurt_overlay.set_alpha(40)
            texture = texture.copy()
            texture.blit(hurt_overlay, (0, 0))
        
        self.screen.blit(texture, (screen_x, screen_y))
        
        # Draw mining indicator
        if player.is_mining:
            pygame.draw.circle(self.screen, (255, 215, 0), 
                             (screen_x + player.width // 2, 
                              screen_y + player.height + 10), 
                             3)
        
        # DEBUG: Show animation state
        if debug:
            font = pygame.font.Font(None, 20)
            debug_text = f"State: {player.animation_state} | Frame: {player.animation_frame}"
            debug_surface = font.render(debug_text, True, (255, 255, 0))
            self.screen.blit(debug_surface, (screen_x - 20, screen_y - 25))
            
            facing_text = "RIGHT" if player.facing_right else "LEFT"
            facing_surface = font.render(f"Facing: {facing_text}", True, (255, 255, 0))
            self.screen.blit(facing_surface, (screen_x - 20, screen_y - 45))
            
            velocity_text = f"Vel: ({player.velocity_x:.1f}, {player.velocity_y:.1f})"
            velocity_surface = font.render(velocity_text, True, (255, 255, 0))
            self.screen.blit(velocity_surface, (screen_x - 20, screen_y - 65))
            
            # Draw hitbox
            pygame.draw.rect(self.screen, (0, 255, 0), 
                           (screen_x, screen_y, player.width, player.height), 1)
