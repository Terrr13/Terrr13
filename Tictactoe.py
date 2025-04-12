import pygame
import sys
import os

# Get absolute paths for assets - Hoang
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(BASE_PATH, "canada_bg.png")
MUSIC_PATH = os.path.join(BASE_PATH, "background_music.mp3")

# Initialize Pygame and Mixer - Hoang
pygame.init()
pygame.mixer.init()

# Set up the window (resizable) - Hoang
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tic Tac Toe - Canada Theme")

# Load background image - Hoang
try:
    BG_IMAGE = pygame.image.load(BG_PATH)
except Exception as e:
    print("Background image not found:", e)
    BG_IMAGE = None

# Load and play background music - Hoang
if os.path.exists(MUSIC_PATH):
    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Error loading music:", e)
else:
    print("Music file not found.")

# Define fonts (using Comic Sans MS if available) - Hoang
try:
    BOLD_FONT = pygame.font.SysFont("Comic Sans MS", 36, bold=True)
    BOLD_SMALL_FONT = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
    REG_FONT = pygame.font.SysFont("Comic Sans MS", 36, bold=False)
    REG_SMALL_FONT = pygame.font.SysFont("Comic Sans MS", 28, bold=False)
except Exception:
    BOLD_FONT = pygame.font.Font(None, 36)
    BOLD_SMALL_FONT = pygame.font.Font(None, 28)
    REG_FONT = pygame.font.Font(None, 36)
    REG_SMALL_FONT = pygame.font.Font(None, 28)

# Global state variables - Moiz
state = "menu"  # States: menu, game - 
music_on = True
theme = "light"

# Colors and helper functions for colors - Moiz
LIGHT_BG = (245, 245, 245)
DARK_BG = (40, 40, 40)
LIGHT_TEXT = (20, 20, 20)
DARK_TEXT = (235, 235, 235)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)

def get_result_text_color():
    return LIGHT_TEXT if theme == "light" else DARK_TEXT

TEXT_BG_LIGHT = (200, 200, 200)
TEXT_BG_DARK = (60, 60, 60)

def get_title_bg_color():
    return (50, 50, 50) if theme == "light" else (220, 220, 220)
def get_title_text_color():
    return (255, 255, 255) if theme == "light" else (0, 0, 0)

# Tic Tac Toe game variables- Toby 
board = [["" for _ in range(3)] for _ in range(3)]
current_turn = "X"  # "X" is Player 1, "O" is Player 2
game_over = False
winner = None
winning_cells = []
result_message = ""

def draw_text(text, font, color, surface, x, y):
    # Draw text at (x, y)- Toby
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def draw_button(surface, rect, text):
    # Draw a button with centered text; change color on hover-Toby
    mouse_pos = pygame.mouse.get_pos()
    btn_color = BUTTON_COLOR if not rect.collidepoint(mouse_pos) else BUTTON_HOVER
    pygame.draw.rect(surface, btn_color, rect)
    text_surf = REG_SMALL_FONT.render(text, True, LIGHT_TEXT if theme=="light" else DARK_TEXT)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

# Toggle between light and dark themes - Hoang
def switch_theme():
    global theme
    theme = "dark" if theme == "light" else "light"

# Toggle background music on or off - Hoang
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

# Reset the game board and variables - Moiz
def reset_game():
    global board, current_turn, game_over, winner, winning_cells, result_message
    board = [["" for _ in range(3)] for _ in range(3)]
    current_turn = "X"
    game_over = False
    winner = None
    winning_cells = []
    result_message = ""

def check_win():
    global game_over, winner, winning_cells, result_message
    for i in range(3):
        if board[i][0] != "" and board[i][0] == board[i][1] == board[i][2]:
            winner = board[i][0]
            winning_cells = [(i, 0), (i, 1), (i, 2)]
            game_over = True
            return
        if board[0][i] != "" and board[0][i] == board[1][i] == board[2][i]:
            winner = board[0][i]
            winning_cells = [(0, i), (1, i), (2, i)]
            game_over = True
            return
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
        winning_cells = [(0, 0), (1, 1), (2, 2)]
        game_over = True
        return
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        winner = board[0][2]
        winning_cells = [(0, 2), (1, 1), (2, 0)]
        game_over = True
        return
    if all(cell != "" for row in board for cell in row):
        game_over = True

