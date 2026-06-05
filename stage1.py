import pygame
import sys
from pygame.locals import *

# [수정] main.py에서 제어하므로 pygame.init()을 제거하고 run 함수로 감쌉니다.
def run(DISPLAYSURF, selected_gender):
    # =========================
    # 화면 설정 값 (내부 연산용)
    # =========================
    WIDTH = 800
    HEIGHT = 600
    clock = pygame.time.Clock()

    # =========================
    # 폰트
    # =========================
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)

    # =========================
    # 이미지 불러오기
    # =========================
    background = pygame.image.load("image/stage1_bg.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # 교수 이미지
    professor_side = pygame.image.load("image/professor_side.png").convert_alpha()
    professor_front = pygame.image.load("image/professor_front.png").convert_alpha()
    professor_side = pygame.transform.scale(professor_side, (180, 220))
    professor_front = pygame.transform.scale(professor_front, (180, 220))

    # 학생(책상)
    student_img = pygame.image.load("image/student_img.png").convert_alpha()
    student_img = pygame.transform.scale(student_img, (180, 180))

    # 게임오버
    gameover_img = pygame.image.load("image/stage3_gameover.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # =========================
    # 캐릭터 이미지
    # =========================
    male_run1 = pygame.image.load("image/male_run.png").convert_alpha()
    male_run2 = pygame.image.load("image/male_run2.png").convert_alpha()
    female_run1 = pygame.image.load("image/female_run.png").convert_alpha()
    female_run2 = pygame.image.load("image/female_run2.png").convert_alpha()

    male_run1 = pygame.transform.scale(male_run1, (100,100))
    male_run2 = pygame.transform.scale(male_run2, (100,100))
    female_run1 = pygame.transform.scale(female_run1, (100,100))
    female_run2 = pygame.transform.scale(female_run2, (100,100))

    # =========================
    # 변수
    # =========================
    scene = "game"
    frame_index = 0
    animation_timer = 0
    animation_speed = 200

    # 시작 위치
    start_x = WIDTH
    start_y = HEIGHT
    game_started = False

    # =========================
    # 교수 상태
    # =========================
    professor_state = "side"
    professor_timer = 0
    SIDE_TIME = 1200
    FRONT_TIME = 2000

    # 마우스 움직임 감지용
    last_mouse_pos = (0, 0)

    # 앞모습 유예시간
    front_grace_timer = 0
    FRONT_GRACE_TIME = 200

    # =========================
    # 위치
    # =========================
    professor_pos = (500, 200)
    student_positions = [(70, 320), (310, 320), (570, 320)]

    # 학생 히트박스
    student_rects = [
        pygame.Rect(85, 350, 130, 130),
        pygame.Rect(330, 350, 130, 130),
        pygame.Rect(590, 350, 130, 130)
    ]

    # 문 히트박스
    door_rect = pygame.Rect(60, 130, 90, 260)

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False # [수정] 창을 닫으면 게임 전체 종료를 위해 False 반환

            # =====================
            # 게임오버 재도전
            # =====================
            if scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    professor_state = "side"
                    professor_timer = 0
                    front_grace_timer = 0
                    pygame.mouse.set_pos((start_x,start_y))
                    last_mouse_pos = (start_x,start_y)
                    game_started = False

            # =====================
            # [수정] 스테이지 클리어 후 넘어가기
            # =====================
            elif scene == "stage2":
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    return True # 아무 키나 누르면 True를 반환하며 다음 스테이지로 제어권을 넘김

        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()

        # 플레이어 히트박스
        player_rect = pygame.Rect(mx - 20, my - 20, 40, 40)

        # =========================
        # 게임 화면
        # =========================
        if scene == "game":
            # 시작 위치
            if not game_started:
                pygame.mouse.set_pos((start_x, start_y))
                last_mouse_pos = (start_x, start_y)
                game_started = True

            DISPLAYSURF.blit(background, (0,0))

            # 교수 상태 변경
            professor_timer += dt
            if professor_state == "side":
                if professor_timer >= SIDE_TIME:
                    professor_state = "front"
                    professor_timer = 0
                    front_grace_timer = 0
            else:
                if professor_timer >= FRONT_TIME:
                    professor_state = "side"
                    professor_timer = 0

            # 교수 출력
            if professor_state == "side":
                professor_img = professor_side
            else:
                professor_img = professor_front

            DISPLAYSURF.blit(professor_img, professor_pos)

            # 학생 출력
            for pos in student_positions:
                DISPLAYSURF.blit(student_img, pos)

            # 학생 충돌
            for rect in student_rects:
                if player_rect.colliderect(rect):
                    scene = "gameover"

            # 교수 앞모습 감지
            if professor_state == "front":
                front_grace_timer += dt
                if front_grace_timer >= FRONT_GRACE_TIME:
                    if (mx, my) != last_mouse_pos:
                        scene = "gameover"

            last_mouse_pos = (mx, my)

            # 문 충돌
            if player_rect.colliderect(door_rect):
                scene = "stage2"

            # 캐릭터 애니메이션
            animation_timer += dt
            if animation_timer >= animation_speed:
                animation_timer = 0
                frame_index = (frame_index + 1) % 2

            # [수정] main.py에서 전달받은 매개변수 selected_gender를 사용합니다.
            if selected_gender == "male":
                player_img = male_run1 if frame_index == 0 else male_run2
            else:
                player_img = female_run1 if frame_index == 0 else female_run2

            # 캐릭터 출력
            DISPLAYSURF.blit(player_img, (mx - 50, my - 50))

        # =========================
        # 게임오버 화면
        # =========================
        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0,0))
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (255,255,255))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        # =========================
        # [수정] Stage2 대기 화면 연출
        # =========================
        elif scene == "stage2":
            DISPLAYSURF.fill((0,0,0))
            clear_text = font.render("STAGE 1 CLEAR! (PRESS ANY KEY)", True, (255,255,255))
            clear_rect = clear_text.get_rect(center=(400,300))
            DISPLAYSURF.blit(clear_text, clear_rect)

        pygame.display.update()
