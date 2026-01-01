"""
World generation and management
Handles block grid, TNT, and particle systems
"""

import random
from block import Block
from tnt import TNT
from particle import Particle
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
        
        # Generate initial world
        self._generate_world()
    
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
    
    def spawn_tnt(self, x, y):
        """Spawn TNT at world position"""
        grid_x = int(x // BLOCK_SIZE)
        grid_y = int(y // BLOCK_SIZE)
        
        # Check if position is valid
        if self.get_block(grid_x, grid_y):
            return  # Can't spawn in solid block
        
        tnt = TNT(x, y)
        self.tnt_list.append(tnt)
        print(f"TNT spawned at ({grid_x}, {grid_y})")
    
    def _explode_tnt(self, tnt):
        # Play explosion sound
        if SOUND_ENABLED:
            sound_gen.play_explosion()
        
        """Handle TNT explosion"""
        center_x = int(tnt.x // BLOCK_SIZE)
        center_y = int(tnt.y // BLOCK_SIZE)
        
        print(f"TNT exploding at ({center_x}, {center_y})")
        
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
    
    def update(self, dt):
        """Update TNT and particles"""
        # Update TNT
        for tnt in self.tnt_list[:]:
            tnt.update(dt, self)
            
            if tnt.should_explode():
                self._explode_tnt(tnt)
                self.tnt_list.remove(tnt)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.is_dead():
                self.particles.remove(particle)
    
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