def menu_screen():
    # Display main menu with title and  buttons- Toby & Jonathan
    global state, theme, music_on
    clock = pygame.time.Clock()
    while state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                win_width, win_height = SCREEN.get_width(), SCREEN.get_height()
                btn_width, btn_height = 200, 50
                start_y = win_height * 0.3
                gap = 70
                buttons = {
                    "Play Game": pygame.Rect((win_width - btn_width) / 2, start_y, btn_width, btn_height),
                    "Toggle Theme": pygame.Rect((win_width - btn_width) / 2, start_y + gap, btn_width, btn_height),
                    "Toggle Music": pygame.Rect((win_width - btn_width) / 2, start_y + 2 * gap, btn_width, btn_height),
                    "Quit Game": pygame.Rect((win_width - btn_width) / 2, start_y + 3 * gap, btn_width, btn_height)
                }
                if buttons["Play Game"].collidepoint(mouse_pos):
                    reset_game()
                    state = "game"
                elif buttons["Toggle Theme"].collidepoint(mouse_pos):
                    switch_theme()
                elif buttons["Toggle Music"].collidepoint(mouse_pos):
                    toggle_music()
                elif buttons["Quit Game"].collidepoint(mouse_pos):
                    pygame.quit(); sys.exit()

        win_width, win_height = SCREEN.get_width(), SCREEN.get_height()
        if BG_IMAGE:
            scaled_bg = pygame.transform.scale(BG_IMAGE, (win_width, win_height))
            SCREEN.blit(scaled_bg, (0, 0))
        else:
            SCREEN.fill(LIGHT_BG if theme=="light" else DARK_BG)

        # Draw title with background for contrast- Jonathan
        title_text = "Tic Tac Toe"
        title_surf = BOLD_FONT.render(title_text, True, get_title_text_color())
        title_rect = title_surf.get_rect(center=(win_width/2, win_height*0.15))
        padding = 10
        bg_rect = pygame.Rect(title_rect.left - padding, title_rect.top - padding,
                              title_rect.width + 2 * padding, title_rect.height + 2 * padding)
        pygame.draw.rect(SCREEN, get_title_bg_color(), bg_rect)
        SCREEN.blit(title_surf, title_rect)

        btn_width, btn_height = 200, 50
        start_y = win_height * 0.3
        gap = 70
        button_labels = ["Play Game", "Toggle Theme", "Toggle Music", "Quit Game"]
        for idx, label in enumerate(button_labels):
            rect = pygame.Rect((win_width - btn_width) / 2, start_y + idx * gap, btn_width, btn_height)
            draw_button(SCREEN, rect, label)

        pygame.display.flip()
        clock.tick(30)

