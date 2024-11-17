import pygame
import random
import time

# 파이게임 라이브러리 초기화
pygame.init()

# 화면 크기 == 1280x720
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("색깔 기억력 게임")  # 창 제목

# RGB
colors = [
    (255, 0, 0),    # 빨간색
    (0, 0, 255),    # 파란색
    (0, 255, 0),    # 초록색
    (255, 255, 0),  # 노란색
    (255, 165, 0),  # 주황색
    (128, 0, 128),  # 보라색
    (255, 255, 255) # 흰색
]

# RGB 키보드 설정
color_keys = {
    pygame.K_KP1: 0,  # 1 : 빨간색
    pygame.K_KP2: 1,  # 2 : 파란색
    pygame.K_KP3: 2,  # 3 : 초록색
    pygame.K_KP4: 3,  # 4 : 노란색
    pygame.K_KP5: 4,  # 5 : 주황색
    pygame.K_KP6: 5,  # 6 : 보라색
    pygame.K_KP7: 6   # 7 : 흰색
}

# 폰트,크기 : 일반, 48
font = pygame.font.Font(None, 48)

# 밸런스 패치용 / (난이도 : N, 색깔 종류[RGB 키로 설정해야함])
levels = [
    (2, [0, 1]),                # 난 1: 2 라운드, 빨, 파
    (4, [0, 1, 2]),             # 난 2: 4 라운드, 빨, 파, 초
    (6, [0, 1, 2, 3]),          # 난 3: 6 라운드, 빨, 파, 초, 노
    (8, [0, 1, 2, 3, 4]),       # 난 4: 8 라운드, 빨, 파, 초, 노, 주
    (10, [0, 1, 2, 3, 4, 5]),   # 난 5: 10 라운드, 빨, 파, 초, 노, 주, 보
    (12, [0, 1, 2, 3, 4, 5, 6]) # 난 6: 12 라운드, 빨, 파, 초, 노, 주, 보, 흰
]

# 색상 시퀀스 생성 함수
def generate_sequence(rounds, available_colors):
    sequence = [random.choice(available_colors)]                # 첫 번째 색상 선택
    for _ in range(1, rounds):
        next_color = random.choice(available_colors)            # 다음 색상 선택
        while next_color == sequence[-1]:                       # 두 번 연속 같은 색상 방지
            next_color = random.choice(available_colors)
        sequence.append(next_color)                             # 선택된 색상 추가
    return sequence

# 색상 시퀀스 보여주는 함수
def show_sequence(sequence):
    for color_index in sequence:
        screen.fill(colors[color_index])        # 화면 전체 현재 색깔
        pygame.display.flip()                   # 화면 전환
        time.sleep(0.5)                         # 0.5초 대기
        screen.fill((0, 0, 0))                  # 화면 전우주
        pygame.display.flip()                   # 화면 전환
        time.sleep(0.2)                         # 0.2초 대기

# 텍스트 표시
def display_text(text, y_offset=0):
    text_surface = font.render(text, True, (255, 255, 255))             # 텍스트 표면 생성
    text_rect = text_surface.get_rect(center=(640, 360 + y_offset))     # 텍스트 위치 설정 (화면 중앙)
    screen.blit(text_surface, text_rect)                                # 화면에 텍스트 생성

# 시작 화면 표시 함수
def start_screen():
    screen.fill((0, 0, 0))                              # 화면 검은색
    display_text("Game Start : Press Spacebar")         # 시작 텍스트
    display_text("Quit Game : press q", y_offset=50)    # 코드 종료 텍스트
    pygame.display.flip()                               # 화면 전환

# 레벨 표시 함수
def show_level(level):
    screen.fill((0, 0, 0))                  # 화면 검은색
    display_text(f"Level {level + 1}")      # 현재 레벨 표시
    pygame.display.flip()                   # 화면 업데이트
    time.sleep(1)                           # 1초 대기

