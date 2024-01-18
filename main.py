import pygame
from sys import exit
import random as ra
from pygame.sprite import Group

# Game

pygame.init()

window_height = 700
window_width = 551
scroll_speed = 2
scores = 0

screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe", 30)

start_game_pic = pygame.image.load("graphics/start.png")
game_over_pic = pygame.image.load("graphics/game_over.png")

# Background

sky_pic = pygame.image.load("graphics/background.png")
ground_pic = pygame.image.load("graphics/ground.png")

# Tower

top_tower_pic = pygame.image.load("graphics/tower_top.png")
bottom_tower_pic = pygame.image.load("graphics/tower_bottom.png")

# Bat

bat_pos = (100, 250)
bat_pics = [pygame.image.load("graphics/bat_up.png").convert_alpha(),
            pygame.image.load("graphics/bat_down.png").convert_alpha(),
            pygame.image.load("graphics/bat_mid.png").convert_alpha()]


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


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tower_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.leave, self.pas = False, False, False
        self.tower_type = tower_type

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -window_width:
            self.kill()

        global scores
        if self.tower_type == "bot":
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


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def start_game():
    global scores
    entity = pygame.sprite.GroupSingle()
    entity.add(Bat())

    tower_time = 0
    towers = pygame.sprite.Group()

    x_posit_ground, y_posit_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_posit_ground, y_posit_ground))

    while True:
        close_game()

        screen.fill((0, 0, 0))

        user_input = pygame.key.get_pressed()

        screen.blit(sky_pic, (0, 0))

        if len(ground) <= 2:
            ground.add(Ground(window_width, y_posit_ground))

        towers.draw(screen)
        ground.draw(screen)
        entity.draw(screen)

        scores_text = font.render(
            "Scores: " + str(scores),
            True,
            pygame.Color(255, 255, 255)
        )

        screen.blit(scores_text, (20, 20))

        if entity.sprite.vital:
            towers.update()
            ground.update()
            entity.update(user_input)

        col_towers = pygame.sprite.spritecollide(
            entity.sprites()[0], towers, False)
        col_ground = pygame.sprite.spritecollide(
            entity.sprites()[0], ground, False)
        if col_ground or col_towers:
            entity.sprite.vital = False
            if col_ground or col_towers:
                screen.blit(game_over_pic, (window_width//2 - game_over_pic.get_width()//2,
                                            window_height//2 - game_over_pic.get_height()//2))

                if user_input[pygame.K_r]:
                    scores = 0
                    break

        if tower_time <= 0 and entity.sprite.vital:
            x_top, x_bot = 550, 550
            y_top = ra.randint(-600, -480)
            y_bot = y_top + ra.randint(90, 130) + bottom_tower_pic.get_height()
            towers.add(Tower(x_top, y_top, top_tower_pic, "top"))
            towers.add(Tower(x_bot, y_bot, bottom_tower_pic, "bot"))
            tower_time = ra.randint(180, 250)
        tower_time -= 1

        clock.tick(60)
        pygame.display.update()


def main():

    while True:
        close_game()

        screen.fill((0, 0, 0))
        screen.blit(sky_pic, (0, 0))
        screen.blit(ground_pic, (0, 520))
        screen.blit(bat_pics[0], (100, 250))
        screen.blit(start_game_pic, (window_width//2 - start_game_pic.get_width()//2,
                                     window_height//2 - start_game_pic.get_height()//2))

        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            start_game()

        pygame.display.update()


main()
