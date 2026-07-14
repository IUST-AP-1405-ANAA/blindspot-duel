import pygame
from blindspot_duel.contracts.i_state import IState
from blindspot_duel.contracts.i_renderable import IRenderable
from blindspot_duel.config.messages import MATCH_RESULTS_TITLE, MATCH_RESULTS_SUBTITLE, MATCH_RESULTS_WINNER, MATCH_RESULTS_TIE, MATCH_RESULTS_STATS, MATCH_RESULTS_FOOTER
from blindspot_duel.config.colors import (
    MENU_TITLE_COLOR, MENU_SUBTITLE_COLOR, P1_COLOR, P2_COLOR, TEXT_COLOR, MENU_FOOTER_COLOR, BG_COLOR
)
import blindspot_duel.config.settings as cfg


class MatchResultsScreen(IState):
    """
    Displays the final scores of the two players before proceeding to the global leaderboard.
    """
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def enter(self) -> None:
        pass

    def update(self, dt: float, commands: dict) -> None:
        for event in commands["raw_events"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state_manager.engine.audio.play_sfx("hit")
                    self.state_manager.change_state("LEADERBOARD")
                elif event.key == pygame.K_ESCAPE:
                    self.state_manager.engine.audio.play_sfx("hit")
                    self.state_manager.change_state("MAIN_MENU")

    def render(self, renderer: IRenderable) -> None:
        renderer.clear_screen(BG_COLOR)

        # Title
        renderer.draw_ui_text(MATCH_RESULTS_TITLE, cfg.WIDTH//2, 80, color=MENU_TITLE_COLOR, size=36, align="center")
        renderer.draw_ui_text(MATCH_RESULTS_SUBTITLE, cfg.WIDTH//2, 120, color=MENU_SUBTITLE_COLOR, size=14, align="center")

        stats = getattr(self.state_manager, "last_match_stats", None)
        if not stats:
            return

        p1_score = stats["p1_score"]
        p2_score = stats["p2_score"]

        # Winner text
        if p1_score > p2_score:
            winner_text = MATCH_RESULTS_WINNER.format(stats["p1_name"])
            winner_color = P1_COLOR
        elif p2_score > p1_score:
            winner_text = MATCH_RESULTS_WINNER.format(stats["p2_name"])
            winner_color = P2_COLOR
        else:
            winner_text = MATCH_RESULTS_TIE
            winner_color = TEXT_COLOR

        renderer.draw_ui_text(winner_text, cfg.WIDTH//2, 220, color=winner_color, size=28, align="center")

        # P1 Stats
        pygame.draw.rect(renderer.screen, P1_COLOR, (cfg.WIDTH//4 - 150, 300, 300, 100), 2, border_radius=8)
        renderer.draw_ui_text(f"P1: {stats['p1_name']}", cfg.WIDTH//4, 320, color=P1_COLOR, size=20, align="center")
        renderer.draw_ui_text(MATCH_RESULTS_STATS.format(stats["p1_score"], stats["p1_combo"]), cfg.WIDTH//4, 360, color=TEXT_COLOR, size=14, align="center")

        # P2 Stats
        pygame.draw.rect(renderer.screen, P2_COLOR, (3 * cfg.WIDTH//4 - 150, 300, 300, 100), 2, border_radius=8)
        renderer.draw_ui_text(f"P2: {stats['p2_name']}", 3 * cfg.WIDTH//4, 320, color=P2_COLOR, size=20, align="center")
        renderer.draw_ui_text(MATCH_RESULTS_STATS.format(stats["p2_score"], stats["p2_combo"]), 3 * cfg.WIDTH//4, 360, color=TEXT_COLOR, size=14, align="center")

        # Footer
        renderer.draw_ui_text(MATCH_RESULTS_FOOTER, cfg.WIDTH//2, cfg.HEIGHT - 40, color=MENU_FOOTER_COLOR, size=12, align="center")

    def exit(self) -> None:
        pass