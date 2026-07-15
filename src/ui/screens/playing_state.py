"""
Playing screen executing mechanics, displaying concentric bullseyes, items, and drawing visual shot feedback.
"""
import pygame
import random
from src.contracts.i_state import IState
from src.contracts.i_renderable import IRenderable
from src.entities.player.player_model import Player
from src.entities.player.crosshair import Crosshair
from src.mechanics.spawning.target_lifecycle import TargetManager
from src.mechanics.physics.movement_system import move_crosshair
from src.mechanics.physics.boundary_clamp import clamp_position
from src.mechanics.combat.shooting_logic import process_shot
from src.ui.hud.player_dashboard import PlayerDashboard
from src.database.dtos import MatchResultDTO
from src.config.settings import (
    WIDTH, HEIGHT, DEFAULT_AMMO, DEFAULT_TIME, CROSSHAIR_SPEED,
    MAX_TARGETS_ON_SCREEN, P1_START_POS, P2_START_POS, VFX_TEXT_OFFSET_X, VFX_TEXT_OFFSET_Y,
    SFX_POWERUP, TARGET_RING_RATIO, TARGET_RING_WIDTH, TARGET_INNER_RATIO,
    AMMO_BOX_BORDER_RADIUS, ITEM_LABEL_OFFSET_Y, ITEM_LABEL_SIZE,
    TIME_BOOST_BORDER_WIDTH, TIME_BOOST_HAND_1_OFFSET_Y, TIME_BOOST_HAND_2_OFFSET_X,
    TIME_BOOST_HANDS_WIDTH, GLITCH_DEBUFF_LABEL_SIZE, GLITCH_DEBUFF_LABEL_OFFSET_Y,
    RETICLE_RADIUS, RETICLE_LINE_WIDTH, RETICLE_LINE_OUTER, RETICLE_LINE_INNER,
    RETICLE_CENTER_RADIUS
)
from src.config.colors import (
    P1_COLOR, P2_COLOR, P1_VFX_COLOR, P2_VFX_COLOR, TARGET_BG_COLOR,
    TARGET_RING_COLOR, TARGET_INNER_COLOR, AMMO_COLOR, BG_COLOR,
    TIME_BOOST_BG_COLOR, TIME_COLOR, TEXT_COLOR, GLITCH_COLOR, CENTER_DOT_COLOR
)
from src.config.messages import ITEM_AMMO_LABEL, ITEM_GLITCH_LABEL
from src.entities.items.item_base import Item


