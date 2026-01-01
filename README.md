# Minecraft-Style 2D Mining Game (Python/Pygame)

A fully functional 2D mining game inspired by Minecraft, built with Python and Pygame featuring procedural pixel art textures, physics, TNT explosions, and procedural sound effects.

## 🎮 Features

### Block System
- **12 Block Types**: Air, Dirt, Grass, Stone, Coal, Iron, Gold, Diamond, Mythic Ore, Bedrock, Water, Lava
- **16x16 Pixel Blocks** with procedural textures
- **Block Properties**: Health, hardness, mineable status
- **Minecraft-Style Colors** with pixel variation
- **Ore Sparkles**: Shimmering pixels on valuable ores

### Player Mechanics
- **32x32 Pixel Character** with pickaxe
- **Physics**: Gravity, collision detection, ground detection
- **Auto-Mining**: Automatically digs blocks below player
- **Manual Mining**: Click blocks to mine them
- **Animations**: Idle, mining, falling states

### TNT System
- **Physics-Based**: TNT falls under gravity
- **3-Second Fuse** with visual countdown
- **Explosion Radius**: Destroys blocks in 3-block radius
- **Chain Reactions**: Nearby TNT triggers explosively
- **Particle Debris**: Color-matched block particles

### Procedural Generation
- **Layered World**: Grass → Dirt → Stone → Bedrock
- **Random Ores**: Depth-based ore spawning
- **500 Blocks Deep**: Extensive mining opportunities
- **100 Blocks Wide**: Horizontal exploration

### Visual Effects
- **Procedural Textures**: Each block type has unique pixel patterns
- **Particle System**: Flying debris when blocks break
- **Health Bars**: Visual damage indicators on blocks
- **TNT Flash**: Warning flash before explosion
- **Smooth Animations**: Frame-based player animations

### Procedural Sound (Optional)
- **TNT Fuse**: High-pitch warning beep
- **Explosion**: Low-frequency boom
- **Block Break**: Sharp click sound
- **Digging**: Mining sound effect
- Generated using numpy + pygame.sndarray

## 📋 Requirements

```bash
pip install pygame numpy
```

**Minimum:**
- Python 3.7+
- pygame 2.0+
- numpy (optional, for sound)

## 🚀 Running the Game

```bash
cd python_game
python main.py
```

## 🎮 Controls

- **A / D** or **Left/Right Arrows**: Move player
- **Left Click**: Mine block manually
- **SPACE**: Spawn TNT at player position
- **R**: Reset player position
- **ESC**: Quit game

## 📁 Project Structure

```
python_game/
├── main.py                 # Game loop and initialization
├── constants.py            # Game configuration
├── block.py               # Block class
├── player.py              # Player character
├── world.py               # World generation and management
├── tnt.py                 # TNT entity
├── particle.py            # Particle effects
├── texture_generator.py   # Procedural texture creation
├── renderer.py            # Rendering system
├── sound_generator.py     # Procedural sound effects
└── README.md             # This file
```

## 🎨 Block Types & Colors

| Block | Color | Hardness | Depth | Value |
|-------|-------|----------|-------|-------|
| Dirt | #966F33 | 0.5 | Surface | Common |
| Grass | #00FF00 | 0.5 | Surface | Common |
| Stone | #7D7D7D | 2.0 | 20m+ | Common |
| Coal | #323232 | 3.0 | 20m+ | Common |
| Iron | #C0C0C0 | 5.0 | 40m+ | Uncommon |
| Gold | #FFD700 | 4.0 | 80m+ | Rare |
| Diamond | #00FFFF | 8.0 | 120m+ | Very Rare |
| Mythic Ore | #9400D3 | 10.0 | 200m+ | Ultra Rare |
| Bedrock | #202020 | ∞ | 480m+ | Unbreakable |

## 🔧 Customization

### Adjust Mining Speed
Edit `constants.py`:
```python
AUTO_DIG_DAMAGE = 20  # Damage per second
MANUAL_MINE_DAMAGE = 50  # Damage per click
```

### Change TNT Power
Edit `constants.py`:
```python
TNT_FUSE_TIME = 3.0  # Seconds
TNT_EXPLOSION_RADIUS = 3  # Blocks
```

### Modify Ore Spawn Rates
Edit `constants.py`:
```python
ORE_SPAWN_RATES = {
    'diamond': 0.002,  # Increase for more diamonds
    'mythic_ore': 0.001  # Make mythic ore more common
}
```

### Adjust World Size
Edit `constants.py`:
```python
CHUNK_WIDTH = 100  # Blocks wide
WORLD_HEIGHT = 500  # Blocks deep
```

