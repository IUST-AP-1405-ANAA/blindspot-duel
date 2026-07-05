"""
Interface for audio playback.
"""
from abc import ABC, abstractmethod

class IAudioPlayer(ABC):
    """Abstract base class for playing sounds and music."""

    @abstractmethod
    def play_sfx(self, sound_name: str) -> None:
        """Play a short sound effect (shoot, hit, miss, powerup, glitch)."""
        pass

    @abstractmethod
    def play_background_music(self, track_name: str) -> None:
        """Play background track in loop."""
        pass

    @abstractmethod
    def stop_all_sounds(self) -> None:
        """Stop playing all sounds and tracks."""
        pass
