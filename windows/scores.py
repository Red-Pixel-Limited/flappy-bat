import pygame
import pygame_gui

class ScoresWindow(pygame_gui.elements.UIWindow):
    def __init__(self, rect, manager):
        super().__init__(rect, manager,
                         window_display_title="Top players",
                         object_id='#scores_window',
                         resizable=True)
        self.set_blocking(True)
