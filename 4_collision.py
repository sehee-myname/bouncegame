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

#공만들기(4종류 크기 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path,"balloon1.png")),
    pygame.image.load(os.path.join(image_path,"balloon2.png")),
    pygame.image.load(os.path.join(image_path,"balloon3.png")),
    pygame.image.load(os.path.join(image_path,"balloon4.png"))
]

#각각 속도 지정
ball_speed_y = [ -18, -15, -12 , -9] #index 0,1,2,3에 해당
#공들 정보
balls = []
#최초 발생하는 큰 공
balls.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0, #가장 큰 공
    "to_x": 3, #공의 x축 이동방향
    "to_y": -6, #y축 이동방향,
    "init_spd_y": ball_speed_y[0] #y로 최초 속도
})

running = True
while running:

    dt = clock.tick(30) #초 당 프레임 수


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

    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val ["pos_x"]
        ball_pos_y = ball_val ["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿았을때 공 위치 ( 튕겨나감 )
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        #세로
        #스테이지에 튕겨 올라가는 위치
        if ball_pos_y > screen_height - ball_height - stage_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: #그 외 속도를 줄여나가는 것
            ball_val["to_y"] += 0.5
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    #충돌처리
    #캐릭터 rect정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val ["pos_x"]
            ball_pos_y = ball_val ["pos_y"]
            ball_img_idx = ball_val["img_idx"]

    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    

    pygame.display.update() #화면을 다시 그리기 (반드시 계속 호출)

#종료
pygame.quit()