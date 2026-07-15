"""
Boundary enforcement pure functions.
"""

def clamp_position(x: float, y: float, max_x: float, max_y: float) -> tuple:
    """Ensures coordinates stay within window bounds."""
    clamped_x = max(0.0, min(x, max_x))
    clamped_y = max(0.0, min(y, max_y))
    return clamped_x, clamped_y
