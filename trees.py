import pygame

pygame.init()

s_height = 720
s_width = 551
screen = pygame.display.set_mode((s_width, s_height))
entity_begin_pos = (100, 250)
scroll_speed = 2

top_pipe_pic = pygame.image.load("graphics/pipe_top.png")
bottom_pipe_pic = pygame.image.load("graphics/pipe_bottom.png")


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tree_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.leave, self.pas = False, False, False
        self.tree_type = tree_type
        self.points = 0

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -s_width:
            self.kill()

        global points
        if self.tree_type == "bot":
            if entity_begin_pos[0] > self.rect.topleft[0] and not self.pas:
                self.enter = True
            if entity_begin_pos[0] > self.rect.topright[0] and not self.pas:
                self.leave = True
            if self.enter and self.leave and not self.pas:
                self.pas = True
                self.points += 1