def game_screen():
    # Display the game screen with the board, turn info, and end-game buttons- Jonathan
    global state, current_turn, game_over, winner, winning_cells, result_message
    clock = pygame.time.Clock()
    while state == "game":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                win_width, win_height = SCREEN.get_width(), SCREEN.get_height()
                board_size = min(win_width * 0.6, win_height * 0.6)
                cell_size = board_size / 3
                board_origin_x = (win_width - board_size) / 2
                board_origin_y = (win_height - board_size) / 2
                row = int((my - board_origin_y) // cell_size)
                col = int((mx - board_origin_x) // cell_size)
                if 0 <= row < 3 and 0 <= col < 3:
                    if board[row][col] == "":
                        board[row][col] = current_turn
                        check_win()
                        if game_over:
                            if winner:
                                result_message = f"Player {1 if winner=='X' else 2} ({winner}) wins!"
                            else:
                                result_message = "Draw!"
                        else:
                            current_turn = "O" if current_turn == "X" else "X"
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                win_width, win_height = SCREEN.get_width(), SCREEN.get_height()
                btn_width, btn_height, gap = 150, 50, 20
                total_width = 3 * btn_width + 2 * gap
                start_x = (win_width - total_width) / 2
                y = win_height - 100
                play_again_rect = pygame.Rect(start_x, y, btn_width, btn_height)
                menu_rect = pygame.Rect(start_x + btn_width + gap, y, btn_width, btn_height)
                quit_rect = pygame.Rect(start_x + 2 * (btn_width + gap), y, btn_width, btn_height)
                if play_again_rect.collidepoint(mouse_pos):
                    reset_game()
                elif menu_rect.collidepoint(mouse_pos):
                    state = "menu"
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit(); sys.exit()

        win_width, win_height = SCREEN.get_width(), SCREEN.get_height()
        if BG_IMAGE:
            scaled_bg = pygame.transform.scale(BG_IMAGE, (win_width, win_height))
            SCREEN.blit(scaled_bg, (0, 0))
        else:
            SCREEN.fill(LIGHT_BG if theme=="light" else DARK_BG)

        board_size = min(win_width * 0.6, win_height * 0.6)
        cell_size = board_size / 3
        board_origin_x = (win_width - board_size) / 2
        board_origin_y = (win_height - board_size) / 2

        # Draw board cells with borders-Bobby
        for r in range(3):
            for c in range(3):
                cell_rect = pygame.Rect(board_origin_x + c * cell_size, board_origin_y + r * cell_size, cell_size, cell_size)
                pygame.draw.rect(SCREEN, LIGHT_BG if theme=="light" else DARK_BG, cell_rect)
                pygame.draw.rect(SCREEN, LIGHT_TEXT if theme=="light" else DARK_TEXT, cell_rect, 2)

        # Draw marks (X and O) centered in cells
        for r in range(3):
            for c in range(3):
                mark = board[r][c]
                if mark != "":
                    text_surf = BOLD_FONT.render(mark, True, LIGHT_TEXT if theme=="light" else DARK_TEXT)
                    text_rect = text_surf.get_rect(center=(board_origin_x + c * cell_size + cell_size/2,
                                                            board_origin_y + r * cell_size + cell_size/2))
                    SCREEN.blit(text_surf, text_rect)

        # Highlight winning cells if any-Bobby
        if game_over and winner:
            for cell in winning_cells:
                r, c = cell
                rect = pygame.Rect(board_origin_x + c * cell_size, board_origin_y + r * cell_size, cell_size, cell_size)
                pygame.draw.rect(SCREEN, (255, 0, 0), rect, 5)

        # Display turn info or result with background for contrast- Jonathan
        if not game_over:
            player_turn = "Player 1 (X)" if current_turn == "X" else "Player 2 (O)"
            turn_text = f"Turn: {player_turn}"
            turn_surf = REG_FONT.render(turn_text, True, LIGHT_TEXT if theme=="light" else DARK_TEXT)
            turn_rect = turn_surf.get_rect(center=(win_width/2, 30))
            padding = 10
            turn_bg_rect = pygame.Rect(turn_rect.left - padding, turn_rect.top - padding,
                                       turn_rect.width + 2 * padding, turn_rect.height + 2 * padding)
            pygame.draw.rect(SCREEN, TEXT_BG_DARK if theme=="dark" else TEXT_BG_LIGHT, turn_bg_rect)
            SCREEN.blit(turn_surf, turn_rect)
        else:
            result_surf = BOLD_FONT.render(result_message, True, get_result_text_color())
            result_rect = result_surf.get_rect(center=(win_width/2, 30))
            padding = 10
            bg_rect = pygame.Rect(result_rect.left - padding, result_rect.top - padding,
                                  result_rect.width + 2 * padding, result_rect.height + 2 * padding)
            pygame.draw.rect(SCREEN, TEXT_BG_DARK if theme=="dark" else TEXT_BG_LIGHT, bg_rect)
            SCREEN.blit(result_surf, result_rect)
            # Draw buttons: Play Again, Menu, Quit- Bobby
            btn_width, btn_height, gap = 150, 50, 20
            total_width = 3 * btn_width + 2 * gap
            start_x = (win_width - total_width) / 2
            y = win_height - 100
            play_again_rect = pygame.Rect(start_x, y, btn_width, btn_height)
            menu_rect = pygame.Rect(start_x + btn_width + gap, y, btn_width, btn_height)
            quit_rect = pygame.Rect(start_x + 2 * (btn_width + gap), y, btn_width, btn_height)
            draw_button(SCREEN, play_again_rect, "Play Again")
            draw_button(SCREEN, menu_rect, "Menu")
            draw_button(SCREEN, quit_rect, "Quit")
        pygame.display.flip()
        clock.tick(30)

def main():
    # Main loop to switch between screens - Hoang
    while True:
        if state == "menu":
            menu_screen()
        elif state == "game":
            game_screen()

if __name__ == "__main__":
    main()
