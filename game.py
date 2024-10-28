import pygame
import os 
import sys
from random import *
from hashlib import *


pygame.init()
#More Codes

def obstacle(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            move = choice([12,10.2,8.4,12.6,13.2,18.6,6.4])
            obstacle_rect.y += move
            screen.blit(playee,obstacle_rect)
        obstacle_list = [obstacle_rect for obstacle_rect in obstacle_list if obstacle_rect.y < 505]
        return obstacle_list
    else:
        return []

            
def collisions(playee,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if playee.colliderect(obstacle_rect):
                return False
    return True

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = front.render( f' SCORE: {current_time}',False,(233, 233, 106))
    score_rect = score_surf.get_rect(center = (380,62))
    screen.blit(score_surf,score_rect)
    return current_time

pin = "1b8a4255d420ee020ba062f65a947fad07727f91338a2435731ae69029faebba"


clock = pygame.time.Clock()
pygame.display.set_caption("ATLAS")

icon = pygame.image.load("IMAGE/EYE_IMG.png","icon")
pygame.display.set_icon(icon)

font = pygame.font.Font("font/GIGI.TTF",72)
fost = pygame.font.Font("font/BELLI.TTF",42)
front = pygame.font.Font("font/BRADHITC.TTF",36)
frost = pygame.font.Font("font/SCRIPTBL.TTF",42)
froze = pygame.font.Font("font/BRUSHSCI.TTF",40)

screen = pygame.display.set_mode((800,600))

surface = pygame.image.load("IMAGE/helicopter.png").convert_alpha().convert_alpha()
surface = pygame.transform.scale(surface,(160,142))
surface_rect = surface.get_rect(center = (388,320))

text = font.render("GAMELAS",0,(29,29,27))
text_rect = text.get_rect(center = (380,205))

test = fost.render("ENTER SPACE KEY TO START",0,(29,29,27))
test_rect = test.get_rect(midbottom = (390,445))

test_dup = fost.render("ENTER SPACE KEY TO RESTART",0,(29,29,27))
test_dup_rect = test_dup.get_rect(midbottom = (385,445))

playee = pygame.image.load("IMAGE/ELSE.gif",'player')
playee = pygame.transform.scale(playee,(21,20))

player = pygame.image.load("IMAGE/EYE_IMG.png",'player')
player = pygame.transform.scale(player,(60,60))
player_rect = player.get_rect(midbottom = (380,532))

screen_surf = pygame.image.load("IMAGE/background.gif")
screen_surf = pygame.transform.scale(screen_surf,(800,600))

game_active = False
start_time = 0
score = 0

jump_sound = pygame.mixer.Sound("IMAGE/house_lo.mp3")
jump_sound.set_volume(1.2)
jump_sound.play(-1,0,2000)

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,400)

obstacle_rect_list = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_END:
                game_active = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player_rect.x -= 32
                if player_rect.left <= 40:
                    player_rect.left = 40
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player_rect.x += 32
                if player_rect.right >= 760:
                    player_rect.right = 760
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player_rect.y -= 32
                if player_rect.top <= 20:
                    player_rect.top = 20
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player_rect.y += 32
                if player_rect.bottom >= 532:
                    player_rect.bottom = 532
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F:
                pygame.FULLSCREEN = 4.0
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

        
        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(playee.get_rect(midtop = (randint(48,740),randint(-4,4))))

    if game_active:
        screen.blit(screen_surf,(0,0))
        score = display_score()
        screen.blit(player,player_rect)
        obstacle_rect_list = obstacle(obstacle_rect_list)
        game_active = collisions(player_rect,obstacle_rect_list)

    
    else:
        screen.fill((16, 227, 206))
        screen.blit(surface,surface_rect)
        screen.blit(text,text_rect)
        obstacle_rect_list.clear()
        player_rect = player.get_rect(midbottom = (380,532))

        score_message = frost.render(f' SCORE: {score} ',False, (4, 12, 117))
        score_message_rect = score_message.get_rect(midtop = (384,72))
        if score != 0:
            screen.blit(score_message,score_message_rect)
            screen.blit(test_dup,test_dup_rect)
        else:
            screen.blit(test,test_rect)
    

    pygame.display.update()
    clock.tick(25)

