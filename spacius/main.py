WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

import pygame
import sys
import random
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spacius")

clock = pygame.time.Clock()

font_bold = pygame.freetype.SysFont("Arial", 48, bold=True)
font = pygame.freetype.SysFont("Arial", 28)

enemy_counter = 0
enemies_on_screen = pygame.sprite.Group()
enemy_timer = 0

player = pygame.sprite.Sprite()

title = True
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if game_over:
        # Source - https://stackoverflow.com/a/39580531
        # Posted by The4thIceman
        # Retrieved 2026-04-22, License - CC BY-SA 3.0

        # draw text
        text, rect = font_bold.render("Game Over", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-32))
        screen.blit(text, text_rect)

        text, rect = font.render("Press \"ENTER\" to return to title screen.", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+32))
        screen.blit(text, text_rect)

        if keys[pygame.K_RETURN]:
            for sprite in enemies_on_screen.sprites():
                sprite.kill()
            game_over = False
            title = True
    elif title:
        # Source - https://stackoverflow.com/a/39580531
        # Posted by The4thIceman
        # Retrieved 2026-04-22, License - CC BY-SA 3.0

        # draw text
        text, rect = font_bold.render("Welcome to Spacius", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-32))
        screen.blit(text, text_rect)

        text, rect = font.render("Press \"ENTER\" to begin", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+32))
        screen.blit(text, text_rect)

        if keys[pygame.K_RETURN]:
            title = False
            #enemy.x = random.randint(0, WINDOW_WIDTH-enemy.size)
            #enemy.y = random.randint(0, WINDOW_HEIGHT-enemy.size)
    else:
        pass

    pygame.display.flip()
    
    clock.tick(60)