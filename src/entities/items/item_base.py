"""
Base class for special items.
"""
from src.entities.targets.target_base import Target
import src.config.settings as cfg


class Item(Target):
    """
    Abstract base item granting special effects.
    """

    def __init__(self, x: float, y: float, radius: float = cfg.ITEM_RADIUS, base_score: int = cfg.ITEM_BASE_SCORE):
        super().__init__(x, y, radius, base_score)

    def apply_effect(self, player, opponent) -> None:
        """Apply custom power-up logic on the player or debuff opponent."""
        pass