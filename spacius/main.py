import pygame
import sys
import random
import os
pygame.init()

class Enemy(pygame.sprite.Sprite):
    bullet_timer = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        unscaled_image = pygame.image.load(os.path.join("sprites", "enemies", f"{random.randint(1, 15)}.png"))
        self.image = pygame.transform.scale_by(unscaled_image, 2)
        
        self.rect = player.image.get_rect()
        self.rect.y = random.randint(50, WINDOW_HEIGHT//3*2)
        self.rect.x = -90
        
        self.distance_left = random.randint(100, WINDOW_WIDTH-100) + 90

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        unscaled_image = pygame.image.load(os.path.join("sprites", "shuttle.png"))
        self.image = pygame.transform.scale_by(unscaled_image, 2)
        
        self.rect = self.image.get_rect()
        self.rect.move_ip(WINDOW_WIDTH/2-(self.rect.w/2), WINDOW_HEIGHT/6*5)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, is_player, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.is_player = is_player

        self.image = pygame.Surface([6, 32])
        if is_player:
            self.image.fill("white")
        else:
            self.image.fill("red")
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        if self.is_player:
            self.rect.move_ip(0, -14)
            if self.rect.y < -32:
                self.kill()
        else:
            self.rect.move_ip(0, 14)
            if self.rect.y > WINDOW_HEIGHT+32:
                self.kill()


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
window_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spacius")

clock = pygame.time.Clock()

font_bold = pygame.freetype.SysFont("Arial", 48, bold=True)
font = pygame.freetype.SysFont("Arial", 28)

enemies = pygame.sprite.Group()
enemy_spawn_timer = 0

player = Player()

player_speed = 6
enemy_speed = 8

player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
bullet_just_shot = False

newest_enemy = None
newest_enemy_distance_left = 0

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
        text, rect = font_bold.render("Welcome to Spacius", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-32))
        screen.blit(text, text_rect)

        text, rect = font.render("Press \"ENTER\" to begin", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+32))
        screen.blit(text, text_rect)

        if keys[pygame.K_RETURN]:
            title = False

    else:
        if not newest_enemy or newest_enemy.distance_left <= 0:
            if enemy_spawn_timer > 0:
                enemy_spawn_timer -= 1
            else:
                newest_enemy = Enemy()
                enemies.add(newest_enemy)
                enemy_spawn_timer = 60
        else:
            newest_enemy.rect.move_ip(enemy_speed, 0)
            newest_enemy.distance_left -= enemy_speed

        if keys[pygame.K_LEFT]:
            player.rect.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT]:
            player.rect.move_ip(player_speed, 0)
        if keys[pygame.K_UP]:
            player.rect.move_ip(0, -player_speed)
        if keys[pygame.K_DOWN]:
            player.rect.move_ip(0, player_speed)
        if keys[pygame.K_z] and not bullet_just_shot:
            x = (player.rect.right + player.rect.left) // 2 - 3
            y = player.rect.y
            bullet = Bullet(True, x, y)
            player_bullets.add(bullet)
            bullet_just_shot = True
        elif not keys[pygame.K_z] and bullet_just_shot:
            bullet_just_shot = False

        player.rect.clamp_ip(window_rect)

        enemies.draw(screen)

        player_bullets.update()
        player_bullets.draw(screen)
        enemy_bullets.update()
        enemy_bullets.draw(screen)

        screen.blit(player.image, player.rect)

        

    pygame.display.flip()
    
    clock.tick(60)