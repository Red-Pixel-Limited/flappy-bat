import pygame
from typing import Tuple
from pygame_gui.elements import UITextBox, UIWindow


class ScoresWindow(UIWindow):
    def __init__(self, rect, manager, players: list[Tuple[str, int]]):
        super().__init__(rect, manager,
                         window_display_title="Top players",
                         object_id='#scores_window',
                         resizable=True)

        self.set_blocking(True)

        html_message = "<p>Players with top scores</p>" + \
            "".join([f"<p>{i + 1}. {username} {scores}</p>" for i, (username, scores)
                    in enumerate(players)]) if players else "<p>Nothing to show :(</p>"

        self.text_block = UITextBox(html_message,
                                    pygame.Rect(
                                        (0, 0), self.get_container().get_size()),
                                    manager=manager,
                                    container=self,
                                    anchors={"left": "left",
                                             "top": "top",
                                             "right": "right",
                                             "bottom": "bottom"})
