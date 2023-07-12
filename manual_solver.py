import pygame
import random

# Initialize Pygame
pygame.init()

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the dimensions of the game window
WINDOW_WIDTH = 425
WINDOW_HEIGHT = 425

# Set the size of each grid cell
CELL_SIZE = 100

# Set the margin between cells
CELL_MARGIN = 10

# Set the font for the score display
FONT = pygame.font.Font(None, 36)

# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2048 Game")


def draw_grid():
    for row in range(4):
        for col in range(4):
            pygame.draw.rect(window, GRAY, (col * (CELL_SIZE + CELL_MARGIN), row * (CELL_SIZE + CELL_MARGIN), CELL_SIZE, CELL_SIZE))


def draw_tile(row, col, value):
    colors = {
        0: WHITE,
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46)
    }
    tile_color = colors.get(value, BLACK)
    text_color = BLACK if value <= 4 else WHITE
    pygame.draw.rect(window, tile_color, (col * (CELL_SIZE + CELL_MARGIN), row * (CELL_SIZE + CELL_MARGIN), CELL_SIZE, CELL_SIZE))
    text = FONT.render(str(value), True, text_color)
    text_rect = text.get_rect(center=(col * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE / 2, row * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE / 2))
    window.blit(text, text_rect)


def main_game_loop():
    # Initialize the game board and scores
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    current_score = 0
    best_score = 0
    game_start = True
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Restart the game
                    board = [[0] * 4 for _ in range(4)]
                    add_new_tile(board)
                    add_new_tile(board)
                    current_score = 0
                    game_over = False

            elif game_start:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Start the game
                    game_start = False

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        board, moved, current_score = move_up(board, current_score)
                        if moved:
                            add_new_tile(board)
                    elif event.key == pygame.K_DOWN:
                        board, moved, current_score = move_down(board, current_score)
                        if moved:
                            add_new_tile(board)
                    elif event.key == pygame.K_LEFT:
                        board, moved, current_score = move_left(board, current_score)
                        if moved:
                            add_new_tile(board)
                    elif event.key == pygame.K_RIGHT:
                        board, moved, current_score = move_right(board, current_score)
                        if moved:
                            add_new_tile(board)

        window.fill(BLACK)

        if game_start:
            start_text = FONT.render("Game Start", True, WHITE)
            start_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            window.blit(start_text, start_text_rect)
        elif game_over:
            over_text = FONT.render("Game Over", True, WHITE)
            over_text_rect = over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            score_text = FONT.render("Score: " + str(current_score), True, WHITE)
            score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            best_score_text = FONT.render("Best Score: " + str(best_score), True, WHITE)
            best_score_text_rect = best_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            restart_text = FONT.render("Press ENTER to restart", True, WHITE)
            restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
            window.blit(over_text, over_text_rect)
            window.blit(score_text, score_text_rect)
            window.blit(best_score_text, best_score_text_rect)
            window.blit(restart_text, restart_text_rect)
        else:
            draw_grid()
            for row in range(4):
                for col in range(4):
                    draw_tile(row, col, board[row][col])

        pygame.display.update()

        if not game_start and not game_over and is_board_full(board) and not valid_moves_exist(board):
            game_over = True
            best_score = max(best_score, current_score)


def add_new_tile(board):
    empty_cells = [(row, col) for row in range(4) for col in range(4) if board[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = random.choice([2, 4])


def move_up(board, current_score):
    moved = False
    for col in range(4):
        merged = False
        for row in range(1, 4):
            if board[row][col] != 0:
                for prev_row in range(row - 1, -1, -1):
                    if board[prev_row][col] == 0:
                        board[prev_row][col] = board[row][col]
                        board[row][col] = 0
                        moved = True
                        break
                    elif board[prev_row][col] == board[row][col] and not merged:
                        board[prev_row][col] *= 2
                        board[row][col] = 0
                        current_score += board[prev_row][col]
                        moved = True
                        merged = True
                        break
                    else:
                        break
    return board, moved, current_score
def move_down(board, current_score):
    moved = False
    for col in range(4):
        merged = False
        for row in range(2, -1, -1):
            if board[row][col] != 0:
                for prev_row in range(row + 1, 4):
                    if board[prev_row][col] == 0:
                        board[prev_row][col] = board[row][col]
                        board[row][col] = 0
                        moved = True
                        break
                    elif board[prev_row][col] == board[row][col] and not merged:
                        board[prev_row][col] *= 2
                        board[row][col] = 0
                        current_score += board[prev_row][col]
                        moved = True
                        merged = True
                        break
                    else:
                        break
    return board, moved, current_score


def move_left(board, current_score):
    moved = False
    for row in range(4):
        merged = False
        for col in range(1, 4):
            if board[row][col] != 0:
                for prev_col in range(col - 1, -1, -1):
                    if board[row][prev_col] == 0:
                        board[row][prev_col] = board[row][col]
                        board[row][col] = 0
                        moved = True
                        break
                    elif board[row][prev_col] == board[row][col] and not merged:
                        board[row][prev_col] *= 2
                        board[row][col] = 0
                        current_score += board[row][prev_col]
                        moved = True
                        merged = True
                        break
                    else:
                        break
    return board, moved, current_score


def move_right(board, current_score):
    moved = False
    for row in range(4):
        merged = False
        for col in range(2, -1, -1):
            if board[row][col] != 0:
                for prev_col in range(col + 1, 4):
                    if board[row][prev_col] == 0:
                        board[row][prev_col] = board[row][col]
                        board[row][col] = 0
                        moved = True
                        break
                    elif board[row][prev_col] == board[row][col] and not merged:
                        board[row][prev_col] *= 2
                        board[row][col] = 0
                        current_score += board[row][prev_col]
                        moved = True
                        merged = True
                        break
                    else:
                        break
    return board, moved, current_score


def is_board_full(board):
    for row in board:
        if 0 in row:
            return False
    return True


def valid_moves_exist(board):
    # Check if any adjacent cells have the same value
    for row in range(4):
        for col in range(4):
            if col < 3 and board[row][col] == board[row][col + 1]:
                return True
            if row < 3 and board[row][col] == board[row + 1][col]:
                return True
    return False


main_game_loop()
