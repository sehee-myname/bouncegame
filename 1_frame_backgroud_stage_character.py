from random import randint
import pygame
import os
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

running = True

while running:

    dt = clock.tick(60) #초 당 프레임 수


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    screen.blit(background, (0,0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    pygame.display.update() #화면을 다시 그리기 (반드시 계속 호출)

#종료
pygame.quit()