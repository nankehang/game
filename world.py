"""
World generation and management
Handles block grid, TNT, and particle systems
"""

import random
from block import Block
from tnt import TNT
from particle import Particle
from explosion import Explosion
from item import Item
from meteor import Meteor
from sound_generator import sound_gen, SOUND_ENABLED
from constants import *

class World:
    """Manages the block world and entities"""
    
    def __init__(self):
        self.width = CHUNK_WIDTH
        self.height = WORLD_HEIGHT
        self.blocks = {}  # Dict for sparse storage {(x,y): Block}
        self.tnt_list = []
        self.particles = []
        self.explosions = []  # Explosion animations
        self.items = []  # Collectible items
        self.meteors = []  # Meteor shower
        
        # TNT spawning system
        self.tnt_spawn_timer = 0
        self.tnt_spawn_interval = TNT_SPAWN_INTERVAL
        self.total_tnt_spawned = 0
        
        # Meteor shower system (rare event)
        self.meteor_shower_timer = 0
        self.meteor_shower_interval = random.uniform(40, 60)  # Every 40-60 seconds
        self.meteor_shower_active = False
        self.meteor_shower_duration = 0
        self.meteor_spawn_timer = 0
        
        # Generate initial world
        self._generate_world()
        
        # Spawn test pickaxes (for demonstration)
        self._spawn_test_items()
    
    def _spawn_test_items(self):
        """Spawn some pickaxes for testing"""
        # Spawn one of each type near spawn
        spawn_y = (GRASS_LAYER + 1) * BLOCK_SIZE
        
        self.spawn_item(5 * BLOCK_SIZE, spawn_y, 'wood_pickaxe')
        self.spawn_item(8 * BLOCK_SIZE, spawn_y, 'stone_pickaxe')
        self.spawn_item(11 * BLOCK_SIZE, spawn_y, 'iron_pickaxe')
        self.spawn_item(14 * BLOCK_SIZE, spawn_y, 'diamond_pickaxe')
    
    def _generate_world(self):
        """Generate procedural world layers"""
        print("Generating world...")
        
        for x in range(self.width):
            for y in range(self.height):
                block_type = self._determine_block_type(x, y)
                if block_type != 'air':
                    self.blocks[(x, y)] = Block(block_type, x, y)
        
        print(f"World generated: {self.width}x{self.height} blocks")
    
    def _determine_block_type(self, x, y):
        """Determine block type based on position and randomness"""
        # Sky
        if y < GRASS_LAYER:
            return 'air'
        
        # Grass layer
        if y == GRASS_LAYER:
            return 'grass'
        
        # Dirt layer
        if y < DIRT_LAYER:
            return 'dirt'
        
        # Bedrock at bottom
        if y >= BEDROCK_START:
            return 'bedrock'
        
        # Stone layer with ores
        depth = y - STONE_START
        
        # Check for ore generation
        rand = random.random()
        
        if depth > 180 and rand < ORE_SPAWN_RATES['mythic_ore']:
            return 'mythic_ore'
        if depth > 100 and rand < ORE_SPAWN_RATES['diamond']:
            return 'diamond'
        if depth > 60 and rand < ORE_SPAWN_RATES['gold']:
            return 'gold'
        if depth > 20 and rand < ORE_SPAWN_RATES['iron']:
            return 'iron'
        if depth > 0 and rand < ORE_SPAWN_RATES['coal']:
            return 'coal'
        
        # Default to stone
        return 'stone'
    
    def get_block(self, x, y):
        """Get block at grid position"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.blocks.get((x, y), None)
    
    def set_block(self, x, y, block_type):
        """Set block at grid position"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        
        if block_type == 'air' or block_type is None:
            if (x, y) in self.blocks:
                del self.blocks[(x, y)]
        else:
            self.blocks[(x, y)] = Block(block_type, x, y)
    
    def mine_block_at(self, x, y, damage):
        """
        Apply damage to block at position
        Returns True if block was destroyed
        """
        block = self.get_block(x, y)
        
        if not block or not block.is_mineable():
            return False
        
        if block.damage(damage):
            # Block destroyed - create particles
            self._create_break_particles(x, y, block.type)
            
            # Play break sound
            if SOUND_ENABLED:
                sound_gen.play_block_break()
            
            # Remove block
            self.set_block(x, y, 'air')
            return True
        
        return False
    
    def _create_break_particles(self, x, y, block_type):
        """Create debris particles when block breaks"""
        world_x = x * BLOCK_SIZE + BLOCK_SIZE // 2
        world_y = y * BLOCK_SIZE + BLOCK_SIZE // 2
        
        color = BLOCK_COLORS.get(block_type, (255, 255, 255))
        
        # Create 8-12 particles
        num_particles = random.randint(8, 12)
        for _ in range(num_particles):
            particle = Particle(world_x, world_y, color)
            self.particles.append(particle)
    
    def spawn_tnt(self, x, y, fuse_time=None):
        """Spawn TNT at world position"""
        grid_x = int(x // BLOCK_SIZE)
        grid_y = int(y // BLOCK_SIZE)
        
        # Check if position is valid
        if self.get_block(grid_x, grid_y):
            return  # Can't spawn in solid block
        
        tnt = TNT(x, y, fuse_time)
        self.tnt_list.append(tnt)
        print(f"[TNT] Spawned at ({grid_x}, {grid_y}) with {tnt.fuse_time:.1f}s fuse")
    
    def spawn_item(self, x, y, item_type):
        """Spawn collectible item at world position"""
        item = Item(x, y, item_type)
        self.items.append(item)
        print(f"[ITEM] Spawned {item_type} at ({int(x)}, {int(y)})")
    
    def spawn_random_tnt_from_top(self, player_depth):
        """Spawn TNT from random position at top of screen"""
        # Calculate spawn chance based on depth
        depth_factor = player_depth * TNT_DEPTH_MULTIPLIER
        spawn_chance = TNT_BASE_SPAWN_CHANCE + depth_factor
        spawn_chance = min(0.95, spawn_chance)  # Cap at 95%
        
        if random.random() < spawn_chance:
            # Random horizontal position
            spawn_x = random.randint(1, self.width - 2) * BLOCK_SIZE
            spawn_y = 0  # Top of world
            
            # Spawn with random fuse time
            self.spawn_tnt(spawn_x, spawn_y)
            self.total_tnt_spawned += 1
            
            return True
        return False
    
    def _explode_tnt(self, tnt, player=None, game=None):
        """Handle TNT explosion"""
        # Play explosion sound
        if SOUND_ENABLED:
            sound_gen.play_explosion()
        
        center_x = int(tnt.x // BLOCK_SIZE)
        center_y = int(tnt.y // BLOCK_SIZE)
        
        # Create explosion animation
        explosion_x = center_x * BLOCK_SIZE + BLOCK_SIZE // 2
        explosion_y = center_y * BLOCK_SIZE + BLOCK_SIZE // 2
        self.explosions.append(Explosion(explosion_x, explosion_y))
        
        print(f"[TNT] BOOM at ({center_x}, {center_y})!")
        
        # Trigger screen shake and flash
        if game:
            # Shake intensity based on distance to player
            if player:
                dx = player.x - tnt.x
                dy = player.y - tnt.y
                distance_to_player = (dx * dx + dy * dy) ** 0.5
                max_shake_distance = (TNT_EXPLOSION_RADIUS + 5) * BLOCK_SIZE
                
                if distance_to_player < max_shake_distance:
                    shake_intensity = 15 * (1.0 - distance_to_player / max_shake_distance)
                    game.trigger_screen_shake(shake_intensity, 0.3)
            else:
                game.trigger_screen_shake(10, 0.3)
            
            game.trigger_flash((255, 200, 100), 180)
        
        # Apply knockback to player if nearby
        if player:
            dx = player.x + player.width / 2 - (tnt.x + tnt.width / 2)
            dy = player.y + player.height / 2 - (tnt.y + tnt.height / 2)
            distance = (dx * dx + dy * dy) ** 0.5
            
            max_knockback_distance = (TNT_EXPLOSION_RADIUS + 2) * BLOCK_SIZE
            
            if distance < max_knockback_distance:
                # Calculate knockback with improved physics
                if distance > 0:
                    # Normalize direction
                    dir_x = dx / distance
                    dir_y = dy / distance
                    
                    # Force decreases with distance (inverse square law, but clamped)
                    distance_ratio = 1.0 - (distance / max_knockback_distance)
                    force_multiplier = distance_ratio ** 0.7  # Power < 1 for smoother falloff
                    
                    # Base force
                    base_force = TNT_KNOCKBACK_FORCE
                    
                    # Apply force with upward bias (launch effect)
                    knockback_x = dir_x * base_force * force_multiplier
                    knockback_y = dir_y * base_force * force_multiplier
                    
                    # Add extra upward force for dramatic effect
                    if knockback_y > 0:  # If pushing down, reduce it
                        knockback_y *= 0.5
                    else:  # If pushing up, enhance it
                        knockback_y *= 1.5
                    
                    # Ensure minimum upward component
                    knockback_y = min(knockback_y, -base_force * 0.3)
                    
                    # Variable hurt duration based on distance
                    hurt_duration = 0.5 + (0.5 * distance_ratio)  # 0.5-1.0 seconds
                    
                    player.apply_knockback(knockback_x, knockback_y, hurt_duration)
                    print(f"[TNT] Player launched! Distance: {distance:.1f}, Force: ({knockback_x:.1f}, {knockback_y:.1f}), Hurt: {hurt_duration:.1f}s")
                else:
                    # Direct hit - maximum force
                    player.apply_knockback(0, -TNT_KNOCKBACK_FORCE * 1.5, 1.0)
                    print(f"[TNT] DIRECT HIT! Maximum knockback!")
        
        # Destroy blocks in radius
        destroyed_count = 0
        for dy in range(-TNT_EXPLOSION_RADIUS, TNT_EXPLOSION_RADIUS + 1):
            for dx in range(-TNT_EXPLOSION_RADIUS, TNT_EXPLOSION_RADIUS + 1):
                # Check if in circular radius
                distance = (dx * dx + dy * dy) ** 0.5
                if distance <= TNT_EXPLOSION_RADIUS:
                    bx = center_x + dx
                    by = center_y + dy
                    
                    block = self.get_block(bx, by)
                    if block and block.is_mineable():
                        self._create_break_particles(bx, by, block.type)
                        self.set_block(bx, by, 'air')
                        destroyed_count += 1
        
        # Create explosion particles
        for _ in range(30):
            particle = Particle(tnt.x, tnt.y, (255, 100, 0))
            particle.velocity_x = random.uniform(-200, 200)
            particle.velocity_y = random.uniform(-200, 200)
            particle.lifetime = 1.0
            self.particles.append(particle)
        
        print(f"Explosion destroyed {destroyed_count} blocks")
        
        # Check for chain reactions
        self._check_chain_reaction(center_x, center_y)
    
    def _check_chain_reaction(self, x, y):
        """Check if explosion triggers nearby TNT"""
        for tnt in self.tnt_list[:]:  # Copy list to avoid modification during iteration
            tnt_x = int(tnt.x // BLOCK_SIZE)
            tnt_y = int(tnt.y // BLOCK_SIZE)
            
            distance = ((tnt_x - x) ** 2 + (tnt_y - y) ** 2) ** 0.5
            if distance <= TNT_EXPLOSION_RADIUS + 1:
                # Trigger this TNT immediately
                tnt.fuse_time = 0
    
    def update(self, dt, player=None, game=None):
        """Update TNT and particles"""
        # Update meteor shower system
        self._update_meteor_shower(dt)
        
        # Update TNT spawn timer
        self.tnt_spawn_timer += dt
        if self.tnt_spawn_timer >= self.tnt_spawn_interval:
            self.tnt_spawn_timer = 0
            
            # Try to spawn TNT from top
            if player:
                player_depth = max(0, (player.y // BLOCK_SIZE) - GRASS_LAYER)
                if self.spawn_random_tnt_from_top(player_depth):
                    # Vary next spawn interval slightly
                    self.tnt_spawn_interval = TNT_SPAWN_INTERVAL + random.uniform(-1.0, 1.0)
        
        # Update TNT
        for tnt in self.tnt_list[:]:
            tnt.update(dt, self)
            
            if tnt.should_explode():
                self._explode_tnt(tnt, player, game)
                self.tnt_list.remove(tnt)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.is_dead():
                self.particles.remove(particle)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update(dt)
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        # Update items
        for item in self.items[:]:
            item.update(dt, self)
            
            # Check if player collects item
            if player and item.can_collect(player):
                print(f"[ITEM] Player collected {item.item_type}!")
                self.items.remove(item)
        
        # Update meteors
        for meteor in self.meteors[:]:
            meteor.update(dt)
            
            # Check if meteor should impact
            if meteor.should_impact(self):
                self._meteor_impact(meteor)
                self.meteors.remove(meteor)
    
    def get_visible_blocks(self, camera_x, camera_y, screen_width, screen_height):
        """Get blocks visible on screen for efficient rendering"""
        start_x = max(0, int(camera_x // BLOCK_SIZE) - 1)
        start_y = max(0, int(camera_y // BLOCK_SIZE) - 1)
        end_x = min(self.width, int((camera_x + screen_width) // BLOCK_SIZE) + 2)
        end_y = min(self.height, int((camera_y + screen_height) // BLOCK_SIZE) + 2)
        
        visible = []
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                block = self.get_block(x, y)
                if block:
                    visible.append((x, y, block))
        
        return visible

    def _update_meteor_shower(self, dt):
        """Update meteor shower event system"""
        self.meteor_shower_timer += dt
        
        # Check if it's time for a new meteor shower
        if not self.meteor_shower_active and self.meteor_shower_timer >= self.meteor_shower_interval:
            # Start meteor shower!
            self.meteor_shower_active = True
            self.meteor_shower_duration = random.uniform(12, 18)  # 12-18 seconds of chill shower
            self.meteor_shower_timer = 0
            self.meteor_spawn_timer = 0
            print("[METEOR SHOWER] ✨🌠 Beautiful meteor shower begins! 🌠✨")
        
        # Update active meteor shower
        if self.meteor_shower_active:
            self.meteor_shower_duration -= dt
            self.meteor_spawn_timer += dt
            
            # Spawn meteors during shower (every 0.5-1.2 seconds for chill effect)
            if self.meteor_spawn_timer >= random.uniform(0.5, 1.2):
                self.meteor_spawn_timer = 0
                self._spawn_meteor()
            
            # End shower
            if self.meteor_shower_duration <= 0:
                self.meteor_shower_active = False
                self.meteor_shower_timer = 0
                self.meteor_shower_interval = random.uniform(40, 60)  # Next shower in 40-60s
                print("[METEOR SHOWER] 🌙 The sky calms down... peaceful night returns.")
    
    def _spawn_meteor(self):
        """Spawn a single meteor from the sky"""
        # Spawn from top of screen, slightly off to the right
        spawn_x = random.uniform(self.width * BLOCK_SIZE * 0.3, self.width * BLOCK_SIZE * 0.9)
        spawn_y = -20  # Above screen
        
        meteor = Meteor(spawn_x, spawn_y)
        self.meteors.append(meteor)
    
    def _meteor_impact(self, meteor):
        """Handle meteor impact with ground"""
        block_x, block_y = meteor.get_block_pos()
        
        print(f"[METEOR] ✨ Impact at ({block_x}, {block_y})!")
        
        # Very soft impact - no destruction or only 1 block
        impact_radius = 0
        destroyed = 0
        
        # Only destroy block at exact impact point (30% chance)
        if random.random() < 0.3:
            if self.mine_block_at(block_x, block_y, 999):
                destroyed += 1
        
        # Create beautiful impact particles
        impact_particles = meteor.create_impact_particles()
        for particle_data in impact_particles:
            particle = Particle(
                particle_data['x'], 
                particle_data['y'],
                meteor.get_color_rgb()
            )
            # Override velocity with custom values
            particle.velocity_x = particle_data['vx']
            particle.velocity_y = particle_data['vy']
            particle.lifetime = particle_data['life']
            particle.max_lifetime = particle_data['max_life']
            self.particles.append(particle)
        
        # Spawn rare items (crystal or rare ore) - guaranteed drop!
        spawn_chance = random.random()
        if spawn_chance < 0.80:  # 80% chance for crystal
            self.spawn_item(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, 'crystal')
        else:  # 20% chance for rare ore
            self.spawn_item(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, 'rare_ore')
        
        # Soft sound effect
        if SOUND_ENABLED:
            sound_gen.play_meteor_impact()
    
    def is_meteor_shower_active(self):
        """Check if meteor shower is currently active"""
        return self.meteor_shower_active