# 게임 오버 화면 표시
def game_over_screen():
    screen.fill((0, 0, 0))                      # 화면 검은색
    display_text("GAME OVER", y_offset=-20)     # 게임 오버 텍스트 생성
    pygame.display.flip()                       # 화면 전환
    time.sleep(2)                               # 2초 대기

# 메인 게임 루프
def main_game():
    level = 0                                                   # 첫 레벨 설정
    while level < len(levels):
        rounds, available_colors = levels[level]                # 현재 레벨 + 사용 가능한 색상 불러옴
        sequence = generate_sequence(rounds, available_colors)  # 색상 시퀀스 생성

        # 레벨 표시
        show_level(level)

        # 1. 색상 순서대로 표시
        show_sequence(sequence)

        # 2. 입력 화면 전환
        user_sequence = []        # 사용자의 입력 시퀀스 초기화
        start_time = time.time()  # 시작 시간 기록
        input_timeout = 15        # 입력 제한 시간 설정 (15초)

        # 3. 키보드 입력
        while len(user_sequence) < rounds and time.time() - start_time < input_timeout:
            remaining_time = input_timeout - (time.time() - start_time)         # 남은 시간 계산
            screen.fill((0, 0, 0))                                              # 화면 검은색(초기화)
            display_text(f"Time: {int(remaining_time)} Second", y_offset=-20)   # 남은 시간 표시 텍스트 생성
            display_text("Press Color Number:", y_offset=20)                    # 숫자키를 눌러주세요 텍스트 생성
            pygame.display.flip()                                               # 화면 전환

            for event in pygame.event.get():        # 이벤트 처리
                if event.type == pygame.QUIT:
                    pygame.quit()                   # pygame 종료
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:     # q 키 눌림
                        pygame.quit()               # pygame 종료
                        return "quit"
                    elif event.key in color_keys:   # 색상 번호 키 눌림
                        user_sequence.append(color_keys[event.key])     # 입력한 색상 추가
                        if len(user_sequence) == rounds:                # 모든 입력이 완료되면
                            break

        # 제한 시간 초과
        if time.time() - start_time >= input_timeout:
            print("Time Out!")      # 타임아웃 메시지 생성
            print("Game Over!")     # 게임 오버 메시지 생성
            game_over_screen()      # 게임 오버 화면 전환
            return "game_over"

        # 정답 확인
        if user_sequence == sequence:
            level += 1  # 다음 레벨로 진행
            print(f"Success! Next Level: {level + 1} Level")  # 성공 메시지 출력
        else:
            print("Game Over!")     # 게임 오버 메시지 출력
            game_over_screen()      # 게임 오버 화면 표시
            return "game_over"

        screen.fill((0, 0, 0))      # 화면 초기화
        pygame.display.flip()       # 화면 업데이트
        time.sleep(1)               # 1초 대기

    return "completed"              # 게임 완료 메시지 반환

# 메인 루프
def main():
    running = True          # 게임 실행 상태 변수
    while running:
        start_screen()      # 시작 화면 표시
        
        waiting_for_start = True                # 시작 대기 상태 변수
        while waiting_for_start:
            for event in pygame.event.get():    # 이벤트 처리
                if event.type == pygame.QUIT:   # 종료 이벤트
                    running = False             # 게임 종료
                    waiting_for_start = False
                elif event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_q:     # q 키 눌림
                        running = False             # 게임 종료
                        waiting_for_start = False
                    elif event.key == pygame.K_SPACE:           # 스페이스바 눌렸다면
                        waiting_for_start = False               # 시작 대기 종료
                        result = main_game()                    # 메인 게임 시작
                        if result == "quit":                    # 종료라면
                            running = False
                        elif result == "game_over":             # 게임 오버일때
                            print("Return to Start Screen")     # 시작 화면으로 텍스트 생성

    pygame.quit()  # pygame 종료

if __name__ == "__main__":
    main()  # 메인 함수 실행
