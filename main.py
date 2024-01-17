import pygame as pg
from sys import exit
import random as ra
from pygame.sprite import Group

pg.init()
clock = pg.time.Clock()

s_height = 700
s_width = 551
screen = pg.display.set_mode((s_width, s_height))

entity_pics = [pg.image.load("graphics/bat_up.png").convert_alpha(),
               pg.image.load("graphics/bat_down.png").convert_alpha(),
               pg.image.load("graphics/bat_mid.png").convert_alpha()]

top_tower_pic = pg.image.load("graphics/tower_top.png")
bottom_tower_pic = pg.image.load("graphics/tower_bottom.png")
game_over_pic = pg.image.load("graphics/game_over.png")
start_game_pic = pg.image.load("graphics/start.png")
sky_pic = pg.image.load("graphics/background.png")
ground_pic = pg.image.load("graphics/ground.png")

scroll_speed = 2
entity_begin_pos = (100, 250)
points = 0
font = pg.font.SysFont("Segoe", 30)
game_over = True


class Entity(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = entity_pics[0]
        self.rect = self.image.get_rect()
        self.rect.center = entity_begin_pos
        self.image_index = 0
        self.velocity = 0
        self.jump = False
        self.vital = True

    def update(self, user_input):
        if self.vital:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = entity_pics[self.image_index // 10]

        self.velocity += 0.5
        if self.velocity > 7:
            self.velocity = 7
        if self.rect.y < 500:
            self.rect.y += int(self.velocity)
        if self.velocity == 0:
            self.jump = False

        self.image = pg.transform.rotate(self.image, self.velocity * -7)

        if user_input[pg.K_SPACE] and not self.jump and self.rect.y > 0 and self.vital:
            self.jump = True
            self.velocity = -7


class Tower(pg.sprite.Sprite):
    def __init__(self, x, y, image, tower_type):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.leave, self.pas = False, False, False
        self.tower_type = tower_type

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -s_width:
            self.kill()

        global points
        if self.tower_type == "bot":
            if entity_begin_pos[0] > self.rect.topleft[0] and not self.pas:
                self.enter = True
            if entity_begin_pos[0] > self.rect.topright[0] and not self.pas:
                self.leave = True
            if self.enter and self.leave and not self.pas:
                self.pas = True
                points += 1


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = ground_pic
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -s_width:
            self.kill()


def close_game():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()


def main():
    global points
    entity = pg.sprite.GroupSingle()
    entity.add(Entity())

    tower_time = 0
    towers = pg.sprite.Group()

    x_posit_ground, y_posit_ground = 0, 520
    ground = pg.sprite.Group()
    ground.add(Ground(x_posit_ground, y_posit_ground))

    run = True
    while run:
        close_game()

        screen.fill((0, 0, 0))

        user_input = pg.key.get_pressed()

        screen.blit(sky_pic, (0, 0))

        if len(ground) <= 2:
            ground.add(Ground(s_width, y_posit_ground))

        towers.draw(screen)
        ground.draw(screen)
        entity.draw(screen)

        point_text = font.render(
            "Points: " + str(points), True, pg.Color(255, 255, 255))
        screen.blit(point_text, (20, 20))

        if entity.sprite.vital:
            towers.update()
            ground.update()
            entity.update(user_input)

        col_towers = pg.sprite.spritecollide(
            entity.sprites()[0], towers, False)
        col_ground = pg.sprite.spritecollide(
            entity.sprites()[0], ground, False)
        if col_ground or col_towers:
            entity.sprite.vital = False
            if col_ground or col_towers:
                screen.blit(game_over_pic, (s_width//2 - game_over_pic.get_width()//2,
                                            s_height//2 - game_over_pic.get_height()//2))

                if user_input[pg.K_r]:
                    points = 0
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
        pg.display.update()


def menu():
    global game_over

    while game_over:
        close_game()

        screen.fill((0, 0, 0))
        screen.blit(sky_pic, (0, 0))
        screen.blit(ground_pic, (0, 520))
        screen.blit(entity_pics[0], (100, 250))
        screen.blit(start_game_pic, (s_width//2 - start_game_pic.get_width()//2,
                                     s_height//2 - start_game_pic.get_height()//2))

        user_input = pg.key.get_pressed()
        if user_input[pg.K_SPACE]:
            main()

        pg.display.update()


menu()
