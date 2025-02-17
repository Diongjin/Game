import sys
import pygame
import random

# 게임 초기 설정
pygame.init()
TILE_SIZE = 30  # 타일 크기 축소

# 난이도 설정 (쉬움: 15x15, 보통: 21x21, 어려움: 25x25)
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DIFFICULTY_SIZES = {
    "easy": (15, 15),
    "medium": (21, 21),
    "hard": (25, 25)
}

def select_difficulty():
    """게임 시작 전에 난이도를 선택하는 함수"""
    print("난이도를 선택하세요: \n1. 쉬움 (Easy)\n2. 보통 (Medium)\n3. 어려움 (Hard)")
    choice = input("번호를 입력하세요 (1-3): ")
    if choice in ["1", "2", "3"]:
        return DIFFICULTY_LEVELS[int(choice) - 1]
    else:
        print("잘못된 입력입니다. 기본 난이도(보통)로 설정합니다.")
        return "medium"

def next_level(difficulty):
    """현재 난이도가 쉬움 또는 보통이면 다음 단계로 진행할지 묻기"""
    if difficulty in ["easy", "medium"]:
        choice = input("다음 단계로 진행하시겠습니까? (y/n): ")
        if choice.lower() == "y":
            return DIFFICULTY_LEVELS[DIFFICULTY_LEVELS.index(difficulty) + 1]
    return None

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

def move_enemy(enemy_x, enemy_y, maze):
    """적 NPC를 랜덤하게 이동시키는 함수"""
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = enemy_x + dx, enemy_y + dy
        if maze[new_y][new_x] == 0:  # 길이 있는 경우만 이동
            return new_x, new_y
    return enemy_x, enemy_y

def play_game(difficulty):
    ROWS, COLS = DIFFICULTY_SIZES[difficulty]
    WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
    maze = generate_maze(ROWS, COLS)
    player_x, player_y = 1, 1
    enemy_x, enemy_y = COLS - 3, ROWS - 3  # 적의 초기 위치

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Maze Escape - {difficulty.capitalize()} Mode")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill((255, 255, 255))
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if maze[row][col] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                elif maze[row][col] == 2:
                    pygame.draw.rect(screen, (0, 255, 0), rect)
        pygame.draw.rect(screen, (0, 0, 255), (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, (255, 0, 0), (enemy_x * TILE_SIZE, enemy_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 적 그리기
        
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
                    print("탈출 성공!")
                    running = False
        
        enemy_x, enemy_y = move_enemy(enemy_x, enemy_y, maze)  # 적 이동
        
        if player_x == enemy_x and player_y == enemy_y:
            print("적에게 잡혔습니다! 게임 오버!")
            running = False
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    return difficulty

if __name__ == "__main__":
    difficulty = select_difficulty()
    while difficulty:
        difficulty = play_game(difficulty)
        difficulty = next_level(difficulty)
