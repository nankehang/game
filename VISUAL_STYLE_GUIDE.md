# 🎨 Visual Style Guide - Livestream Mining Game

## 🎯 Design Philosophy

**Core Aesthetic**: Minecraft-inspired 16-bit pixel art with modern particle effects and dynamic lighting optimized for livestream overlays.

**Key Principles**:
- **High Contrast**: Clear visibility against streaming overlays
- **Bright Particles**: Eye-catching effects for viewer engagement
- **Smooth Animations**: 60 FPS for professional stream quality
- **Transparent Background**: Clean overlay on livestream feed

---

## 🎨 Color Palette

### Primary Colors
```
Background    : Transparent / Dark (#0F0F28 if solid)
UI Elements   : White (#FFFFFF) with subtle glow
Warning       : Red (#FF0000) for TNT/danger
Success       : Green (#00FF00) for rewards
Epic          : Purple (#9400D3) for legendary items
```

### Block Color System
```
SKY LAYER (0-10m)
├─ Air            : Transparent
└─ Clouds         : White (#FFFFFF, 30% opacity)

SURFACE (10-20m)
├─ Grass          : Bright Green (#00FF00)
├─ Dirt           : Brown (#966F33)
└─ Stone          : Gray (#7D7D7D)

CAVE LAYER (20-100m)
├─ Stone          : Gray (#7D7D7D)
├─ Coal Ore       : Black (#323232) with sparkles
├─ Iron Ore       : Silver (#C0C0C0) with sparkles
└─ Gravel         : Gray-brown (#888877)

DEEP CAVE (100-300m)
├─ Deep Stone     : Dark Gray (#555555)
├─ Gold Ore       : Gold (#FFD700) with sparkles
├─ Diamond Ore    : Cyan (#00FFFF) with sparkles
└─ Lava Pockets   : Orange-Red (#FF4500)

MYTHIC DEPTHS (300m+)
├─ Obsidian       : Black (#1A1A1A)
├─ Mythic Ore     : Purple (#9400D3) with sparkles
├─ Crystal Blocks : Cyan (#00FFFF) translucent
└─ Bedrock        : Darkest Gray (#202020) UNBREAKABLE
```

---

## 👾 Character Design

### Player Sprite (32x32 pixels)

#### Base Character
```
Minecraft Steve-inspired design:
- Square head: 12x8 pixels (beige/tan #FFDCB1)
- Body: 12x10 pixels (blue shirt #3C78DC)
- Arms: 3x7 pixels each (beige)
- Legs: 3x10 pixels each (blue pants #2850A8)
- Eyes: 2x2 pixels black squares
- Mouth: 1-2 pixel line
```

#### Pickaxe Tool
```
Position: Held in right arm
Size: 10x6 pixels diagonal
Colors by tier:
- Wood   : Brown (#8B5A2B)
- Stone  : Gray (#808080)
- Iron   : Silver (#C8C8C8)
- Diamond: Cyan (#00FFFF)
- Mythic : Purple (#9400D3)
```

### Animation States

#### Idle Animation (60 FPS)
```
Frame 1-30: Normal stance
Frame 31-40: Slight head bob down (1px)
Frame 41-60: Return to normal
Total: 1 second loop
```

#### Mining Animation (8 frames)
```
Frame 1: Pickaxe raised (45° angle)
Frame 2: Pickaxe swing start
Frame 3-4: Pickaxe at bottom (impact frame)
Frame 5-6: Recoil
Frame 7-8: Return to raised
Duration: 0.133 seconds (8 frames @ 60 FPS)
Trigger: On viewer Like input
```

#### Collection Animation (12 frames)
```
Frame 1-3: Arms reach forward
Frame 4-6: Item absorbed (glow effect)
Frame 7-9: Arms pull back
Frame 10-12: Return to idle
Duration: 0.2 seconds
Trigger: When item collected
```

#### Knockback Animation (20 frames)
```
Frame 1-5: Spin 90° clockwise
Frame 6-10: Spin 180°
Frame 11-15: Spin 270°
Frame 16-20: Complete 360° and stabilize
Duration: 0.33 seconds
Trigger: TNT explosion nearby
Add: Screen shake (5px amplitude, 0.2s)
```

#### Level Up Animation (40 frames)
```
Frame 1-10: Character flashes white
Frame 11-20: Aura expands outward
Frame 21-30: Particles rise
Frame 31-40: Glow settles
Duration: 0.67 seconds
Effects: Screen flash (white), particle burst
```

---

## ✨ Particle Effects

