"""
Procedural sound generation using pygame.sndarray and numpy
Generates simple 8-bit style sound effects
"""

import pygame
import numpy as np

class SoundGenerator:
    """Generate procedural sound effects"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
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
        
        # Convert mono to stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_explosion(self, duration=0.6):
        """Generate retro 8-bit explosion with strong impact"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Phase 1: Initial blast (0-0.1s) - Sharp, low-frequency impact
        blast_duration = 0.1
        blast_samples = int(blast_duration * sample_rate)
        
        # Super low frequency for knockback feel (40-80 Hz sweep down)
        blast_freq = np.linspace(80, 40, blast_samples)
        blast_wave = np.sin(2 * np.pi * np.cumsum(blast_freq) / sample_rate)
        
        # Add square wave harmonics for 8-bit character
        blast_wave += 0.3 * np.sign(np.sin(2 * np.pi * np.cumsum(blast_freq * 2) / sample_rate))
        
        # Sharp attack envelope for blast
        blast_envelope = np.exp(-np.linspace(0, 12, blast_samples))
        blast_wave *= blast_envelope
        
        # Phase 2: White noise explosion body (0.1-0.3s)
        body_duration = 0.2
        body_samples = int(body_duration * sample_rate)
        
        # Filtered white noise for debris/crackle
        body_noise = np.random.uniform(-1, 1, body_samples)
        
        # Band-pass filter effect (keep mid-high frequencies)
        for i in range(1, len(body_noise)):
            body_noise[i] = body_noise[i] * 0.7 + body_noise[i-1] * 0.3
        
        # Decay envelope
        body_envelope = np.exp(-np.linspace(0, 8, body_samples))
        body_noise *= body_envelope
        
        # Phase 3: Pixel crackle tail (0.3-0.6s)
        tail_samples = samples - blast_samples - body_samples
        
        # Random crackle/debris sounds
        tail_crackle = np.random.uniform(-0.4, 0.4, tail_samples)
        
        # Add occasional "pops" for pixel debris
        pop_positions = np.random.randint(0, tail_samples, 15)
        for pos in pop_positions:
            if pos < tail_samples - 20:
                # Mini explosion pops
                pop_freq = np.random.uniform(200, 600)
                pop_length = 20
                pop_t = np.linspace(0, pop_length/sample_rate, pop_length)
                pop = np.sin(2 * np.pi * pop_freq * pop_t) * np.exp(-pop_t * 50)
                tail_crackle[pos:pos+pop_length] += pop * 0.3
        
        # Fast decay envelope for tail
        tail_envelope = np.exp(-np.linspace(0, 10, tail_samples))
        tail_crackle *= tail_envelope
        
        # Combine all phases
        wave = np.zeros(samples)
        wave[:blast_samples] = blast_wave
        wave[blast_samples:blast_samples+body_samples] = body_noise
        wave[blast_samples+body_samples:] = tail_crackle
        
        # Normalize and convert with emphasis on low end
        wave = wave / np.max(np.abs(wave)) * 0.8
        wave = np.int16(wave * 32767)
        
        # Convert mono to stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
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
        
        # Convert mono to stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
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
        
        # Convert mono to stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
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
    import numpy as np  # Ensure numpy is imported
    sound_gen = SoundGenerator()
    SOUND_ENABLED = True
    print("[SOUND] Retro explosion sound effects loaded!")
except ImportError as e:
    # If numpy not available, disable sound
    sound_gen = None
    SOUND_ENABLED = False
    print(f"[SOUND] Disabled - numpy not available: {e}")
except Exception as e:
    sound_gen = None
    SOUND_ENABLED = False
    print(f"[SOUND] Disabled - initialization error: {e}")
