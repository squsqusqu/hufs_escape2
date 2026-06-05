import pygame
import sys
from pygame.locals import *

# [수정] main.py에서 호출할 수 있도록 run 함수로 감싸고 매개변수를 받습니다.
def run(DISPLAYSURF, selected_gender):
    # =========================
    # 화면 설정 (내부 연산용)
    # =========================
    WIDTH = 800
    HEIGHT = 600
    clock = pygame.time.Clock()

    # =========================
    # 폰트
    # =========================
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)

    # =========================
    # 반투명 레이어 설정
    # =========================
    light_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    YELLOW_ALPHA = (255, 255, 0, 100) 

    # =========================
    # 이미지 불러오기
    # =========================
    background = pygame.image.load("image/stage3_bg.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    cctv_img = pygame.image.load("image/CCTV.png").convert_alpha()
    cctv_img = pygame.transform.scale(cctv_img, (80, 80))

    gameover_img = pygame.image.load("image/stage3_gameover.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # 캐릭터 이미지
    male_run1 = pygame.image.load("image/male_run.png").convert_alpha()
    male_run2 = pygame.image.load("image/male_run2.png").convert_alpha()
    female_run1 = pygame.image.load("image/female_run.png").convert_alpha()
    female_run2 = pygame.image.load("image/female_run2.png").convert_alpha()

    male_run1 = pygame.transform.scale(male_run1, (100,100))
    male_run2 = pygame.transform.scale(male_run2, (100,100))
    female_run1 = pygame.transform.scale(female_run1, (100,100))
    female_run2 = pygame.transform.scale(female_run2, (100,100))

    # =========================
    # 변수 설정
    # =========================
    scene = "game"
    frame_index = 0
    animation_timer = 0
    animation_speed = 200

    # 시작 위치 (오른쪽 하단)
    start_x = WIDTH - 60
    start_y = HEIGHT - 60
    game_started = False

    cctv_y = 60

    # 1. 첫 번째 CCTV (0.3초 대기, 0.8초 켜짐)
    cctv1_x = 40
    cctv1_timer = 0
    cctv1_is_on = False
    CCTV1_OFF_TIME = 300  
    CCTV1_ON_TIME = 800   

    # 2. 두 번째 CCTV (0.4초 대기, 0.5초 켜짐)
    cctv2_x = 260
    cctv2_timer = 0
    cctv2_is_on = False
    CCTV2_OFF_TIME = 400   
    CCTV2_ON_TIME = 500   

    # 3. 세 번째 CCTV (1.5초 대기, 1.5초 켜짐)
    cctv3_x = 480
    cctv3_timer = 0
    cctv3_is_on = False
    CCTV3_OFF_TIME = 1500   
    CCTV3_ON_TIME = 1500    

    # 4. 네 번째 CCTV (0.4초 대기, 0.5초 켜짐)
    cctv4_x = 700
    cctv4_timer = 0
    cctv4_is_on = False
    CCTV4_OFF_TIME = 400   
    CCTV4_ON_TIME = 500    

    # 문 및 직사각형 불빛 히트박스
    door_rect = pygame.Rect(130, 180, 150, 160)

    light1_rect = pygame.Rect(cctv1_x - 60, cctv_y + 60, 200, 480) 
    light2_rect = pygame.Rect(cctv2_x - 60, cctv_y + 60, 200, 480)
    light3_rect = pygame.Rect(cctv3_x - 60, cctv_y + 60, 200, 480)
    light4_rect = pygame.Rect(cctv4_x - 60, cctv_y + 60, 200, 360)

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False # [수정] 창을 닫으면 전체 프로세스 종료를 위해 False 반환

            # 게임오버 재시작
            if scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    game_started = False
                    
                    # CCTV 타이머 및 상태 초기화
                    cctv1_timer = cctv2_timer = cctv3_timer = cctv4_timer = 0
                    cctv1_is_on = cctv2_is_on = cctv3_is_on = cctv4_is_on = False

            # [수정] 스테이지 클리어 대기 화면에서 조작 시 True를 반환하며 다음 스테이지로 제어권 전환
            elif scene == "stage4":
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    return True

        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()

        # 플레이어 히트박스
        player_rect = pygame.Rect(mx - 20, my - 20, 40, 40)

        # =========================
        # 게임 화면
        # =========================
        if scene == "game":
            if not game_started:
                pygame.mouse.set_pos((start_x, start_y))
                mx, my = start_x, start_y
                player_rect = pygame.Rect(mx - 20, my - 20, 40, 40)
                game_started = True

            DISPLAYSURF.blit(background, (0,0))

            # CCTV 타이머 로직 업데이트
            cctv1_timer += dt
            cctv2_timer += dt
            cctv3_timer += dt
            cctv4_timer += dt

            # CCTV 1 제어
            if not cctv1_is_on and cctv1_timer >= CCTV1_OFF_TIME:
                cctv1_is_on = True
                cctv1_timer = 0
            elif cctv1_is_on and cctv1_timer >= CCTV1_ON_TIME:
                cctv1_is_on = False
                cctv1_timer = 0

            # CCTV 2 제어
            if not cctv2_is_on and cctv2_timer >= CCTV2_OFF_TIME:
                cctv2_is_on = True
                cctv2_timer = 0
            elif cctv2_is_on and cctv2_timer >= CCTV2_ON_TIME:
                cctv2_is_on = False
                cctv2_timer = 0

            # CCTV 3 제어
            if not cctv3_is_on and cctv3_timer >= CCTV3_OFF_TIME:
                cctv3_is_on = True
                cctv3_timer = 0
            elif cctv3_is_on and cctv3_timer >= CCTV3_ON_TIME:
                cctv3_is_on = False
                cctv3_timer = 0

            # CCTV 4 제어 
            if not cctv4_is_on and cctv4_timer >= CCTV4_OFF_TIME:
                cctv4_is_on = True
                cctv4_timer = 0
            elif cctv4_is_on and cctv4_timer >= CCTV4_ON_TIME:
                cctv4_is_on = False
                cctv4_timer = 0

            # 반투명 불빛 레이어 초기화 & 그리기
            light_surface.fill((0, 0, 0, 0))

            if cctv1_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light1_rect)
                if player_rect.colliderect(light1_rect):
                    scene = "gameover"
                    
            if cctv2_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light2_rect)
                if player_rect.colliderect(light2_rect):
                    scene = "gameover"
                    
            if cctv3_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light3_rect)
                if player_rect.colliderect(light3_rect):
                    scene = "gameover"
                    
            if cctv4_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light4_rect)
                if player_rect.colliderect(light4_rect):
                    scene = "gameover"

            # 투명 도화지 합치기
            DISPLAYSURF.blit(light_surface, (0, 0))

            # CCTV 본체 출력
            DISPLAYSURF.blit(cctv_img, (cctv1_x, cctv_y))
            DISPLAYSURF.blit(cctv_img, (cctv2_x, cctv_y))
            DISPLAYSURF.blit(cctv_img, (cctv3_x, cctv_y))
            DISPLAYSURF.blit(cctv_img, (cctv4_x, cctv_y))

            # 문 닿기 (클리어)
            if player_rect.colliderect(door_rect):
                scene = "stage4"

            # 캐릭터 애니메이션 및 출력
            animation_timer += dt
            if animation_timer >= animation_speed:
                animation_timer = 0
                frame_index = 1 if frame_index == 0 else 0

            # [수정] main.py에서 선택된 성별 값을 기반으로 분기 처리합니다.
            if selected_gender == "male":
                player_img = male_run1 if frame_index == 0 else male_run2
            else:
                player_img = female_run1 if frame_index == 0 else female_run2

            DISPLAYSURF.blit(player_img, (mx - 50, my - 50))

        # =========================
        # 게임오버 화면
        # =========================
        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0,0))
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (0,0,0))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        # =========================
        # [수정] Stage4 대기 화면 연출
        # =========================
        elif scene == "stage4":
            DISPLAYSURF.fill((0,0,0))
            clear_text = font.render("STAGE 3 CLEAR! (PRESS ANY KEY)", True, (255,255,255))
            clear_rect = clear_text.get_rect(center=(400,300))
            DISPLAYSURF.blit(clear_text, clear_rect)

        pygame.display.update()
