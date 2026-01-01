"""
Procedural sound generation using pygame.sndarray and numpy
Generates simple 8-bit style sound effects
"""

import pygame
import numpy as np

class SoundGenerator:
    """Generate procedural sound effects"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        self.sounds = {}
        self._generate_all_sounds()
    
    def _generate_all_sounds(self):
        """Pre-generate all sound effects"""
        self.sounds['tnt_fuse'] = self._generate_beep()
        self.sounds['explosion'] = self._generate_explosion()
        self.sounds['block_break'] = self._generate_click()
        self.sounds['dig'] = self._generate_dig()
    
    def _generate_beep(self, duration=0.1, frequency=800):
        """Generate high-pitch beep for TNT fuse"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        
        # Generate sine wave
        t = np.linspace(0, duration, samples)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Add envelope (fade in/out)
        envelope = np.ones_like(wave)
        fade_samples = samples // 10
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        wave *= envelope
        
        # Convert to 16-bit
        wave = np.int16(wave * 32767)
        
        return pygame.sndarray.make_sound(wave)
    
    def _generate_explosion(self, duration=0.5):
        """Generate low boom for explosion"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        
        # Generate noise with low-pass filter
        noise = np.random.uniform(-1, 1, samples)
        
        # Apply envelope (quick attack, slow decay)
        envelope = np.exp(-np.linspace(0, 8, samples))
        wave = noise * envelope
        
        # Add low frequency rumble
        t = np.linspace(0, duration, samples)
        rumble = np.sin(2 * np.pi * 60 * t) * 0.5
        wave += rumble * envelope
        
        # Normalize and convert
        wave = wave / np.max(np.abs(wave))
        wave = np.int16(wave * 32767 * 0.5)  # Lower volume
        
        return pygame.sndarray.make_sound(wave)
    
    def _generate_click(self, duration=0.05):
        """Generate short click for block break"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        
        # Generate brief noise burst
        wave = np.random.uniform(-0.5, 0.5, samples)
        
        # Sharp envelope
        envelope = np.exp(-np.linspace(0, 15, samples))
        wave *= envelope
        
        # Convert
        wave = np.int16(wave * 32767)
        
        return pygame.sndarray.make_sound(wave)
    
    def _generate_dig(self, duration=0.08):
        """Generate digging sound"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        
        # Generate filtered noise
        t = np.linspace(0, duration, samples)
        wave = np.random.uniform(-0.3, 0.3, samples)
        
        # Add tone
        tone = np.sin(2 * np.pi * 400 * t) * 0.2
        wave += tone
        
        # Envelope
        envelope = np.exp(-np.linspace(0, 10, samples))
        wave *= envelope
        
        # Convert
        wave = np.int16(wave * 32767)
        
        return pygame.sndarray.make_sound(wave)
    
    def play_sound(self, sound_name):
        """Play a generated sound effect"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Fail silently if sound can't play
    
    def play_tnt_fuse(self):
        """Play TNT fuse beep"""
        self.play_sound('tnt_fuse')
    
    def play_explosion(self):
        """Play explosion boom"""
        self.play_sound('explosion')
    
    def play_block_break(self):
        """Play block break click"""
        self.play_sound('block_break')
    
    def play_dig(self):
        """Play dig sound"""
        self.play_sound('dig')

# Global sound generator instance
try:
    sound_gen = SoundGenerator()
    SOUND_ENABLED = True
except:
    # If numpy not available, disable sound
    sound_gen = None
    SOUND_ENABLED = False
    print("Sound disabled (numpy not available)")
