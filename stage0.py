import pygame, sys
from pygame.locals import *

def run(DISPLAYSURF):
    WIDTH = 800
    HEIGHT = 600
    
    clock = pygame.time.Clock()
    
    # =========================
    # 이미지 불러오기
    # =========================
    
    background = pygame.image.load("image/start_background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    male_img = pygame.image.load("image/male_select.png").convert_alpha()
    male_img = pygame.transform.scale(male_img, (150, 250))
    
    female_img = pygame.image.load("image/female_select.png").convert_alpha()
    female_img = pygame.transform.scale(female_img, (150, 250))
    
    # =========================
    # 남자 달리기 이미지
    # =========================
    
    male_run1 = pygame.image.load("image/male_run.png").convert_alpha()
    male_run2 = pygame.image.load("image/male_run2.png").convert_alpha()
    
    male_run1 = pygame.transform.scale(male_run1, (100, 100))
    male_run2 = pygame.transform.scale(male_run2, (100, 100))
    
    # =========================
    # 여자 달리기 이미지
    # =========================
    
    female_run1 = pygame.image.load("image/female_run.png").convert_alpha()
    female_run2 = pygame.image.load("image/female_run2.png").convert_alpha()
    
    female_run1 = pygame.transform.scale(female_run1, (100, 100))
    female_run2 = pygame.transform.scale(female_run2, (100, 100))
    
    # =========================
    # 폰트
    # =========================
    
    title_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 70)
    
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 28)
    
    small_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 20)
    
    # =========================
    # 변수
    # =========================
    
    scene = "start"
    
    player_name = ""
    selected_gender = None
    
    input_active = True
    
    # 캐릭터 애니메이션 변수
    frame_index = 0
    animation_timer = 0
    animation_speed = 200
    
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    
    # 캐릭터 선택 박스
    male_rect = pygame.Rect(170, 230, 150, 250)
    female_rect = pygame.Rect(480, 230, 150, 250)
    
    # =========================
    # 게임 루프
    # =========================
    
    while True:
    
        dt = clock.tick(60)
    
        for event in pygame.event.get():
    
            if event.type == QUIT:
                return None
    
            # =========================
            # 시작 화면 작동
            # =========================
    
            if scene == "start":
    
                if event.type == MOUSEBUTTONDOWN:
                    scene = "setting"
    
            # =========================
            # 설정 화면
            # =========================
    
            elif scene == "setting":
    
                # 이름 입력
                if event.type == KEYDOWN:
    
                    if input_active:
    
                        if event.key == K_BACKSPACE:
                            player_name = player_name[:-1]
    
                        elif event.key == K_RETURN:
    
                            if player_name != "" and selected_gender != None:
                                scene = "game"
    
                        else:
    
                            if len(player_name) < 10:
                                player_name += event.unicode
    
                # 성별 선택
                if event.type == MOUSEBUTTONDOWN:
    
                    if male_rect.collidepoint(event.pos):
                        selected_gender = "male"
    
                    if female_rect.collidepoint(event.pos):
                        selected_gender = "female"
    
        # =====================================================
        # 시작 화면
        # =====================================================
    
        if scene == "start":
    
            pygame.mouse.set_visible(True)
    
            DISPLAYSURF.blit(background, (0, 0))
    
            # 제목
            title = title_font.render("외대탈출", True, (255,255,255))
            title_rect = title.get_rect(center=(400,120))
    
            DISPLAYSURF.blit(title, title_rect)
    
            # 깜빡이는 문구
            current_time = pygame.time.get_ticks()
    
            if (current_time // 500) % 2 == 0:
    
                text = small_font.render(
                    ">> PRESS THE MOUSE BUTTON <<",
                    True,
                    (255,255,255)
                )
    
                text_rect = text.get_rect(center=(400,520))
    
                DISPLAYSURF.blit(text, text_rect)
    
        # =====================================================
        # 설정 화면
        # =====================================================
    
        elif scene == "setting":
    
            pygame.mouse.set_visible(True)
    
            DISPLAYSURF.fill((30,30,30))
    
            # 이름 입력
            name_text = font.render(
                f"이름(영어로 입력) : {player_name}",
                True,
                (255,255,255)
            )
    
            DISPLAYSURF.blit(name_text, (50,50))
    
            guide_text = small_font.render(
                "성별 선택 후 ENTER 를 누르면 시작",
                True,
                (180,180,180)
            )
    
            DISPLAYSURF.blit(guide_text, (50,90))
    
            # 게임 설명
            info1 = small_font.render(
                "교수님을 피해 외대를 탈출하세요.",
                True,
                (255,255,255)
            )
    
            info2 = small_font.render(
                "마우스로 이동할 수 있습니다.",
                True,
                (255,255,255)
            )
    
            DISPLAYSURF.blit(info1, (50,140))
            DISPLAYSURF.blit(info2, (50,170))
    
            # 남자 캐릭터
            DISPLAYSURF.blit(male_img, (170,230))
    
            # 여자 캐릭터
            DISPLAYSURF.blit(female_img, (480,230))
    
            # 선택 표시
            if selected_gender == "male":
                pygame.draw.rect(DISPLAYSURF, (0,255,0), male_rect, 5)
    
            if selected_gender == "female":
                pygame.draw.rect(DISPLAYSURF, (0,255,0), female_rect, 5)
    
        # =====================================================
        # 게임 화면
        # =====================================================
    
        elif scene == "game":
    
            pygame.mouse.set_visible(False)
    
            DISPLAYSURF.fill((0,0,0))
    
            # =========================
            # 마우스 위치
            # =========================
    
            mx, my = pygame.mouse.get_pos()
    
            player_x = mx
            player_y = my
    
            # =========================
            # 애니메이션
            # =========================
    
            animation_timer += dt
    
            if animation_timer >= animation_speed:
    
                animation_timer = 0
    
                if frame_index == 0:
                    frame_index = 1
                else:
                    frame_index = 0
    
            # =========================
            # 성별에 따라 캐릭터 변경
            # =========================
    
            if selected_gender == "male":
    
                if frame_index == 0:
                    player_img = male_run1
                else:
                    player_img = male_run2
    
            elif selected_gender == "female":
    
                if frame_index == 0:
                    player_img = female_run1
                else:
                    player_img = female_run2
    
            # =========================
            # 캐릭터 출력
            # =========================
    
            DISPLAYSURF.blit(
                player_img,
                (player_x - 50, player_y - 50)
            )
    
        pygame.display.update()
