import pygame
import sys
import random
import os
pygame.init()

class Enemy(pygame.sprite.Sprite):
    bullet_timer = 100

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        unscaled_image = pygame.image.load(os.path.join("sprites", "enemies", f"{random.randint(1, 15)}.png"))
        self.image = pygame.transform.scale_by(unscaled_image, 2).convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.y = random.randint(50, WINDOW_HEIGHT//2)
        self.rect.x = -90
        
        self.distance_left = random.randint(0, WINDOW_WIDTH-64) + 90
    
    def update(self):
        self.bullet_timer -= 1
        if self.bullet_timer == 0:
            self.bullet_timer = 150
            x = self.rect.width // 2 + self.rect.x
            y = self.rect.bottom - 32
            bullet = Bullet(False, x, y)
            enemy_bullets.add(bullet)

class Boss(pygame.sprite.Sprite):
    bullet_timer = 60

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        unscaled_image = pygame.image.load(os.path.join("sprites", "boss.png"))
        self.image = pygame.transform.scale_by(unscaled_image, 3).convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.y = WINDOW_HEIGHT//4
        self.rect.x = WINDOW_WIDTH//2 - (self.rect.width//2)
    
    def update(self):
        self.bullet_timer -= 1
        if self.bullet_timer == 0:
            self.bullet_timer = 60

            self.rect.x = random.randint(0, WINDOW_WIDTH-64)
            self.rect.y = random.randint(50, WINDOW_HEIGHT//2)

            x = self.rect.width // 2 + self.rect.x
            y = self.rect.bottom - 32
            bullet = Bullet(False, x, y)
            enemy_bullets.add(bullet)

class Player(pygame.sprite.Sprite):
    ammo = 5
    enemies_killed = 0
    enemy_just_killed = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        unscaled_image = pygame.image.load(os.path.join("sprites", "shuttle.png"))
        self.image = pygame.transform.scale_by(unscaled_image, 2).convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.move_ip(WINDOW_WIDTH/2-(self.rect.w/2), WINDOW_HEIGHT//10*7)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, is_player, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.is_player = is_player

        self.image = pygame.Surface([6, 32])
        if is_player:
            self.image.fill("white")
        else:
            self.image.fill("red")
        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        if self.is_player:
            self.rect.move_ip(0, -10)
            if self.rect.y < -32:
                self.kill()
        else:
            self.rect.move_ip(0, 10)
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

boss = None
boss_battle_happening = False

player = None

player_speed = 6
enemy_speed = 8

player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
bullet_just_shot = False

newest_enemy = None
newest_enemy_distance_left = 0

msg = ""
msg_timer = 0

title = True
game_over = False
win = False

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

        text, rect = font.render("Press X to return to title screen.", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+32))
        screen.blit(text, text_rect)

        if keys[pygame.K_x]:
            boss_battle_happening = False
            enemies.empty()
            player_bullets.empty()
            enemy_bullets.empty()
            game_over = False
            title = True
            continue
    elif win:
        text, rect = font_bold.render("You won!", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-32))
        screen.blit(text, text_rect)

        text, rect = font.render("Press X to return to title screen.", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+32))
        screen.blit(text, text_rect)

        if keys[pygame.K_x]:
            boss_battle_happening = False
            enemies.empty()
            player_bullets.empty()
            enemy_bullets.empty()
            win = False
            title = True
            continue
    elif title:
        text, rect = font_bold.render("Welcome to Spacius", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-32))
        screen.blit(text, text_rect)

        text, rect = font.render("Press 'ENTER' to begin", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+32))
        screen.blit(text, text_rect)

        if keys[pygame.K_RETURN]:
            player = Player()
            title = False
    else:
        if keys[pygame.K_LEFT]:
            player.rect.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT]:
            player.rect.move_ip(player_speed, 0)
        """if keys[pygame.K_UP]:
            player.rect.move_ip(0, -player_speed)
        if keys[pygame.K_DOWN]:
            player.rect.move_ip(0, player_speed)"""
        if keys[pygame.K_z] and not bullet_just_shot:
            x = (player.rect.right + player.rect.left) // 2 - 3
            y = player.rect.y
            bullet = Bullet(True, x, y)
            player_bullets.add(bullet)
            bullet_just_shot = True
            player.ammo -= 1
        elif not keys[pygame.K_z] and bullet_just_shot:
            bullet_just_shot = False
        player.rect.clamp_ip(window_rect)

        if (len(player_bullets.sprites()) == 0 and player.ammo == 0) or pygame.sprite.spritecollideany(player, enemy_bullets, collided = pygame.sprite.collide_mask):
            game_over = True
            continue
        
        if boss_battle_happening:
            for hit in pygame.sprite.spritecollide(boss, player_bullets, True, pygame.sprite.collide_mask):
                win = True
                continue
            
            boss.update()
            screen.blit(boss.image, boss.rect)
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
            
            collisions = pygame.sprite.groupcollide(enemies, player_bullets, True, True, collided = pygame.sprite.collide_mask)
            for _ in collisions:
                player.ammo += 1
                player.enemies_killed += 1
                player.enemy_just_killed = True
            
            if player.enemy_just_killed:
                if player.enemies_killed == 10:
                    player.ammo = 8
                    msg = "10 enemies killed, ammo increased to 10"
                    msg_timer = 60
                elif player.enemies_killed == 15:
                    player.ammo = 3
                    msg = "Boss battle starting!"
                    msg_timer = 60

                    boss = Boss()
                    boss_battle_happening = True
                    enemies.empty()
                    enemy_bullets.empty()
                player.enemy_just_killed = False

            enemies.update()
            enemies.draw(screen)

        player_bullets.update()
        player_bullets.draw(screen)
        enemy_bullets.update()
        enemy_bullets.draw(screen)

        screen.blit(player.image, player.rect)

        if msg_timer != 0:
            msg_timer -= 1
            text, rect = font.render(msg, "white")
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT-72))
            screen.blit(text, text_rect) 
        
        text, rect = font.render(f"Enemies killed: {player.enemies_killed}", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT-48))
        screen.blit(text, text_rect) 

        text, rect = font_bold.render(f"{player.ammo} bullets", "white")
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, 48))
        screen.blit(text, text_rect)        

    pygame.display.flip()
    
    clock.tick(60)