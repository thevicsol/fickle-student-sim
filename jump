# pep8
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("StudFacL")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/RoughenCorner.ttf", 50)
game_active = True

sky_surface = pygame.image.load("image/pixel-art-sky-background.jpg").convert()
ground_surface = pygame.image.load("image/pygame_floating.png").convert()  
text_surface = test_font.render("StudFacL", False, "#c0e8ec")  
character_surface = pygame.image.load("image/pixil-frame-0 (2).png").convert_alpha()
character_rect = character_surface.get_rect(bottomright=(80, 304))
another_surface = pygame.image.load("image/pixil-frame-0 (3).png")
another_rect = another_surface.get_rect(bottomleft=(360, 330))
another_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and another_rect.bottom >= 300:
                another_gravity = -20

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (225, 50))
    character_rect.x -= 4
    if character_rect.right <= 0:
        character_rect.left = 600
    screen.blit(character_surface, character_rect)
    # another
    another_gravity += 1
    another_rect.y += another_gravity
    if another_rect.bottom >= 326:
        another_rect.bottom = 326
    screen.blit(another_surface, another_rect)

    if character_rect.colliderect(another_rect):
        game_active = False

    pygame.display.update()
    clock.tick(60)
