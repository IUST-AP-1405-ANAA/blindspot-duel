"""
Leaderboard screen logic and rendering with cyberpunk panels.
"""
import pygame
from src.contracts.i_state import IState
from src.contracts.i_renderable import IRenderable

import src.config.settings as cfg
from src.config.colors import (
    LEADERBOARD_TITLE_COLOR, LEADERBOARD_SUBTITLE_COLOR, LEADERBOARD_PANEL_BG,
    LEADERBOARD_BORDER_COLOR, LEADERBOARD_HEADER_COLOR, LEADERBOARD_LINE_COLOR,
    LEADERBOARD_NO_DATA_COLOR, RANK_1_COLOR, RANK_2_COLOR, RANK_3_COLOR,
    RANK_DEFAULT_COLOR, LEADERBOARD_TEXT_COLOR, LEADERBOARD_FOOTER_COLOR
)
from src.config.messages import (
    LEADERBOARD_TITLE, LEADERBOARD_SUBTITLE, LEADERBOARD_COL_RANK,
    LEADERBOARD_COL_USERNAME, LEADERBOARD_COL_SCORE, LEADERBOARD_NO_DATA,
    LEADERBOARD_FOOTER
)


class LeaderboardScreen(IState):
    """
    Displays match entries from database inside a high-tech panel.
    """

    def __init__(self, state_manager, database):
        self.state_manager = state_manager
        self.database = database
        self.leaderboard_entries = []

    def enter(self) -> None:
        self.leaderboard_entries = self.database.get_top_scores(cfg.LEADERBOARD_LIMIT)

    def update(self, dt: float, commands: dict) -> None:
        for event in commands["raw_events"]:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
                    self.state_manager.engine.audio.play_sfx("hit")
                    self.state_manager.change_state("MAIN_MENU")

    def render(self, renderer: IRenderable) -> None:
        # Title
        renderer.draw_ui_text(LEADERBOARD_TITLE, 400, 60, color=LEADERBOARD_TITLE_COLOR, size=36, align="center")
        renderer.draw_ui_text(LEADERBOARD_SUBTITLE, 400, 100, color=LEADERBOARD_SUBTITLE_COLOR, size=12, align="center")

        # Leaderboard panel container
        bx = cfg.LEADERBOARD_BOX_X
        by = cfg.LEADERBOARD_BOX_Y
        bw = cfg.LEADERBOARD_BOX_WIDTH
        bh = cfg.LEADERBOARD_BOX_HEIGHT

        container = pygame.Surface((bw, bh), pygame.SRCALPHA)
        container.fill(LEADERBOARD_PANEL_BG)
        pygame.draw.rect(container, LEADERBOARD_BORDER_COLOR, (0, 0, bw, bh), 1, border_radius=cfg.LEADERBOARD_BOX_BORDER_RADIUS)
        renderer.screen.blit(container, (bx, by))

        # Headers
        renderer.draw_ui_text(LEADERBOARD_COL_RANK, bx + 30, by + 20, color=LEADERBOARD_HEADER_COLOR, size=15)
        renderer.draw_ui_text(LEADERBOARD_COL_USERNAME, bx + 120, by + 20, color=LEADERBOARD_HEADER_COLOR, size=15)
        renderer.draw_ui_text(LEADERBOARD_COL_SCORE, bx + 420, by + 20, color=LEADERBOARD_HEADER_COLOR, size=15)

        # Horizontal line
        pygame.draw.line(renderer.screen, LEADERBOARD_LINE_COLOR, (bx + 20, by + 45), (bx + bw - 20, by + 45), 1)

        # Content
        if not self.leaderboard_entries:
            renderer.draw_ui_text(LEADERBOARD_NO_DATA, 400, by + 180, color=LEADERBOARD_NO_DATA_COLOR, size=18, align="center")
        else:
            for i, entry in enumerate(self.leaderboard_entries):
                y_pos = by + cfg.LEADERBOARD_ROW_Y_START + i * cfg.LEADERBOARD_ROW_Y_SPACING

                # Rank coloring
                if i == 0:
                    rank_color = RANK_1_COLOR   # Gold
                elif i == 1:
                    rank_color = RANK_2_COLOR  # Silver
                elif i == 2:
                    rank_color = RANK_3_COLOR  # Bronze
                else:
                    rank_color = RANK_DEFAULT_COLOR

                rank_str = f"# {entry.rank}"
                renderer.draw_ui_text(rank_str, bx + 30, y_pos, color=rank_color, size=13)
                renderer.draw_ui_text(entry.player_name, bx + 120, y_pos, color=LEADERBOARD_TEXT_COLOR, size=13)
                renderer.draw_ui_text(str(entry.score), bx + 420, y_pos, color=LEADERBOARD_TEXT_COLOR, size=13)

        renderer.draw_ui_text(LEADERBOARD_FOOTER, 400, 545, color=LEADERBOARD_FOOTER_COLOR, size=13, align="center")

    def exit(self) -> None:
        pass