# 🎮 Livestream Viewer Interaction Design Document

## Overview
Transform the existing 2D mining game into a **viewer-driven interactive livestream experience** where audience reactions directly control gameplay mechanics.

## 🎯 Core Design Philosophy

### No Auto-Mining
- **Current System**: Player auto-digs blocks continuously
- **New System**: Mining **ONLY** occurs when viewers react (Like button)
- **Player stays stationary horizontally** - purely vertical mining gameplay
- All mining is viewer-driven, creating high engagement

---

## 📊 Viewer Interaction Mechanics

### 1. LIKE Button → Mining System

#### Base Mechanic
- **1 Like = 1 Mining Action**
- Each Like applies damage to the block directly below the player
- Mining animation + particles appear on viewer input

#### Dynamic Mining Speed Scaling
```
Simultaneous Likes → Mining Speed Multiplier
──────────────────────────────────────────
1 Like          → 1x speed (20 damage/sec)
5 Likes         → 1.5x speed
10 Likes        → 2x speed
25 Likes        → 3x speed
50+ Likes       → 5x speed (capped)
```

#### Implementation Strategy
- Track Like count in rolling 1-second window
- Apply mining speed multiplier based on concurrent Likes
- Visual feedback: Mining progress bar scales with speed
- Particle density increases with more Likes

#### Mining Feedback
- **Mining Animation**: Pickaxe swings on each Like
- **Block Damage**: Health bar decreases proportionally
- **Particle Effects**: More particles = more Likes
- **Sound Effects**: Mining sounds layer based on intensity
- **Screen Effects**: Glow/flash on high Like bursts

---

### 2. LIKE Volume → TNT Spawning

#### TNT Spawn Triggers
```
Like Burst Size → TNT Type
─────────────────────────────────────
1-5 Likes       → No TNT
5-10 Likes      → 30% chance normal TNT
10-20 Likes     → 60% chance normal TNT
20-30 Likes     → 80% chance normal TNT + 20% sticky TNT
30-50 Likes     → 100% normal TNT + 40% sticky TNT
50+ Likes       → Multi-TNT + Air-burst TNT
```

#### TNT Types

**Normal TNT**
- Falls with gravity (500 px/s²)
- 3-second fuse
- Explosion radius: 3 blocks (120px)
- Spawns at/above player position

**Sticky TNT** *(High Like Volume)*
- Spawns and sticks to blocks near player
- 4-second fuse
- Larger explosion radius: 4 blocks
- Red + black pattern

**Air-burst TNT** *(50+ Likes)*
- Spawns high above player
- Explodes mid-air at set height
- Wide horizontal blast
- Golden glow effect

#### TNT Physics
- Gravity: 500 px/s²
- Max fall speed: 150 px/s
- Explosion force: 450 (knockback)
- Player knockback: Light push away from blast

---

### 3. SHARE Button → Sword/Item Drops

#### Sword System
- **Share = Sword Drop from Sky**
- Swords fall from top of screen
- Player collects → Mining speed buff

#### Sword Tiers
```
Random Sword Type → Mining Speed Buff
──────────────────────────────────────
Wood Sword      → +10% mining speed (5 sec)
Stone Sword     → +20% mining speed (8 sec)
Iron Sword      → +35% mining speed (10 sec)
Diamond Sword   → +50% mining speed (15 sec)
Legendary Sword → +100% mining speed (20 sec)
```

#### Sword Drop Physics
- Gravity: 300 px/s²
- Max fall speed: 120 px/s
- Rotation: ±20 deg/s (spinning effect)
- Collection radius: 24-32 px
- Glow aura: Brighter = more powerful

#### Sword Fusion
- Multiple swords collected → Stack buffs
- Max 3 active buffs at once
- Stacked buffs show as glowing aura layers

---

### 4. SHARE Volume → Rare Item Drops

#### Rare Items (High Share Volume)
```
Share Count → Rare Item Chance
────────────────────────────────
1-2 Shares  → 10% rare item
3-5 Shares  → 30% rare item
5-10 Shares → 60% rare item
10+ Shares  → 100% rare item + bonus
```

#### Rare Item Types

**Magnet** *(Cyan glow)*
- Duration: 10 seconds
- Auto-collects items within 5-block radius
- Items fly toward player

**Double Jump** *(Green glow)*
- Duration: 15 seconds
- Press SPACE mid-air for second jump
- Allows dodging TNT

**Speed Boost** *(Yellow glow)*
- Duration: 8 seconds
- +200% mining speed
- Golden particle trail

**Shield** *(Blue glow)*
- Duration: 12 seconds
- Immune to TNT knockback
- Blue energy barrier visual

**Block Breaker** *(Red glow)*
- Duration: 6 seconds
- Mines 3x3 area at once
- Red shockwave effect

---

### 5. SUBSCRIBE / HIGH-TIER Reactions

