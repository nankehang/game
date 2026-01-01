# 🎮 Minecraft-Style 2D Mining Game - Quick Start

## Installation

### Windows
1. Install Python 3.7+ from [python.org](https://python.org)
2. Open terminal in `python_game` folder
3. Run:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

   Or double-click `run.bat`

### Linux/Mac
1. Ensure Python 3.7+ is installed
2. Open terminal in `python_game` folder
3. Run:
   ```bash
   pip3 install -r requirements.txt
   python3 main.py
   ```

   Or run `chmod +x run.sh && ./run.sh`

## Controls

- **A/D or Arrow Keys**: Move left/right
- **Left Click**: Mine block manually
- **SPACE**: Spawn TNT
- **R**: Reset position
- **ESC**: Quit

## Features

✅ **Procedural Pixel Art** - Minecraft-style 16x16 textures
✅ **12 Block Types** - Including rare ores
✅ **Auto-Mining** - Dig automatically while standing
✅ **TNT System** - Explosions with chain reactions
✅ **Particle Effects** - Flying debris
✅ **Procedural Sounds** - Generated audio effects
✅ **Physics** - Gravity, collisions, falling

## Tips

1. **Auto-dig**: Stand still to mine blocks below
2. **Manual mining**: Click blocks to mine faster
3. **Go deep**: Best ores spawn at 100+ depth
4. **Use TNT**: Clear large areas quickly
5. **Watch for sparkles**: Ores have shimmering pixels

## Customization

Edit `constants.py` to customize:
- Mining speed
- TNT power
- World size
- Ore spawn rates
- Physics settings

## Troubleshooting

**Import Error:**
```bash
pip install pygame numpy
```

**Sound Not Working:**
Sound will auto-disable if numpy unavailable. Install numpy for sound.

**Slow Performance:**
- Reduce CHUNK_WIDTH and WORLD_HEIGHT in constants.py
- Lower FPS in constants.py

---

**Enjoy! ⛏️💎**
