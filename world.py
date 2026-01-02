"""
World generation and management
Handles block grid, TNT, and particle systems
"""

import random
import math
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
        """Determine block type based on position, randomness, and biome"""
        # Determine biome based on X position
        biome = self._get_biome(x)
        
        # Sky
        if y < GRASS_LAYER:
            return 'air'
        
        # Grass layer (varies by biome)
        if y == GRASS_LAYER:
            if biome == 'ocean':
                return 'water'
            elif biome == 'desert':
                return 'sand'
            elif biome == 'jungle':
                return 'jungle_grass'
            elif biome == 'tundra':
                return 'snow'
            else:
                return 'grass'
        
        # Dirt/sand layer (varies by biome)
        if y < DIRT_LAYER:
            if biome == 'ocean':
                return 'sand'
            elif biome == 'desert':
                return 'red_sand'
            elif biome == 'jungle':
                return 'dirt'
            elif biome == 'tundra':
                return 'ice'
            else:
                return 'dirt'
        
        # First bedrock layer (portal to Nether)
        if y == BEDROCK_START:
            return 'bedrock'
        
        # NETHER DIMENSION (below bedrock)
        if y > BEDROCK_START:
            return self._determine_nether_block(x, y)
        
        # Stone layer with ores (above bedrock)
        depth = y - STONE_START
        
        # Check for ore generation (each ore gets its own random check)
        # Check rarest ores first
        if depth > 100 and random.random() < ORE_SPAWN_RATES['mythic_ore']:
            return 'mythic_ore'
        if depth > 60 and random.random() < ORE_SPAWN_RATES['diamond']:
            return 'diamond'
        if depth > 40 and random.random() < ORE_SPAWN_RATES['gold']:
            return 'gold'
        if depth > 20 and random.random() < ORE_SPAWN_RATES['iron']:
            return 'iron'
        if depth > 10 and random.random() < ORE_SPAWN_RATES['coal']:
            return 'coal'
        
        # Default to stone or biome-specific stone
        if biome == 'ocean':
            return 'ocean_stone'
        elif biome == 'jungle':
            # Add occasional vines and mossy stone
            if random.random() < 0.05:
                return 'mossy_stone'
            return 'stone'
        elif biome == 'desert':
            # Sandstone in desert
            if depth < 10:
                return 'sandstone'
            return 'stone'
        elif biome == 'tundra':
            # Packed ice in tundra
            if depth < 5:
                return 'packed_ice'
            return 'stone'
        else:
            return 'stone'
    
    def _get_biome(self, x):
        """Determine biome based on X position"""
        # Divide world into 5 biomes
        biome_size = self.width // 5
        
        if x < biome_size:
            return 'tundra'  # Snow biome
        elif x < biome_size * 2:
            return 'ocean'  # Ocean biome
        elif x < biome_size * 3:
            return 'normal'  # Normal terrain
        elif x < biome_size * 4:
            return 'jungle'  # Jungle biome
        else:
            return 'desert'  # Desert biome
    
    def _determine_nether_block(self, x, y):
        """Determine block type in the Nether dimension"""
        nether_depth = y - BEDROCK_START
        
        # Glowstone clusters (rare, near top)
        if nether_depth < 10 and random.random() < 0.03:
            return 'glowstone'
        
        # Nether quartz ore
        if random.random() < 0.08:
            return 'nether_quartz'
        
        # Soul sand patches
        if random.random() < 0.15:
            return 'soul_sand'
        
        # Nether brick structures
        if random.random() < 0.05:
            return 'nether_brick'
        
        # Default: Netherrack
        return 'netherrack'
    
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
    
    def mine_block_at(self, x, y, damage, game=None):
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
            
            # Track statistics
            if game and hasattr(game, 'stats'):
                game.stats.on_block_mined(y)
            
            # Drop items from ore blocks
            if block.type in ['coal', 'iron', 'gold', 'diamond']:
                # Spawn ore item at block location
                item_x = x * BLOCK_SIZE + BLOCK_SIZE // 2
                item_y = y * BLOCK_SIZE
                self.spawn_item(item_x, item_y, block.type + '_ore')
                print(f"[ORE DROP] {block.type} ore dropped!")
            
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
    
    def spawn_tnt(self, x, y, fuse_time=None, power_level=0):
        """Spawn TNT at world position"""
        grid_x = int(x // BLOCK_SIZE)
        grid_y = int(y // BLOCK_SIZE)
        
        # Check if position is valid (but allow air)
        block = self.get_block(grid_x, grid_y)
        if block and block.is_solid():
            return  # Can't spawn in solid block
        
        tnt = TNT(x, y, fuse_time, power_level)
        self.tnt_list.append(tnt)
        print(f"[TNT] Ignited at ({grid_x}, {grid_y}) with {tnt.fuse_time:.1f}s fuse, Power Level: {power_level}")
    
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
        # Play explosion sound with distance-based volume
        if SOUND_ENABLED:
            volume = 1.0
            if player:
                # Calculate distance from player
                distance = math.sqrt((tnt.x - player.x)**2 + (tnt.y - player.y)**2)
                max_distance = 500  # Maximum hearing distance
                volume = max(0.1, 1.0 - (distance / max_distance))
            sound_gen.play_explosion(volume)
        
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
                    
                    # Calculate damage based on TNT power level (1 base damage + 1 per 2 levels)
                    tnt_damage = 1 + (tnt.power_level // 2)
                    
                    player.apply_knockback(knockback_x, knockback_y, hurt_duration, damage=tnt_damage)
                    print(f"[TNT] Player launched! Distance: {distance:.1f}, Force: ({knockback_x:.1f}, {knockback_y:.1f}), Hurt: {hurt_duration:.1f}s, Damage: {tnt_damage}")
                else:
                    # Direct hit - maximum force and damage
                    tnt_damage = 2 + (tnt.power_level // 2)
                    player.apply_knockback(0, -TNT_KNOCKBACK_FORCE * 1.5, 1.0, damage=tnt_damage)
                    print(f"[TNT] DIRECT HIT! Maximum knockback! Damage: {tnt_damage}")
        
        # Apply knockback to nearby TNT entities (chain reaction)
        tnt_knockback_radius = (TNT_EXPLOSION_RADIUS + 3) * BLOCK_SIZE
        for other_tnt in self.tnt_list:
            if other_tnt is tnt:  # Skip the exploding TNT itself
                continue
                
            # Calculate distance from explosion center
            dx = other_tnt.x - tnt.x
            dy = other_tnt.y - tnt.y
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < tnt_knockback_radius and distance > 0:
                # Calculate knockback force
                dir_x = dx / distance
                dir_y = dy / distance
                
                # Force decreases with distance
                distance_ratio = 1.0 - (distance / tnt_knockback_radius)
                force_multiplier = distance_ratio ** 0.5
                
                # TNT gets stronger knockback than player
                base_force = TNT_KNOCKBACK_FORCE * 2.5
                
                # Apply force with upward bias
                knockback_x = dir_x * base_force * force_multiplier
                knockback_y = dir_y * base_force * force_multiplier
                
                # Add upward component to make TNT fly
                if knockback_y > 0:  # If pushing down
                    knockback_y *= 0.3
                else:  # If pushing up
                    knockback_y *= 1.2
                
                # Ensure minimum upward component
                knockback_y = min(knockback_y, -base_force * 0.4)
                
                # Apply velocity to TNT
                other_tnt.velocity_x = knockback_x
                other_tnt.velocity_y = knockback_y
                other_tnt.is_falling = True
                other_tnt.on_ground = False
                
                # Reduce fuse time slightly to create cascading effect
                other_tnt.fuse_time = min(other_tnt.fuse_time, random.uniform(1.0, 2.5))
                
                print(f"[TNT] Chain reaction! Pushed TNT at distance {distance:.1f}, Force: ({knockback_x:.1f}, {knockback_y:.1f}), New fuse: {other_tnt.fuse_time:.1f}s")
        
        # Destroy blocks in radius (with TNT power bonus)
        destroyed_count = 0
        
        # Calculate boosted radius from player's TNT power level
        base_radius = TNT_EXPLOSION_RADIUS
        if player:
            radius_bonus = int(player.tnt_power_level * 0.5)  # +0.5 blocks per level
            explosion_radius = base_radius + radius_bonus
            print(f"[TNT] Explosion radius: {explosion_radius} (base: {base_radius}, bonus: +{radius_bonus})")
        else:
            explosion_radius = base_radius
        
        for dy in range(-explosion_radius, explosion_radius + 1):
            for dx in range(-explosion_radius, explosion_radius + 1):
                # Check if in circular radius
                distance = (dx * dx + dy * dy) ** 0.5
                if distance <= explosion_radius:
                    bx = center_x + dx
                    by = center_y + dy
                    
                    block = self.get_block(bx, by)
                    if block and block.is_mineable():
                        self._create_break_particles(bx, by, block.type)
                        self.set_block(bx, by, 'air')
                        destroyed_count += 1
        
        # Create colored explosion particles based on TNT power level
        if tnt.power_level >= 5:
            particle_colors = [(255, 100, 255), (200, 0, 255), (255, 0, 200)]  # Pink/Purple
        elif tnt.power_level >= 2:
            particle_colors = [(150, 0, 255), (200, 50, 255), (100, 0, 200)]  # Purple
        else:
            particle_colors = [(255, 100, 0), (255, 150, 0), (255, 200, 0)]  # Orange/Yellow
        
        # Particle count increases with power level
        particle_count = 30 + (tnt.power_level * 10)
        for _ in range(particle_count):
            color = particle_colors[_ % len(particle_colors)]
            particle = Particle(tnt.x, tnt.y, color)
            particle.velocity_x = random.uniform(-200, 200) * (1 + tnt.power_level * 0.2)
            particle.velocity_y = random.uniform(-200, 200) * (1 + tnt.power_level * 0.2)
            particle.lifetime = 1.0 + (tnt.power_level * 0.2)
            self.particles.append(particle)
        
        print(f"Explosion destroyed {destroyed_count} blocks")
        
        # Trigger screen effects if game reference provided
        if game:
            game.explosion_flash = 0.5
            game.screen_shake = 10 * (1 + tnt.power_level * 0.3)
        
        # RARE ITEM DROPS from TNT! 
        drop_chance = random.random()
        if drop_chance < 0.10:  # 10% chance to drop rare item (reduced from 30%)
            rare_items = ['magnet', 'double_jump', 'speed_boost', 'shield', 'block_breaker']
            item_type = random.choice(rare_items)
            
            # Spawn item at explosion location with upward velocity
            item_x = tnt.x + random.uniform(-BLOCK_SIZE, BLOCK_SIZE)
            item_y = tnt.y - BLOCK_SIZE * 2  # Spawn above explosion
            
            self.spawn_item(item_x, item_y, item_type)
            print(f"[RARE DROP] {item_type}!")
            
            # Extra particles for item drop
            for _ in range(20):
                particle = Particle(item_x, item_y, (255, 255, 0))  # Gold sparkles
                particle.velocity_x = random.uniform(-100, 100)
                particle.velocity_y = random.uniform(-150, -50)
                particle.lifetime = 0.8
                self.particles.append(particle)
        
        # 5% chance to drop heart item (reduced from 15%)
        elif drop_chance < 0.15:
            item_x = tnt.x + random.uniform(-BLOCK_SIZE, BLOCK_SIZE)
            item_y = tnt.y - BLOCK_SIZE * 2
            self.spawn_item(item_x, item_y, 'heart')
            print(f"[HEART DROP] Heart item!")
        
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
        self._update_meteor_shower(dt, player)
        
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
            
            # Remove expired items
            if item.lifetime <= 0:
                print(f"[ITEM] {item.item_type} disappeared (not collected)")
                self.items.remove(item)
                continue
            
            # Check if player collects item
            if player and item.can_collect(player):
                print(f"[ITEM] Player collected {item.item_type}!")
                
                # Track in statistics (get game reference from player if available)
                if hasattr(player, 'game') and player.game and hasattr(player.game, 'stats'):
                    player.game.stats.on_item_collected(item.item_type)
                
                # Special item: Heart (increases max HP)
                if item.item_type == 'heart':
                    player.max_hp += 1
                    player.current_hp += 1  # Also heal
                    print(f"[HEART] +1 Max HP! Total: {player.max_hp}")
                
                # Ore items (coal, iron, gold, diamond) - just collect for score
                elif item.item_type in ['coal_ore', 'iron_ore', 'gold_ore', 'diamond_ore']:
                    ore_name = item.item_type.replace('_ore', '').upper()
                    print(f"[COLLECT] {ore_name} collected!")
                
                # Crystal and rare ore upgrade TNT power
                elif item.item_type in ['crystal', 'rare_ore']:
                    player.tnt_power_level += 1
                    player.tnt_power_bonus = player.tnt_power_level * 0.10
                    bonus_percent = int(player.tnt_power_bonus * 100)
                    print(f"[TNT POWER] +1 TNT Power Level! Level: {player.tnt_power_level} | Bonus: +{bonus_percent}%")
                    
                    # Also heal 1 HP
                    if player.current_hp < player.max_hp:
                        player.current_hp += 1
                        print(f"[HP] HP Restored! Current HP: {player.current_hp}/{player.max_hp}")
                
                # Level up mining speed for rare items (excluding crystal/rare_ore)
                elif item.is_rare:
                    player.mining_level += 1
                    player.level_up_flash = 0.5  # Flash effect for 0.5 seconds
                    # Recalculate bonus immediately to show correct value
                    player.mining_speed_bonus = min(2.0, player.mining_level * 0.10)
                    bonus_percent = int(player.mining_speed_bonus * 100)
                    print(f"[LEVEL UP] Mining Level: {player.mining_level} | Speed Bonus: +{bonus_percent}%")
                    
                    # Increase max HP on level up (every level)
                    player.max_hp += 1
                    print(f"[HEART] +1 Max HP from level up! Total: {player.max_hp}")
                    
                    # Heal 1 HP when collecting rare items
                    if player.current_hp < player.max_hp:
                        player.current_hp += 1
                        print(f"[HP] HP Restored! Current HP: {player.current_hp}/{player.max_hp}")
                
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

    def _update_meteor_shower(self, dt, player=None):
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
                # Pass player from update call chain if available
                self._spawn_meteor(player)
            
            # End shower
            if self.meteor_shower_duration <= 0:
                self.meteor_shower_active = False
                self.meteor_shower_timer = 0
                self.meteor_shower_interval = random.uniform(40, 60)  # Next shower in 40-60s
                print("[METEOR SHOWER] 🌙 The sky calms down... peaceful night returns.")
    
    def _spawn_meteor(self, player=None):
        """Spawn a single meteor from the sky near player"""
        # Spawn near player if available, otherwise random
        if player:
            # Spawn within 200 pixels of player
            player_x = player.x
            spawn_x = player_x + random.uniform(-200, 200)
            # Clamp to world bounds
            spawn_x = max(50, min(spawn_x, self.width * BLOCK_SIZE - 50))
        else:
            # Fallback to random spawn
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
        if spawn_chance < 0.60:  # 60% chance for crystal
            self.spawn_item(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, 'crystal')
        elif spawn_chance < 0.80:  # 20% chance for rare ore
            self.spawn_item(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, 'rare_ore')
        else:  # 20% chance for heart
            self.spawn_item(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, 'heart')
        
        # Soft sound effect
        if SOUND_ENABLED:
            sound_gen.play_meteor_impact()
    
    def is_meteor_shower_active(self):
        """Check if meteor shower is currently active"""
        return self.meteor_shower_active
