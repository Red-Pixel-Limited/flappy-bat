import pygame
import pygame_gui
from sys import exit
from random import randint
from enum import Enum
from windows.scores import ScoresWindow
from windows.settings import SettingsWindow
from db.repository import Repository
from player import *
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
from pygame.sprite import Sprite, GroupSingle, Group
from pygame.rect import Rect


class Bat(Sprite):
    def __init__(self, bat_pics, bat_pos, lift_key):
        Sprite.__init__(self)
        self.bat_pics = bat_pics
        self.image = bat_pics[0]
        self.rect = self.image.get_rect()
        self.rect.center = bat_pos
        self.image_index = 0
        self.velocity = 0
        self.jump = False
        self.vital = True
        self.lift_key = lift_key

    def update(self, user_input):
        if self.vital:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = self.bat_pics[self.image_index // 10]

        self.velocity += 0.5
        if self.velocity > 7:
            self.velocity = 7
        if self.rect.y < 500:
            self.rect.y += int(self.velocity)
        if self.velocity == 0:
            self.jump = False

        self.image = pygame.transform.rotate(self.image, self.velocity * -7)

        if user_input[self.lift_key] and not self.jump and self.rect.y > 0 and self.vital:
            self.jump = True
            self.velocity = -7


class TowerPosition(Enum):
    TOP = 1
    BOTTOM = 2


class Tower(Sprite):
    def __init__(self, x, y, image, tower_pos):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.leave, self.pas = False, False, False
        self.tower_pos = tower_pos

    def update(self, game):
        self.rect.x -= game.scroll_speed
        if self.rect.x <= -game.window_width:
            self.kill()

        if self.tower_pos == TowerPosition.BOTTOM:
            if game.bat_pos[0] > self.rect.topleft[0] and not self.pas:
                self.enter = True
            if game.bat_pos[0] > self.rect.topright[0] and not self.pas:
                self.leave = True
            if self.enter and self.leave and not self.pas:
                self.pas = True
                game.scores_per_game += 1


class Ground(Sprite):
    def __init__(self, x, y, ground_pic):
        Sprite.__init__(self)
        self.image = ground_pic
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, game):
        self.rect.x -= game.scroll_speed
        if self.rect.x <= -game.window_width:
            self.kill()


