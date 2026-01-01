"""
AI Bot that plays the game automatically
"""

import random
import math
from constants import *

class AIBot:
    """AI controller for automatic gameplay"""
    
    def __init__(self, player, world):
        self.player = player
        self.world = world
        self.enabled = False
        
        # AI state
        self.target_x = None
        self.target_y = None
        self.state = 'explore'  # explore, mine, collect, flee
        self.state_timer = 0
        self.decision_cooldown = 0
        
        # Behavior settings
        self.danger_radius = 100  # Distance to flee from TNT
        self.collect_radius = 150  # Distance to detect items
        self.mine_depth_target = 20  # How deep to mine
        
    def update(self, dt):
        """Update AI decision making and control player"""
        if not self.enabled:
            return
            
        self.state_timer += dt
        self.decision_cooldown -= dt
        
        # Make new decision every 0.5 seconds
        if self.decision_cooldown <= 0:
            self.make_decision()
            self.decision_cooldown = 0.5
        
        # Execute current behavior
        self.execute_behavior(dt)
    
    def make_decision(self):
        """Decide what action to take"""
        # Priority 1: Flee from nearby TNT
        nearest_tnt = self.find_nearest_tnt()
        if nearest_tnt:
            distance = math.sqrt((nearest_tnt.x - self.player.x)**2 + (nearest_tnt.y - self.player.y)**2)
            if distance < self.danger_radius:
                self.state = 'flee'
                self.target_x = self.player.x + (self.player.x - nearest_tnt.x) * 2  # Run away
                self.target_y = max(0, self.player.y - 100)  # Jump up
                return
        
        # Priority 2: Collect nearby items
        nearest_item = self.find_nearest_item()
        if nearest_item:
            distance = math.sqrt((nearest_item.x - self.player.x)**2 + (nearest_item.y - self.player.y)**2)
            if distance < self.collect_radius:
                self.state = 'collect'
                self.target_x = nearest_item.x
                self.target_y = nearest_item.y
                return
        
        # Priority 3: Mine downward if not deep enough
        player_block_y = int(self.player.y // BLOCK_SIZE)
        if player_block_y < self.mine_depth_target:
            self.state = 'mine'
            self.target_x = self.player.x
            self.target_y = self.player.y + BLOCK_SIZE * 3
        else:
            # Priority 4: Explore horizontally
            self.state = 'explore'
            # Random horizontal movement
            explore_range = 200
            self.target_x = self.player.x + random.randint(-explore_range, explore_range)
            self.target_x = max(50, min(self.target_x, CHUNK_WIDTH * BLOCK_SIZE - 50))
            self.target_y = self.player.y
    
    def execute_behavior(self, dt):
        """Execute the current behavior state"""
        if not self.target_x:
            return
        
        # Calculate direction to target
        dx = self.target_x - self.player.x
        dy = self.target_y - self.player.y
        
        # Horizontal movement
        if abs(dx) > 5:
            if dx > 0:
                self.player.move_direction = 1  # Move right
            else:
                self.player.move_direction = -1  # Move left
        else:
            self.player.move_direction = 0
        
        # Jumping behavior
        if self.state == 'flee':
            # Jump when fleeing and on ground (but not every frame)
            if self.player.on_ground and self.state_timer % 0.8 < 0.1:
                self.player.jump()
        elif self.state == 'mine':
            # Don't jump while mining - stay still
            self.try_mine_down()
        elif self.state == 'collect':
            # Jump only if item is above and far enough
            if dy < -30 and self.player.on_ground and abs(dx) < 50:
                self.player.jump()
        elif self.state == 'explore':
            # Jump over obstacles only, not randomly
            if self.is_obstacle_ahead() and self.player.on_ground:
                # Check if obstacle is high enough to require jump
                player_block_x = int(self.player.x // BLOCK_SIZE)
                if self.player.move_direction > 0:
                    check_x = player_block_x + 1
                else:
                    check_x = player_block_x - 1
                
                player_block_y = int(self.player.y // BLOCK_SIZE)
                # Only jump if there's actually a block in the way
                if 0 <= check_x < CHUNK_WIDTH and 0 <= player_block_y < WORLD_HEIGHT:
                    block = self.world.get_block(check_x, player_block_y)
                    if block and block != 'air':
                        self.player.jump()
    
    def try_mine_down(self):
        """Try to mine blocks below the player"""
        player_block_x = int(self.player.x // BLOCK_SIZE)
        player_block_y = int(self.player.y // BLOCK_SIZE)
        
        # Try to mine block directly below
        target_y = player_block_y + 2
        
        if 0 <= player_block_x < CHUNK_WIDTH and 0 <= target_y < WORLD_HEIGHT:
            block = self.world.get_block(player_block_x, target_y)
            if block and block != 'air' and block != 'bedrock':
                # Position player above the block to mine it
                target_x = player_block_x * BLOCK_SIZE + BLOCK_SIZE / 2
                
                # Move to position
                if abs(self.player.x - target_x) > 5:
                    if self.player.x < target_x:
                        self.player.move_direction = 1
                    else:
                        self.player.move_direction = -1
                else:
                    self.player.move_direction = 0
                    # Start mining
                    self.player.is_mining = True
                    return True
        
        self.player.is_mining = False
        return False
    
    def is_obstacle_ahead(self):
        """Check if there's an obstacle in front of the player"""
        player_block_x = int(self.player.x // BLOCK_SIZE)
        player_block_y = int(self.player.y // BLOCK_SIZE)
        
        # Check ahead based on movement direction
        check_x = player_block_x + (1 if self.player.move_direction > 0 else -1)
        
        if 0 <= check_x < CHUNK_WIDTH and 0 <= player_block_y < WORLD_HEIGHT:
            block = self.world.get_block(check_x, player_block_y)
            return block and block != 'air'
        
        return False
    
    def find_nearest_tnt(self):
        """Find the nearest TNT entity"""
        if not self.world.tnt_list:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for tnt in self.world.tnt_list:
            distance = math.sqrt((tnt.x - self.player.x)**2 + (tnt.y - self.player.y)**2)
            if distance < min_distance:
                min_distance = distance
                nearest = tnt
        
        return nearest
    
    def find_nearest_item(self):
        """Find the nearest collectible item"""
        if not self.world.items:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for item in self.world.items:
            distance = math.sqrt((item.x - self.player.x)**2 + (item.y - self.player.y)**2)
            if distance < min_distance:
                min_distance = distance
                nearest = item
        
        return nearest
    
    def toggle(self):
        """Toggle AI bot on/off"""
        self.enabled = not self.enabled
        if self.enabled:
            print("[AI BOT] Enabled - Bot is now playing!")
        else:
            print("[AI BOT] Disabled - Manual control resumed")
            # Reset player input
            self.player.move_direction = 0
            self.player.is_mining = False
