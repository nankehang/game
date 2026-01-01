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
        
        # Night sky stars (generate once)
        self.stars = self._generate_stars()
        
        # Shooting stars (dynamic)
        self.shooting_stars = []
        self.shooting_star_timer = 0
        
        # Snow particles
        self.snow_particles = self._generate_snow()
    
    def _generate_stars(self):
        """Generate random stars for night sky"""
        import random
        stars = []
        for _ in range(150):  # 150 stars
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)  # Only in top half
            brightness = random.uniform(0.3, 1.0)
            twinkle_speed = random.uniform(2, 5)
            twinkle_offset = random.uniform(0, 6.28)  # Random phase
            size = random.choice([1, 1, 1, 2])  # Mostly small, some bigger
            stars.append({
                'x': x,
                'y': y,
                'brightness': brightness,
                'twinkle_speed': twinkle_speed,
                'twinkle_offset': twinkle_offset,
                'size': size
            })
        return stars
    
    def render_stars(self):
        """Render twinkling stars"""
        import math
        import pygame
        time = pygame.time.get_ticks() / 1000.0
        
        for star in self.stars:
            # Calculate twinkle
            twinkle = abs(math.sin(time * star['twinkle_speed'] + star['twinkle_offset']))
            alpha = int(255 * star['brightness'] * twinkle)
            
            # Star color (white with slight blue tint)
            color = (200 + int(55 * twinkle), 200 + int(55 * twinkle), 255)
            
            # Draw star
            if star['size'] == 1:
                self.screen.set_at((star['x'], star['y']), color)
            else:
                pygame.draw.circle(self.screen, color, (star['x'], star['y']), star['size'])
    
    def _generate_snow(self):
        """Generate snow particles"""
        import random
        snow = []
        for _ in range(100):  # 100 snowflakes
            snow.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT),
                'speed': random.uniform(20, 50),
                'drift': random.uniform(-10, 10),
                'size': random.choice([1, 1, 2]),
                'opacity': random.uniform(0.5, 1.0)
            })
        return snow
    
    def update_background_effects(self, dt):
        """Update shooting stars and snow"""
        import random
        
        # Update snow
        for flake in self.snow_particles:
            flake['y'] += flake['speed'] * dt
            flake['x'] += flake['drift'] * dt
            
            # Wrap around
            if flake['y'] > SCREEN_HEIGHT:
                flake['y'] = -10
                flake['x'] = random.randint(0, SCREEN_WIDTH)
            if flake['x'] < 0:
                flake['x'] = SCREEN_WIDTH
            if flake['x'] > SCREEN_WIDTH:
                flake['x'] = 0
        
        # Spawn shooting stars randomly
        self.shooting_star_timer += dt
        if self.shooting_star_timer > random.uniform(2, 5):  # Every 2-5 seconds
            self.shooting_star_timer = 0
            self._spawn_shooting_star()
        
        # Update shooting stars
        for star in self.shooting_stars[:]:
            star['x'] += star['vx'] * dt
            star['y'] += star['vy'] * dt
            star['life'] -= dt
            
            if star['life'] <= 0 or star['y'] > SCREEN_HEIGHT:
                self.shooting_stars.remove(star)
    
    def _spawn_shooting_star(self):
        """Spawn a shooting star"""
        import random
        
        # Start from top-right area
        start_x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH + 100)
        start_y = random.randint(-50, SCREEN_HEIGHT // 3)
        
        self.shooting_stars.append({
            'x': start_x,
            'y': start_y,
            'vx': random.uniform(-300, -200),  # Move left
            'vy': random.uniform(100, 200),    # Move down
            'life': random.uniform(1.0, 2.0),
            'max_life': 2.0,
            'length': random.uniform(30, 60)
        })
    
    def render_background_effects(self):
        """Render snow and shooting stars (before everything)"""
        import pygame
        import math
        
        # Render snow
        for flake in self.snow_particles:
            alpha = int(255 * flake['opacity'])
            color = (255, 255, 255)
            
            if flake['size'] == 1:
                if 0 <= flake['x'] < SCREEN_WIDTH and 0 <= flake['y'] < SCREEN_HEIGHT:
                    self.screen.set_at((int(flake['x']), int(flake['y'])), color)
            else:
                pygame.draw.circle(self.screen, color, 
                                 (int(flake['x']), int(flake['y'])), flake['size'])
        
        # Render shooting stars
        for star in self.shooting_stars:
            alpha = int(255 * (star['life'] / star['max_life']))
            
            # Calculate trail end point
            dx = star['vx'] / abs(star['vx']) if star['vx'] != 0 else 0
            dy = star['vy'] / abs(star['vy']) if star['vy'] != 0 else 0
            length = star['length']
            
            # Normalize direction
            mag = math.sqrt(dx*dx + dy*dy)
            if mag > 0:
                dx /= mag
                dy /= mag
            
            end_x = star['x'] + dx * length
            end_y = star['y'] + dy * length
            
            # Draw gradient trail
            for i in range(3):
                offset = i * 0.3
                fade = 1.0 - (i * 0.3)
                color = (255, 255, 255)
                width = max(1, 3 - i)
                
                pygame.draw.line(self.screen, color,
                               (int(star['x'] + dx * offset), int(star['y'] + dy * offset)),
                               (int(end_x + dx * offset), int(end_y + dy * offset)),
                               width)
        
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
        
        # Render items
        for item in world.items:
            self._render_item(item, camera_x, camera_y)
        
        # Render explosions (in front of TNT but behind particles)
        for explosion in world.explosions:
            self._render_explosion(explosion, camera_x, camera_y)
        
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
        
        # Get TNT texture based on power level
        if tnt.power_level >= 5:
            base_texture = texture_gen.generate_block_texture('mythic_tnt')  # Purple/pink for high level
        elif tnt.power_level >= 2:
            base_texture = texture_gen.generate_block_texture('super_tnt')  # Purple for level 2+
        else:
            base_texture = texture_gen.generate_block_texture('tnt')  # Normal red
        
        # Scale texture if TNT is bigger
        if tnt.width != BLOCK_SIZE:
            texture = pygame.transform.scale(base_texture, (tnt.width, tnt.height))
        else:
            texture = base_texture.copy()
        
        # Red flash effect when close to explosion
        if tnt.should_flash():
            if int(tnt.fuse_time * 8) % 2 == 0:  # Faster flash
                flash_surface = pygame.Surface((tnt.width, tnt.height))
                # Flash color based on power level
                if tnt.power_level >= 2:
                    flash_surface.fill((200, 0, 255))  # Purple flash
                else:
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
        
        # Show power level if > 0
        if tnt.power_level > 0:
            timer_text = f"Lv.{tnt.power_level} {tnt.fuse_time:.1f}s"
            power_color = (200, 100, 255) if tnt.power_level >= 2 else (255, 200, 0)
        else:
            timer_text = f"{tnt.fuse_time:.1f}s"
            power_color = color
        
        fuse_text = font.render(timer_text, True, power_color)
        text_rect = fuse_text.get_rect(center=(screen_x + tnt.width // 2, 
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
    
    def _render_item(self, item, camera_x, camera_y):
        """Render collectible item with floating animation"""
        screen_x = int(item.x - camera_x)
        screen_y = int(item.get_render_y() - camera_y)
        
        # Only render if on screen
        if (-32 <= screen_x < SCREEN_WIDTH + 32 and 
            -32 <= screen_y < SCREEN_HEIGHT + 32):
            
            # Adjust position for glowing items (they have bigger texture)
            if item.texture.get_width() > BLOCK_SIZE:
                offset = (item.texture.get_width() - BLOCK_SIZE) // 2
                screen_x -= offset
                screen_y -= offset
            
            self.screen.blit(item.texture, (screen_x, screen_y))
    
    def _render_explosion(self, explosion, camera_x, camera_y):
        """Render explosion animation"""
        # Get current frame and position
        frame_surface = explosion.get_current_frame()
        pos_x, pos_y = explosion.get_position()
        
        # Convert to screen coordinates
        screen_x = int(pos_x - camera_x)
        screen_y = int(pos_y - camera_y)
        
        # Render the explosion frame
        self.screen.blit(frame_surface, (screen_x, screen_y))
    
    def render_player(self, player, camera_x, camera_y, debug=True):
        """Render player sprite"""
        # Hitbox is 26x28 but sprite is 32x32, so offset sprite to center it
        hitbox_to_sprite_offset_x = (32 - player.width) // 2
        hitbox_to_sprite_offset_y = (32 - player.height) // 2
        
        screen_x = int(player.x - camera_x - hitbox_to_sprite_offset_x)
        screen_y = int(player.y - camera_y - hitbox_to_sprite_offset_y)
        
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
        
        # Render HP hearts above player head
        heart_size = 8
        heart_spacing = 10
        total_width = player.max_hp * heart_spacing - 2
        hearts_x = screen_x + (32 - total_width) // 2  # Center above player
        hearts_y = screen_y - 15  # Above player head
        
        for i in range(player.max_hp):
            x = hearts_x + i * heart_spacing
            
            # Draw heart (filled or empty)
            if i < player.current_hp:
                # Filled heart (red)
                if player.current_hp == 1:
                    # Pulse when low HP
                    import math
                    pulse = abs(math.sin(pygame.time.get_ticks() / 200))
                    heart_color = (int(255 * (0.7 + 0.3 * pulse)), 50, 50)
                else:
                    heart_color = (255, 50, 50)
                
                # Draw filled heart shape
                pygame.draw.circle(self.screen, heart_color, (x + 2, hearts_y + 2), 3)
                pygame.draw.circle(self.screen, heart_color, (x + 6, hearts_y + 2), 3)
                pygame.draw.polygon(self.screen, heart_color, [
                    (x, hearts_y + 3),
                    (x + 4, hearts_y + 8),
                    (x + 8, hearts_y + 3)
                ])
                # Shine
                pygame.draw.circle(self.screen, (255, 150, 150), (x + 2, hearts_y + 1), 1)
            else:
                # Empty heart (dark outline)
                outline_color = (80, 20, 20)
                pygame.draw.circle(self.screen, outline_color, (x + 2, hearts_y + 2), 3, 1)
                pygame.draw.circle(self.screen, outline_color, (x + 6, hearts_y + 2), 3, 1)
                pygame.draw.polygon(self.screen, outline_color, [
                    (x, hearts_y + 3),
                    (x + 4, hearts_y + 8),
                    (x + 8, hearts_y + 3)
                ], 1)
        
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
    
    def render_meteors(self, world, camera_x, camera_y):
        """Render meteors with beautiful glowing trails"""
        for meteor in world.meteors:
            # Render trail particles first (behind meteor)
            for particle in meteor.trail_particles:
                screen_x = int(particle['x'] - camera_x)
                screen_y = int(particle['y'] - camera_y)
                
                # Get color based on meteor type
                color_map = {
                    'orange': (255, 140, 50),
                    'cyan': (80, 220, 255),
                    'purple': (200, 80, 255),
                    'yellow': (255, 240, 80)
                }
                base_color = color_map.get(particle['color'], (255, 140, 50))
                
                # Apply alpha
                alpha = int(particle['alpha'] * 255)
                size = int(particle['size'] * particle['alpha'])
                
                if size > 0:
                    # Draw glowing particle
                    glow_surf = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
                    
                    # Outer glow
                    for r in range(size * 3, size, -1):
                        glow_alpha = int(alpha * (1 - (r - size) / (size * 2)))
                        color = (*base_color, glow_alpha)
                        pygame.draw.circle(glow_surf, color, (size * 3 // 2, size * 3 // 2), r)
                    
                    # Core
                    core_color = tuple(min(255, c + 50) for c in base_color) + (alpha,)
                    pygame.draw.circle(glow_surf, core_color, (size * 3 // 2, size * 3 // 2), max(1, size))
                    
                    self.screen.blit(glow_surf, (screen_x - size * 3 // 2, screen_y - size * 3 // 2))
            
            # Render meteor body
            screen_x = int(meteor.x - camera_x)
            screen_y = int(meteor.y - camera_y)
            
            # Get meteor color
            meteor_color = meteor.get_color_rgb()
            glow_intensity = meteor.get_glow_intensity()
            
            # Draw outer glow
            glow_size = int(meteor.width * 2)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            
            for r in range(glow_size, meteor.width // 2, -1):
                glow_alpha = int(100 * glow_intensity * (1 - (r - meteor.width // 2) / glow_size))
                color = (*meteor_color, glow_alpha)
                pygame.draw.circle(glow_surf, color, (glow_size, glow_size), r)
            
            self.screen.blit(glow_surf, (screen_x - glow_size + meteor.width // 2, 
                                         screen_y - glow_size + meteor.height // 2))
            
            # Draw meteor core (rotated rock)
            rock_surf = pygame.Surface((meteor.width, meteor.height), pygame.SRCALPHA)
            
            # Draw irregular rock shape
            rock_points = [
                (meteor.width * 0.2, meteor.height * 0.4),
                (meteor.width * 0.5, meteor.height * 0.1),
                (meteor.width * 0.8, meteor.height * 0.3),
                (meteor.width * 0.9, meteor.height * 0.7),
                (meteor.width * 0.6, meteor.height * 0.9),
                (meteor.width * 0.1, meteor.height * 0.8),
            ]
            
            # Dark rock with colored glow
            rock_base = tuple(c // 3 for c in meteor_color)
            pygame.draw.polygon(rock_surf, rock_base, rock_points)
            
            # Glowing edges
            for i in range(len(rock_points)):
                p1 = rock_points[i]
                p2 = rock_points[(i + 1) % len(rock_points)]
                edge_color = tuple(min(255, int(c * (0.8 + 0.4 * glow_intensity))) for c in meteor_color)
                pygame.draw.line(rock_surf, edge_color, p1, p2, 2)
            
            # Rotate meteor
            rotated = pygame.transform.rotate(rock_surf, meteor.rotation)
            rotated_rect = rotated.get_rect(center=(screen_x + meteor.width // 2, 
                                                     screen_y + meteor.height // 2))
            
            self.screen.blit(rotated, rotated_rect)
    
    def render_meteor_shower_indicator(self, world):
        """Render beautiful indicator when meteor shower is active"""
        if world.is_meteor_shower_active():
            import math
            
            # Main title
            font_large = pygame.font.Font(None, 48)
            font_small = pygame.font.Font(None, 28)
            
            # Title text with sparkle
            title = "✨ METEOR SHOWER ✨"
            title_surface = font_large.render(title, True, (255, 250, 200))
            
            # Subtitle
            subtitle = "Beautiful meteors falling from the sky..."
            subtitle_surface = font_small.render(subtitle, True, (200, 220, 255))
            
            # Calculate positions
            title_x = SCREEN_WIDTH // 2 - title_surface.get_width() // 2
            title_y = 15
            subtitle_x = SCREEN_WIDTH // 2 - subtitle_surface.get_width() // 2
            subtitle_y = 55
            
            # Pulsing glow effect
            pulse = abs(math.sin(pygame.time.get_ticks() / 400))
            glow_alpha = int(80 + 175 * pulse)
            
            # Draw glowing background
            glow_surf = pygame.Surface((title_surface.get_width() + 40, 70), pygame.SRCALPHA)
            glow_color = (100, 150, 255, int(60 + 40 * pulse))
            pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=10)
            self.screen.blit(glow_surf, (title_x - 20, title_y - 5))
            
            # Draw glow for title
            glow_surface = font_large.render(title, True, (150, 200, 255))
            glow_surface.set_alpha(glow_alpha)
            
            # Multi-layer glow
            for offset in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
                self.screen.blit(glow_surface, (title_x + offset[0], title_y + offset[1]))
            
            # Draw main text
            self.screen.blit(title_surface, (title_x, title_y))
            self.screen.blit(subtitle_surface, (subtitle_x, subtitle_y))
            
            # Draw small star particles
            time = pygame.time.get_ticks() / 1000
            for i in range(5):
                star_x = title_x - 30 + (i * 15) + int(math.sin(time * 3 + i) * 10)
                star_y = title_y + 35 + int(math.cos(time * 2 + i) * 8)
                star_size = 2 + int(pulse * 2)
                pygame.draw.circle(self.screen, (255, 255, 150), (star_x, star_y), star_size)
            
            # Draw shooting star trails
            for i in range(3):
                trail_x = title_x + title_surface.get_width() + 40 + i * 20
                trail_y = title_y + 20 + int(math.sin(time * 4 + i * 2) * 15)
                trail_color = (150 + int(pulse * 100), 200 + int(pulse * 50), 255)
                pygame.draw.line(self.screen, trail_color, 
                               (trail_x, trail_y), 
                               (trail_x - 15, trail_y - 10), 2)
    
    def render_rare_items(self, world, camera_x, camera_y):
        """Render items with gorgeous visual effects"""
        import math
        import random
        
        time = pygame.time.get_ticks() / 1000.0
        
        for item in world.items:
            # Calculate screen position with floating
            screen_x = int(item.x - camera_x)
            screen_y = int(item.get_render_y() - camera_y)
            
            # Skip if off-screen (with margin)
            if screen_x < -100 or screen_x > SCREEN_WIDTH + 100:
                continue
            if screen_y < -100 or screen_y > SCREEN_HEIGHT + 100:
                continue
            
            # === RARE ITEM SPECIAL EFFECTS ===
            if item.is_rare:
                center_x = screen_x + item.width // 2
                center_y = screen_y + item.height // 2
                
                # Get item glow color
                glow_colors = {
                    'magnet': (0, 255, 255),
                    'double_jump': (0, 255, 0),
                    'speed_boost': (255, 255, 0),
                    'shield': (0, 128, 255),
                    'block_breaker': (255, 0, 0),
                    'crystal': (150, 220, 255),
                    'rare_ore': (180, 100, 220),
                    'diamond_pickaxe': (0, 255, 255),
                    'heart': (255, 100, 150),
                    'coal_ore': (80, 80, 80),
                    'iron_ore': (192, 192, 192),
                    'gold_ore': (255, 215, 0),
                    'diamond_ore': (0, 255, 255),
                }
                glow_color = glow_colors.get(item.item_type, (255, 255, 255))
                
                # === MULTI-LAYER GLOW RINGS ===
                glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
                glow_center = (100, 100)
                
                # Outer pulsing rings (3 layers)
                for ring in range(3):
                    ring_radius = 60 - ring * 15 + int(math.sin(time * 3 + ring * 1.5) * 8)
                    ring_alpha = int(40 - ring * 10 + math.sin(time * 4 + ring) * 20)
                    ring_alpha = max(0, min(255, ring_alpha))  # Clamp to 0-255
                    ring_width = 3 - ring
                    
                    # Create color with alpha
                    r, g, b = glow_color
                    ring_r = max(0, min(255, int(r * (0.8 + 0.2 * ring))))
                    ring_g = max(0, min(255, int(g * (0.8 + 0.2 * ring))))
                    ring_b = max(0, min(255, int(b * (0.8 + 0.2 * ring))))
                    ring_color = (ring_r, ring_g, ring_b, ring_alpha)
                    
                    pygame.draw.circle(glow_surf, ring_color, glow_center, ring_radius, ring_width)
                
                # Inner bright glow (layered)
                for layer in range(5, 0, -1):
                    glow_radius = 35 + layer * 5
                    glow_alpha = int(30 * (layer / 5) * item.get_glow_alpha() / 255)
                    glow_alpha = max(0, min(255, glow_alpha))  # Clamp to 0-255
                    inner_color = glow_color + (glow_alpha,)
                    pygame.draw.circle(glow_surf, inner_color, glow_center, glow_radius)
                
                # === ENERGY WAVES (rotating) ===
                wave_angle = time * 120  # Rotation speed
                for wave in range(4):
                    angle = math.radians(wave_angle + wave * 90)
                    wave_radius = 45 + int(math.sin(time * 2 + wave) * 5)
                    
                    # Wave start and end points
                    x1 = glow_center[0] + int(math.cos(angle) * wave_radius)
                    y1 = glow_center[1] + int(math.sin(angle) * wave_radius)
                    x2 = glow_center[0] + int(math.cos(angle + 0.3) * (wave_radius + 10))
                    y2 = glow_center[1] + int(math.sin(angle + 0.3) * (wave_radius + 10))
                    
                    wave_alpha = int(100 + math.sin(time * 5 + wave) * 50)
                    wave_alpha = max(0, min(255, wave_alpha))  # Clamp to 0-255
                    r, g, b = glow_color
                    wave_color = (min(255, r + 50), min(255, g + 50), min(255, b + 50), wave_alpha)
                    pygame.draw.line(glow_surf, wave_color, (x1, y1), (x2, y2), 2)
                
                # === STAR SPARKLES (orbiting) ===
                for star in range(8):
                    star_angle = (time * 90 + star * 45) % 360
                    star_orbit = 50 + int(math.sin(time * 3 + star) * 8)
                    
                    star_x = glow_center[0] + int(math.cos(math.radians(star_angle)) * star_orbit)
                    star_y = glow_center[1] + int(math.sin(math.radians(star_angle)) * star_orbit)
                    
                    star_size = 2 + int(math.sin(time * 6 + star) * 1)
                    star_alpha = int(150 + math.sin(time * 8 + star) * 105)
                    star_alpha = max(0, min(255, star_alpha))  # Clamp to 0-255
                    star_color = (255, 255, 255, star_alpha)
                    
                    pygame.draw.circle(glow_surf, star_color, (star_x, star_y), star_size)
                
                # Blit glow surface
                self.screen.blit(glow_surf, (center_x - 100, center_y - 100))
                
                # === SPARKLE PARTICLES ===
                for sparkle in item.sparkles:
                    s_x = int(sparkle['x'] - camera_x)
                    s_y = int(sparkle['y'] - camera_y)
                    
                    if 0 <= s_x < SCREEN_WIDTH and 0 <= s_y < SCREEN_HEIGHT:
                        # Sparkle with glow
                        sparkle_glow = pygame.Surface((12, 12), pygame.SRCALPHA)
                        sparkle_alpha = max(0, min(255, sparkle['alpha']))
                        
                        # Outer glow
                        for glow_layer in range(3, 0, -1):
                            layer_alpha = max(0, min(255, sparkle_alpha // (4 - glow_layer)))
                            layer_color = sparkle['color'] + (layer_alpha // 2,)
                            pygame.draw.circle(sparkle_glow, layer_color, (6, 6), glow_layer)
                        
                        # Bright center
                        center_color = (255, 255, 255, sparkle['alpha'])
                        pygame.draw.circle(sparkle_glow, center_color, (6, 6), sparkle['size'])
                        
                        self.screen.blit(sparkle_glow, (s_x - 6, s_y - 6))
            
            # === RENDER ITEM TEXTURE ===
            # Get rotation and scale
            rotation = item.get_rotation()
            scale = item.get_scale()
            
            # Apply rotation if needed
            if rotation != 0 or scale != 1.0:
                # Scale first
                if scale != 1.0:
                    new_width = int(item.width * scale)
                    new_height = int(item.height * scale)
                    scaled_texture = pygame.transform.scale(item.texture, (new_width, new_height))
                else:
                    scaled_texture = item.texture
                
                # Then rotate
                if rotation != 0:
                    rotated_texture = pygame.transform.rotate(scaled_texture, -rotation)
                else:
                    rotated_texture = scaled_texture
                
                # Center the texture
                texture_rect = rotated_texture.get_rect(center=(screen_x + item.width // 2, 
                                                                screen_y + item.height // 2))
                self.screen.blit(rotated_texture, texture_rect)
            else:
                # No transformation needed
                self.screen.blit(item.texture, (screen_x, screen_y))
            
            # === RARE ITEM OVERLAY GLOW ===
            if item.is_rare:
                # Pulsing bright edge
                pulse_alpha = int(100 + math.sin(time * 5) * 80)
                pulse_alpha = max(0, min(255, pulse_alpha))  # Clamp to 0-255
                # Add bright highlight on item itself
                highlight_surf = pygame.Surface((item.width + 8, item.height + 8), pygame.SRCALPHA)
                
                item_glow = glow_colors.get(item.item_type, (255, 255, 255))
                r, g, b = item_glow
                edge_color = (min(255, r + 100), min(255, g + 100), min(255, b + 100), pulse_alpha)
                
                pygame.draw.rect(highlight_surf, edge_color, highlight_surf.get_rect(), 2, border_radius=3)
                
                center_x = screen_x + item.width // 2
                center_y = screen_y + item.height // 2
                self.screen.blit(highlight_surf, (center_x - (item.width + 8) // 2, 
                                                  center_y - (item.height + 8) // 2))
            
            # === NORMAL ITEM SIMPLE GLOW ===
            elif item.item_type in ['diamond_pickaxe', 'iron_pickaxe']:
                # Simple glow for valuable pickaxes
                glow_surf = pygame.Surface((item.width + 20, item.height + 20), pygame.SRCALPHA)
                glow_center = (item.width // 2 + 10, item.height // 2 + 10)
                
                simple_colors = {
                    'diamond_pickaxe': (0, 255, 255),
                    'iron_pickaxe': (200, 220, 255),
                }
                simple_glow = simple_colors.get(item.item_type, (255, 255, 255))
                
                for layer in range(3, 0, -1):
                    layer_alpha = 20 * layer
                    layer_color = simple_glow + (layer_alpha,)
                    pygame.draw.circle(glow_surf, layer_color, glow_center, 15 + layer * 3)
                
                self.screen.blit(glow_surf, (screen_x - 10, screen_y - 10))
                self.screen.blit(item.texture, (screen_x, screen_y))

