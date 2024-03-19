import pygame as pygame
from sys import exit
from random import randint


# Timer
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = text_style.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


# Obstacle movement
def obstacle_movement(obstacle_list):  # if list is empty is False (if not run)
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5    # movement of obstacles

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


# Collision
def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacle_rect_list:
            if player.colliderect(obstacle_rect):
                return False
    return True


# Walking animation and jump
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
pygame.init()
icon = pygame.image.load('Graphics and font/Characters/player_stand.png')
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Jumpy")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

# Font
text_style = pygame.font.Font('Graphics and font/Font/Pixeltype.ttf', 50)

# Sky and ground
sky_surface = pygame.image.load('Graphics and font/Background/Sky.png').convert()
ground_surface = pygame.image.load('Graphics and font/Background/ground.png').convert()

# Player
player_walk1 = pygame.image.load('Graphics and font/Characters/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('Graphics and font/Characters/player_walk_2.png').convert_alpha()
player_walk = [player_walk2, player_walk1]
player_index = 0
player_jump = pygame.image.load('Graphics and font/Characters/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Text over
name_surf = text_style.render('Valeria', False, (255, 255, 255))
name_rect = name_surf.get_rect(midbottom=(400, 305))

# Background over
over_back = pygame.image.load('Graphics and font/Background/night.png').convert_alpha()
over_back = pygame.transform.scale(over_back, (800, 420))

# Player_stand over
player_surf_s = pygame.image.load('Graphics and font/Characters/player_stand.png').convert_alpha()
player_rect_s = player_surf_s.get_rect(midbottom=(400, 390))

# Message over
message_surf = text_style.render("Press 'space' to play", False, (255, 255, 255))
message_rect = message_surf.get_rect(midbottom=(400, 100))

# Snails
snail_frame_1 = pygame.image.load('Graphics and font/Characters/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Graphics and font/Characters/snail2.png').convert_alpha()
snail_frames = [snail_frame_2, snail_frame_1]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# FLies
fly_frame_1 = pygame.image.load('Graphics and font/Characters/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Graphics and font/Characters/Fly2.png').convert_alpha()
fly_frames = [fly_frame_2, fly_frame_1]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Timer for obstacles spawn
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

# Snail timer
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

# Fly timer
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.bottom == 300 and player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if player_rect.bottom == 300 and event.key == pygame.K_SPACE:
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1000), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1000), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        game_active = collision(player_rect, obstacle_rect_list)

    else:
        screen.blit(over_back, (0, 0))
        screen.blit(player_surf_s, player_rect_s)
        screen.blit(name_surf, name_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        # Time over
        score_surf_back = text_style.render(f'Score: {score}', False, (255, 255, 255))
        score_rect_back = score_surf_back.get_rect(center=(400, 50))

        if score == 0:
            screen.blit(message_surf, message_rect)
        else:
            screen.blit(score_surf_back, score_rect_back)

    pygame.display.update()
    clock.tick(60)
