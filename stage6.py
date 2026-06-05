import pygame
import sys
import random
from pygame.locals import *

# [수정] main.py와 연동하기 위해 run 함수로 감싸고 매개변수를 받습니다.
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
    title_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 40)
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 30)
    small_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 24)

    # =========================
    # 배경 이미지
    # =========================
    background = pygame.image.load("image/start_background.png").convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background.set_alpha(50)

    # =========================
    # 게임오버 이미지
    # =========================
    gameover_img = pygame.image.load("image/stage3_gameover.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # =========================
    # 게임 진행 변수
    # =========================
    scene = "game"
    current_q = 1      
    q2_attempts = 0    
    question = ""      
    answers_data = []  
    q4_timer = 0       

    title_num_rect = pygame.Rect(0, 0, 0, 0) 

    # =========================
    # 문제 세팅 함수
    # [수정] run() 함수 내부에서 지역 변수를 수정할 수 있도록 nonlocal 선언을 사용합니다.
    # =========================
    def setup_question(q_num):
        nonlocal question, answers_data, q4_timer
        answers_data = []
        q4_timer = 0 
        
        if q_num == 1:
            question = "2+5=?"
            choices = ["17", "77", "70", "7"]
            correct_idx = 3 
            speed_options = [-8, -6, 6, 8] 
            for i in range(4):
                rect = pygame.Rect(80 + (i * 170), 300, 100, 70)
                answers_data.append({
                    "rect": rect, "text": choices[i], "index": i,
                    "is_correct": (i == correct_idx),
                    "dx": random.choice(speed_options), "dy": random.choice(speed_options)
                })
                
        elif q_num == 2:
            question = "1+4=?"
            choices = ["5", "15", "25", "35"]
            correct_idx = 3 
            for i in range(4):
                rect = pygame.Rect(80 + (i * 170), 300, 100, 70)
                answers_data.append({
                    "rect": rect, "text": choices[i], "index": i,
                    "is_correct": (i == correct_idx), "dx": 0, "dy": 0
                })
                
        elif q_num == 3:
            question = "21 - 18 = ?"
            choices = ["11", "6", "4", "2"]
            correct_idx = -1 # 상자에는 정답 없음
            for i in range(4):
                rect = pygame.Rect(80 + (i * 170), 300, 100, 70)
                answers_data.append({
                    "rect": rect, "text": choices[i], "index": i,
                    "is_correct": (i == correct_idx), "dx": 0, "dy": 0
                })

        elif q_num == 4:
            question = "5 x 3 = ?"
            choices = ["10", "20", "30", "40"]
            for i in range(4):
                rect = pygame.Rect(80 + (i * 170), 300, 100, 70)
                answers_data.append({
                    "rect": rect, "text": choices[i], "index": i,
                    "is_correct": False, "dx": 0, "dy": 0
                })
            falling_rect = pygame.Rect(335, -100, 100, 70)
            answers_data.append({
                "rect": falling_rect, "text": "15", "index": 4,
                "is_correct": True, "dx": 0, "dy": 0
            })

        elif q_num == 5:
            question = "오른쪽을 클릭하시오."
            rect_left = pygame.Rect(150, 300, 120, 70)
            answers_data.append({
                "rect": rect_left, "text": "왼쪽", "index": 0,
                "is_correct": False, "dx": 0, "dy": 0
            })
            rect_right = pygame.Rect(530, 300, 120, 70)
            answers_data.append({
                "rect": rect_right, "text": "오른쪽", "index": 1,
                "is_correct": False, "dx": 0, "dy": 0
            })

    # 첫 문제 세팅
    setup_question(1)

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False # [수정] 강제 종료 대신 False 반환

            # =====================
            # 게임오버 재시작
            # =====================
            if scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    current_q = 1
                    q2_attempts = 0 # [수정] 재시작 시 시도 횟수도 초기화
                    setup_question(1)

            # =====================
            # [수정] 스테이지 클리어 (Stage 7로 넘어가기)
            # =====================
            elif scene == "stage7":
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    return True # 키 입력이 있으면 True 반환

            # =====================
            # 마우스 클릭 판정
            # =====================
            if scene == "game" and event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                clicked_box = False

                # 좌클릭 (일반적인 선택)
                if event.button == 1: 
                    for data in answers_data:
                        if data["rect"].collidepoint(mx, my):
                            clicked_box = True
                            
                            if data["is_correct"]:
                                if current_q == 1:
                                    current_q = 2
                                    q2_attempts += 1 
                                    setup_question(2)
                                elif current_q == 2:
                                    current_q = 3
                                    setup_question(3)
                                elif current_q == 4:
                                    current_q = 5
                                    setup_question(5)
                            else:
                                scene = "gameover"
                            break
                    
                    # 3번 문제: 상자가 아닌 QUESTION 번호를 클릭했을 때
                    if not clicked_box and current_q == 3:
                        if title_num_rect.collidepoint(mx, my):
                            current_q = 4
                            setup_question(4)

                # 우클릭 (5번 문제 파훼법)
                elif event.button == 3:
                    if current_q == 5:
                        scene = "stage7"

        pygame.mouse.set_visible(True)

        # =========================
        # 게임 화면 출력
        # =========================
        if scene == "game":
            DISPLAYSURF.fill((255,255,255))
            DISPLAYSURF.blit(background, (0,0))

            q_surface = title_font.render("QUESTION ", True, (0,0,0))
            q_rect = q_surface.get_rect(topleft=(280, 40))
            DISPLAYSURF.blit(q_surface, q_rect)

            num_surface = title_font.render(str(current_q), True, (0,0,0))
            title_num_rect = num_surface.get_rect(topleft=(q_rect.right, 40))
            DISPLAYSURF.blit(num_surface, title_num_rect)

            question_text = font.render(question, True, (0,0,0))
            q_rect_txt = question_text.get_rect(center=(400, 130))
            DISPLAYSURF.blit(question_text, q_rect_txt)

            # 1번 문제: 상자 튕김 이동
            if current_q == 1:
                for data in answers_data:
                    rect = data["rect"]
                    rect.x += data["dx"]
                    rect.y += data["dy"]
                    
                    if rect.left <= 0: rect.left = 0; data["dx"] *= -1
                    elif rect.right >= WIDTH: rect.right = WIDTH; data["dx"] *= -1
                        
                    if rect.top <= 0: rect.top = 0; data["dy"] *= -1
                    elif rect.bottom >= HEIGHT: rect.bottom = HEIGHT; data["dy"] *= -1

                for i in range(len(answers_data)):
                    for j in range(i + 1, len(answers_data)):
                        rect1 = answers_data[i]["rect"]
                        rect2 = answers_data[j]["rect"]
                        
                        if rect1.colliderect(rect2):
                            answers_data[i]["dx"] *= -1
                            answers_data[i]["dy"] *= -1
                            answers_data[j]["dx"] *= -1
                            answers_data[j]["dy"] *= -1
                            
                            if rect1.centerx < rect2.centerx: rect1.x -= 8; rect2.x += 8
                            else: rect1.x += 8; rect2.x -= 8
                                
                            if rect1.centery < rect2.centery: rect1.y -= 8; rect2.y += 8
                            else: rect1.y += 8; rect2.y -= 8

            # 4번 문제: 인내심 타이머 & 박스 하강 로직
            elif current_q == 4:
                q4_timer += dt
                if q4_timer >= 5000: 
                    box5 = answers_data[4]["rect"]
                    if box5.y < 380:
                        box5.y += 10 
                        if box5.y > 380: 
                            box5.y = 380

            # 답안지 그리기
            for data in answers_data:
                rect = data["rect"]

                pygame.draw.rect(DISPLAYSURF, (180,180,180), rect)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), rect, 2)
                
                # 2번 문제 글자 페이드 효과 및 정렬
                if current_q == 2 and data["index"] == 0:
                    if q2_attempts == 1: col_4 = (180, 180, 180) 
                    elif q2_attempts == 2: col_4 = (120, 120, 120) 
                    else: col_4 = (0, 0, 0)       
                        
                    t4 = small_font.render("4", True, col_4)
                    t5 = small_font.render("5", True, (0,0,0))
                    
                    total_width = t4.get_width() + t5.get_width()
                    start_x = rect.centerx - (total_width // 2)
                    start_y = rect.centery - (t4.get_height() // 2)
                    
                    DISPLAYSURF.blit(t4, (start_x, start_y))
                    DISPLAYSURF.blit(t5, (start_x + t4.get_width(), start_y))

                elif current_q == 2 and data["index"] == 3:
                    if q2_attempts == 1: col_3 = (0, 0, 0)       
                    elif q2_attempts == 2: col_3 = (120, 120, 120) 
                    else: col_3 = (180, 180, 180) 
                        
                    t3 = small_font.render("3", True, col_3)
                    t5 = small_font.render("5", True, (0,0,0))
                    
                    total_width = t3.get_width() + t5.get_width()
                    start_x = rect.centerx - (total_width // 2)
                    start_y = rect.centery - (t3.get_height() // 2)
                    
                    DISPLAYSURF.blit(t3, (start_x, start_y))
                    DISPLAYSURF.blit(t5, (start_x + t3.get_width(), start_y))
                    
                else:
                    text_surface = small_font.render(data["text"], True, (0,0,0))
                    text_rect = text_surface.get_rect(center=rect.center)
                    DISPLAYSURF.blit(text_surface, text_rect)

        # =========================
        # 게임오버 화면
        # =========================
        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0,0))
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (255,255,255))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        # =========================
        # Stage 7 클리어 화면
        # =========================
        elif scene == "stage7":
            DISPLAYSURF.fill((0,0,0))
            clear_text = title_font.render("STAGE 6 CLEAR! (PRESS ANY KEY)", True, (255,255,255))
            clear_rect = clear_text.get_rect(center=(400,300))
            DISPLAYSURF.blit(clear_text, clear_rect)

        pygame.display.update()
