"""
Shooting business logic.
"""
from src.mechanics.combat.collision_detector import check_intersection
from src.mechanics.scoring.math_formulas import calculate_distance_score, calculate_final_score
from src.entities.items.item_base import Item
from src.config.settings import SFX_SHOOT, SFX_HIT, SFX_MISS

def process_shot(player, crosshair, target_manager, audio_player, prev_hit_coord=None) -> tuple:
    """Check if the shot hits a target and apply consequences."""
    if not player.fire_shot():
        return 0, prev_hit_coord, None # Cannot fire
        
    audio_player.play_sfx(SFX_SHOOT)
    shot_x, shot_y = crosshair.x, crosshair.y
    shot_point = (shot_x, shot_y)
    
    hit_target = None
    for t in target_manager.active_targets:
        if check_intersection(shot_point, t.get_hitbox()):
            hit_target = t
            break
            
    if hit_target:
        audio_player.play_sfx(SFX_HIT)
        target_manager.active_targets.remove(hit_target)
        
        # Calculate base score (distance from previous hit or target's base score)
        if prev_hit_coord:
            base_score = calculate_distance_score(prev_hit_coord, shot_point)
        else:
            base_score = hit_target.base_score
            
        player.increment_combo()
        final_score = calculate_final_score(base_score, player.combo)
        player.add_score(final_score)
        
        return final_score, shot_point, hit_target
    else:
        audio_player.play_sfx(SFX_MISS)
        player.reset_combo()
        return 0, prev_hit_coord, None
