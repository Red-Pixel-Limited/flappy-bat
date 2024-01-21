import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from player import Player

class SettingsWindow(pygame_gui.elements.UIWindow):
    def __init__(self, rect, manager, player: Player):
        super().__init__(rect, manager,
                         window_display_title="Settings",
                         object_id='#settings_window',
                         resizable=False)

        self.save_btn = UIButton(pygame.Rect((int(self.rect.width - 150), int(self.rect.height - 109)), (100, 30)),
                                'Save',
                                self.ui_manager,
                                container=self,
                                object_id='#save_button')
    