### Mining Particles
```
Spawn: On block damage
Count: 3-8 per mining action (more if Like burst)
Color: Match mined block color
Size: 2x2 to 4x4 pixels
Velocity: Random outward (50-150 px/s)
Gravity: 400 px/s²
Lifespan: 0.5-1.0 seconds
Fade: Alpha 255 → 0 over lifespan
```

### TNT Explosion Particles
```
Spawn: On TNT detonation
Count: 50-100 particles
Types:
  - Fire: Orange (#FF8C00) 6x6 pixels
  - Smoke: Gray (#808080) 8x8 pixels
  - Debris: Block colors 4x4 pixels
Velocity: Radial outward (200-400 px/s)
Rotation: Random spin (180°/s)
Gravity: 300 px/s² (for debris)
Lifespan: 1.0-2.0 seconds
```

### Item Drop Trail
```
Spawn: Continuously while item falling
Count: 2-3 per frame
Color: Item-specific (gold, cyan, purple)
Size: 3x3 pixels
Velocity: Slight random offset
Gravity: None (fades in place)
Lifespan: 0.3 seconds
Effect: Sparkle/twinkle
```

### Item Collection Burst
```
Spawn: On item pickup
Count: 20-30 particles
Color: Item color + white sparkles
Pattern: Circular burst from item position
Velocity: 100-200 px/s outward
Fade: Quick (0.3 seconds)
Effect: Flash frame + sound
```

### Level Up Particles
```
Spawn: On subscriber level up
Count: 100+ particles
Types:
  - Rising sparkles (yellow/gold)
  - Expanding ring (white glow)
  - Confetti (multi-color)
Velocity: Upward (100-300 px/s) + random spread
Pattern: Fountain-like
Lifespan: 1.5-2.0 seconds
Effects: Screen glow, sound fanfare
```

---

## 💎 Buff Visual Effects

### Sword Buff Glow
```
Effect: Aura around player
Colors by tier:
  - Wood    : Brown (#8B5A2B, 30% opacity)
  - Stone   : Gray (#808080, 40% opacity)
  - Iron    : Silver (#C8C8C8, 50% opacity)
  - Diamond : Cyan (#00FFFF, 60% opacity)
  - Legendary: Rainbow cycle (70% opacity)

Rendering:
  - 2-pixel glow outline around sprite
  - Pulsing effect (0.5s cycle)
  - Multiply blend mode
```

### Rare Item Buffs

#### Magnet (Cyan Glow)
```
Color: Cyan (#00FFFF)
Effect: Rotating sparkles around player (8-12 particles)
Radius: 80 pixels
Rotation: 180°/s
Particle trail: Items curve toward player
```

#### Double Jump (Green Glow)
```
Color: Green (#00FF00)
Effect: Vertical energy lines along player
Count: 6 vertical lines
Animation: Rising (scrolling texture)
Jump trail: Green particles left behind
```

#### Speed Boost (Yellow Glow)
```
Color: Yellow (#FFFF00)
Effect: Motion blur + trailing afterimage
Afterimage: 3 fading copies behind player
Particles: Yellow speed lines
```

#### Shield (Blue Glow)
```
Color: Blue (#0080FF)
Effect: Hexagonal energy barrier
Size: 48x48 pixels
Animation: Rotating hexagon (60°/s)
Opacity: Pulses 40%-70%
```

#### Block Breaker (Red Glow)
```
Color: Red (#FF0000)
Effect: Shockwave rings
Count: 3 expanding rings
Speed: Expand 200 px/s
Lifespan: 0.5 seconds each
Trigger: On block break (3x3 area)
```

---

## 🎆 Level Visual Progression

### Level 1 (Base)
```
Sprite: Normal colors
Glow: None
Pickaxe: Wood (brown)
Effect: Standard animations
```

### Level 2 (White Glow)
```
Sprite: Normal colors
Glow: White outline (2px, 20% opacity)
Pickaxe: Stone (gray)
Effect: Faint sparkles on mining
```

### Level 3 (Blue Aura)
```
Sprite: Slightly brighter
Glow: Blue aura (3px, 30% opacity)
Pickaxe: Iron (silver)
Effect: Blue particles trail
```

### Level 4 (Purple Aura)
```
Sprite: Enhanced contrast
Glow: Purple aura (4px, 40% opacity)
Pickaxe: Diamond (cyan)
Effect: Purple energy crackles
```

### Level 5 (Golden Aura)
```
Sprite: Golden tint overlay
Glow: Gold aura (5px, 50% opacity)
Pickaxe: Golden (bright gold)
Effect: Gold particles constantly
```

### Level 6+ (Rainbow Aura)
```
Sprite: Brightness boost
Glow: Rainbow cycle (6px, 60% opacity)
Pickaxe: Rainbow shimmer
Effect: Rainbow trail + sparkles
Hue rotation: 360° over 2 seconds
```

