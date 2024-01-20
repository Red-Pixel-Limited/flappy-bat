import pygame
import pygame_gui
from sys import exit
from random import randint
from enum import Enum

# Game

pygame.init()

window_height = 700
window_width = 551
scroll_speed = 2
scores = 0

screen = pygame.display.set_mode((window_width, window_height))
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

        global scores
        if self.tower_pos == TowerPosition.BOTTOM:
            if bat_pos[0] > self.rect.topleft[0] and not self.pas:
                self.enter = True
            if bat_pos[0] > self.rect.topright[0] and not self.pas:
                self.leave = True
            if self.enter and self.leave and not self.pas:
                self.pas = True
                scores += 1


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
    global scores
    scores = 0
    bat = pygame.sprite.GroupSingle()
    bat.add(Bat())

    tower_time = 0
    towers = pygame.sprite.Group()

    x_posit_ground, y_posit_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_posit_ground, y_posit_ground))

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
        scores_text = font.render("Scores: " + str(scores), True, scores_color)

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
                bg_music.stop()
                game_over_sound.play(loops=0)

            screen.blit(game_over_pic, (window_width//2 - game_over_pic.get_width()//2, window_height//3))

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

    manager = pygame_gui.UIManager(
        (window_width, window_height), "./themes/menu.json")

    screen.fill((0, 0, 0))
    screen.blit(sky_pic, (0, 0))
    screen.blit(ground_pic, (0, 520))
    
    x = window_width // 2 - start_game_pic.get_width() // 2
    y = 130
    screen.blit(start_game_pic, (x, y))

    start_game_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (195, 230), (155, 40)),  text="Start", manager=manager)

    settings_game_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (195, 280), (155, 40)),  text="Settings", manager=manager)

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.display.quit()
                exit()
            elif (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == start_game_btn) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                start_game()
            elif (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == settings_game_btn):
                settings_window = pygame_gui.elements.UIWindow(rect=pygame.Rect(
                    (100, 100), (200, 100)), window_display_title="Settings", resizable=True)
                settings_window.show()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()


menu()
