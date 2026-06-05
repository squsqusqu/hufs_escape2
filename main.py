# main.py
import pygame
import sys

# 수정한 스테이지 파일들을 불러옵니다.
import stage0
import stage1
import stage3
import stage4
import stage5
import stage6
import stage7

def main():
    # 1. 게임 초기화 및 통합 화면 생성 (여기서 딱 한 번만 실행)
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("외대탈출")

    # 2. Stage 0 (시작 화면) 실행 및 성별 데이터 받아오기
    # 주의: stage0.py의 run 함수는 성별(selected_gender)을 return 하도록 수정해야 합니다.
    # 예시: return selected_gender
    selected_gender = stage0.run(DISPLAYSURF) 
    
    if not selected_gender: # 창을 끄거나 중간에 나갔을 경우
        pygame.quit()
        sys.exit()

    # 3. 스테이지 순차 실행 (상태 머신 구조)
    # 스테이지가 클리어되어 True를 반환하면 다음 if문으로 넘어갑니다.
    
    if stage1.run(DISPLAYSURF, selected_gender):
        # 교양관 클리어 후 다음 스테이지로
        pass
    else:
        quit_game()

    # stage2가 있다면 여기에 추가
    # if stage2.run(DISPLAYSURF, selected_gender): ...

    if stage3.run(DISPLAYSURF, selected_gender):
        pass
    else:
        quit_game()

    if stage4.run(DISPLAYSURF, selected_gender):
        pass
    else:
        quit_game()

    if stage5.run(DISPLAYSURF, selected_gender):
        pass
    else:
        quit_game()

    if stage6.run(DISPLAYSURF, selected_gender):
        pass
    else:
        quit_game()

    if stage7.run(DISPLAYSURF, selected_gender):
        # 모든 스테이지 클리어! (엔딩 화면 호출 등)
        print("게임 최종 클리어!")
    else:
        quit_game()

    quit_game()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
