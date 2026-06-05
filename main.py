import pygame
import sys

# 각 스테이지 파이썬 파일을 모듈로 불러옵니다.
import stage0
import stage1
import stage2

def main():
    pygame.init() # 게임 전체 초기화는 메인에서 한 번만 해줍니다.

    # 1. 시작 화면 실행
    # stage0.run()이 끝나면 다음 줄로 넘어갑니다.
    stage0.run()

    # 2. 스테이지 1 (교실 탈출) 실행
    stage1.run()

    # 3. 성별 선택 (필요에 따라 메인에서 정하거나 이전 스테이지에서 받아올 수 있습니다)
    # 지금은 임의로 "male"로 설정하여 넘겨줍니다.
    selected_gender = "male" 

    # 4. 스테이지 2 (엘리베이터) 실행
    stage2.run(selected_gender)

    # 모든 스테이지가 끝나면 게임 종료
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()