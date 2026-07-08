"""
Pure mathematical scoring formulas.
"""
import math

from src.config.thresholds import DISTANCE_SCORE_MAPPING, DEFAULT_DISTANCE_SCORE, COMBO_MULTIPLIER_FACTOR

def calculate_distance_score(p1: tuple, p2: tuple) -> int:
    """Calculate score based on euclidean distance between hits."""
    x1, y1 = p1
    x2, y2 = p2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Linearly map distance (50 to 500) to points (1 to 5)
    # The farther the target from last hit, the higher the score
    for threshold_distance, score_value in DISTANCE_SCORE_MAPPING:
        if distance >= threshold_distance:
            return score_value
    return DEFAULT_DISTANCE_SCORE

def calculate_final_score(base_score: int, combo: int) -> int:
    """Apply combo multiplier: Score = BaseScore * (1 + Combo * 0.1)"""
    return int(base_score * (1.0 + (combo * COMBO_MULTIPLIER_FACTOR)))
