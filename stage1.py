import pygame
import sys
import random

def run():

    # 화면 설정 (배경 이미지 비율에 맞춰 조정 가능)
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("교실 탈출 게임")
    clock = pygame.time.Clock()

    # === 수정된 부분: 폰트 설정 (재시작 텍스트용) ===
    font = pygame.font.SysFont(None, 50) 
    # ================================================

    # 마우스 커서 숨기기 (남학생 이미지가 커서를 대신함)
    pygame.mouse.set_visible(False)

    # --- 이미지 로드 및 크기 조정 ---

    # 1. 배경
    bg_img = pygame.image.load("image/Stage2_강의실 배경.png").convert()
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

    # 2. 교수님 (전면/후면)
    prof_front = pygame.image.load("image/Stage2_교수님 객체_전면.png").convert_alpha()
    prof_back = pygame.image.load("image/Stage2_교수님 객체_후면.png").convert_alpha()

    # 교수님 크기 조정
    prof_size = (80, 150)
    prof_front = pygame.transform.scale(prof_front, prof_size)
    prof_back = pygame.transform.scale(prof_back, prof_size)

    # 교수님 위치 (마이크 단상 바로 오른쪽)
    prof_rect = prof_front.get_rect(center=(330, 270)) 

    # 3. 플레이어 (학생 걷기/뛰기)
    player_walk = pygame.image.load("image/male_run_l.png").convert_alpha()
    player_run = pygame.image.load("image/male_run2_l.png").convert_alpha()

    # === 수정된 부분: 학생 크기를 교수님과 동일하게(80, 150) 확대 ===
    player_size = (80, 150) 
    player_walk = pygame.transform.scale(player_walk, player_size)
    player_run = pygame.transform.scale(player_run, player_size)
    # ================================================================

    # 4. 결과 화면 이미지
    fail1_img = pygame.image.load("image/Stage2_선택지1.png").convert() # 출튀 걸림
    success_img = pygame.image.load("image/Stage2_선택지3_남학생.png").convert() # 탈출 성공 (남학생 기준)

    fail1_img = pygame.transform.scale(fail1_img, (screen_width, screen_height))
    success_img = pygame.transform.scale(success_img, (screen_width, screen_height))

    # --- 게임 상태 및 변수 설정 ---
    # 플레이어 초기 위치를 마우스 현재 위치로 설정
    player_rect = player_walk.get_rect(center=pygame.mouse.get_pos())
    prev_mouse_pos = pygame.mouse.get_pos() # 이전 프레임의 마우스 위치 추적용

    # 충돌 박스 (히트박스) 설정
    # 문 위치 대략적 수정 (왼쪽 문)
    door_rect = pygame.Rect(20, 150, 100, 250) 

    # 교수님 상태 변수
    prof_facing_front = False # False면 칠판을 봄(이동 가능), True면 앞을 봄(이동 불가)
    last_turn_time = pygame.time.get_ticks()
    turn_interval = random.randint(1500, 3000) # 1.5초 ~ 3초 사이 랜덤하게 돌아봄

    # 게임 진행 상태 ('PLAYING', 'FAIL1', 'SUCCESS')
    game_state = 'PLAYING'

    # --- 메인 게임 루프 ---
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # === 수정된 부분: 실패 화면에서 아무 키나 누르면 재시작 ===
            if event.type == pygame.KEYDOWN:
                if game_state == 'FAIL1':
                    # 게임 상태 초기화
                    game_state = 'PLAYING'
                    pygame.mouse.set_visible(False) # 마우스 다시 숨김
                    prof_facing_front = False # 교수님은 다시 칠판을 봄
                    last_turn_time = pygame.time.get_ticks() # 타이머 초기화
                    
                    # 플레이어 위치 마우스 위치로 재설정 (재시작 시 바로 죽는 현상 방지)
                    pygame.mouse.set_pos(screen_width // 2, screen_height - 100) # 커서를 화면 하단으로 초기화
                    prev_mouse_pos = pygame.mouse.get_pos()
                    player_rect.center = prev_mouse_pos
                elif game_state == "SUCCESS" :
                    return
            # ==========================================================

        if game_state == 'PLAYING':
            # 1. 교수님 뒤돌아보는 로직 (타이머 기반)
            if current_time - last_turn_time > turn_interval:
                prof_facing_front = not prof_facing_front # 상태 반전
                last_turn_time = current_time
                turn_interval = random.randint(1500, 3500) # 다음 턴 시간 다시 랜덤 설정

            # 2. 마우스 좌표 기반 이동 로직
            current_mouse_pos = pygame.mouse.get_pos()
            player_rect.center = current_mouse_pos # 남학생 이미지가 마우스를 따라감
            
            is_moving = False
            
            # 이전 마우스 좌표와 현재 좌표가 다르면 '움직임'으로 판정
            if current_mouse_pos != prev_mouse_pos:
                is_moving = True
                
            prev_mouse_pos = current_mouse_pos # 다음 프레임 비교를 위해 현재 위치 저장

            # 3. 충돌 및 게임 오버 판정 로직
            if is_moving:
                # [실패 조건] 교수님이 앞을 볼 때 마우스를 움직인 경우
                if prof_facing_front:
                    game_state = 'FAIL1'
                    pygame.mouse.set_visible(True) # 게임 오버 시 기본 마우스 커서 다시 표시
                    
            # [성공 조건] 문 히트박스와 닿은 경우
            if player_rect.colliderect(door_rect):
                game_state = 'SUCCESS'
                pygame.mouse.set_visible(True) # 게임 클리어 시 기본 마우스 커서 다시 표시

            # 4. 화면 그리기
            screen.blit(bg_img, (0, 0)) # 배경
            
            # 교수님 그리기
            if prof_facing_front:
                screen.blit(prof_front, prof_rect)
            else:
                screen.blit(prof_back, prof_rect)
                
            # 플레이어 그리기 (마우스가 움직일 땐 뛰는 프레임, 멈춰있을 땐 걷는 프레임)
            if is_moving:
                screen.blit(player_run, player_rect)
            else:
                screen.blit(player_walk, player_rect)

        # 결과 화면 출력
        elif game_state == 'FAIL1':
            screen.blit(fail1_img, (0, 0))
            
            # === 수정된 부분: 재시작 안내 텍스트 출력 ===
            gameover_text = font.render(
                "PRESS ANY KEY TO RETRY",
                True,
                (0, 0, 0) # 검은색 텍스트
            )
            # 텍스트를 화면 하단 중앙에 배치
            text_rect = gameover_text.get_rect(center=(screen_width // 2, 520))
            screen.blit(gameover_text, text_rect)
            # ============================================
            
        elif game_state == 'SUCCESS':
            screen.blit(success_img, (0, 0))
            # 다음 스테이지 안내 문구 추가
            next_text = font.render("PRESS ANY KEY TO NEXT STAGE", True, (0, 0, 0))
            text_rect = next_text.get_rect(center=(screen_width // 2, 520))
            screen.blit(next_text, text_rect)

        pygame.display.flip() # 화면 업데이트
        clock.tick(60) # 60 FPS 유지
