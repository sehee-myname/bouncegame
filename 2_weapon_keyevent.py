from random import randint
import secrets
import pygame
import os

from zmq import EVENT_BIND_FAILED
##기본 초기화 반드시 해야 할 것

pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("sehee pang")

clock = pygame.time.Clock()
############################

#1. 사용자 게임 초기화 (배경화면, 이미지, 좌표, 속도, 폰트 등 설정)
#배경 불러오기

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

#배경
background = pygame.image.load(os.path.join(image_path,"background.png"))
#스테이지
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지 위에 캐릭터 그리기 위해
#캐릭터
character = pygame.image.load(os.path.join(image_path,"character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2 - character_width / 2)
character_y_pos = screen_height - character_height - stage_height

character_to_x = 0
character_speed = 5

#무기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#한번에 여러발 발사
weapons = []
#이동속도
weapon_speed = 10

running = True
while running:

    dt = clock.tick(60) #초 당 프레임 수


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0


    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width


    #무기 위치조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons ] #무기 위치를 위로 쏘는
    
    #천장에 닿으면 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    

    pygame.display.update() #화면을 다시 그리기 (반드시 계속 호출)

#종료
pygame.quit()