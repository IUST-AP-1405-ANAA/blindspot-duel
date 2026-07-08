"""
AABB and distance-based collision detection.
"""
import math

def check_intersection(point: tuple, hitbox: tuple) -> bool:
    """Returns True if point is inside the circular hitbox."""
    px, py = point
    tx, ty, radius = hitbox
    distance = math.sqrt((tx - px) ** 2 + (ty - py) ** 2)
    return distance <= radius
