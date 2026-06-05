import pygame
import sys
import random

# [수정] main.py에서 생성한 화면 스크린과 선택된 성별을 매개변수로 받습니다.
def run(screen, selected_gender):

    # 화면 설정 (정의 값은 유지하되 디스플레이 생성 코드는 제거)
    screen_width = 800
    screen_height = 600
    clock = pygame.time.Clock()

    # 폰트 설정
    font = pygame.font.SysFont(None, 50) 

    # 마우스 커서 숨기기
    pygame.mouse.set_visible(False)

    # --- 이미지 로드 및 크기 조정 ---

    # 1. 배경
    bg_img = pygame.image.load("image/Stage2_강의실 배경.png").convert()
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

    # 2. 교수님 (전면/후면)
    prof_front = pygame.image.load("image/Stage2_교수님 객체_전면.png").convert_alpha()
    prof_back = pygame.image.load("image/Stage2_교수님 객체_후면.png").convert_alpha()
    prof_size = (80, 150)
    prof_front = pygame.transform.scale(prof_front, prof_size)
    prof_back = pygame.transform.scale(prof_back, prof_size)
    prof_rect = prof_front.get_rect(center=(330, 270)) 

    # 3. 플레이어 (성별 데이터에 따른 분기 처리)
    player_size = (80, 150) 
    
    if selected_gender == "male":
        player_walk = pygame.image.load("image/male_run_l.png").convert_alpha()
        player_run = pygame.image.load("image/male_run2_l.png").convert_alpha()
        success_bg_path = "image/Stage2_선택지3_남학생.png"
    else:
        # [수정] 여학생 전용 대형 이미지가 없을 경우를 대비한 예외 처리 로직입니다.
        try:
            player_walk = pygame.image.load("image/female_run_l.png").convert_alpha()
            player_run = pygame.image.load("image/female_run2_l.png").convert_alpha()
        except:
            player_walk = pygame.image.load("image/female_run.png").convert_alpha()
            player_run = pygame.image.load("image/female_run2.png").convert_alpha()
        
        try:
            success_bg_path = "image/Stage2_선택지3_여학생.png"
            pygame.image.load(success_bg_path)
        except:
            success_bg_path = "image/Stage2_선택지3_남학생.png"

    player_walk = pygame.transform.scale(player_walk, player_size)
    player_run = pygame.transform.scale(player_run, player_size)

    # 4. 결과 화면 이미지
    fail1_img = pygame.image.load("image/Stage2_선택지1.png").convert() 
    success_img = pygame.image.load(success_bg_path).convert()

    fail1_img = pygame.transform.scale(fail1_img, (screen_width, screen_height))
    success_img = pygame.transform.scale(success_img, (screen_width, screen_height))

    # --- 게임 상태 및 변수 설정 ---
    player_rect = player_walk.get_rect(center=pygame.mouse.get_pos())
    prev_mouse_pos = pygame.mouse.get_pos() 

    door_rect = pygame.Rect(20, 150, 100, 250) 

    prof_facing_front = False 
    last_turn_time = pygame.time.get_ticks()
    turn_interval = random.randint(1500, 3000) 

    game_state = 'PLAYING'

    # --- 메인 게임 루프 ---
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # [수정] 창을 닫으면 전체 프로세스 종료를 위해 False 반환
                
            # [수정] 키보드 입력뿐만 아니라 마우스 클릭으로도 상태를 넘길 수 있도록 보완
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == 'FAIL1':
                    game_state = 'PLAYING'
                    pygame.mouse.set_visible(False) 
                    prof_facing_front = False 
                    last_turn_time = pygame.time.get_ticks() 
                    
                    pygame.mouse.set_pos(screen_width // 2, screen_height - 100) 
                    prev_mouse_pos = pygame.mouse.get_pos()
                    player_rect.center = prev_mouse_pos
                    
                elif game_state == 'SUCCESS':
                    return True # [수정] 성공 화면에서 조작 시 True를 반환하며 Stage 3로 전환

        if game_state == 'PLAYING':
            if current_time - last_turn_time > turn_interval:
                prof_facing_front = not prof_facing_front 
                last_turn_time = current_time
                turn_interval = random.randint(1500, 3500) 

            current_mouse_pos = pygame.mouse.get_pos()
            player_rect.center = current_mouse_pos 
            
            is_moving = False
            if current_mouse_pos != prev_mouse_pos:
                is_moving = True
                
            prev_mouse_pos = current_mouse_pos 

            if is_moving:
                if prof_facing_front:
                    game_state = 'FAIL1'
                    pygame.mouse.set_visible(True) 
                    
            if player_rect.colliderect(door_rect):
                game_state = 'SUCCESS'
                pygame.mouse.set_visible(True) 

            screen.blit(bg_img, (0, 0)) 
            
            if prof_facing_front:
                screen.blit(prof_front, prof_rect)
            else:
                screen.blit(prof_back, prof_rect)
                
            if is_moving:
                screen.blit(player_run, player_rect)
            else:
                screen.blit(player_walk, player_rect)

        elif game_state == 'FAIL1':
            screen.blit(fail1_img, (0, 0))
            gameover_text = font.render("PRESS ANY KEY TO RETRY", True, (0, 0, 0))
            text_rect = gameover_text.get_rect(center=(screen_width // 2, 520))
            screen.blit(gameover_text, text_rect)
            
        elif game_state == 'SUCCESS':
            screen.blit(success_img, (0, 0))
            next_text = font.render("PRESS ANY KEY TO NEXT STAGE", True, (0, 0, 0))
            text_rect = next_text.get_rect(center=(screen_width // 2, 520))
            screen.blit(next_text, text_rect)

        pygame.display.flip() 
        clock.tick(60)