---

## 🎯 UI Elements

### Mining Progress Bar
```
Position: Above mined block (centered)
Size: 32x4 pixels
Background: Dark gray (#333333)
Fill: Gradient based on health
  - 100-75%: Green (#00FF00)
  - 75-50%: Yellow (#FFFF00)
  - 50-25%: Orange (#FF8800)
  - 25-0%: Red (#FF0000)
Border: 1px black outline
Animation: Fill drains left-to-right
```

### Buff Icon Display
```
Position: Top-left corner (16px margin)
Icon Size: 24x24 pixels
Layout: Horizontal row, 4px spacing
Border: 2px white outline
Background: Semi-transparent black (60%)
Timer: Circular countdown overlay (white)
Glow: Buff color halo (4px)

Icons:
  - Sword: Crossed pickaxes
  - Magnet: Cyan horseshoe
  - Double Jump: Green wings
  - Speed: Yellow lightning bolt
  - Shield: Blue hexagon
  - Block Breaker: Red explosion
```

### Reaction Ticker
```
Position: Bottom-right corner (16px margin)
Size: 300x80 pixels (flexible height)
Background: Semi-transparent black (70%)
Border: 2px white outline
Font: Pixel font, 12px
Color: White text with colored icons

Format:
  💣 TNT from @username
  ⚔️ Sword drop from @viewer
  ⭐ @subscriber leveled you up!
  
Animation: Scroll up, fade in/out
Lifespan: 3 seconds per message
Max visible: 4 messages
```

### Like Counter
```
Position: Top-right corner (16px margin)
Size: 100x40 pixels
Background: Semi-transparent black (70%)
Border: 2px white outline
Font: Large pixel font, 24px

Display: 
  ❤️ 15 (current Like burst)
  
Color coding:
  - 1-10: White
  - 10-25: Yellow
  - 25-50: Orange
  - 50+: Red (pulsing)
  
Animation: Scale pulse on new Like
```

### Depth Meter
```
Position: Left side (centered vertically)
Size: 60x400 pixels
Background: Semi-transparent black (70%)
Border: 2px white outline

Display:
  ╔════════╗
  ║ 0m     ║ ← Surface marker
  ║        ║
  ║  You   ║ ← Player position (flashing)
  ║   ↓    ║
  ║        ║
  ║ 100m   ║ ← Milestone marker
  ║        ║
  ║ 500m   ║
  ║        ║
  ║ 1000m  ║
  ╚════════╝

Colors:
  - Surface: Green (#00FF00)
  - Milestones: Yellow (#FFFF00)
  - Player: White (blinking)
  - Background: Depth gradient (lighter → darker)
```

---

## 🎬 Screen Effects

### Screen Shake (TNT Explosion)
```
Trigger: TNT explosion within 5 blocks
Amplitude: 3-8 pixels (closer = stronger)
Duration: 0.2-0.4 seconds
Pattern: Random sine wave
Falloff: Linear over duration
```

### Screen Flash (Level Up)
```
Trigger: Player levels up
Color: White (#FFFFFF)
Opacity: 100% → 0%
Duration: 0.3 seconds
Easing: Exponential out
```

### Screen Glow (High Like Burst)
```
Trigger: 50+ simultaneous Likes
Color: Yellow-orange gradient (#FFFF00 → #FF8800)
Effect: Vignette glow from edges
Intensity: 30% opacity
Duration: 1.0 second
Pulse: 0.5 second cycle
```

### Mining Speed Indicator
```
Trigger: Active mining with speed boost
Effect: Motion lines from mined block
Color: Yellow (#FFFF00)
Count: Based on speed multiplier
  - 1x: No lines
  - 2x: 3 lines
  - 3x: 6 lines
  - 5x: 12 lines
Animation: Outward from impact point
```

---

## 🌈 Theme Variations

### Forest Theme
```
Sky: Light blue (#87CEEB)
Blocks: Green grass, brown dirt, gray stone
Decorations: Trees, leaves, flowers
Particles: Leaves falling slowly
Ambient: Birds, butterflies
```

### Cave Theme (Default)
```
Sky: Dark blue-gray (#0F0F28)
Blocks: Gray stone, ores with sparkles
Decorations: Stalactites, crystals
Particles: Dust motes floating
Ambient: Dripping water, echoes
```

### Lava Theme
```
Sky: Dark red (#330000)
Blocks: Dark stone, obsidian, lava
Decorations: Fire, magma pools
Particles: Embers rising, smoke
Ambient: Heat shimmer effect
Glow: Orange tint over entire scene
```

