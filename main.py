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
                    # Spawn TNT at player position
                    self.world.spawn_tnt(self.player.x, self.player.y)
                elif event.key == pygame.K_r:
                    # Reset player position
                    self.player.x = SCREEN_WIDTH // 2
                    self.player.y = 100
                    self.player.velocity_y = 0
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
        # Update player
        self.player.update(dt, self.world)
        
        # Update world (TNT, particles)
        self.world.update(dt)
        
        # Update camera to follow player
        self.camera_x = max(0, self.player.x - SCREEN_WIDTH // 2)
        self.camera_y = max(0, self.player.y - SCREEN_HEIGHT // 2)
        
    def render(self):
        """Render everything to screen"""
        self.screen.fill(SKY_COLOR)
        
        # Render world with camera offset
        self.renderer.render_world(self.world, self.camera_x, self.camera_y)
        
        # Render player
        self.renderer.render_player(self.player, self.camera_x, self.camera_y)
        
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
        
        # Controls
        controls = [
            "A/D or Arrows: Move",
            "SPACE: Spawn TNT",
            "Click: Mine Block",
            "R: Reset Position",
            "ESC: Quit"
        ]
        y = 40
        for control in controls:
            text = font.render(control, True, (200, 200, 200))
            self.screen.blit(text, (10, y))
            y += 25
            
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
