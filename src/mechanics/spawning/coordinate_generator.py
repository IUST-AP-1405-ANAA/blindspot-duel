"""
Random coordinate generation logic.
"""
import random

def generate_random_position(width: int, height: int, padding: float) -> tuple:
    """Returns a valid random (x, y) coordinate inside screen padded boundaries."""
    x = random.uniform(padding, width - padding)
    y = random.uniform(padding, height - padding)
    return x, y
