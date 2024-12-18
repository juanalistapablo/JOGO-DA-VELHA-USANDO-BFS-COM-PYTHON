import pygame
import sys
from collections import deque

# Configurações do jogo
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
O_COLOR = (0, 0, 255)
X_COLOR = (255, 0, 0)
CELL_SIZE = WIDTH // 3
LINE_WIDTH = 5
FPS = 30

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha com BFS")
clock = pygame.time.Clock()

# Função para desenhar o tabuleiro
def draw_board():
    screen.fill(BG_COLOR)
    for i in range(1, 3):
        # Linhas verticais
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        # Linhas horizontais
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)

# Função para desenhar X e O no tabuleiro
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

# Verifica o vencedor
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

# Função BFS para encontrar o melhor movimento
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

        # Verifica se é o melhor estado
        if check_winner(current_board, player):
            return path[0] if path else None

        # Gera próximos movimentos
        for row in range(3):
            for col in range(3):
                if current_board[row][col] == '':
                    new_board = [r[:] for r in current_board]
                    new_board[row][col] = player
                    queue.append((new_board, path + [(row, col)]))
    return None

# Função principal
def main():
    board = [['' for _ in range(3)] for _ in range(3)]
    player_turn = True  # True para jogador (X), False para computador (O)

    while True:
        draw_board()
        draw_symbols(board)
        pygame.display.flip()

        # Verifica eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Jogador faz um movimento
            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if board[row][col] == '':
                    board[row][col] = 'X'
                    if check_winner(board, 'X'):
                        print("Jogador X venceu!")
                        pygame.time.wait(2000)
                        pygame.quit()
                        sys.exit()
                    player_turn = False

        # Movimento do computador usando BFS
        if not player_turn:
            move = bfs_best_move(board, 'O')
            if move:
                row, col = move
                board[row][col] = 'O'
                if check_winner(board, 'O'):
                    print("Computador O venceu!")
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()
            player_turn = True

        # Verifica empate
        if all(all(cell != '' for cell in row) for row in board):
            print("Empate!")
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        clock.tick(FPS)

# Executa o jogo
if _name_ == "_main_":
    main()
