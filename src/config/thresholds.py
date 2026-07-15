"""
Balancing and gameplay thresholds.
"""

GLITCH_EFFECT_DURATION = 3.0
MAX_SCORE_DISTANCE = 500.0
MIN_SCORE_DISTANCE = 50.0

# Spawning rules
STANDARD_SPAWN_CHANCE = 0.7

# HUD visual thresholds
MIN_COMBO_FOR_TEXT = 2
HUD_TIME_WARN_HIGH = 0.5
HUD_TIME_WARN_LOW = 0.2

# Scoring rules & Multipliers mapping
DISTANCE_SCORE_MAPPING = [
    (400.0, 5),
    (300.0, 4),
    (200.0, 3),
    (100.0, 2)
]
DEFAULT_DISTANCE_SCORE = 1
COMBO_MULTIPLIER_FACTOR = 0.1
