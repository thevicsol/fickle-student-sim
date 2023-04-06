import random
import pygame

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 1000
HEIGHT = 625 # размер экрана

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        player_img = pygame.image.load("sprites/player.png")
        self.image = pygame.transform.scale(player_img, (50, 180))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
 
        pygame.draw.rect(self.image,
                         color,
                         self.rect)
        self.rect = self.image.get_rect()
 
    def moveRight(self, pixels):
        self.rect.x += pixels
 
    def moveLeft(self, pixels):
        self.rect.x -= pixels
 
    def moveForward(self, speed): # контролирует скорость
        self.rect.y += speed * speed/5
 
    def moveBack(self, speed):
        self.rect.y -= speed * speed/5
 
 
pygame.init()
 
 
RED = (255, 0, 0)
 
 
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprite")
 
all_sprites_list = pygame.sprite.Group()
 
player_sprite = Sprite(RED, 20, 30)
player_sprite.rect.x = 200
player_sprite.rect.y = 300
background = pygame.image.load('sprites/bg.jpg').convert()
background_rect = background.get_rect()
 
 
all_sprites_list.add(player_sprite)
 
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
    if keys[pygame.K_LEFT]:
        player_sprite.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        player_sprite.moveRight(5)
    if keys[pygame.K_DOWN]:
        player_sprite.moveForward(5)
    if keys[pygame.K_UP]:
        player_sprite.moveBack(5)
 
    all_sprites_list.update()
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(30) # скорость перемещения
 
pygame.quit()