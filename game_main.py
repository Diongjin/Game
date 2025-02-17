import sys
import pygame

# 미로 데이터 (1: 벽, 0: 길, 2: 출구)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 게임 초기 설정
pygame.init()
TILE_SIZE = 40  # 타일 크기
ROWS = len(maze)  # 행 개수
COLS = len(maze[0])  # 열 개수
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE  # 크기 동적 설정

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 플레이어 초기 위치
player_x, player_y = 1, 1

def draw_maze(screen):
    """미로를 화면에 그리는 함수"""
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, GREEN, rect)

def main():
    global player_x, player_y
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Escape")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill(WHITE)
        draw_maze(screen)
        pygame.draw.rect(screen, BLUE, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
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
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