## 🎯 Game Mechanics

### Mining System
- **Auto-Dig**: Player continuously mines blocks directly below
- **Manual Mining**: Click any block within reach to mine it
- **Block Health**: Each block has health that decreases with mining
- **Hardness**: Harder blocks take longer to mine

### TNT Mechanics
1. Press **SPACE** to spawn TNT
2. TNT falls under gravity
3. 3-second fuse countdown
4. Explosion destroys blocks in radius
5. Chain reactions trigger nearby TNT
6. Creates particle debris

### Physics
- **Gravity**: 800 pixels/second²
- **Terminal Velocity**: 600 pixels/second
- **Collision Detection**: AABB collision with blocks
- **Ground Detection**: Player knows when on solid ground

## 🏗️ Code Architecture

### Modular Design
- **Separation of Concerns**: Each system in separate file
- **Class-Based**: Object-oriented structure
- **Clear Interfaces**: Well-defined methods
- **Optimized Rendering**: Only renders visible blocks

### Key Classes

**Block**
- Properties: type, health, hardness
- Methods: `is_solid()`, `is_mineable()`, `damage()`

**Player**
- Properties: position, velocity, animation state
- Methods: `update()`, `move()`, `_auto_mine()`

**World**
- Properties: block grid, TNT list, particles
- Methods: `generate_world()`, `mine_block_at()`, `spawn_tnt()`

**TNT**
- Properties: position, velocity, fuse time
- Methods: `update()`, `should_explode()`

**TextureGenerator**
- Procedurally generates 16x16 pixel textures
- Caches textures for performance
- Different patterns for each block type

**Renderer**
- Handles all drawing operations
- Camera-based rendering
- Particle and effect rendering

## 🎨 Texture System

### Procedural Generation
Each block texture is generated pixel-by-pixel with:
- **Base Color**: Block type color
- **Noise**: Random variation (±20 brightness)
- **Patterns**: Type-specific patterns (grass top, ore sparkles)
- **Caching**: Generated once and reused

### Special Textures
- **Grass**: Green top with dirt bottom
- **Ores**: Stone background with colored sparkles
- **Water**: Semi-transparent with wave pattern
- **Lava**: Hot spots and flowing effect
- **TNT**: Red/white striped pattern

## 🔊 Sound System

### Procedural Audio
Sounds are generated using numpy waveform synthesis:
- **Beep**: Sine wave at 800Hz
- **Explosion**: Filtered noise + low rumble
- **Click**: Brief noise burst
- **Dig**: Filtered noise + tone

### No External Files
All sounds generated in code - no .wav files needed!

## 🎮 Gameplay Tips

1. **Dig Strategically**: Find a good spot and let auto-dig work
2. **Watch for Ores**: Look for sparkly blocks
3. **Use TNT Wisely**: Great for clearing large areas
4. **Avoid Bedrock**: You can't mine through it
5. **Go Deep**: Best ores are at great depths

## 🐛 Troubleshooting

**Game runs slowly:**
- Reduce world size in constants.py
- Disable particle effects
- Lower FPS target

**No sound:**
- Install numpy: `pip install numpy`
- Sound will auto-disable if numpy unavailable

**Blocks not mining:**
- Check block hardness
- Increase mining damage in constants.py

**TNT not spawning:**
- Press SPACE in open air (not inside blocks)

## 🚀 Performance

- **Optimized Rendering**: Only visible blocks drawn
- **Sparse Block Storage**: Empty air not stored
- **Texture Caching**: Textures generated once
- **Efficient Particles**: Limited particle count
- **60 FPS Target**: Smooth gameplay

## 📊 Technical Specs

- **Resolution**: 1280x720 (configurable)
- **Block Size**: 16x16 pixels
- **Player Size**: 32x32 pixels
- **World Size**: 100x500 blocks (16,000x80,000 pixels)
- **Frame Rate**: 60 FPS
- **Physics Rate**: 60 updates/second

## 🎓 Learning Resources

This project demonstrates:
- **Game Loop Architecture**: Update-Render pattern
- **2D Physics**: Gravity and collision detection
- **Procedural Generation**: Texture and world generation
- **Particle Systems**: Visual effects
- **State Management**: Player and world state
- **Modular Design**: Clean code structure

## 📝 License

MIT License - Free to use and modify!

## 🙏 Credits

- Inspired by Minecraft
- Built with Python + Pygame
- Procedural textures and sounds

---

**Enjoy Mining! ⛏️💎**
