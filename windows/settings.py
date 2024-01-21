import pygame_gui

class SettingsWindow(pygame_gui.elements.UIWindow):
    def __init__(self, rect, manager):
        super().__init__(rect, manager,
                         window_display_title="Settings",
                         object_id='#settings_window',
                         resizable=True)
        self.set_blocking(True)
