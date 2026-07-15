"""
Ammo power-up.
"""
from src.entities.items.item_base import Item
import src.config.settings as cfg


class ItemAmmoBox(Item):
    """
    Grants extra ammo to the player.
    """

    def __init__(self, x: float, y: float, radius: float = cfg.ITEM_RADIUS):
        super().__init__(x, y, radius, base_score=cfg.ITEM_BASE_SCORE)

    def apply_effect(self, player, opponent) -> None:
        player.add_ammo(cfg.AMMO_BOX_BONUS)