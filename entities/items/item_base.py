"""
Base class for special items.
"""
from blindspot_duel.entities.targets.target_base import Target
from blindspot_duel.config.settings import ITEM_RADIUS, ITEM_BASE_SCORE


class Item(Target):
    """
    Abstract base item granting special effects.
    """

    def __init__(self, x: float, y: float, radius: float = ITEM_RADIUS, base_score: int = ITEM_BASE_SCORE):
        super().__init__(x, y, radius, base_score)

    def apply_effect(self, player, opponent) -> None:
        """Apply custom power-up logic on the player or debuff opponent."""
        pass