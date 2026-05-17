import numpy as np
import pygame
from constants import SAMPLE_RATE, RED_FREQ_BASE, GREEN_FREQ_BASE, BLUE_FREQ_BASE


class AudioSynth:
    def __init__(self):
        pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
        pygame.mixer.init()
        self.channels = [pygame.mixer.Channel(i) for i in range(3)]
        self.sounds = [None, None, None]
        self.current_values = [0, 0, 0]

    def generate_tone(self, freq, value):
        if value == 0:
            return None
        
        amplitude = value / 255.0 * 0.3
        duration = 0.1
        
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
        wave = amplitude * np.sin(2 * np.pi * freq * t)
        
        fade = np.linspace(1, 0, len(wave))
        wave = wave * fade
        
        stereo_wave = np.column_stack((wave, wave))
        audio = (stereo_wave * 32767).astype(np.int16)
        
        return pygame.sndarray.make_sound(audio)

    def update(self, r, g, b):
        values = [r, g, b]
        freqs = [RED_FREQ_BASE, GREEN_FREQ_BASE, BLUE_FREQ_BASE]
        
        for i in range(3):
            if values[i] != self.current_values[i]:
                if self.sounds[i]:
                    self.sounds[i].stop()
                
                self.current_values[i] = values[i]
                self.sounds[i] = self.generate_tone(freqs[i], values[i])
                
                if self.sounds[i]:
                    self.channels[i].play(self.sounds[i], loops=-1)

    def stop_all(self):
        for sound in self.sounds:
            if sound:
                sound.stop()
        self.current_values = [0, 0, 0]
