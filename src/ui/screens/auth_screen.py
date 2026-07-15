import pygame
import math
from src.contracts.i_state import IState
from src.contracts.i_renderable import IRenderable

import src.config.settings as cfg
from src.config.colors import (
    P1_COLOR, P2_COLOR, TEXT_COLOR, AUTH_BOX_BG, INACTIVE_FIELD_BORDER,
    AUTH_LABEL_COLOR, SUCCESS_COLOR, ERROR_COLOR, FOOTER_TEXT_COLOR, FOOTER_ALT_TEXT_COLOR
)
from src.config.messages import (
    AUTH_TITLE, AUTH_CONFIGURING_PREFIX, AUTH_LABEL_USERNAME, AUTH_LABEL_PASSWORD,
    AUTH_ERR_EMPTY_FIELDS, AUTH_ERR_DUPLICATE_P2, AUTH_ERR_FAILED,
    AUTH_MSG_P1_VERIFIED, AUTH_FOOTER_NAV, AUTH_FOOTER_EXIT
)


class AuthScreen(IState):
    """
    Draws styled login forms.
    """

    def __init__(self, state_manager, database):
        self.state_manager = state_manager
        self.database = database

        self.p1_authenticated = False
        self.p2_authenticated = False

        self.reset_form()

    def reset_form(self):
        self.username_input = ""
        self.password_input = ""
        self.active_field = "username"  # or "password"
        self.error_message = ""
        self.success_message = ""

    def enter(self) -> None:
        self.reset_form()
        self.p1_authenticated = False
        self.p2_authenticated = False
        self.state_manager.p1_username = "Player1"
        self.state_manager.p2_username = "Player2"

    def update(self, dt: float, commands: dict) -> None:
        for event in commands["raw_events"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.active_field = "password" if self.active_field == "username" else "username"
                    self.state_manager.engine.audio.play_sfx("shoot")
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_field == "username":
                        self.username_input = self.username_input[:-1]
                    else:
                        self.password_input = self.password_input[:-1]
                elif event.key == pygame.K_RETURN:
                    self.submit_auth()
                elif event.key == pygame.K_ESCAPE:
                    self.state_manager.is_running = False
                else:
                    if event.unicode.isalnum() or event.unicode in cfg.ALLOWED_CHARS:
                        if self.active_field == "username" and len(self.username_input) < cfg.MAX_USERNAME_LEN:
                            self.username_input += event.unicode
                        elif self.active_field == "password" and len(self.password_input) < cfg.MAX_PASSWORD_LEN:
                            self.password_input += event.unicode

    def submit_auth(self):
        if not self.username_input or not self.password_input:
            self.error_message = AUTH_ERR_EMPTY_FIELDS
            self.state_manager.engine.audio.play_sfx("miss")
            return

        success = self.database.authenticate_or_register(self.username_input, self.password_input)
        if success:
            self.state_manager.engine.audio.play_sfx("hit")
            if not self.p1_authenticated:
                self.state_manager.p1_username = self.username_input
                self.p1_authenticated = True
                self.reset_form()
                self.success_message = AUTH_MSG_P1_VERIFIED
            elif not self.p2_authenticated:
                if self.username_input == self.state_manager.p1_username:
                    self.error_message = AUTH_ERR_DUPLICATE_P2
                    self.state_manager.engine.audio.play_sfx("miss")
                    return
                self.state_manager.p2_username = self.username_input
                self.p2_authenticated = True
                self.state_manager.change_state("MAIN_MENU")
        else:
            self.error_message = AUTH_ERR_FAILED
            self.state_manager.engine.audio.play_sfx("miss")

    def render(self, renderer: IRenderable) -> None:
        curr_p = "PLAYER 1" if not self.p1_authenticated else "PLAYER 2"
        theme_color = P1_COLOR if not self.p1_authenticated else P2_COLOR

        # Display title
        renderer.draw_ui_text(AUTH_TITLE, cfg.AUTH_BOX_X, 80, color=TEXT_COLOR, size=32, align="center")
        renderer.draw_ui_text(f"{AUTH_CONFIGURING_PREFIX}{curr_p}", cfg.AUTH_BOX_X, 130, color=theme_color, size=18, align="center")

        # Container box
        box_w = cfg.AUTH_BOX_WIDTH
        box_h = cfg.AUTH_BOX_HEIGHT
        bx = cfg.AUTH_BOX_X - box_w // 2
        by = cfg.AUTH_BOX_Y

        container = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        container.fill(AUTH_BOX_BG)
        pygame.draw.rect(container, theme_color, (0, 0, box_w, box_h), 1, border_radius=cfg.AUTH_BOX_BORDER_RADIUS)
        renderer.screen.blit(container, (bx, by))

        # Draw input boxes
        u_glow = theme_color if self.active_field == "username" else INACTIVE_FIELD_BORDER
        p_glow = theme_color if self.active_field == "password" else INACTIVE_FIELD_BORDER

        # Username input box
        pygame.draw.rect(renderer.screen, u_glow, (bx + 140, by + 40, 280, 36), 1, border_radius=cfg.AUTH_INPUT_BORDER_RADIUS)
        renderer.draw_ui_text(AUTH_LABEL_USERNAME, bx + 20, by + 48, color=AUTH_LABEL_COLOR, size=16)
        renderer.draw_ui_text(self.username_input, bx + 150, by + 48, color=TEXT_COLOR, size=16)

        # Password input box
        pygame.draw.rect(renderer.screen, p_glow, (bx + 140, by + 110, 280, 36), 1, border_radius=cfg.AUTH_INPUT_BORDER_RADIUS)
        renderer.draw_ui_text(AUTH_LABEL_PASSWORD, bx + 20, by + 118, color=AUTH_LABEL_COLOR, size=16)
        masked_pass = "*" * len(self.password_input)
        renderer.draw_ui_text(masked_pass, bx + 150, by + 118, color=TEXT_COLOR, size=16)

        # Error/Success
        if self.error_message:
            renderer.draw_ui_text(self.error_message, cfg.AUTH_BOX_X, by + 185, color=ERROR_COLOR, size=14, align="center")
        elif self.success_message:
            renderer.draw_ui_text(self.success_message, cfg.AUTH_BOX_X, by + 185, color=SUCCESS_COLOR, size=14, align="center")

        # Footers
        renderer.draw_ui_text(AUTH_FOOTER_NAV, cfg.AUTH_BOX_X, 460, color=FOOTER_TEXT_COLOR, size=12, align="center")
        renderer.draw_ui_text(AUTH_FOOTER_EXIT, cfg.AUTH_BOX_X, 490, color=FOOTER_ALT_TEXT_COLOR, size=12, align="center")

    def exit(self) -> None:
        pass