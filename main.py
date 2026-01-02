"""
Minecraft-Style 2D Mining Game
Main game file with Pygame initialization
"""

import pygame
import sys
from world import World
from player import Player
from renderer import Renderer
from ai_bot import AIBot
from statistics import Statistics
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
        self.player.game = self  # Link player to game for statistics
        self.renderer = Renderer(self.screen)
        self.ai_bot = AIBot(self.player, self.world)
        self.stats = Statistics()
        
        # Camera offset for scrolling
        self.camera_x = 0
        self.camera_y = 0
        
        # Screen effects
        self.screen_shake_intensity = 0
        self.screen_shake_duration = 0
        self.flash_alpha = 0
        self.flash_color = (255, 255, 255)
        
        # Death/respawn system
        self.death_timer = 0
        self.is_waiting_respawn = False
        
        # Debug mode
        self.debug_mode = True  # Start with debug ON
        
        # Game state
        self.game_state = 'menu'  # menu, playing
        self.menu_selection = 0  # 0 = Manual, 1 = AI Bot
        
        self.running = True
    
    def start_game(self):
        """Start the game based on menu selection"""
        self.game_state = 'playing'
        
        if self.menu_selection == 1:  # AI Bot
            self.ai_bot.enabled = True
            print("[GAME] Starting game with AI Bot!")
        else:  # Manual
            self.ai_bot.enabled = False
            print("[GAME] Starting game in Manual mode!")
        
        # Reset game state
        self.world = World()
        self.player = Player(SCREEN_WIDTH // 2, 100)
        self.player.game = self  # Link player to game
        self.renderer = Renderer(self.screen)
        self.ai_bot = AIBot(self.player, self.world)
        self.stats = Statistics()  # Reset stats
        if self.menu_selection == 1:
            self.ai_bot.enabled = True
        self.camera_x = 0
        self.camera_y = 0
        self.death_timer = 0
        self.is_waiting_respawn = False
        
    def handle_events(self):
        """Handle keyboard and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == 'playing':
                        self.game_state = 'menu'  # Return to menu
                        self.ai_bot.enabled = False
                    else:
                        self.running = False
                
                # Menu controls
                if self.game_state == 'menu':
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.menu_selection = max(0, self.menu_selection - 1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.menu_selection = min(1, self.menu_selection + 1)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.start_game()
                    continue  # Skip other controls in menu
                
                # Game controls (only when playing)
                if event.key == pygame.K_SPACE:
                    # Jump
                    self.player.jump()
                elif event.key == pygame.K_t:
                    # Drop TNT at player position (with player's power level)
                    # Random fuse time for staggered explosions (Minecraft-style)
                    import random
                    fuse_time = random.uniform(2.0, 4.0)  # 2-4 seconds
                    self.world.spawn_tnt(self.player.x, self.player.y, fuse_time=fuse_time, power_level=self.player.tnt_power_level)
                elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    # Share/Production mode: Spawn multiple TNT rapidly
                    import random
                    for i in range(5):  # Spawn 5 TNT
                        offset_x = random.uniform(-40, 40)
                        offset_y = random.uniform(-20, 20)
                        fuse_time = random.uniform(1.5, 5.0)  # Varied fuse times
                        self.world.spawn_tnt(
                            self.player.x + offset_x,
                            self.player.y + offset_y,
                            fuse_time=fuse_time,
                            power_level=self.player.tnt_power_level
                        )
                    print("[TNT] Mass spawn activated! (Share mode)")
                elif event.key == pygame.K_r:
                    # Reset player position (respawn)
                    self.respawn_player()
                    print("[GAME] Player respawned at surface!")
                elif event.key == pygame.K_F3:
                    # Toggle debug mode
                    self.debug_mode = not self.debug_mode
                    print(f"[DEBUG MODE] {'ON' if self.debug_mode else 'OFF'}")
                elif event.key == pygame.K_1:
                    # Add heart (like system)
                    if self.player.max_hp < 10:  # Max 10 hearts
                        self.player.max_hp += 1
                        self.player.current_hp = self.player.max_hp  # Full heal
                        print(f"[HEART] +1 Heart collected! Max HP: {self.player.max_hp}")
                    else:
                        print("[HEART] Max hearts reached (10)!")
                elif event.key == pygame.K_m:
                    # Trigger meteor shower (for testing)
                    if not self.world.meteor_shower_active:
                        self.world.meteor_shower_active = True
                        self.world.meteor_shower_duration = 15
                        self.world.meteor_spawn_timer = 0
                        print("[TEST] Meteor shower triggered!")
                elif event.key == pygame.K_b:
                    # Toggle AI bot
                    self.ai_bot.toggle()
            elif event.type == pygame.KEYUP:
                # Variable jump - release jump button
                if event.key == pygame.K_SPACE:
                    self.player.release_jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Manual mining at mouse position (with level bonus)
                    mouse_x, mouse_y = event.pos
                    world_x = (mouse_x + self.camera_x) // BLOCK_SIZE
                    world_y = (mouse_y + self.camera_y) // BLOCK_SIZE
                    speed_multiplier = 1.0 + self.player.mining_speed_bonus
                    damage = MANUAL_MINE_DAMAGE * speed_multiplier
                    print(f"[DEBUG] Manual mine: Base={MANUAL_MINE_DAMAGE}, Multiplier={speed_multiplier:.2f}x, Damage={damage:.2f}")
                    self.world.mine_block_at(world_x, world_y, damage, self)
        
        # Continuous input (only if AI bot is disabled and in game)
        if self.game_state == 'playing' and not self.ai_bot.enabled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
        
    def update(self, dt):
        """Update game state"""
        # Only update game when playing
        if self.game_state != 'playing':
            return
        
        # Update background effects (snow, shooting stars)
        self.renderer.update_background_effects(dt)
        
        # Update AI bot (controls player if enabled)
        self.ai_bot.update(dt)
        
        # Update statistics
        self.stats.update(dt)
        self.stats.update_achievements(dt)
        
        # Update player
        self.player.update(dt, self.world)
        
        # Check if player died (HP = 0)
        if self.player.current_hp <= 0 and not self.is_waiting_respawn:
            print("[GAME] Player died! Respawning in 3 seconds...")
            self.stats.on_death()
            self.is_waiting_respawn = True
            self.death_timer = 3.0  # 3 second countdown
        
        # Update death timer
        if self.is_waiting_respawn:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.respawn_player()
                self.is_waiting_respawn = False
                self.death_timer = 0
        
        # Check if player hit bedrock or fell out of world
        if self.player.fell_to_bedrock:
            print("[GAME] Player reached bedrock! Respawning at surface...")
            self.respawn_player()
        
        max_y = (BEDROCK_START + 5) * BLOCK_SIZE  # 5 blocks below bedrock (backup)
        if self.player.y > max_y:
            print("[GAME] Player fell out of world! Respawning...")
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
        # Render menu if in menu state
        if self.game_state == 'menu':
            self.render_menu()
            return
        
        # Check if player is in Nether (below bedrock)
        player_depth_y = int(self.player.y // BLOCK_SIZE)
        in_nether = player_depth_y > BEDROCK_START
        
        # Change sky color based on dimension
        if in_nether:
            nether_sky = (60, 20, 20)  # Dark red for Nether
            self.screen.fill(nether_sky)
        else:
            self.screen.fill(SKY_COLOR)
        
        # Render twinkling stars (background) - only in overworld
        if not in_nether:
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
        
        # Render rare items with gorgeous effects (before player)
        self.renderer.render_rare_items(self.world, camera_x, camera_y)
        
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
        
        # Death flash (red overlay)
        if self.player.death_flash > 0:
            death_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            death_surface.fill((255, 0, 0))
            death_surface.set_alpha(int(self.player.death_flash * 150))
            self.screen.blit(death_surface, (0, 0))
        
        # Death screen with countdown
        if self.is_waiting_respawn:
            # Dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            
            # Death message
            font_huge = pygame.font.Font(None, 72)
            font_large = pygame.font.Font(None, 48)
            
            death_text = font_huge.render("YOU DIED", True, (255, 50, 50))
            death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(death_text, death_rect)
            
            # Countdown
            countdown = int(self.death_timer) + 1
            countdown_text = font_large.render(f"Respawning in {countdown}...", True, (255, 200, 200))
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(countdown_text, countdown_rect)
        
        # Render UI
        self.render_ui()
        
        pygame.display.flip()
        
    def render_ui(self):
        """Render UI overlay"""
        font = pygame.font.Font(None, 24)
        font_large = pygame.font.Font(None, 36)
        
        # Depth indicator
        depth = max(0, (self.player.y // BLOCK_SIZE) - 10)
        
        # Check dimension
        player_block_y = int(self.player.y // BLOCK_SIZE)
        if player_block_y > BEDROCK_START:
            dimension_text = font_large.render("THE NETHER", True, (255, 100, 50))
            dim_rect = dimension_text.get_rect(center=(SCREEN_WIDTH // 2, 15))
            
            # Pulsing glow effect
            import math
            pulse = abs(math.sin(pygame.time.get_ticks() / 300))
            glow_surf = font_large.render("THE NETHER", True, (255, 150, 100))
            glow_surf.set_alpha(int(150 * pulse))
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, 15))
            self.screen.blit(glow_surf, glow_rect)
            self.screen.blit(dimension_text, dim_rect)
            
            # Nether depth
            nether_depth = player_block_y - BEDROCK_START
            depth_text = font.render(f"Nether Depth: {nether_depth}m", True, (255, 150, 100))
        else:
            depth_text = font.render(f"Depth: {depth}m", True, (255, 255, 255))
        
        self.screen.blit(depth_text, (10, 10))
        
        # AI Bot indicator
        if self.ai_bot.enabled:
            bot_text = font_large.render(f"🤖 AI BOT: {self.ai_bot.state.upper()}", True, (100, 255, 100))
            # Add glow effect
            import math
            pulse = abs(math.sin(pygame.time.get_ticks() / 200))
            glow_alpha = int(100 * pulse)
            glow_surf = font_large.render(f"🤖 AI BOT: {self.ai_bot.state.upper()}", True, (255, 255, 255))
            glow_surf.set_alpha(glow_alpha)
            self.screen.blit(glow_surf, (SCREEN_WIDTH - 252, 8))
            self.screen.blit(glow_surf, (SCREEN_WIDTH - 248, 8))
            self.screen.blit(bot_text, (SCREEN_WIDTH - 250, 10))
        
        # Statistics Display (right side, compact)
        stats = self.stats.get_summary()
        stats_y = 40
        stats_font = pygame.font.Font(None, 22)
        
        # Format times
        minutes = int(stats['play_time'] // 60)
        seconds = int(stats['play_time'] % 60)
        time_alive_min = int(stats['time_alive'] // 60)
        time_alive_sec = int(stats['time_alive'] % 60)
        
        stat_texts = [
            f"Blocks: {stats['blocks_mined']}",
            f"Items: {stats['items_collected']}",
            f"Deaths: {stats['deaths']}",
            f"Time: {minutes}:{seconds:02d}",
        ]
        
        for text in stat_texts:
            stat_surf = stats_font.render(text, True, (255, 255, 255))
            shadow_surf = stats_font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow_surf, (SCREEN_WIDTH - 122, stats_y + 1))
            self.screen.blit(stat_surf, (SCREEN_WIDTH - 120, stats_y))
            stats_y += 20
        
        # Achievement Popups (centered, bottom)
        popup_y = SCREEN_HEIGHT - 100
        for achievement in self.stats.new_achievements:
            box_width = 350
            box_height = 60
            box_x = (SCREEN_WIDTH - box_width) // 2
            
            alpha = min(255, int(achievement['timer'] * 200)) if achievement['timer'] < 1 else 255
            
            popup_surface = pygame.Surface((box_width, box_height))
            popup_surface.fill((50, 50, 50))
            popup_surface.set_alpha(min(200, alpha))
            self.screen.blit(popup_surface, (box_x, popup_y))
            
            pygame.draw.rect(self.screen, (255, 215, 0), (box_x, popup_y, box_width, box_height), 3)
            
            achievement_font = pygame.font.Font(None, 32)
            desc_font = pygame.font.Font(None, 24)
            
            title_text = achievement_font.render(f"🏆 {achievement['name']}", True, (255, 215, 0))
            desc_text = desc_font.render(achievement['description'], True, (200, 200, 200))
            
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 20))
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 42))
            
            self.screen.blit(title_text, title_rect)
            self.screen.blit(desc_text, desc_rect)
            
            popup_y -= 70
        
        # Controls
        controls = [
            "A/D or Arrows: Move",
            "SPACE: Manual TNT (player pos)",
            "Click: Mine Block",
            "1: Add Heart (+1 Max HP)",
            "R: Reset Position",
            "F3: Toggle Debug",
            "ESC: Quit"
        ]
        y = 100  # Start lower to account for level displays
        for control in controls:
            text = font.render(control, True, (200, 200, 200))
            self.screen.blit(text, (10, y))
            y += 25
        
        # Debug mode indicator
        if self.debug_mode:
            debug_text = font.render("[DEBUG MODE ON]", True, (255, 255, 0))
            self.screen.blit(debug_text, (10, y + 10))
    
    def render_menu(self):
        """Render the main menu"""
        # Background gradient
        for y in range(SCREEN_HEIGHT):
            alpha = y / SCREEN_HEIGHT
            color_top = (20, 100, 180)  # Sky blue
            color_bottom = (100, 150, 255)  # Light blue
            color = (
                int(color_top[0] + (color_bottom[0] - color_top[0]) * alpha),
                int(color_top[1] + (color_bottom[1] - color_top[1]) * alpha),
                int(color_top[2] + (color_bottom[2] - color_top[2]) * alpha)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Title
        font_huge = pygame.font.Font(None, 84)
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        
        title_text = font_huge.render("MINECRAFT MINER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        
        # Title shadow
        shadow_text = font_huge.render("MINECRAFT MINER", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, 123))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = font_medium.render("2D Mining Adventure", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        options = ["▶ PLAY MANUAL", "▶ AI BOT PLAY"]
        option_y = 280
        
        for i, option in enumerate(options):
            # Highlight selected option
            if i == self.menu_selection:
                color = (255, 255, 100)
                scale_font = font_large
                # Add glow effect
                import math
                pulse = abs(math.sin(pygame.time.get_ticks() / 200))
                glow_alpha = int(150 * pulse)
                glow_surf = scale_font.render(option, True, (255, 255, 255))
                glow_surf.set_alpha(glow_alpha)
                glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, option_y + i * 80))
                self.screen.blit(glow_surf, glow_rect)
            else:
                color = (180, 180, 180)
                scale_font = font_medium
            
            text = scale_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, option_y + i * 80))
            self.screen.blit(text, text_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 28)
        instructions = [
            "↑/↓ - Select Option",
            "ENTER/SPACE - Start Game",
            "ESC - Quit"
        ]
        
        inst_y = SCREEN_HEIGHT - 120
        for instruction in instructions:
            text = font_small.render(instruction, True, (150, 150, 150))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, inst_y))
            self.screen.blit(text, text_rect)
            inst_y += 30
        
        pygame.display.flip()
    
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
        import random
        
        # Find random safe spawn position (grass layer)
        # Spawn somewhere in the middle 60% of the world (avoid edges)
        world_width_blocks = self.world.width * BLOCK_SIZE
        min_x = world_width_blocks * 0.2
        max_x = world_width_blocks * 0.8
        spawn_x = random.uniform(min_x, max_x)
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
        self.player.death_flash = 0
        
        # Give HP on respawn (half of max HP, minimum 2)
        self.player.current_hp = max(2, self.player.max_hp // 2)
        print(f"[RESPAWN] Respawned at random location ({int(spawn_x/BLOCK_SIZE)}, {int(spawn_y/BLOCK_SIZE)}) with {self.player.current_hp}/{self.player.max_hp} HP")
            
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