### Snow Theme
```
Sky: White-gray (#D3D3D3)
Blocks: White snow, ice, frozen stone
Decorations: Icicles, snowdrifts
Particles: Snowflakes falling
Ambient: Wind effect, frost
```

### Magic Theme
```
Sky: Purple gradient (#4B0082 → #9400D3)
Blocks: Crystal, enchanted stone, runes
Decorations: Floating crystals, magic circles
Particles: Sparkles, fairy dust
Ambient: Magical glow, starfield
Effect: Everything has subtle glow
```

---

## 🎮 Camera & Framing

### Camera Behavior
```
Position: Centered on player
Smooth follow: Lerp factor 0.1 (smooth lag)
Vertical priority: Keep player in upper 40% of screen
Horizontal lock: Player stays horizontally centered
Boundaries: Prevent showing out-of-world space
```

### Zoom Levels
```
Default: 1.0x (full pixel art clarity)
Mining Focus: 1.2x zoom (during intense mining)
Level Up: 1.5x zoom in → 1.0x zoom out (0.5s)
Overview: 0.8x zoom (when showing depth)
```

### Background Layers (Parallax)
```
Far Background (0.3x speed): Stars/sky
Mid Background (0.6x speed): Clouds/fog
Near Background (0.9x speed): Decorations
Foreground (1.0x speed): Blocks + player
```

---

## 📐 Layout Specifications

### 16:9 Livestream Overlay Layout
```
┌─────────────────────────────────────────────┐
│ [Buff Icons]              [Like Counter]    │ ← Top bar
│                                              │
│ [Depth]         GAME AREA           [Stats] │ ← Main game
│ [Meter]       (Player Mining)       [Panel] │
│                                              │
│                               [Reaction]     │ ← Bottom
│                               [Ticker]       │
└─────────────────────────────────────────────┘

Margins: 16px all sides
Safe area: 32px (for platform overlays)
Transparent background for clean stream overlay
```

### Resolution Support
```
1920x1080: Full HD (recommended)
1280x720: HD (supported)
2560x1440: 2K (supported, scales up)
3840x2160: 4K (supported, scales up)

Scaling: Integer multiples for pixel art clarity
UI Scale: Adjustable (100%, 125%, 150%)
```

---

## 🎨 Pixel Art Best Practices

### Sprite Creation
- Use 16x16 or 32x32 base sizes
- No anti-aliasing (pure pixel edges)
- Limited color palette per sprite (8-12 colors)
- 1-2 outline colors for definition
- Highlight + shadow for depth

### Animation Guidelines
- Squash & stretch for impact
- Anticipation frames before action
- Follow-through for weight
- Pixel-perfect alignment (no sub-pixel)
- Consistent frame timing (60 FPS base)

### Color Usage
- High saturation for key elements
- Darker shades for shadows (not just black)
- Highlight with lighter + more saturated
- Avoid pure black (use #1A1A1A)
- Use complementary colors for contrast

---

## 🚀 Performance Optimization

### Rendering Pipeline
```
1. Background layer (static, cached)
2. Block grid (only visible blocks)
3. Items (sorted by Y position)
4. Particles (pooled, batch rendered)
5. Player sprite (always on top)
6. UI elements (drawn last)
7. Screen effects (post-processing)
```

### Particle Pooling
- Pre-allocate 1000 particle objects
- Reuse inactive particles
- Cull off-screen particles
- Limit max active particles: 500

### Texture Caching
- Generate all block textures at startup
- Store in dictionary by type
- Avoid runtime texture generation
- Use sprite sheets for UI

---

## 🎯 Accessibility Considerations

### High Contrast Mode
- Thicker outlines on all sprites (3px instead of 2px)
- Brighter colors (increase saturation +20%)
- Larger UI elements (+25% scale)
- Clearer text (white on black, no transparency)

### Colorblind Support
- Option to add patterns to color-coded elements
- Shape differentiation (not just color)
- Icons with clear shapes
- Text labels on important elements

### Reduced Motion
- Option to disable screen shake
- Reduce particle count (50% reduction)
- Slower/simpler animations
- Static buff indicators (no pulse)

---

## 📝 Summary

This visual style creates:
- **Clear, readable pixel art** optimized for streaming
- **Eye-catching particle effects** for viewer engagement
- **Professional polish** with smooth animations
- **Scalable UI** that works at any resolution
- **High visibility** against stream overlays
- **Consistent aesthetic** across all elements

**Result**: A visually spectacular, instantly recognizable game perfect for livestream entertainment.

---

*"Every pixel tells a story. Every effect engages a viewer."*
