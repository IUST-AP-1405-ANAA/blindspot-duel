from blindspot_duel.entities.targets.target_base import Target
from blindspot_duel.config.settings import TARGET_RADIUS, DEFAULT_BASE_SCORE


class StandardTarget(Target):
    """
    A normal target that grants score when shot.
    """

    def __init__(self, x: float, y: float, radius: float = TARGET_RADIUS):
        super().__init__(x, y, radius, base_score=DEFAULT_BASE_SCORE)