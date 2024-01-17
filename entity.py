import pygame

pygame.init()

s_height = 720
s_width = 551
screen = pygame.display.set_mode((s_width, s_height))
entity_begin_pos = (100, 250)

entity_pics = [pygame.image.load("graphics/bat_down1.png").convert_alpha(),
               pygame.image.load("graphics/bat_mid1.png").convert_alpha(),
               pygame.image.load("graphics/bat_up1.png").convert_alpha()]


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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

        self.image = pygame.transform.rotate(self.image, self.velocity * -7)

        if user_input[pygame.K_SPACE] and not self.jump and self.rect.y > 0 and self.vital:
            self.jump = True
            self.velocity = -7
