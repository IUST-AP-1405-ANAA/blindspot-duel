"""
Crosshair state and position.
"""
from src.entities.base.game_object import GameObject
from src.config.settings import RETICLE_RADIUS


class Crosshair(GameObject):
    """
    Represents the player's aiming point.
    """

    def __init__(self, x: float, y: float, hitbox_radius: float = RETICLE_RADIUS):
        super().__init__(x, y)
        self._validate_hitbox_radius(hitbox_radius)
        self._is_visible = False
        self._hitbox_radius = hitbox_radius

    def _validate_hitbox_radius(self, hitbox_radius: float) -> None:
        if not isinstance(hitbox_radius, (int, float)):
            raise TypeError("hitbox_radius must be a number")
        if hitbox_radius <= 0:
            raise ValueError("hitbox_radius must be positive")

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @property
    def hitbox_radius(self) -> float:
        return self._hitbox_radius

    def reveal(self) -> None:
        """Make the crosshair visible."""
        self._is_visible = True

    def hide(self) -> None:
        """Hide the crosshair."""
        self._is_visible = False