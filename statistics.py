"""
Game statistics tracker for AFK streaming
"""

class Statistics:
    """Track game statistics for display"""
    
    def __init__(self):
        # Mining stats
        self.blocks_mined = 0
        self.total_depth = 0
        self.deepest_depth = 0
        
        # Item stats
        self.items_collected = 0
        self.rare_items_collected = 0
        self.coal_collected = 0
        self.iron_collected = 0
        self.gold_collected = 0
        self.diamond_collected = 0
        self.hearts_collected = 0
        
        # Combat stats
        self.deaths = 0
        self.explosions_survived = 0
        self.damage_taken = 0
        
        # Time stats
        self.play_time = 0.0
        self.time_since_death = 0.0
        
        # Achievements
        self.achievements = set()
        self.new_achievements = []  # For popup display
        
    def update(self, dt):
        """Update time-based stats"""
        self.play_time += dt
        self.time_since_death += dt
    
    def on_block_mined(self, depth):
        """Called when a block is mined"""
        self.blocks_mined += 1
        self.deepest_depth = max(self.deepest_depth, depth)
        
        # Check achievements
        if self.blocks_mined == 100:
            self.unlock_achievement("First Hundred!", "Mine 100 blocks")
        elif self.blocks_mined == 1000:
            self.unlock_achievement("Mining Master", "Mine 1,000 blocks")
        elif self.blocks_mined == 5000:
            self.unlock_achievement("Mining Legend", "Mine 5,000 blocks")
        
        if depth >= 50:
            self.unlock_achievement("Deep Diver", "Reach depth 50")
        if depth >= 100:
            self.unlock_achievement("Abyss Explorer", "Reach depth 100")
    
    def on_item_collected(self, item_type):
        """Called when an item is collected"""
        self.items_collected += 1
        
        if item_type in ['magnet', 'double_jump', 'speed_boost', 'shield', 'block_breaker', 
                         'crystal', 'rare_ore', 'heart']:
            self.rare_items_collected += 1
        
        if item_type == 'coal_ore':
            self.coal_collected += 1
        elif item_type == 'iron_ore':
            self.iron_collected += 1
        elif item_type == 'gold_ore':
            self.gold_collected += 1
        elif item_type == 'diamond_ore':
            self.diamond_collected += 1
            self.unlock_achievement("Diamond Hunter", "Collect a diamond")
        elif item_type == 'heart':
            self.hearts_collected += 1
        
        # Achievements
        if self.items_collected == 50:
            self.unlock_achievement("Collector", "Collect 50 items")
        if self.rare_items_collected == 10:
            self.unlock_achievement("Treasure Hunter", "Collect 10 rare items")
    
    def on_death(self):
        """Called when player dies"""
        self.deaths += 1
        self.time_since_death = 0.0
        
        if self.deaths == 1:
            self.unlock_achievement("First Blood", "Die for the first time")
    
    def on_damage_taken(self, damage):
        """Called when player takes damage"""
        self.damage_taken += damage
    
    def on_explosion_survived(self):
        """Called when player survives an explosion"""
        self.explosions_survived += 1
        
        if self.explosions_survived == 10:
            self.unlock_achievement("Blast Resistant", "Survive 10 explosions")
    
    def unlock_achievement(self, name, description):
        """Unlock an achievement"""
        if name not in self.achievements:
            self.achievements.add(name)
            self.new_achievements.append({
                'name': name,
                'description': description,
                'timer': 5.0  # Display for 5 seconds
            })
            print(f"[ACHIEVEMENT] {name}: {description}")
    
    def update_achievements(self, dt):
        """Update achievement popup timers"""
        for achievement in self.new_achievements[:]:
            achievement['timer'] -= dt
            if achievement['timer'] <= 0:
                self.new_achievements.remove(achievement)
    
    def get_summary(self):
        """Get statistics summary as dict"""
        return {
            'blocks_mined': self.blocks_mined,
            'deepest_depth': self.deepest_depth,
            'items_collected': self.items_collected,
            'rare_items': self.rare_items_collected,
            'deaths': self.deaths,
            'play_time': self.play_time,
            'time_alive': self.time_since_death,
            'achievements': len(self.achievements)
        }