class PlayingState(IState):
    def __init__(self, state_manager, engine):
        self.state_manager = state_manager
        self.engine = engine
        self.hud = PlayerDashboard()

    def enter(self) -> None:
        self.p1 = Player(self.state_manager.p1_username, DEFAULT_AMMO, DEFAULT_TIME)
        self.p2 = Player(self.state_manager.p2_username, DEFAULT_AMMO, DEFAULT_TIME)

        self.c1 = Crosshair(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.c2 = Crosshair(random.randint(0, WIDTH), random.randint(0, HEIGHT))

        self.target_manager = TargetManager()
        for _ in range(MAX_TARGETS_ON_SCREEN):
            self.target_manager.spawn_target()

        self.p1_last_hit = None
        self.p2_last_hit = None

    def update(self, dt: float, commands: dict) -> None:
        self.p1.update_time(dt)
        self.p2.update_time(dt)

        if self.p1.is_locked_out and self.p2.is_locked_out:
            self.state_manager.change_state("MATCH_RESULTS")
            return

        p1_dx, p1_dy = commands["p1_move"]
        p2_dx, p2_dy = commands["p2_move"]

        p1_glitched = (self.p1.glitch_timer > 0.0)
        p2_glitched = (self.p2.glitch_timer > 0.0)

        if not self.p1.is_locked_out:
            if p1_dx != 0 or p1_dy != 0:
                self.c1.hide()
            move_crosshair(self.c1, p1_dx, p1_dy, CROSSHAIR_SPEED, dt, p1_glitched)
            self.c1.set_position(*clamp_position(self.c1.x, self.c1.y, WIDTH, HEIGHT))

        if not self.p2.is_locked_out:
            if p2_dx != 0 or p2_dy != 0:
                self.c2.hide()
            move_crosshair(self.c2, p2_dx, p2_dy, CROSSHAIR_SPEED, dt, p2_glitched)
            self.c2.set_position(*clamp_position(self.c2.x, self.c2.y, WIDTH, HEIGHT))

        # P1 Shoot
        if commands["p1_shoot"] and not self.p1.is_locked_out:
            self.c1.reveal()
            self.engine.vfx_system.spawn_shockwave(self.c1.x, self.c1.y, P1_COLOR)
            added_score, shot_point, hit_target = process_shot(
                self.p1, self.c1, self.target_manager, self.engine.audio, self.p1_last_hit
            )
            if hit_target:
                self.p1_last_hit = shot_point
                self.engine.vfx_system.spawn(f"+{added_score}", shot_point[0] + VFX_TEXT_OFFSET_X, shot_point[1] + VFX_TEXT_OFFSET_Y, color=P1_VFX_COLOR)
                self.engine.vfx_system.spawn_explosion(shot_point[0], shot_point[1], P1_COLOR)
                if isinstance(hit_target, Item):
                    hit_target.apply_effect(self.p1, self.p2)
                    self.engine.audio.play_sfx(SFX_POWERUP)
            else:
                self.p1_last_hit = None

        # P2 Shoot
        if commands["p2_shoot"] and not self.p2.is_locked_out:
            self.c2.reveal()
            self.engine.vfx_system.spawn_shockwave(self.c2.x, self.c2.y, P2_COLOR)
            added_score, shot_point, hit_target = process_shot(
                self.p2, self.c2, self.target_manager, self.engine.audio, self.p2_last_hit
            )
            if hit_target:
                self.p2_last_hit = shot_point
                self.engine.vfx_system.spawn(f"+{added_score}", shot_point[0] + VFX_TEXT_OFFSET_X, shot_point[1] + VFX_TEXT_OFFSET_Y, color=P2_VFX_COLOR)
                self.engine.vfx_system.spawn_explosion(shot_point[0], shot_point[1], P2_COLOR)
                if isinstance(hit_target, Item):
                    hit_target.apply_effect(self.p2, self.p1)
                    self.engine.audio.play_sfx(SFX_POWERUP)
            else:
                self.p2_last_hit = None

        while len(self.target_manager.active_targets) < MAX_TARGETS_ON_SCREEN:
            self.target_manager.spawn_target()

    def render(self, renderer: IRenderable) -> None:
        from src.entities.targets.standard_target import StandardTarget
        from src.entities.items.ammo_box import ItemAmmoBox
        from src.entities.items.time_boost import ItemTimeBoost
        from src.entities.items.glitch_debuff import ItemGlitch

        # 1. Render Targets
        for target in self.target_manager.active_targets:
            if isinstance(target, StandardTarget):
                # Standard concentric bullseye target drawing
                pygame.draw.circle(renderer.screen, TARGET_BG_COLOR, (int(target.x), int(target.y)), int(target.radius))
                pygame.draw.circle(renderer.screen, TARGET_RING_COLOR, (int(target.x), int(target.y)), int(target.radius * TARGET_RING_RATIO), TARGET_RING_WIDTH)
                pygame.draw.circle(renderer.screen, TARGET_INNER_COLOR, (int(target.x), int(target.y)), int(target.radius * TARGET_INNER_RATIO))
            elif isinstance(target, ItemAmmoBox):
                # Draw yellow Ammo box
                rect = pygame.Rect(int(target.x - target.radius), int(target.y - target.radius), int(target.radius * 2), int(target.radius * 2))
                pygame.draw.rect(renderer.screen, AMMO_COLOR, rect, border_radius=AMMO_BOX_BORDER_RADIUS)
                renderer.draw_ui_text(ITEM_AMMO_LABEL, target.x, target.y + ITEM_LABEL_OFFSET_Y, color=BG_COLOR, size=ITEM_LABEL_SIZE, align="center")
            elif isinstance(target, ItemTimeBoost):
                # Draw cyan Clock
                pygame.draw.circle(renderer.screen, TIME_BOOST_BG_COLOR, (int(target.x), int(target.y)), int(target.radius))
                pygame.draw.circle(renderer.screen, TIME_COLOR, (int(target.x), int(target.y)), int(target.radius), TIME_BOOST_BORDER_WIDTH)
                pygame.draw.line(renderer.screen, TEXT_COLOR, (target.x, target.y), (target.x, target.y + TIME_BOOST_HAND_1_OFFSET_Y), TIME_BOOST_HANDS_WIDTH)
                pygame.draw.line(renderer.screen, TEXT_COLOR, (target.x, target.y), (target.x + TIME_BOOST_HAND_2_OFFSET_X, target.y), TIME_BOOST_HANDS_WIDTH)
            elif isinstance(target, ItemGlitch):
                # Draw glitch magenta triangle
                tx, ty, r = target.x, target.y, target.radius
                pts = [(tx, ty - r), (tx - r, ty + r), (tx + r, ty + r)]
                pygame.draw.polygon(renderer.screen, GLITCH_COLOR, pts)
                renderer.draw_ui_text(ITEM_GLITCH_LABEL, tx, ty + GLITCH_DEBUFF_LABEL_OFFSET_Y, color=TEXT_COLOR, size=GLITCH_DEBUFF_LABEL_SIZE, align="center")

        # 2. Render Crosshairs
        # طبق تصمیم معماری: منبع حقیقت برای نمایان بودن نشانگر، Crosshair.is_visible است.
        if self.c1.is_visible:
            self.draw_crosshair_reticle(renderer.screen, self.c1.x, self.c1.y, P1_COLOR)
        if self.c2.is_visible:
            self.draw_crosshair_reticle(renderer.screen, self.c2.x, self.c2.y, P2_COLOR)

        # 3. Draw Dashboard HUD
        self.hud.draw(self.p1, self.p2, renderer.screen)

    def draw_crosshair_reticle(self, surface, x: float, y: float, color: tuple) -> None:
        # Crosshair drawing: reticle circle + cross lines
        pygame.draw.circle(surface, color, (int(x), int(y)), RETICLE_RADIUS, RETICLE_LINE_WIDTH)
        pygame.draw.line(surface, color, (x - RETICLE_LINE_OUTER, y), (x - RETICLE_LINE_INNER, y), RETICLE_LINE_WIDTH)
        pygame.draw.line(surface, color, (x + RETICLE_LINE_INNER, y), (x + RETICLE_LINE_OUTER, y), RETICLE_LINE_WIDTH)
        pygame.draw.line(surface, color, (x, y - RETICLE_LINE_OUTER), (x, y - RETICLE_LINE_INNER), RETICLE_LINE_WIDTH)
        pygame.draw.line(surface, color, (x, y + RETICLE_LINE_INNER), (x, y + RETICLE_LINE_OUTER), RETICLE_LINE_WIDTH)
        pygame.draw.circle(surface, CENTER_DOT_COLOR, (int(x), int(y)), RETICLE_CENTER_RADIUS)

    def exit(self) -> None:
        self.engine.database.save_match_result(MatchResultDTO(self.p1.username, self.p1.score, self.p1.max_combo))
        self.engine.database.save_match_result(MatchResultDTO(self.p2.username, self.p2.score, self.p2.max_combo))

        self.state_manager.last_match_stats = {
            "p1_name": self.p1.username, "p1_score": self.p1.score, "p1_combo": self.p1.max_combo,
            "p2_name": self.p2.username, "p2_score": self.p2.score, "p2_combo": self.p2.max_combo
        }