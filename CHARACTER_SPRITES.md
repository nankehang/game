# Character Sprite System

## Overview
The player character features detailed 32x32 pixel art sprites with multiple animation states, inspired by Minecraft's blocky aesthetic but with original design.

## Character Design

### Appearance
- **Head**: Square, blocky shape with beige/tan skin tone (255, 220, 177)
- **Face**: Two square eyes (2x2 pixels each) in neutral/square style
- **Body**: Blue shirt (60, 120, 220) with darker outline
- **Legs**: Dark blue pants (40, 60, 100)
- **Shoes**: Brown footwear (101, 67, 33)
- **Arms**: Skin-toned, blocky limbs
- **Weapon**: Pixel pickaxe with brown handle and gray metal head

### Style
- Minecraft-inspired blocky humanoid design
- Clean outlines for definition
- Side-view optimized for 2D platforming
- Transparent background (alpha channel)

## Animation States

### 1. Idle
- Standing still with pickaxe held at side
- Neutral square-eyed expression
- Stable, grounded pose

### 2. Walking (2 frames)
- **Frame 1**: Left leg forward, right leg back
- **Frame 2**: Right leg forward, left leg back
- Alternates every 0.2 seconds
- Triggered when horizontal velocity > 0.5

### 3. Mining (2 frames)
- **Frame 1**: Pickaxe raised above head
- **Frame 2**: Pickaxe lowered/swinging down
- Fast animation (0.15 seconds per frame)
- Triggered when standing on mineable blocks

### 4. Falling
- Arms raised up in surprised/flailing pose
- Wider eyes (3x3 pixels each)
- Pickaxe held tight in hand
- Triggered when not on ground

### 5. Knockback
- Body tilted back defensively
- Arms raised in protective pose
- Worried expression
- Pickaxe dropped/falling
- Duration: 0.3 seconds after knockback force applied

## Technical Implementation

### Sprite Generation
All sprites are procedurally generated in `player.py` using pixel-by-pixel drawing:
- No external image files required
- Consistent style and colors
- Easy to modify and customize

### Animation System
```python
# Animation states tracked per frame
self.animation_state = 'idle' | 'walk' | 'mining' | 'falling' | 'knockback'
self.animation_frame = 0 or 1  # For multi-frame animations
self.animation_timer = 0.0     # Frame timing
```

### Sprite Flipping
- Character automatically flips horizontally based on `facing_right` boolean
- Ensures correct orientation when moving left/right
- Handled in `get_texture()` method

### Color Palette
| Element | RGB Color | Description |
|---------|-----------|-------------|
| Skin | (255, 220, 177) | Face and arms |
| Skin Shadow | (200, 170, 130) | Outlines |
| Shirt | (60, 120, 220) | Blue torso |
| Shirt Shadow | (40, 80, 160) | Body outline |
| Pants | (40, 60, 100) | Dark blue legs |
| Shoes | (101, 67, 33) | Brown footwear |
| Eyes | (50, 50, 50) | Dark gray/black |
| Pickaxe Handle | (101, 67, 33) | Brown wood |
| Pickaxe Head | (150, 150, 150) | Light gray metal |
| Pickaxe Shadow | (100, 100, 100) | Dark gray metal |

## Usage

### Applying Knockback
```python
# Apply knockback force (e.g., from explosion)
player.apply_knockback(force_x=-5.0, force_y=-3.0)
```

### Getting Current Sprite
```python
# Returns appropriately animated and flipped texture
texture = player.get_texture()
```

### Animation Triggers
- **Idle**: Automatic when stationary and on ground
- **Walking**: Automatic when moving horizontally
- **Mining**: Automatic when on ground above mineable blocks
- **Falling**: Automatic when in air
- **Knockback**: Manual via `apply_knockback()` method

## Future Enhancements
Potential additions to the sprite system:
- Jumping animation (different from falling)
- Crouching/sneaking pose
- Tool variety (shovel, axe, sword)
- Damage/hurt flash effect
- Victory/celebration animation
- Swimming animation (for water blocks)
- Climbing animation (for ladders)
