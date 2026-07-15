"""
Ammo power-up.
"""
from src.entities.items.item_base import Item
from src.config.settings import ITEM_RADIUS, ITEM_BASE_SCORE, AMMO_BOX_BONUS


class ItemAmmoBox(Item):
    """
    Grants extra ammo to the player.
    """

    def __init__(self, x: float, y: float, radius: float = ITEM_RADIUS):
        super().__init__(x, y, radius, base_score=ITEM_BASE_SCORE)

    def apply_effect(self, player, opponent) -> None:
        player.add_ammo(AMMO_BOX_BONUS)