#### Level Up System
- **Subscriber = Instant Level Up**
- Player gains permanent mining power boost
- Visual transformation: Glow + aura

#### Level Benefits
```
Level → Mining Power → Visual Effect
─────────────────────────────────────────
Lv 1   → Base power   → Normal sprite
Lv 2   → +10% power   → White glow
Lv 3   → +25% power   → Blue aura
Lv 4   → +40% power   → Purple aura
Lv 5   → +60% power   → Golden aura
Lv 6+  → +80% power   → Rainbow aura
```

#### Special Subscriber Events

**Sword Storm** *(5 Subscribers in 10 sec)*
- 20 swords rain from sky
- All buffs stack temporarily
- Screen flashes gold

**Massive Loot Drop** *(10 Subscribers)*
- Mix of all rare items spawn
- Guaranteed legendary sword
- Rainbow particle effects

**Mining Frenzy** *(Tier 3 Sub)*
- 30-second instant mining mode
- All blocks below player break instantly
- Player descends rapidly
- Purple lightning effects

---

## 🎨 Visual Design System

### Character Design
- **Base Sprite**: 32x32 pixel Steve-like character
- **Pickaxe**: Visible tool that swings on mining
- **Glow Layers**: Stacking buffs = more glow
- **Level Aura**: Expands with higher level

### Animation States
1. **Idle**: Subtle breathing animation
2. **Mining**: Pickaxe swing (triggered by Like)
3. **Collecting**: Reach out grab animation
4. **Knockback**: Spin + hurt animation
5. **Level Up**: Flash + expand + particle burst

### Particle Effects

**Mining Particles**
- Color-matched to mined block
- Quantity scales with Like volume
- Fly outward in arc pattern

**TNT Explosion**
- Fire + smoke particles
- Shockwave ring expands
- Block debris scatter

**Item Collection**
- Sparkle trail toward player
- Fusion flash on contact
- Buff glow persists

**Level Up**
- Energy burst from player
- Rising sparkles
- Screen flash (gold/rainbow)

### UI Elements

**Mining Progress Bar**
- Above mined block
- Color: Yellow → Red (low health)
- Width scales with mining speed

**Buff Icons** *(Top-left)*
- Shows active buffs
- Timer countdown
- Glow when activated

**Reaction Ticker** *(Bottom-right)*
- Scrolling viewer actions
- "💣 TNT from @viewer!"
- "⚔️ Sword from @username"
- "@subscriber just leveled you up!"

**Like Counter** *(Top-right)*
- Shows current Like burst count
- Color scales with intensity
- Pulses on new Likes

**Depth Meter** *(Left side)*
- Shows how deep player has mined
- Milestone markers (100m, 500m, 1000m)

---

## ⚙️ Technical Implementation

### Viewer Input Queue System
```python
class ViewerInputQueue:
    - like_queue: deque[Like]
    - share_queue: deque[Share]
    - subscribe_queue: deque[Subscribe]
    
    def process_likes(dt):
        # Count Likes in 1-sec window
        # Calculate mining speed multiplier
        # Check TNT spawn threshold
    
    def process_shares(dt):
        # Spawn sword drops
        # Check rare item threshold
    
    def process_subscribes(dt):
        # Instant level up
        # Check special event thresholds
```

### Mining System Refactor
```python
class Player:
    def mine_block(self, world, like_count):
        # Remove auto-mining
        # Only mine on viewer input
        # Apply speed multiplier
        # Trigger animations
```

### TNT Spawning Logic
```python
class TNTSpawner:
    def check_spawn(like_burst_count):
        if like_burst_count >= 50:
            spawn_airburst_tnt()
        elif like_burst_count >= 30:
            spawn_sticky_tnt()
        elif like_burst_count >= 10:
            if random() < 0.6:
                spawn_normal_tnt()
```

### Item Drop System
```python
class ItemDropManager:
    def spawn_sword(share_count):
        tier = calculate_sword_tier(share_count)
        sword = Sword(tier, spawn_position)
        world.items.append(sword)
    
    def spawn_rare_item(share_count):
        if should_spawn_rare(share_count):
            item_type = random_rare_item()
            item = RareItem(item_type, spawn_position)
            world.items.append(item)
```

---

## 🎯 Livestream Integration APIs

### Platform Integration Options

#### TikTok LIVE
```python
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import LikeEvent, ShareEvent, SubscribeEvent

client = TikTokLiveClient("@username")

@client.on("like")
async def on_like(event: LikeEvent):
    game.queue_likes(event.count)

@client.on("share")
async def on_share(event: ShareEvent):
    game.queue_share(event.user.username)

@client.on("subscribe")
async def on_subscribe(event: SubscribeEvent):
    game.queue_subscribe(event.user.username)
```

