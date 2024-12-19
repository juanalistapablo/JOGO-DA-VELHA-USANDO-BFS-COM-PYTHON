# JOGO DA VELHA COM BSF
import pygame
import sys
from collections import deque


WIDTH, HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
O_COLOR = (0, 0, 255)
X_COLOR = (255, 0, 0)
CELL_SIZE = WIDTH // 3
LINE_WIDTH = 5
FPS = 30


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha com BFS")
clock = pygame.time.Clock()


def draw_board():
    screen.fill(BG_COLOR)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)


def draw_symbols(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, 
                                 (col * CELL_SIZE + 20, row * CELL_SIZE + 20), 
                                 ((col+1) * CELL_SIZE - 20, (row+1) * CELL_SIZE - 20), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, 
                                 (col * CELL_SIZE + 20, (row+1) * CELL_SIZE - 20), 
                                 ((col+1) * CELL_SIZE - 20, row * CELL_SIZE + 20), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, 
                                   (col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2), 
                                   CELL_SIZE//3, LINE_WIDTH)


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False


def bfs_best_move(board, player):
    start = (board, [])
    queue = deque([start])
    visited = set()

    while queue:
        current_board, path = queue.popleft()
        board_tuple = tuple(map(tuple, current_board))
        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        
        if check_winner(current_board, player):
            return path[0] if path else None

        
        for row in range(3):
            for col in range(3):
                if current_board[row][col] == '':
                    new_board = [r[:] for r in current_board]
                    new_board[row][col] = player
                    queue.append((new_board, path + [(row, col)]))
    return None


def show_result(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def main():
    board = [['' for _ in range(3)] for _ in range(3)]
    player_turn = True  

    while True:
        draw_board()
        draw_symbols(board)
        pygame.display.flip()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if board[row][col] == '':
                    board[row][col] = 'X'
                    if check_winner(board, 'X'):
                        show_result("Você ganhou!")
                        pygame.quit()
                        sys.exit()
                    player_turn = False

        
        if not player_turn:
            move = bfs_best_move(board, 'O')
            if move:
                row, col = move
                board[row][col] = 'O'
                draw_board()
                draw_symbols(board)
                pygame.display.flip()
                pygame.time.wait(500)
                if check_winner(board, 'O'):
                    show_result("Você perdeu!")
                    pygame.quit()
                    sys.exit()
            player_turn = True

        
        empty_cells = sum(row.count('') for row in board)
        if empty_cells == 2 and not check_winner(board, 'X') and not check_winner(board, 'O'):
            show_result("Deu velha!")
            pygame.quit()
            sys.exit()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
