import pygame
import sys
import random
from pygame.locals import *

# [수정] 충돌 코드 정리 및 main.py 연동을 위한 함수화
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
    small_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 20)

    # =========================
    # 이미지 불러오기
    # =========================
    # 명수당 배경
    background = pygame.image.load("image/Myeongsu_Lake.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # [수정] 충돌 코드에 있던 두 가지 게임오버 이미지를 예외 처리로 묶어 유연하게 불러옵니다.
    try:
        gameover_img = pygame.image.load("image/stage4_gameover.png").convert()
    except:
        gameover_img = pygame.image.load("image/stage3_gameover.png").convert()
    
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # =========================
    # 동물 이미지
    # =========================
    ANIMAL_SIZE = 70

    duck_img = pygame.image.load("image/Duck.png").convert_alpha()
    duck_img = pygame.transform.scale(duck_img, (ANIMAL_SIZE, ANIMAL_SIZE))

    otter_img = pygame.image.load("image/Otter.png").convert_alpha()
    otter_img = pygame.transform.scale(otter_img, (ANIMAL_SIZE, ANIMAL_SIZE))

    # =========================
    # 변수
    # =========================
    scene = "game"

    # 게임 진행 변수
    otter_count = 0
    catch_goal = 3

    # 스폰 타이머 및 애니메이션 변수
    spawn_timer = 0
    spawn_cycle = 1000      # 1초마다 새로 스폰
    visible_time = 500      # 0.5초동안 보임
    emerge_time = 150       # 0.15초 동안 올라오고/내려감

    # 현재 등장한 동물 정보
    current_animal = None   
    animal_x = 0
    animal_y = 0
    is_clickable = False

    # 마우스 포인터 표시
    pygame.mouse.set_visible(True)

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False # [수정] 창을 닫으면 전체 프로그램 종료

            # =====================
            # 마우스 클릭 이벤트 (동물 잡기)
            # =====================
            if scene == "game" and event.type == MOUSEBUTTONDOWN:
                if is_clickable and current_animal != None:
                    mx, my = event.pos
                    animal_rect = pygame.Rect(animal_x, animal_y, ANIMAL_SIZE, ANIMAL_SIZE)
                    
                    if animal_rect.collidepoint(mx, my):
                        if current_animal == "otter":
                            otter_count += 1
                            current_animal = None # 잡으면 즉시 사라짐
                            
                            # 3마리 잡으면 클리어 화면으로
                            if otter_count >= catch_goal:
                                scene = "stage5"
                                
                        elif current_animal == "duck":
                            scene = "gameover"

            # =====================
            # 게임오버 재시작
            # =====================
            elif scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    otter_count = 0
                    spawn_timer = 0
                    current_animal = None

            # =====================
            # [수정] 스테이지 클리어 대기화면 입력
            # =====================
            elif scene == "stage5":
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    return True # 아무 키나 누르면 다음 스테이지로 제어권 넘김

        # =========================
        # 게임 화면
        # =========================
        if scene == "game":
            DISPLAYSURF.blit(background, (0,0))

            # 진행 상황 텍스트
            score_text = font.render(f"수달 구조: {otter_count} / {catch_goal}", True, (255, 255, 255))
            DISPLAYSURF.blit(score_text, (30, 30))

            # 동물 스폰 타이머 로직
            spawn_timer += dt
            if spawn_timer >= spawn_cycle:
                spawn_timer = 0
                animal_x = random.randint(250, 650)
                animal_y = random.randint(350, 480)
                
                # 수달 60% / 오리 40% 확률 등장
                if random.randint(1, 10) <= 6:
                    current_animal = "otter"
                else:
                    current_animal = "duck"

            # 등장 애니메이션 (0.5초 동안만)
            if spawn_timer < visible_time and current_animal != None:
                is_clickable = True
                
                if spawn_timer < emerge_time:
                    ratio = spawn_timer / emerge_time
                elif spawn_timer > (visible_time - emerge_time):
                    ratio = (visible_time - spawn_timer) / emerge_time
                else:
                    ratio = 1.0
                    
                current_height = int(ANIMAL_SIZE * ratio)
                draw_y = animal_y + (ANIMAL_SIZE - current_height)
                crop_rect = (0, 0, ANIMAL_SIZE, current_height)
                
                target_img = otter_img if current_animal == "otter" else duck_img
                    
                DISPLAYSURF.blit(target_img, (animal_x, draw_y), crop_rect)
            else:
                is_clickable = False

        # =========================
        # 게임오버 화면
        # =========================
        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0,0))
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (0,0,0))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        # =========================
        # [수정] Stage 5 대기 (클리어) 화면
        # =========================
        elif scene == "stage5":
            DISPLAYSURF.fill((0,0,0))
            clear_text = font.render("STAGE 4 CLEAR! (PRESS ANY KEY)", True, (255,255,255))
            clear_rect = clear_text.get_rect(center=(400,300))
            DISPLAYSURF.blit(clear_text, clear_rect)

        pygame.display.update()
