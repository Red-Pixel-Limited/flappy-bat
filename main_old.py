import pygame
import pygame_gui
from sys import exit
from random import randint
from enum import Enum
from windows.scores import ScoresWindow
from windows.settings import SettingsWindow
from db.repository import Repository
from player import *

# Game

pygame.init()

window_height = 700
window_width = 551
scroll_speed = 2
scores_per_game = 0
player = Player(username="Nick", scores=0, settings=Settings(volume=100))
repository = Repository(db_file_name='db/players.db')

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy bat")

clock = pygame.time.Clock()
font = pygame.font.Font("font/MetaversRounded.otf", 24)

start_game_pic = pygame.image.load("images/start.png")
game_over_pic = pygame.image.load("images/game_over.png")

# Background

sky_pic = pygame.image.load("images/background.png")
ground_pic = pygame.image.load("images/ground.png")

# Sounds

bg_music = pygame.mixer.Sound("audio/decisive_battle_loop.wav")
game_over_sound = pygame.mixer.Sound("audio/decisive_battle_end.wav")

# Tower

top_tower_pic = pygame.image.load("images/tower_top.png")
bottom_tower_pic = pygame.image.load("images/tower_bottom.png")

# Bat

bat_pos = (100, 250)
bat_pics = [pygame.image.load("images/bat_up.png").convert_alpha(),
            pygame.image.load("images/bat_down.png").convert_alpha(),
            pygame.image.load("images/bat_mid.png").convert_alpha()]


class Bat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bat_pics[0]
        self.rect = self.image.get_rect()
        self.rect.center = bat_pos
        self.image_index = 0
        self.velocity = 0
        self.jump = False
        self.vital = True

    def update(self, user_input):
        if self.vital:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bat_pics[self.image_index // 10]

        self.velocity += 0.5
        if self.velocity > 7:
            self.velocity = 7
        if self.rect.y < 500:
            self.rect.y += int(self.velocity)
        if self.velocity == 0:
            self.jump = False

        self.image = pygame.transform.rotate(self.image, self.velocity * -7)

        if user_input[pygame.K_SPACE] and not self.jump and self.rect.y > 0 and self.vital:
            self.jump = True
            self.velocity = -7


class TowerPosition(Enum):
    TOP = 1
    BOTTOM = 2


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tower_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.leave, self.pas = False, False, False
        self.tower_pos = tower_pos

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -window_width:
            self.kill()

        global scores_per_game
        if self.tower_pos == TowerPosition.BOTTOM:
            if bat_pos[0] > self.rect.topleft[0] and not self.pas:
                self.enter = True
            if bat_pos[0] > self.rect.topright[0] and not self.pas:
                self.leave = True
            if self.enter and self.leave and not self.pas:
                self.pas = True
                scores_per_game += 1


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_pic
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -window_width:
            self.kill()


def start_game():
    global scores_per_game
    scores_per_game = 0
    bat = pygame.sprite.GroupSingle()
    bat.add(Bat())

    tower_time = 0
    towers = pygame.sprite.Group()

    x_posit_ground, y_posit_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_posit_ground, y_posit_ground))

    if player.settings.sound_on():
        bg_music.set_volume(player.settings.volume / 100)
        bg_music.play(loops=-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.display.quit()
                exit()

        screen.fill((0, 0, 0))

        user_input = pygame.key.get_pressed()

        screen.blit(sky_pic, (0, 0))

        if len(ground) <= 2:
            ground.add(Ground(window_width, y_posit_ground))

        towers.draw(screen)
        ground.draw(screen)
        bat.draw(screen)

        scores_color = pygame.Color(255, 255, 255)
        scores_text = font.render(
            "Scores: " + str(scores_per_game), True, scores_color)

        screen.blit(scores_text, (20, 20))

        if bat.sprite.vital:
            towers.update()
            ground.update()
            bat.update(user_input)

        collide_towers = pygame.sprite.spritecollide(
            bat.sprites()[0], towers, False)
        collide_ground = pygame.sprite.spritecollide(
            bat.sprites()[0], ground, False)

        if collide_ground or collide_towers:

            if bat.sprite.vital:
                bat.sprite.vital = False

                if player.settings.sound_on():
                    bg_music.stop()
                    game_over_sound.set_volume(player.settings.volume / 100)
                    game_over_sound.play(loops=0)

                player.scores += scores_per_game

            screen.blit(game_over_pic, (window_width//2 -
                        game_over_pic.get_width()//2, window_height//3))

            if user_input[pygame.K_r]:
                start_game()
            elif user_input[pygame.K_m]:
                menu()
            elif user_input[pygame.K_ESCAPE]:
                pygame.display.quit()
                exit()

        if tower_time <= 0 and bat.sprite.vital:
            x_top, x_bot = 550, 550
            y_top = randint(-600, -480)
            y_bot = y_top + randint(90, 130) + bottom_tower_pic.get_height()
            towers.add(Tower(x_top, y_top, top_tower_pic, TowerPosition.TOP))
            towers.add(
                Tower(x_bot, y_bot, bottom_tower_pic, TowerPosition.BOTTOM))
            tower_time = randint(180, 250)
        tower_time -= 1

        clock.tick(60)/1000.0
        pygame.display.update()


def menu():
    settings_window = None

    manager = pygame_gui.UIManager(
        (window_width, window_height), "./themes/main.json")

    start_game_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (195, 220), (155, 40)),  text="Start", manager=manager)

    scores_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (195, 270), (155, 40)),  text="Scores", manager=manager)

    settings_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (195, 320), (155, 40)),  text="Settings", manager=manager)

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.display.quit()
                exit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_game_btn:
                    start_game()
                elif event.ui_element == scores_btn:
                    players = repository.get_top_20_players()
                    ScoresWindow(pygame.Rect((10, 10), (400, 500)), manager=manager, players=players)
                elif event.ui_element == settings_btn:
                    settings_window = SettingsWindow(pygame.Rect(
                        (10, 10), (400, 270)), manager=manager, player=player)
                elif settings_window and event.ui_element == settings_window.save_btn:
                    player.settings.volume = int(
                        settings_window.volume_slider.get_current_value())
                    # repository.update_settings(player)
                    settings_window.kill()

            manager.process_events(event)

        screen.fill((0, 0, 0))
        screen.blit(sky_pic, (0, 0))
        screen.blit(ground_pic, (0, 520))
        screen.blit(bat_pics[0], (100, 250))

        x = window_width // 2 - start_game_pic.get_width() // 2
        y = 120
        screen.blit(start_game_pic, (x, y))

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()


menu()
