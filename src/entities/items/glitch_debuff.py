"""
Glitch effect applied to the opponent.
"""
from src.entities.items.item_base import Item
import src.config.settings as cfg
from src.config.thresholds import GLITCH_EFFECT_DURATION


class ItemGlitch(Item):
    """
    Applies a negative effect to the opponent.
    """

    def __init__(self, x: float, y: float, radius: float = cfg.ITEM_RADIUS):
        super().__init__(x, y, radius, base_score=cfg.ITEM_BASE_SCORE)

    def apply_effect(self, player, opponent) -> None:
        opponent.set_glitch_timer(GLITCH_EFFECT_DURATION)