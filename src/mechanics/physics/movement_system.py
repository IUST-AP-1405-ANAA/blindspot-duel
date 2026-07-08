"""
Handles crosshair movement logic.
"""
from src.entities.player.crosshair import Crosshair

def move_crosshair(crosshair: Crosshair, dx: float, dy: float, speed: float, dt: float, is_glitched: bool = False) -> None:
    """Update the crosshair position based on delta inputs, clamping is done elsewhere."""
    dir_multiplier = -1.0 if is_glitched else 1.0
    crosshair.x += dx * speed * dt * dir_multiplier
    crosshair.y += dy * speed * dt * dir_multiplier
