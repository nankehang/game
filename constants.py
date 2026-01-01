"""
Game Constants and Configuration
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Block settings
BLOCK_SIZE = 16
CHUNK_WIDTH = 100
WORLD_HEIGHT = 500

# Colors
SKY_COLOR = (135, 206, 235)

# Physics
GRAVITY = 800  # pixels per second squared
PLAYER_SPEED = 150  # pixels per second
JUMP_FORCE = -400
TERMINAL_VELOCITY = 600

# Mining
AUTO_DIG_DAMAGE = 20  # Damage per second
MANUAL_MINE_DAMAGE = 50  # Damage per click

# TNT
TNT_FUSE_TIME = 3.0  # seconds
TNT_EXPLOSION_RADIUS = 3  # blocks
TNT_SPAWN_INTERVAL = 5.0  # Base seconds between TNT spawns
TNT_MIN_FUSE = 2.0  # Minimum fuse time
TNT_MAX_FUSE = 3.5  # Maximum fuse time
TNT_KNOCKBACK_FORCE = 150  # Knockback strength (reduced from 300)
TNT_BASE_SPAWN_CHANCE = 0.3  # 30% base chance per spawn check
TNT_DEPTH_MULTIPLIER = 0.02  # +2% per 10m depth

# Block definitions with Minecraft-like colors
BLOCK_COLORS = {
    'air': None,
    'dirt': (150, 111, 51),
    'grass': (0, 255, 0),
    'stone': (125, 125, 125),
    'coal': (50, 50, 50),
    'iron': (192, 192, 192),
    'gold': (255, 215, 0),
    'diamond': (0, 255, 255),
    'mythic_ore': (148, 0, 211),
    'bedrock': (32, 32, 32),
    'water': (63, 118, 228),
    'lava': (255, 69, 0),
    'tnt': (255, 0, 0)
}

# Block properties
BLOCK_HARDNESS = {
    'air': 0,
    'dirt': 0.5,
    'grass': 0.5,
    'stone': 2.0,
    'coal': 3.0,
    'iron': 5.0,
    'gold': 4.0,
    'diamond': 8.0,
    'mythic_ore': 10.0,
    'bedrock': float('inf'),
    'water': 0.1,
    'lava': 0.1,
    'tnt': 1.0
}

# Ore spawn rates (chance per block at appropriate depth)
ORE_SPAWN_RATES = {
    'coal': 0.02,      # 2% at depth 20+
    'iron': 0.01,      # 1% at depth 40+
    'gold': 0.005,     # 0.5% at depth 80+
    'diamond': 0.002,  # 0.2% at depth 120+
    'mythic_ore': 0.0005  # 0.05% at depth 200+
}

# Layer depths
GRASS_LAYER = 10
DIRT_LAYER = 15
STONE_START = 20
BEDROCK_START = 480
