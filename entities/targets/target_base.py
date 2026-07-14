from blindspot_duel.entities.base.game_object import GameObject
from blindspot_duel.contracts.i_collidable import ICollidable
import math

from blindspot_duel.config.settings import TARGET_RADIUS, DEFAULT_BASE_SCORE


class Target(GameObject, ICollidable):
    """
    Base class for standard targets and special items.
    """

    def __init__(self, x: float, y: float, radius: float = TARGET_RADIUS, base_score: int = DEFAULT_BASE_SCORE):
        super().__init__(x, y)
        self._validate_target_values(radius, base_score)
        self._radius = radius
        self._base_score = base_score

    def _validate_target_values(self, radius: float, base_score: int) -> None:
        if not isinstance(radius, (int, float)):
            raise TypeError("radius must be a number")
        if radius <= 0:
            raise ValueError("radius must be positive")
        if not isinstance(base_score, (int, float)):
            raise TypeError("base_score must be a number")
        if base_score < 0:
            raise ValueError("base_score cannot be negative")

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def base_score(self) -> int:
        return self._base_score

    def get_hitbox(self) -> tuple:
        """Return circle coordinates and radius."""
        return (self.x, self.y, self._radius)

    def is_hit(self, x: float, y: float) -> bool:
        """
        Check if coordinate falls within target radius.
        NOTE: طبق سند module_entities.md این نوع محاسبه باید در
        mechanics/combat/collision_detector.py انجام بشه.
        فعلاً نگه‌داشته شده، ولی حتماً با تیم mechanics هماهنگ کن.
        """
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance <= self.radius