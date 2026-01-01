"""
Game Constants and Configuration
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Block settings
BLOCK_SIZE = 16
CHUNK_WIDTH = 300  # Increased from 100 (3x wider)
WORLD_HEIGHT = 800  # Increased from 500 (deeper for Nether)

# Colors
SKY_COLOR = (15, 15, 40)  # Dark night sky

# Physics
GRAVITY = 1000  # pixels per second squared (increased for better feel)
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
    'tnt': (255, 0, 0),
    # Nether blocks
    'netherrack': (100, 40, 40),
    'soul_sand': (80, 60, 50),
    'nether_brick': (60, 20, 30),
    'glowstone': (255, 200, 100),
    'nether_quartz': (230, 225, 220),
    # Ocean blocks
    'sand': (230, 220, 170),
    'sandstone': (200, 180, 130),
    'ocean_stone': (100, 140, 180),
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
    'tnt': 1.0,
    # Nether blocks
    'netherrack': 0.8,
    'soul_sand': 1.0,
    'nether_brick': 3.0,
    'glowstone': 0.5,
    'nether_quartz': 4.0,
    # Ocean blocks
    'sand': 0.5,
    'sandstone': 1.5,
    'ocean_stone': 2.5,
}

# Ore spawn rates (chance per block at appropriate depth)
ORE_SPAWN_RATES = {
    'coal': 0.15,      # 15% at depth 10+ (very common)
    'iron': 0.10,      # 10% at depth 20+ (common)
    'gold': 0.06,      # 6% at depth 40+ (uncommon)
    'diamond': 0.03,   # 3% at depth 60+ (rare)
    'mythic_ore': 0.005  # 0.5% at depth 100+ (very rare)
}

# Layer depths
GRASS_LAYER = 10
DIRT_LAYER = 15
STONE_START = 20
BEDROCK_START = 480
