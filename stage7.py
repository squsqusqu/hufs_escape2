import pygame
import sys
from pygame.locals import *

# [수정] main.py와 연동하기 위해 run 함수로 감쌉니다.
def run(DISPLAYSURF, selected_gender):
    # =========================
    # 화면 설정
    # =========================
    WIDTH = 800
    HEIGHT = 600
    clock = pygame.time.Clock()

    # =========================
    # 폰트
    # =========================
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)
    large_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 60)

    # =========================
    # 기본 설정
    # =========================
    scene = "game"
    game_started = False

    # =========================
    # 이미지 로드 및 크기 조절
    # =========================
    background = pygame.image.load("image/playground.jpeg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background.set_alpha(150)

    goal_img = pygame.image.load("image/soccer_goal.png").convert_alpha()
    goal_img = pygame.transform.scale(goal_img, (500, 320))

    goalkeeper_img = pygame.image.load("image/goalkeeper.png").convert_alpha()
    goalkeeper_img = pygame.transform.scale(goalkeeper_img, (90, 170))

    ball_img = pygame.image.load("image/soccer_ball.png").convert_alpha()
    ball_img = pygame.transform.scale(ball_img, (140, 100))

    arrow_left = pygame.transform.scale(pygame.image.load("image/arrow_left.png").convert_alpha(), (80, 80))
    arrow_center = pygame.transform.scale(pygame.image.load("image/arrow_center.png").convert_alpha(), (80, 80))
    arrow_right = pygame.transform.scale(pygame.image.load("image/arrow_right.png").convert_alpha(), (80, 80))

    gameover_img = pygame.image.load("image/stage3_gameover.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # 캐릭터 이미지
    male_run1 = pygame.transform.scale(pygame.image.load("image/male_run.png").convert_alpha(), (100, 100))
    male_run2 = pygame.transform.scale(pygame.image.load("image/male_run2.png").convert_alpha(), (100, 100))
    female_run1 = pygame.transform.scale(pygame.image.load("image/female_run.png").convert_alpha(), (100, 100))
    female_run2 = pygame.transform.scale(pygame.image.load("image/female_run2.png").convert_alpha(), (100, 100))

    # 애니메이션 변수
    frame_index = 0
    animation_timer = 0
    animation_speed = 200

    # =========================
    # 변수 사전 선언 (nonlocal을 위해)
    # =========================
    ball_x = ball_y = shooting = shot_direction = shot_speed = None
    goalkeeper_x = goalkeeper_y = goalkeeper_speed = goalkeeper_direction = None
    power_gauge = power_direction = clicked_arrow = result_text = None

    # =========================
    # 게임 리셋 함수
    # =========================
    # [수정] global 대신 nonlocal을 사용하여 run 함수 내부의 상태 변수를 제어합니다.
    def reset_game():
        nonlocal ball_x, ball_y, shooting, shot_direction, shot_speed
        nonlocal goalkeeper_x, goalkeeper_y, goalkeeper_speed, goalkeeper_direction
        nonlocal power_gauge, power_direction, result_text, clicked_arrow
        
        ball_x = 330
        ball_y = 510
        shooting = False
        shot_direction = None
        shot_speed = 15
        
        goalkeeper_x = 355
        goalkeeper_y = 120
        goalkeeper_speed = 5
        goalkeeper_direction = 1
        
        power_gauge = 0
        power_direction = 1
        clicked_arrow = None  
        result_text = ""

    reset_game()

    # 위치 제한 및 화살표 히트박스
    goal_x, goal_y = 150, 30
    LEFT_LIMIT, RIGHT_LIMIT = 230, 480  

    goal_rect = pygame.Rect(230, 90, 360, 200)
    left_rect = pygame.Rect(220, 400, 80, 80)
    center_rect = pygame.Rect(360, 400, 80, 80)
    right_rect = pygame.Rect(500, 400, 80, 80)

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False # [수정] 창 닫을 때 프로그램 종료

            if scene == "game":
                # 마우스 클릭 시작 (게이지 충전)
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if left_rect.collidepoint(mx, my): clicked_arrow = "left"
                    elif center_rect.collidepoint(mx, my): clicked_arrow = "center"
                    elif right_rect.collidepoint(mx, my): clicked_arrow = "right"
                
                # 마우스 클릭 해제 (슛 발사)
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    if clicked_arrow and not shooting:
                        shooting = True
                        shot_direction = clicked_arrow
                    clicked_arrow = None

            elif scene == "gameover" and event.type == KEYDOWN:
                scene = "game"
                game_started = False
                reset_game()

            # [수정] 최종 클리어 대기 화면
            elif scene == "stage8":
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    return True # 아무 키나 누르면 게임 전체 클리어!

        pygame.mouse.set_visible(True)
        mx, my = pygame.mouse.get_pos()

        # =====================
        # 게임 플레이 씬
        # =====================
        if scene == "game":
            if not game_started:
                pygame.mouse.set_pos((400, 500))
                game_started = True
                reset_game()

            DISPLAYSURF.fill((255, 255, 255))
            DISPLAYSURF.blit(background, (0, 0))
            DISPLAYSURF.blit(goal_img, (goal_x, goal_y))

            # 골키퍼 천천히 순찰 이동
            goalkeeper_x += goalkeeper_speed * goalkeeper_direction
            if goalkeeper_x >= RIGHT_LIMIT:
                goalkeeper_direction = -1
            if goalkeeper_x <= LEFT_LIMIT:
                goalkeeper_direction = 1

            goalkeeper_rect = pygame.Rect(goalkeeper_x, goalkeeper_y, 90, 220)
            DISPLAYSURF.blit(goalkeeper_img, (goalkeeper_x, goalkeeper_y))

            # 화살표 그리기
            DISPLAYSURF.blit(arrow_left, (220, 400))
            DISPLAYSURF.blit(arrow_center, (360, 400))
            DISPLAYSURF.blit(arrow_right, (500, 400))

            # 게이지 시스템
            if clicked_arrow and not shooting:
                power_gauge += 2.5 * power_direction
                if power_gauge >= 100:
                    power_gauge = 100
                    power_direction = -1
                elif power_gauge <= 0:
                    power_gauge = 0
                    power_direction = 1
                
                pygame.draw.rect(DISPLAYSURF, (50, 50, 50), pygame.Rect(300, 360, 200, 20))
                fill_color = (0, 255, 0) if 70 <= power_gauge <= 90 else (255, 50, 50)
                pygame.draw.rect(DISPLAYSURF, fill_color, pygame.Rect(300, 360, int(power_gauge) * 2, 20))
                
                guide_txt = font.render(f"파워: {int(power_gauge)}% (70-90 조준!)", True, (255, 255, 255))
                DISPLAYSURF.blit(guide_txt, (210, 310))

            DISPLAYSURF.blit(ball_img, (ball_x, ball_y))

            # 슛 애니메이션 및 궤적 연산
            if shooting:
                if shot_direction == "left":
                    ball_x -= 9.5 if 70 <= power_gauge <= 90 else 5.5
                    ball_y -= shot_speed
                elif shot_direction == "right":
                    ball_x += 9.5 if 70 <= power_gauge <= 90 else 5.5
                    ball_y -= shot_speed
                elif shot_direction == "center":
                    ball_y -= shot_speed

                shot_rect = pygame.Rect(ball_x + 40, ball_y + 20, 60, 60)

                # 판정 조건문 규칙
                if shot_rect.colliderect(goalkeeper_rect):
                    result_text = "MISSED! 골키퍼 정면 선방!"
                    scene = "gameover"
                elif shot_rect.colliderect(goal_rect):
                    if power_gauge > 90:
                        result_text = "OVER THE BAR! 너무 강해서 홈런!"
                        scene = "gameover"
                    elif power_gauge < 70:
                        result_text = "TOO WEAK! 슛이 너무 약합니다!"
                        scene = "gameover"
                    else:
                        scene = "stage8"
                elif ball_y < 50:
                    result_text = "OUT OF BOUNDS! 실축!"
                    scene = "gameover"

            # 캐릭터 애니메이션
            animation_timer += dt
            if animation_timer >= animation_speed:
                animation_timer = 0
                frame_index = (frame_index + 1) % 2

            # [수정] main.py에서 받은 selected_gender 기반으로 표출
            player_img = male_run1 if frame_index == 0 else male_run2 if selected_gender == "male" else female_run1 if frame_index == 0 else female_run2
            DISPLAYSURF.blit(player_img, (350, 500))

        # =====================
        # 게임오버 씬
        # =====================
        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0, 0))
            if result_text:
                reason_txt = font.render(result_text, True, (255, 100, 100))
                DISPLAYSURF.blit(reason_txt, (WIDTH // 2 - reason_txt.get_width() // 2, 220))

            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (255, 255, 255))
            DISPLAYSURF.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, 520))

        # =====================
        # Stage 8 씬 (최종 클리어 대기화면)
        # =====================
        elif scene == "stage8":
            DISPLAYSURF.fill((10, 30, 10))
            clear_text = font.render("모든 스테이지 클리어! (PRESS ANY KEY)", True, (255, 255, 255))
            DISPLAYSURF.blit(clear_text, (WIDTH // 2 - clear_text.get_width() // 2, 320))

        pygame.display.update()
