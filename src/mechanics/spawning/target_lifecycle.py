"""
Target management.
"""
import random
from src.entities.targets.standard_target import StandardTarget
from src.entities.items.ammo_box import ItemAmmoBox
from src.entities.items.time_boost import ItemTimeBoost
from src.entities.items.glitch_debuff import ItemGlitch
from src.mechanics.spawning.coordinate_generator import generate_random_position
from src.config.settings import WIDTH, HEIGHT, MAX_TARGETS_ON_SCREEN, TARGET_RADIUS
from src.config.thresholds import STANDARD_SPAWN_CHANCE

class TargetManager:
    """
    Controls the number of active targets and spawns new ones.
    """

    def __init__(self):
        self.active_targets = []

    def spawn_target(self) -> None:
        """Spawn a new target if under max limit."""
        if len(self.active_targets) >= MAX_TARGETS_ON_SCREEN:
            return
            
        x, y = generate_random_position(WIDTH, HEIGHT, TARGET_RADIUS)
        
        # 70% chance of spawning standard target, 30% chance of a powerup/debuff item
        if random.random() < STANDARD_SPAWN_CHANCE:
            target = StandardTarget(x, y, TARGET_RADIUS)
        else:
            item_class = random.choice([ItemAmmoBox, ItemTimeBoost, ItemGlitch])
            target = item_class(x, y, TARGET_RADIUS)
            
        self.active_targets.append(target)
