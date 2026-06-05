import pygame
import sys
from pygame.locals import *

# [수정] main.py에서 호출할 수 있도록 함수화하고 매개변수를 받습니다.
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
    title_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 45)
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 30)
    small_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 24)

    # =========================
    # 배경 이미지
    # =========================
    background = pygame.image.load("image/start_background.png").convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background.set_alpha(80) # 투명도

    # =========================
    # 게임오버 이미지
    # =========================
    gameover_img = pygame.image.load("image/stage3_gameover.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # =========================
    # 캐릭터 이미지 (현재 화면에는 출력되지 않으나 데이터 보존을 위해 유지)
    # =========================
    male_run1 = pygame.transform.scale(pygame.image.load("image/male_run.png").convert_alpha(), (100,100))
    male_run2 = pygame.transform.scale(pygame.image.load("image/male_run2.png").convert_alpha(), (100,100))
    female_run1 = pygame.transform.scale(pygame.image.load("image/female_run.png").convert_alpha(), (100,100))
    female_run2 = pygame.transform.scale(pygame.image.load("image/female_run2.png").convert_alpha(), (100,100))

    # =========================
    # 문제
    # =========================
    question = "팀원이 올린 코드를 가져오는 Git 명령어는?\n($ 제외하고 입력)"
    lines = question.split("\n")
    correct_answer = 'git pull'

    answer_input = ""

    # =========================
    # 변수
    # =========================
    scene = "game"
    frame_index = 0
    animation_timer = 0
    animation_speed = 200

    # 시작 위치
    start_x = WIDTH - 70
    start_y = HEIGHT - 70
    game_started = False

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False # [수정] 창을 닫으면 메인 시스템에 종료(False) 전달

            # =====================
            # 게임 입력
            # =====================
            if scene == "game":
                if event.type == KEYDOWN:
                    # 지우기
                    if event.key == K_BACKSPACE:
                        answer_input = answer_input[:-1]

                    # 엔터 (답안 제출)
                    elif event.key == K_RETURN:
                        # 정답
                        if answer_input.strip() == correct_answer:
                            scene = "stage6"
                        # 오답
                        else:
                            scene = "gameover"

                    # 글자 입력
                    else:
                        if len(answer_input) < 15:
                            answer_input += event.unicode

            # =====================
            # 게임오버 재도전
            # =====================
            elif scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    answer_input = ""
                    game_started = False

            # =====================
            # [수정] 클리어 대기 화면
            # =====================
            elif scene == "stage6":
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    return True # 아무 키나 누르면 True를 반환하며 다음 스테이지로 이동

        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()

        # =========================
        # 게임 화면
        # =========================
        if scene == "game":
            # 시작 위치로 커서 강제 이동
            if not game_started:
                pygame.mouse.set_pos((start_x, start_y))
                game_started = True

            DISPLAYSURF.fill((255,255,255))
            DISPLAYSURF.blit(background, (0,0))

            # 문제 출력
            title_text = title_font.render("QUESTION", True, (0,0,0))
            DISPLAYSURF.blit(title_text, (150,50))

            for i, line in enumerate(lines):
                question_text = font.render(line, True, (0,0,0))
                DISPLAYSURF.blit(question_text, (100, 150 + i * 40))

            guide_text = small_font.render("Type your answer and press ENTER", True, (50,50,50))
            DISPLAYSURF.blit(guide_text, (180,250))

            # 입력창 배경
            input_rect = pygame.Rect(180, 330, 450, 70)
            pygame.draw.rect(DISPLAYSURF, (255,255,255), input_rect)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), input_rect, 3)

            # 유저 타이핑 텍스트 출력
            answer_text = font.render(answer_input, True, (0,0,0))
            DISPLAYSURF.blit(answer_text, (200,350))

        # =========================
        # 게임오버 화면
        # =========================
        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0,0))
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (255,255,255))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        # =========================
        # Stage 6 (클리어) 화면
        # =========================
        elif scene == "stage6":
            DISPLAYSURF.fill((0,0,0))
            clear_text = title_font.render("공학관 통과! (PRESS ANY KEY)", True, (255,255,255))
            clear_rect = clear_text.get_rect(center=(400,300))
            DISPLAYSURF.blit(clear_text, clear_rect)

        pygame.display.update()
