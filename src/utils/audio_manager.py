"""
Audio subsystem.
"""
import pygame
import os
from src.contracts.i_audio_player import IAudioPlayer
from src.utils.exception_logger import ExceptionLogger

from src.config.settings import ASSETS_DIR, SOUNDS_SUBDIR

class AudioManager(IAudioPlayer):
    """
    Implementation of audio playback using Pygame mixer.
    """

    def __init__(self):
        self.muted = False
        try:
            pygame.mixer.init()
        except Exception as e:
            ExceptionLogger.log_warning(f"Could not initialize audio mixer (continuing muted): {str(e)}")
            self.muted = True
            
        from src.config.settings import MASTER_VOLUME
        self.volume = MASTER_VOLUME
        
        self.sound_cache = {}

    def set_volume(self, volume: float) -> None:
        """Update master volume for all future sounds and current music."""
        self.volume = volume
        if not self.muted:
            pygame.mixer.music.set_volume(self.volume)
            for sound in self.sound_cache.values():
                sound.set_volume(self.volume)

    def play_sfx(self, sound_name: str) -> None:
        """Play a sound effect from Cache, or log warning if missing."""
        if self.muted:
            return
            
        if sound_name not in self.sound_cache:
            path = os.path.join(ASSETS_DIR, SOUNDS_SUBDIR, f"{sound_name}.wav")
            if not os.path.exists(path):
                # Silent skip to avoid crashes
                return
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(self.volume)
                self.sound_cache[sound_name] = snd
            except Exception as e:
                ExceptionLogger.log_warning(f"Error loading sound {sound_name}: {str(e)}")
                return
                
        try:
            self.sound_cache[sound_name].play()
        except Exception as e:
            pass

    def play_background_music(self, track_name: str) -> None:
        """Play background track in loop."""
        if self.muted:
            return
            
        for ext in [".mp3", ".ogg", ".wav"]:
            path = os.path.join(ASSETS_DIR, SOUNDS_SUBDIR, f"{track_name}{ext}")
            if os.path.exists(path):
                break
        else:
            return
            
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
        except Exception as e:
            ExceptionLogger.log_warning(f"Error playing music {track_name}: {str(e)}")

    def stop_all_sounds(self) -> None:
        """Stop playing all sounds and tracks."""
        if self.muted:
            return
        try:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        except Exception as e:
            pass
