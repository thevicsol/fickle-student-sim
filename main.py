import random
import pygame

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 1000
HEIGHT = 625  # размер экрана


class Player(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        player_img = pygame.image.load("sprites/player.png")
        self.collision = pygame.image.load("sprites/collision.png")
        self.image = pygame.transform.scale(player_img, (50, 180))
        self.mask = pygame.mask.from_surface(self.collision)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        pygame.draw.rect(self.image,
                         color,
                         self.rect)
        self.rect = self.image.get_rect()


class Wall(pygame.sprite.Sprite):
    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.side = side
        self.image = pygame.transform.scale(pygame.image.load("testroom/" + side + '.png'), (1000, 625))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, speed):  # контролирует скорость
        self.rect.y += speed * speed / 5

    def moveBack(self, speed):
        self.rect.y -= speed * speed / 5


pygame.init()


RED = (255, 0, 0)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprite")

all_sprites_list = pygame.sprite.Group()
walls = pygame.sprite.Group()
playergroup = pygame.sprite.Group()

player = Player(RED, 20, 30)
player.rect.x = 400
player.rect.y = 240
background = pygame.image.load('sprites/bg.jpg').convert()
background_rect = background.get_rect()

playergroup.add(player)
a = Wall('borderdown')
b = Wall('borderup')
c = Wall('borderleft')
d = Wall('borderright')
e = Wall('floor')
walls.add(a, b, c, d, e)

exit = True
clock = pygame.time.Clock()

while exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                exit = False

    keys = pygame.key.get_pressed()
    # character_rect.colliderect(another_rect)
    if keys[pygame.K_LEFT] and not pygame.sprite.spritecollide(player, [c], False, pygame.sprite.collide_mask):
        for sprite in walls:
            sprite.moveRight(5)
    if keys[pygame.K_RIGHT] and not pygame.sprite.spritecollide(player, [d], False, pygame.sprite.collide_mask):
        for sprite in walls:
            sprite.moveLeft(5)
    if (keys[pygame.K_DOWN] and not pygame.sprite.spritecollide(player, [a], False, pygame.sprite.collide_mask) and not
            pygame.sprite.spritecollide(player, [c], False, pygame.sprite.collide_mask)):
         for sprite in walls:
            sprite.moveBack(5)
    if (keys[pygame.K_UP] and not pygame.sprite.spritecollide(player, [b], False, pygame.sprite.collide_mask) and not
            pygame.sprite.spritecollide(player, [d], False, pygame.sprite.collide_mask)):
        for sprite in walls:
            sprite.moveForward(5)

    all_sprites_list.update()
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    all_sprites_list.draw(screen)
    walls.draw(screen)
    playergroup.draw(screen)
    pygame.display.flip()
    clock.tick(30)  # скорость перемещения


pygame.quit()