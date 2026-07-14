"""
Upgraded player stats dashboard with neon bars and boxes.
"""
import pygame
from blindspot_duel.ui.components.text_renderer import TextRenderer
from blindspot_duel.config.settings import (
    WIDTH, HEIGHT, DEFAULT_AMMO, DEFAULT_TIME, HUD_MARGIN_X, HUD_MARGIN_Y,
    HUD_BOX_WIDTH, HUD_BOX_HEIGHT, HUD_BORDER_RADIUS, HUD_BORDER_WIDTH,
    HUD_TEXT_OFFSET_X, HUD_COMBO_OFFSET_X, HUD_TIME_BAR_WIDTH, HUD_TIME_BAR_HEIGHT,
    HUD_TIME_BAR_OFFSET_X, HUD_TIME_BAR_OFFSET_Y, HUD_TIME_TEXT_OFFSET_X,
    HUD_TIME_TEXT_OFFSET_Y, HUD_AMMO_DOT_SPACING, HUD_AMMO_DOT_RADIUS,
    HUD_AMMO_DOT_OFFSET_X, HUD_AMMO_DOT_OFFSET_Y, HUD_GLITCH_TEXT_OFFSET_Y
)
from blindspot_duel.config.thresholds import (
    MIN_COMBO_FOR_TEXT, HUD_TIME_WARN_HIGH, HUD_TIME_WARN_LOW
)
from blindspot_duel.config.colors import (
    P1_COLOR, P2_COLOR, HUD_BG_COLOR, TEXT_COLOR, COMBO_COLOR,
    HUD_TIME_BAR_BG_COLOR, TIME_COLOR, AMMO_COLOR, ALERT_RED_COLOR,
    HUD_LABEL_COLOR, HUD_EMPTY_AMMO_COLOR, GLITCH_COLOR
)


class PlayerDashboard:
    """
    Renders status bars and stats elegantly.
    """

    def __init__(self):
        self.text_renderer = TextRenderer()

    def draw(self, p1, p2, surface) -> None:
        # Draw P1 Stats (Left Corner)
        self.draw_player_hud(p1, HUD_MARGIN_X, HUD_MARGIN_Y, surface, is_left=True)

        # Draw P2 Stats (Right Corner)
        self.draw_player_hud(p2, WIDTH - HUD_MARGIN_X, HUD_MARGIN_Y, surface, is_left=False)

    def draw_player_hud(self, p, x: float, y: float, surface, is_left: bool) -> None:
        theme_color = P1_COLOR if is_left else P2_COLOR
        align = "left" if is_left else "right"

        # Draw background container box
        box_width = HUD_BOX_WIDTH
        box_height = HUD_BOX_HEIGHT
        bx = int(x) if is_left else int(x - box_width)
        by = int(y)

        # Transparent box background
        container = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        container.fill(HUD_BG_COLOR)  # Dark transparent backing
        pygame.draw.rect(container, theme_color, (0, 0, box_width, box_height), HUD_BORDER_WIDTH, border_radius=HUD_BORDER_RADIUS)
        surface.blit(container, (bx, by))

        # Text positioning offsets
        offset_x = HUD_TEXT_OFFSET_X if is_left else -HUD_TEXT_OFFSET_X
        tx = x + offset_x

        # Player name & Score
        name_text = f"{p.username}"
        score_text = f"SCORE: {p.score}"
        self.text_renderer.render_text(name_text, tx, y + 8, surface, color=theme_color, size=18, align=align)
        self.text_renderer.render_text(score_text, tx, y + 26, surface, color=TEXT_COLOR, size=14, align=align)

        # Display Combo
        if p.combo >= MIN_COMBO_FOR_TEXT:
            combo_offset = HUD_COMBO_OFFSET_X if is_left else -HUD_COMBO_OFFSET_X
            self.text_renderer.render_text(f"COMBO x{p.combo}!", tx + combo_offset, y + 26, surface, color=COMBO_COLOR, size=14, align=align)

        # Draw Time bar
        time_bar_width = HUD_TIME_BAR_WIDTH
        time_bar_height = HUD_TIME_BAR_HEIGHT
        tbx = bx + HUD_TIME_BAR_OFFSET_X if is_left else bx + (box_width - time_bar_width - HUD_TIME_BAR_OFFSET_X)
        tby = by + HUD_TIME_BAR_OFFSET_Y

        # Base bar container
        pygame.draw.rect(surface, HUD_TIME_BAR_BG_COLOR, (tbx, tby, time_bar_width, time_bar_height), border_radius=3)

        # Active bar fill
        time_pct = max(0.0, min(1.0, p.time_remaining / DEFAULT_TIME))
        fill_width = int(time_bar_width * time_pct)
        # Select color based on warning thresholds
        if time_pct > HUD_TIME_WARN_HIGH:
            bar_color = TIME_COLOR  # Cyan
        elif time_pct > HUD_TIME_WARN_LOW:
            bar_color = COMBO_COLOR  # Gold (same as combo/ammo color)
        else:
            bar_color = ALERT_RED_COLOR  # Alert Red

        if fill_width > 0:
            pygame.draw.rect(surface, bar_color, (tbx, tby, fill_width, time_bar_height), border_radius=3)

        # Display time number
        time_num = f"{p.time_remaining:.1f}s"
        t_num_x = tbx + time_bar_width + HUD_TIME_TEXT_OFFSET_X if is_left else tbx - HUD_TIME_TEXT_OFFSET_X
        t_num_align = "left" if is_left else "right"
        self.text_renderer.render_text(time_num, t_num_x, tby + HUD_TIME_TEXT_OFFSET_Y, surface, color=bar_color, size=12, align=t_num_align)

        # Draw Ammo indicator
        abx = bx + 10 if is_left else bx + 10
        aby = by + 62
        self.text_renderer.render_text("AMMO:", abx, aby, surface, color=HUD_LABEL_COLOR, size=11, align="left")

        # Draw bullet dots
        for idx in range(DEFAULT_AMMO):
            dot_color = AMMO_COLOR if idx < p.ammo else HUD_EMPTY_AMMO_COLOR
            dot_x = abx + HUD_AMMO_DOT_OFFSET_X + idx * HUD_AMMO_DOT_SPACING
            pygame.draw.circle(surface, dot_color, (dot_x, aby + HUD_AMMO_DOT_OFFSET_Y), HUD_AMMO_DOT_RADIUS)

        # Draw Glitch status
        if p.glitch_timer > 0.0:
            glitch_x = bx + box_width / 2
            glitch_y = by + HUD_GLITCH_TEXT_OFFSET_Y
            self.text_renderer.render_text("GLITCH ACTIVE!", glitch_x, glitch_y, surface, color=GLITCH_COLOR, size=12, align="center")