#### YouTube Live
```python
from pytchat import LiveChat

chat = LiveChat(video_id="...")

while chat.is_alive():
    data = chat.get()
    for msg in data.items:
        if msg.type == "superChat":
            game.queue_subscribe(msg.author.name)
        # Parse reactions from chat
```

#### Twitch
```python
from twitchio.ext import commands

class Bot(commands.Bot):
    async def event_message(self, message):
        if "!mine" in message.content:
            game.queue_likes(1)
        if "!tnt" in message.content:
            game.queue_likes(15)  # Trigger TNT
```

---

## 🎮 Gameplay Balance

### Mining Speed Progression
- **Early Game**: Slow mining, each Like matters
- **Mid Game**: Sword buffs accelerate progress
- **Late Game**: Level stacking = rapid descent

### TNT Balance
- **Low Volume**: Occasional TNT keeps game dynamic
- **High Volume**: TNT becomes main hazard
- **Player Skill**: Learning to dodge explosions

### Buff Management
- **Cooldowns**: Prevent permanent god mode
- **Stacking Limits**: Max 3 buffs active
- **Synergy**: Some buffs combo well

### Depth Scaling
- **Deeper = Harder Blocks**
- **More Likes needed** to break deep blocks
- **Better rewards** at greater depths

---

## 🌟 Engagement Features

### Milestone Events
- **100m Depth**: Sword Storm
- **500m Depth**: Meteor Shower
- **1000m Depth**: Legendary Item guaranteed

### Viewer Leaderboard
- Top contributors shown on-screen
- Most Likes, Most TNT triggered, etc.

### Goal Systems
- "Get to 500m!" → Countdown timer
- "Break 1000 blocks!" → Progress bar
- "Survive 50 TNT!" → Counter

### Theme Variations
- **Forest**: Green blocks, leaves, vines
- **Cave**: Gray stone, crystals, bats
- **Lava**: Red blocks, fire, magma
- **Snow**: White/blue blocks, ice, snowflakes
- **Magic**: Purple blocks, stars, runes

---

## 📈 Viewer Psychology

### Why This Design Works

**Immediate Feedback**
- Every Like = visible action
- Players see their impact instantly

**Escalating Excitement**
- More viewers = more chaos = more fun
- TNT + items + mining = visual spectacle

**Social Collaboration**
- Viewers work together to progress
- "Spam Likes to break this block!"
- "Everyone Share for Sword Storm!"

**Risk vs Reward**
- TNT can help (clear blocks) or hurt (knockback)
- Viewers balance mining speed vs chaos

**Long-term Goals**
- Level progression keeps viewers invested
- Depth milestones create narrative

---

## 🚀 Implementation Roadmap

### Phase 1: Core Viewer Input System ✅
- [ ] Create ViewerInputQueue class
- [ ] Implement mock input simulator for testing
- [ ] Remove auto-mining from player
- [ ] Add Like-triggered mining

### Phase 2: Mining Speed Scaling ✅
- [ ] Track simultaneous Like count
- [ ] Calculate mining speed multiplier
- [ ] Update mining damage formula
- [ ] Add visual feedback (progress bar scaling)

### Phase 3: TNT Spawn System ✅
- [ ] Implement Like burst detection
- [ ] Add TNT spawn thresholds
- [ ] Create sticky TNT variant
- [ ] Create air-burst TNT variant

### Phase 4: Item Drop System ✅
- [ ] Sword spawning on Share
- [ ] Sword tier randomization
- [ ] Buff stacking system
- [ ] Rare item spawn logic

### Phase 5: Level Up System ✅
- [ ] Subscribe event handling
- [ ] Player level tracking
- [ ] Visual glow/aura effects
- [ ] Special subscriber events

### Phase 6: UI & Feedback ✅
- [ ] Reaction ticker overlay
- [ ] Like counter display
- [ ] Buff icon display
- [ ] Depth meter

### Phase 7: Livestream Integration ✅
- [ ] TikTok LIVE API connection
- [ ] YouTube Live API connection
- [ ] Twitch chat integration
- [ ] Test with real viewers

---

## 🎨 Final Polish

### Visual Enhancements
- Glow shaders for buffed player
- Screen shake on TNT explosions
- Smooth camera follow player descent
- Particle effects everywhere

### Audio Design
- Mining sound layers
- TNT fuse beeping
- Explosion bass boom
- Item collection ding
- Level up fanfare

### Performance Optimization
- Particle pooling
- Texture caching
- Efficient collision detection
- Background thread for API

---

## 📝 Summary

This design transforms a standard mining game into an **interactive livestream phenomenon** where:

1. **Viewers control mining** through Likes
2. **Chaos emerges** from TNT spawns
3. **Rewards rain** from Shares
4. **Power grows** from Subscribers
5. **Community bonds** through shared goals

The result is a **highly engaging, visually spectacular, viewer-driven experience** perfect for livestream entertainment.

---

*"Every Like matters. Every Share helps. Every Subscriber transforms the game."*
