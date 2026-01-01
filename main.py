"""
Minecraft-Style 2D Mining Game
Main game file with Pygame initialization
"""

import pygame
import sys
from world import World
from player import Player
from renderer import Renderer
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minecraft 2D Mining Game")
        self.clock = pygame.time.Clock()
        
        # Initialize game systems
        self.world = World()
        self.player = Player(SCREEN_WIDTH // 2, 100)
        self.renderer = Renderer(self.screen)
        
        # Camera offset for scrolling
        self.camera_x = 0
        self.camera_y = 0
        
        # Screen effects
        self.screen_shake_intensity = 0
        self.screen_shake_duration = 0
        self.flash_alpha = 0
        self.flash_color = (255, 255, 255)
        
        # Debug mode
        self.debug_mode = True  # Start with debug ON
        
        self.running = True
        
    def handle_events(self):
        """Handle keyboard and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Jump
                    self.player.jump()
                elif event.key == pygame.K_t:
                    # Drop TNT at player position
                    self.world.spawn_tnt(self.player.x, self.player.y, fuse_time=2.0)
                elif event.key == pygame.K_r:
                    # Reset player position (respawn)
                    self.respawn_player()
                    print("[GAME] Player respawned at surface!")
                elif event.key == pygame.K_F3:
                    # Toggle debug mode
                    self.debug_mode = not self.debug_mode
                    print(f"[DEBUG MODE] {'ON' if self.debug_mode else 'OFF'}")
                elif event.key == pygame.K_m:
                    # Trigger meteor shower (for testing)
                    if not self.world.meteor_shower_active:
                        self.world.meteor_shower_active = True
                        self.world.meteor_shower_duration = 15
                        self.world.meteor_spawn_timer = 0
                        print("[TEST] Meteor shower triggered!")
            elif event.type == pygame.KEYUP:
                # Variable jump - release jump button
                if event.key == pygame.K_SPACE:
                    self.player.release_jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Manual mining at mouse position
                    mouse_x, mouse_y = event.pos
                    world_x = (mouse_x + self.camera_x) // BLOCK_SIZE
                    world_y = (mouse_y + self.camera_y) // BLOCK_SIZE
                    self.world.mine_block_at(world_x, world_y, MANUAL_MINE_DAMAGE)
        
        # Continuous input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        
    def update(self, dt):
        """Update game state"""
        # Update background effects (snow, shooting stars)
        self.renderer.update_background_effects(dt)
        
        # Update player
        self.player.update(dt, self.world)
        
        # Check if player hit bedrock or fell out of world
        if self.player.fell_to_bedrock:
            print("[GAME] 💀 Player reached bedrock! Respawning at surface...")
            self.respawn_player()
        
        max_y = (BEDROCK_START + 5) * BLOCK_SIZE  # 5 blocks below bedrock (backup)
        if self.player.y > max_y:
            print("[GAME] ⚠️ Player fell out of world! Respawning...")
            self.respawn_player()
        
        # Update world (TNT, particles) - pass player for explosion knockback
        self.world.update(dt, self.player, self)
        
        # Update camera to follow player
        self.camera_x = max(0, self.player.x - SCREEN_WIDTH // 2)
        self.camera_y = max(0, self.player.y - SCREEN_HEIGHT // 2)
        
        # Update screen shake
        if self.screen_shake_duration > 0:
            self.screen_shake_duration -= dt
            if self.screen_shake_duration <= 0:
                self.screen_shake_intensity = 0
        
        # Update flash effect
        if self.flash_alpha > 0:
            self.flash_alpha -= dt * 500  # Fade out
            if self.flash_alpha < 0:
                self.flash_alpha = 0
        
    def render(self):
        """Render everything to screen"""
        self.screen.fill(SKY_COLOR)
        
        # Render twinkling stars (background)
        self.renderer.render_stars()
        
        # Apply screen shake to camera
        shake_x = 0
        shake_y = 0
        if self.screen_shake_intensity > 0:
            import random
            shake_x = random.randint(-int(self.screen_shake_intensity), int(self.screen_shake_intensity))
            shake_y = random.randint(-int(self.screen_shake_intensity), int(self.screen_shake_intensity))
        
        camera_x = self.camera_x + shake_x
        camera_y = self.camera_y + shake_y
        
        # Render world with camera offset
        self.renderer.render_world(self.world, camera_x, camera_y)
        
        # Render meteors (behind player but in front of blocks)
        self.renderer.render_meteors(self.world, camera_x, camera_y)
        
        # Render player with debug mode
        self.renderer.render_player(self.player, camera_x, camera_y, self.debug_mode)
        
        # Render meteor shower indicator
        self.renderer.render_meteor_shower_indicator(self.world)
        
        # Render snow and shooting stars (in front of everything!)
        self.renderer.render_background_effects()
        
        # Render flash effect
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.fill(self.flash_color)
            flash_surface.set_alpha(int(self.flash_alpha))
            self.screen.blit(flash_surface, (0, 0))
        
        # Render UI
        self.render_ui()
        
        pygame.display.flip()
        
    def render_ui(self):
        """Render UI overlay"""
        font = pygame.font.Font(None, 24)
        
        # Depth indicator
        depth = max(0, (self.player.y // BLOCK_SIZE) - 10)
        depth_text = font.render(f"Depth: {depth}m", True, (255, 255, 255))
        self.screen.blit(depth_text, (10, 10))
        
        # TNT statistics
        active_tnt = len(self.world.tnt_list)
        total_spawned = self.world.total_tnt_spawned
        spawn_chance = TNT_BASE_SPAWN_CHANCE + (depth * TNT_DEPTH_MULTIPLIER)
        spawn_chance = min(0.95, spawn_chance) * 100
        
        tnt_stats = font.render(f"TNT: {active_tnt} active | {total_spawned} spawned | {spawn_chance:.0f}% chance", 
                                True, (255, 200, 0))
        self.screen.blit(tnt_stats, (SCREEN_WIDTH - 450, 10))
        
        # Controls
        controls = [
            "A/D or Arrows: Move",
            "SPACE: Manual TNT (player pos)",
            "Click: Mine Block",
            "R: Reset Position",
            "F3: Toggle Debug",
            "ESC: Quit"
        ]
        y = 40
        for control in controls:
            text = font.render(control, True, (200, 200, 200))
            self.screen.blit(text, (10, y))
            y += 25
        
        # Debug mode indicator
        if self.debug_mode:
            debug_text = font.render("[DEBUG MODE ON]", True, (255, 255, 0))
            self.screen.blit(debug_text, (10, y + 10))
    
    def trigger_screen_shake(self, intensity, duration):
        """Trigger screen shake effect"""
        self.screen_shake_intensity = max(self.screen_shake_intensity, intensity)
        self.screen_shake_duration = max(self.screen_shake_duration, duration)
    
    def trigger_flash(self, color=(255, 200, 100), alpha=150):
        """Trigger screen flash effect"""
        self.flash_color = color
        self.flash_alpha = alpha
    
    def respawn_player(self):
        """Respawn player at surface safely"""
        # Find safe spawn position (grass layer)
        spawn_x = SCREEN_WIDTH // 2
        spawn_y = (GRASS_LAYER - 2) * BLOCK_SIZE  # Above grass layer
        
        self.player.x = spawn_x
        self.player.y = spawn_y
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.player.on_ground = False
        
        # Reset all player states
        self.player.knockback_timer = 0
        self.player.hurt_state = False
        self.player.hurt_timer = 0
        self.player.control_locked = False
        self.player.fell_to_bedrock = False  # Reset bedrock flag
            
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
