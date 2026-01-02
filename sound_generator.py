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
        self.sounds['tnt_warning'] = self._generate_tnt_warning()
        self.sounds['explosion'] = self._generate_explosion()
        self.sounds['player_hit'] = self._generate_player_hit()
        self.sounds['block_break'] = self._generate_click()
        self.sounds['dig'] = self._generate_dig()
    
    def _generate_beep(self, duration=0.15, frequency=400):
        """Generate low fizzing hiss for TNT fuse (Minecraft-style)"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Generate filtered noise (hissing/fizzing sound)
        noise = np.random.uniform(-0.5, 0.5, samples)
        
        # Low-pass filter for muffled hiss
        alpha = 0.4
        for i in range(1, len(noise)):
            noise[i] = alpha * noise[i] + (1 - alpha) * noise[i-1]
        
        # Add low frequency tone (400 Hz) for body
        tone = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Mix noise and tone
        wave = noise * 0.7 + tone
        
        # Quick envelope
        envelope = np.ones_like(wave)
        fade_samples = samples // 10
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        wave *= envelope
        
        # Convert to 16-bit
        wave = np.int16(wave * 32767 * 0.4)
        
        # Convert mono to stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_tnt_warning(self, duration=0.2):
        """Generate urgent warning beep (rising pitch, faster)"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Rising frequency sweep (600 -> 1200 Hz)
        start_freq = 600
        end_freq = 1200
        freq = np.linspace(start_freq, end_freq, samples)
        phase = np.cumsum(freq) / sample_rate
        
        # Mix square wave (70%) and sine wave (30%)
        square_wave = np.sign(np.sin(2 * np.pi * phase))
        sine_wave = np.sin(2 * np.pi * phase)
        wave = 0.7 * square_wave + 0.3 * sine_wave
        
        # Add tremolo for urgency
        tremolo_freq = 15  # Fast tremolo
        tremolo = 0.8 + 0.2 * np.sin(2 * np.pi * tremolo_freq * t)
        wave *= tremolo
        
        # Sharp envelope
        envelope = np.ones_like(wave)
        fade_samples = samples // 20
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        wave *= envelope
        
        # Convert to 16-bit
        wave = np.int16(wave * 32767 * 0.5)
        
        # Convert mono to stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_player_hit(self, duration=0.3):
        """Generate pixel-style knockback impact sound (thump + whoosh)"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Part 1: Soft thump (low frequency impact)
        thump_duration = 0.1
        thump_samples = int(thump_duration * sample_rate)
        
        # Low frequency punch (80 -> 40 Hz)
        thump_freq = np.linspace(80, 40, thump_samples)
        thump_phase = np.cumsum(thump_freq) / sample_rate
        thump = np.sin(2 * np.pi * thump_phase)
        
        # Quick decay
        thump_env = np.exp(-np.linspace(0, 20, thump_samples))
        thump *= thump_env
        
        # Part 2: Whoosh (filtered noise sweep)
        whoosh_samples = samples - thump_samples
        
        # Generate noise
        whoosh = np.random.uniform(-0.5, 0.5, whoosh_samples)
        
        # Band-pass filter (sweeping down for doppler effect)
        alpha = np.linspace(0.7, 0.3, whoosh_samples)
        for i in range(1, len(whoosh)):
            whoosh[i] = alpha[i] * whoosh[i] + (1 - alpha[i]) * whoosh[i-1]
        
        # Add pitch sweep for movement feel
        whoosh_freq = np.linspace(800, 200, whoosh_samples)
        whoosh_phase = np.cumsum(whoosh_freq) / sample_rate
        whoosh_tone = np.sin(2 * np.pi * whoosh_phase) * 0.3
        whoosh = whoosh * 0.7 + whoosh_tone
        
        # Smooth envelope
        whoosh_env = np.exp(-np.linspace(0, 8, whoosh_samples))
        whoosh *= whoosh_env
        
        # Combine thump + whoosh
        wave = np.zeros(samples)
        wave[:thump_samples] = thump * 0.8
        wave[thump_samples:] = whoosh * 0.6
        
        # Normalize
        peak = np.max(np.abs(wave))
        if peak > 0:
            wave = wave / peak * 0.3  # Reduced volume
        
        # Convert to 16-bit
        wave = np.int16(wave * 32767)
        
        # Convert mono to stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_explosion(self, duration=1.0):
        """Generate powerful Minecraft-inspired pixel explosion for livestream"""
        sample_rate = 22050
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        # === PHASE 1: Punchy Bass Impact (0-0.15s) ===
        impact_duration = 0.15
        impact_samples = int(impact_duration * sample_rate)
        
        # Deep sub-bass punch (30-70 Hz sweep)
        bass_freq = np.linspace(70, 30, impact_samples)
        bass_t = np.cumsum(bass_freq) / sample_rate
        bass_wave = np.sin(2 * np.pi * bass_t)
        
        # Add distorted square wave for pixel crunch
        square_wave = np.sign(np.sin(2 * np.pi * bass_t * 2))
        bass_wave = bass_wave * 0.7 + square_wave * 0.3
        
        # Super punchy envelope - instant attack
        impact_env = np.exp(-np.linspace(0, 15, impact_samples))
        bass_wave *= impact_env
        
        # === PHASE 2: Glitchy Pixel Distortion (0.15-0.5s) ===
        glitch_duration = 0.35
        glitch_samples = int(glitch_duration * sample_rate)
        
        # Multi-layered noise for chaos
        white_noise = np.random.uniform(-1, 1, glitch_samples)
        
        # Bit-crush effect for pixel distortion
        bit_depth = 8
        white_noise = np.floor(white_noise * (2**(bit_depth-1))) / (2**(bit_depth-1))
        
        # Add glitchy frequency modulation
        glitch_freq = np.random.choice([200, 400, 800, 1600], glitch_samples)
        glitch_sine = np.sin(2 * np.pi * np.cumsum(glitch_freq) / sample_rate) * 0.3
        
        # Random "pixel pops" for extra chaos
        pixel_pops = np.zeros(glitch_samples)
        num_pops = 40  # More pops for chaos
        pop_positions = np.random.randint(0, glitch_samples - 50, num_pops)
        for pos in pop_positions:
            pop_freq = np.random.choice([300, 600, 1200])
            pop_len = np.random.randint(10, 30)
            if pos + pop_len < glitch_samples:
                pop_t = np.arange(pop_len) / sample_rate
                pop = np.sin(2 * np.pi * pop_freq * pop_t)
                # Square it for extra punch
                pop = np.sign(pop) * np.abs(pop) ** 0.5
                pop *= np.exp(-pop_t * 40)
                pixel_pops[pos:pos+pop_len] += pop * 0.4
        
        # Combine glitch elements
        glitch_wave = white_noise * 0.5 + glitch_sine + pixel_pops
        
        # Aggressive decay for glitch layer
        glitch_env = np.exp(-np.linspace(0, 9, glitch_samples))
        glitch_wave *= glitch_env
        
        # === PHASE 3: Debris Falling (0.5-1.0s) ===
        debris_samples = samples - impact_samples - glitch_samples
        
        # Filtered noise for falling debris
        debris = np.random.uniform(-0.5, 0.5, debris_samples)
        
        # Low-pass filter (simulate distance)
        alpha = 0.3
        for i in range(1, len(debris)):
            debris[i] = alpha * debris[i] + (1 - alpha) * debris[i-1]
        
        # Random "clinks" and "clanks" for blocks hitting ground
        num_clinks = 25
        clink_positions = np.random.randint(0, debris_samples - 30, num_clinks)
        for i, pos in enumerate(clink_positions):
            # Clinks get quieter over time
            time_factor = 1.0 - (i / num_clinks) * 0.7
            clink_freq = np.random.uniform(800, 2000)
            clink_len = np.random.randint(15, 25)
            if pos + clink_len < debris_samples:
                clink_t = np.arange(clink_len) / sample_rate
                clink = np.sin(2 * np.pi * clink_freq * clink_t)
                clink *= np.exp(-clink_t * 30) * time_factor * 0.3
                debris[pos:pos+clink_len] += clink
        
        # Smooth decay for debris
        debris_env = np.exp(-np.linspace(0, 6, debris_samples))
        debris *= debris_env
        
        # === COMBINE ALL PHASES ===
        wave = np.zeros(samples)
        wave[:impact_samples] = bass_wave * 1.2  # Boost bass impact
        wave[impact_samples:impact_samples+glitch_samples] = glitch_wave
        wave[impact_samples+glitch_samples:] = debris
        
        # === MASTER PROCESSING ===
        # Soft clipping for loudness without distortion
        def soft_clip(x, threshold=0.9):
            return np.tanh(x / threshold) * threshold
        
        wave = soft_clip(wave, 0.85)
        
        # Normalize with headroom for livestream
        peak = np.max(np.abs(wave))
        if peak > 0:
            wave = wave / peak * 0.5  # Reduced volume
        
        # Convert to 16-bit with dithering for quality
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
    
    def play_sound(self, sound_name, volume=1.0):
        """Play a generated sound effect with adjustable volume"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].set_volume(volume)
                self.sounds[sound_name].play()
            except:
                pass  # Fail silently if sound can't play
    
    def play_tnt_fuse(self):
        """Play TNT fuse beep"""
        self.play_sound('tnt_fuse')
    
    def play_tnt_warning(self):
        """Play urgent TNT warning beep"""
        self.play_sound('tnt_warning')
    
    def play_explosion(self, volume=1.0):
        """Play explosion boom with adjustable volume"""
        self.play_sound('explosion', volume)
    
    def play_player_hit(self):
        """Play player knockback impact"""
        self.play_sound('player_hit')
    
    def play_block_break(self):
        """Play block break click"""
        self.play_sound('block_break')
    
    def play_dig(self):
        """Play dig sound"""
        self.play_sound('dig')
    
    def play_meteor_impact(self):
        """Play soft meteor impact sound"""
        # Generate soft, magical impact sound
        duration = 0.8
        sample_rate = 22050
        num_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, num_samples)
        
        # Soft whoosh with sparkle
        # Phase 1: Soft whoosh (0-0.3s)
        whoosh = np.zeros(num_samples)
        whoosh_duration = 0.3
        whoosh_samples = int(whoosh_duration * sample_rate)
        whoosh_t = t[:whoosh_samples]
        
        # Soft noise sweep
        for freq in [100, 150, 200]:
            whoosh[:whoosh_samples] += np.sin(2 * np.pi * freq * whoosh_t) * np.exp(-whoosh_t * 8)
        
        # Phase 2: Sparkle chime (0.2-0.8s)
        chime = np.zeros(num_samples)
        chime_start = int(0.2 * sample_rate)
        chime_t = t[chime_start:]
        
        # Multiple soft bell tones
        for freq in [800, 1000, 1200, 1600]:
            chime[chime_start:] += np.sin(2 * np.pi * freq * chime_t) * np.exp(-chime_t * 3)
        
        # Combine
        audio = whoosh * 0.3 + chime * 0.4
        
        # Soft volume envelope
        envelope = np.exp(-t * 2.5)
        audio = audio * envelope * 0.15  # Very soft - 15% volume
        
        # Normalize
        audio = audio / np.max(np.abs(audio)) * 0.3  # Cap at 30%
        
        # Convert to 16-bit stereo
        audio = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
        stereo_audio = np.column_stack([audio, audio])
        
        # Play immediately
        sound = pygame.sndarray.make_sound(stereo_audio)
        sound.play()

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
