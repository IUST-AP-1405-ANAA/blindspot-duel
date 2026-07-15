from src.entities.targets.target_base import Target
import src.config.settings as cfg


class StandardTarget(Target):
    """
    A normal target that grants score when shot.
    """

    def __init__(self, x: float, y: float, radius: float = cfg.TARGET_RADIUS):
        super().__init__(x, y, radius, base_score=cfg.DEFAULT_BASE_SCORE)