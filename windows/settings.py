import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UIDropDownMenu
from player import Player, LiftKey


class SettingsWindow(pygame_gui.elements.UIWindow):
    def __init__(self, rect, manager, player: Player):
        super().__init__(rect, manager,
                         window_display_title="Settings",
                         object_id='#settings_window',
                         resizable=False)

        self.key_label = UILabel(pygame.Rect((self.rect.width - 372, self.rect.height - 300), (100, 20)),
                                 "Lift key:",
                                 self.ui_manager,
                                 container=self)

        self.keys_list = UIDropDownMenu([LiftKey.Space, LiftKey.Up, LiftKey.W],
                                        player.settings.lift_key,
                                        pygame.Rect((self.rect.width - 360, self.rect.height - 270), (260, 25)),
                                        self.ui_manager,
                                        container=self)

        self.volume_label = UILabel(pygame.Rect((self.rect.width - 380, self.rect.height - 220), (100, 20)),
                                    "Volume:",
                                    self.ui_manager,
                                    container=self)

        self.volume_slider = UIHorizontalSlider(pygame.Rect((self.rect.width - 360, self.rect.height - 190), (260, 25)),
                                                player.settings.volume,
                                                (0.0, 100.0),
                                                self.ui_manager,
                                                container=self,
                                                click_increment=10)

        self.slider_label = UILabel(pygame.Rect((self.rect.width - 86, self.rect.height - 186), (23, 20)),
                                    str(int(self.volume_slider.get_current_value())),
                                    self.ui_manager,
                                    container=self)

        self.save_btn = UIButton(pygame.Rect((self.rect.width - 155, self.rect.height - 112), (100, 30)),
                                 'Save',
                                 self.ui_manager,
                                 container=self,
                                 object_id='#save_button')

    def update(self, time_delta):
        super().update(time_delta)

        if self.alive() and self.volume_slider.has_moved_recently:
            self.slider_label.set_text(str(int(self.volume_slider.get_current_value())))
