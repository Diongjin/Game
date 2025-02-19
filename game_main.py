import sys
import pygame
import random
import time

# 게임 초기 설정
pygame.init()
TILE_SIZE = 30  # 타일 크기 축소

# 포털 이미지 로드 및 크기 조정
portal_image = pygame.image.load("portal.jpg")
portal_image = pygame.transform.scale(portal_image, (TILE_SIZE, TILE_SIZE))

# 난이도 설정 (쉬움: 15x15, 보통: 21x21, 어려움: 25x25)
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DIFFICULTY_SIZES = {
    "easy": (15, 15),
    "medium": (21, 21),
    "hard": (25, 25)
}

# 최고 기록 로드
try:
    with open("best_time.txt", "r") as file:
        best_time = float(file.read().strip())
except FileNotFoundError:
    best_time = float('inf')

def generate_maze(rows, cols):
    """난이도에 따라 랜덤한 미로 생성"""
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    stack = [(start_x, start_y)]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    maze[rows - 2][cols - 2] = 2  # 출구 설정
    return maze

def play_game(difficulty):
    global best_time
    ROWS, COLS = DIFFICULTY_SIZES[difficulty]
    WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
    maze = generate_maze(ROWS, COLS)
    player_x, player_y = 1, 1
    start_time = time.time()  # 단계 시작 시간

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Maze Escape - {difficulty.capitalize()} Mode")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill((255, 255, 255))

        # 미로 및 플레이어 그리기
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if maze[row][col] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect)  # 벽
                elif maze[row][col] == 2:
                    pygame.draw.rect(screen, (0, 255, 0), rect)  # 출구

        pygame.draw.rect(screen, (0, 0, 255), (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 플레이어

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_x, new_y = player_x, player_y
                if event.key == pygame.K_LEFT:
                    new_x -= 1
                elif event.key == pygame.K_RIGHT:
                    new_x += 1
                elif event.key == pygame.K_UP:
                    new_y -= 1
                elif event.key == pygame.K_DOWN:
                    new_y += 1

                if 0 <= new_y < ROWS and 0 <= new_x < COLS and maze[new_y][new_x] != 1:
                    player_x, player_y = new_x, new_y

                if maze[player_y][player_x] == 2:
                    end_time = time.time() - start_time
                    print(f"{difficulty.capitalize()} 단계 탈출! 걸린 시간: {end_time:.2f}초")
                    return end_time

        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    return None

if __name__ == "__main__":
    total_time = 0
    for difficulty in DIFFICULTY_LEVELS:
        stage_time = play_game(difficulty)
        if stage_time is not None:
            total_time += stage_time
    
    print(f"총 탈출 시간: {total_time:.2f}초")
    
    # 최고 기록 갱신 여부 확인 및 저장
    if total_time < best_time:
        best_time = total_time
        with open("best_time.txt", "w") as file:
            file.write(f"{best_time:.2f}")
        print(f"🎉 새로운 최고 기록! {best_time:.2f}초 🎉")
    else:
        print(f"현재 최고 기록: {best_time:.2f}초")
