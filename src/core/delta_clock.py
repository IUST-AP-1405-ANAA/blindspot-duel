"""
Time management.
"""
import pygame

from src.config.settings import FPS

class DeltaClock:
    """
    Manages delta time calculation for frame-rate independence.
    """

    def __init__(self, target_fps: int = FPS):
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps

    def tick(self) -> float:
        """Calculate and return the time passed since the last frame (in seconds)."""
        # limit framerate and get delta time in ms
        dt_ms = self.clock.tick(self.target_fps)
        return dt_ms / 1000.0
