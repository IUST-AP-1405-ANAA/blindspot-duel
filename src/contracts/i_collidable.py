"""
Interface for objects that can collide.
"""
from abc import ABC, abstractmethod

class ICollidable(ABC):
    """Abstract base class for objects that have a hitbox."""

    @abstractmethod
    def get_hitbox(self) -> tuple:
        """Return coordinates (x, y, radius) of the hitbox."""
        pass

    @abstractmethod
    def is_hit(self, x: float, y: float) -> bool:
        """Check if target is hit by a shot coordinate."""
        pass