class FlappyBatGame:
    def __init__(self, window_height, window_width, player: Player, repository: Repository):
        pygame.init()
        pygame.display.set_caption("Flappy bat")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/MetaversRounded.otf", 24)
        self.screen = pygame.display.set_mode((window_width, window_height))

        self.window_height = window_height
        self.window_width = window_width
        self.scroll_speed = 2
        self.scores_per_game = 0
        self.player = player
        self.repository = repository

        # Sounds

        self.bg_music = pygame.mixer.Sound("audio/decisive_battle_loop.wav")
        self.game_over_sound = pygame.mixer.Sound("audio/decisive_battle_end.wav")

        # Images

        self.start_game_pic = pygame.image.load("images/start.png")
        self.game_over_pic = pygame.image.load("images/game_over.png")

        self.sky_pic = pygame.image.load("images/background.png")
        self.ground_pic = pygame.image.load("images/ground.png")

        self.top_tower_pic = pygame.image.load("images/tower_top.png")
        self.bottom_tower_pic = pygame.image.load("images/tower_bottom.png")

        self.bat_pos = (100, 250)
        self.bat_pics = [
            pygame.image.load("images/bat_up.png").convert_alpha(),
            pygame.image.load("images/bat_down.png").convert_alpha(),
            pygame.image.load("images/bat_mid.png").convert_alpha()]

        bat_icon = pygame.image.load("images/bat.png").convert_alpha()
        pygame.display.set_icon(bat_icon)

        self.pygame_keys = {
            LiftKey.Space: pygame.K_SPACE,
            LiftKey.Up: pygame.K_UP,
            LiftKey.W: pygame.K_w
        }

    def start(self):
        self.scores_per_game = 0

        match self.player.settings.lift_key:
            case "space":
                self.bat_pos = (100, 250)
                self.bat_pics = [
                    pygame.image.load("images/bat_up.png").convert_alpha(),
                    pygame.image.load("images/bat_down.png").convert_alpha(),
                    pygame.image.load("images/bat_mid.png").convert_alpha()]
                
        bat = GroupSingle()
        bat.add(Bat(self.bat_pics, self.bat_pos, lift_key=self.pygame_keys[self.player.settings.lift_key]))

        tower_time = 0
        towers = Group()

        x_posit_ground, y_posit_ground = 0, 520
        ground = Group()
        ground.add(Ground(x_posit_ground, y_posit_ground, self.ground_pic))

        if self.player.settings.sound_on():
            self.bg_music.set_volume(self.player.settings.volume / 100)
            self.bg_music.play(loops=-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    exit()

            self.screen.fill((0, 0, 0))

            user_input = pygame.key.get_pressed()

            self.screen.blit(self.sky_pic, (0, 0))

            if len(ground) <= 2:
                ground.add(Ground(self.window_width, y_posit_ground, self.ground_pic))

            towers.draw(self.screen)
            ground.draw(self.screen)
            bat.draw(self.screen)

            scores_color = pygame.Color(255, 255, 255)
            scores_text = self.font.render(
                f"Scores: {str(self.scores_per_game)}", True, scores_color)

            self.screen.blit(scores_text, (20, 20))

            if bat.sprite.vital:
                towers.update(self)
                ground.update(self)
                bat.update(user_input)

            collide_towers = pygame.sprite.spritecollide(bat.sprites()[0], towers, False)
            collide_ground = pygame.sprite.spritecollide(bat.sprites()[0], ground, False)

            if collide_ground or collide_towers:

                if bat.sprite.vital:
                    bat.sprite.vital = False

                    if self.player.settings.sound_on():
                        self.bg_music.stop()
                        self.game_over_sound.set_volume(self.player.settings.volume / 100)
                        self.game_over_sound.play(loops=0)

                    self.player.scores += self.scores_per_game
                    self.repository.update_scores(self.player)

                self.screen.blit(self.game_over_pic,
                                 (self.window_width//2 - self.game_over_pic.get_width()//2, self.window_height//3))

                if user_input[pygame.K_r]:
                    self.start()
                elif user_input[pygame.K_m]:
                    self.display_menu()
                elif user_input[pygame.K_ESCAPE]:
                    pygame.display.quit()
                    exit()

            if tower_time <= 0 and bat.sprite.vital:
                x_top, x_bot = 550, 550
                y_top = randint(-600, -480)
                y_bot = y_top + randint(90, 130) + \
                    self.bottom_tower_pic.get_height()
                towers.add(Tower(x_top, y_top, self.top_tower_pic, TowerPosition.TOP))
                towers.add(Tower(x_bot, y_bot, self.bottom_tower_pic, TowerPosition.BOTTOM))
                tower_time = randint(180, 250)
            tower_time -= 1

            self.clock.tick(60)/1000.0
            pygame.display.update()

    def display_menu(self):
        settings_window = None

        manager = UIManager((self.window_width, self.window_height), "./themes/main.json")

        start_game_btn = UIButton(relative_rect=Rect((195, 220), (155, 40)), text="Start", manager=manager)
        scores_btn = UIButton(relative_rect=Rect((195, 270), (155, 40)),  text="Scores", manager=manager)
        settings_btn = UIButton(relative_rect=Rect((195, 320), (155, 40)),  text="Settings", manager=manager)

        while True:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    exit()
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_game_btn:
                        self.start()
                    elif event.ui_element == scores_btn:
                        players = self.repository.get_top_20_players()
                        ScoresWindow(Rect((10, 10), (400, 500)), manager=manager, players=players)
                    elif event.ui_element == settings_btn:
                        settings_window = SettingsWindow(Rect((10, 10), (400, 320)), manager=manager, player=self.player)
                    elif settings_window and event.ui_element == settings_window.save_btn:
                        self.player.settings.volume = int(settings_window.volume_slider.get_current_value())
                        self.player.settings.lift_key = settings_window.keys_list.selected_option
                        self.repository.update_settings(self.player)
                        settings_window.kill()

                manager.process_events(event)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.sky_pic, (0, 0))
            self.screen.blit(self.ground_pic, (0, 520))
            self.screen.blit(self.bat_pics[0], (100, 250))

            x = self.window_width // 2 - self.start_game_pic.get_width() // 2
            y = 120
            self.screen.blit(self.start_game_pic, (x, y))

            manager.update(time_delta)
            manager.draw_ui(self.screen)

            pygame.display.update()
