import pygame as pg
from os import listdir, path as os_path
import random
from copy import deepcopy
from time import sleep

#rus start animation
def run_animation_full_screen(path_to_folders: str, animation_frames: list) -> None:
    """Run the start animation using a list of frames.

    Args:
        animation_frames (list): A list of frame filenames to use in the animation.
        path_to_folders (str): The path to the folder containing the animation frames.

    Returns:
        None
    """
    running_animation = True
    frame_index = 0
    while running_animation:
        frame = pg.image.load(os_path.join(path_to_folders, animation_frames[frame_index])).convert()
        screen.blit(frame, (0, 0))
        pg.display.update()
        clock.tick(FPS)
        frame_index += 1
        if frame_index >= len(listdir(path_to_folders)):
            running_animation = False

#play soung
def play_sound(path: str) -> None:
    """
    Plays a sound file.

    Parameters:
    path (str): The path to the sound file.

    Returns:
    None
    """
    sound = pg.mixer.Sound(path)
    sound.play()

# draw background for the board
def draw_board() -> None:
    """
    Draws the game board.
    
    Parameters:
        None

    Returns:
        None

    """
    pg.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    font_one = pg.font.Font( font_one_url , 24)
    score_text = font_one.render(f'Рахунок: {score}', True, 'black')
    high_score_text = font_one.render(f'Найкращий рахунок: {high_score}', True, 'black')
    screen.blit(score_text, (10, 415))
    screen.blit(high_score_text, (10, 460))

#draw skils board
def draw_skils_board() -> None:
    """
    Draws the skils board.
    
    Parameters:
        None
    """
    pg.draw.rect(screen, colors['skils_board'], [400, 0, 150, HEIGHT], 0)
    if keys[pg.K_1]:
        draw_icon_button(mario_save_button_big, (75, 55))
    else:
        draw_icon_button(mario_save_button_small, (75, 55))
    if keys[pg.K_2]:
        draw_icon_button(mario_load_button_big, (75, 55))
    
# draw tiles for game
def draw_pieces(board) -> None:
    """
    Draws the tiles for the game.

    Parameters:
    board (list): The game board.

    Returns:
    None
    """
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            pg.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pg.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color) 
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57)) #Кординати тексту
                screen.blit(value_text, text_rect)
                pg.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5) #Рамочка )

# spawn in new pieces randomly when turns start
def new_pieces(board) -> bool|list:
    """
    Spawns new pieces on the board.

    Parameters:
    board (list): The game board.

    Returns:
    list: The updated game board.
    bool: A flag indicating whether the game is over.
    """
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 512:
                board[row][col] = 4
            else:
                board[row][col] = 256
    if count < 1:
        full = True
    return board, full

# take your turn based on direction
def take_turn(direc, board) -> list:
    """
    Perform a turn in the 2048 game by moving tiles in the specified direction.

    Parameters:
    - direc (str): The direction in which to move the tiles ('UP', 'DOWN', 'LEFT', 'RIGHT').
    - board (list): The current state of the game board represented as a 4x4 list of integers.

    Returns:
    - list: The updated game board after the turn.

    Global Variables:
    - score (int): Tracks the player's score during the game.

    The function implements the logic for moving tiles in the specified direction on the 2048 game board.
    It handles merging tiles with the same value and updating the score accordingly.
    """
    global score
    play_sound(sound_file_path_move)
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board

#display game over
def display_text_message(text: str) -> None:
    """
    Display the text message in the center of the screen.

    This function creates a rectangle to display the text message "text"
    and draws a border around it. The text is centered inside the rectangle.

    Parameters:
    text (str): The message to display.

    Returns:
    None
    """
    rect_game_message = pg.Rect((WIDTH / 2) - 225 , (HEIGHT / 2) - 100, 450, 150)
    font_game_message = pg.font.Font(font_one_url, 32)
    game_text = font_game_message.render(f'{text}', True, 'black')
    text_rect = game_text.get_rect()
    text_rect.center = rect_game_message.center
    pg.draw.rect(screen, colors['gg'], rect_game_message, border_radius=10)
    pg.draw.rect(screen, "black", rect_game_message, border_radius=10, width= 5)
    screen.blit(game_text, text_rect)

def draw_icon_button(path: str, position: tuple, bg_color: tuple = (255, 255, 255))->None:
    """
    Draw an icon button on the screen.

    Parameters:
    path (str): The path to the icon image.
    position (tuple): The position of the icon button.
    bg_color (tuple): The background color of the icon button.
    """
    image_button = pg.image.load(path).convert_alpha()
    image_button.set_colorkey(bg_color)
    image_button_rect = image_button.get_rect()
    image_button_rect.center = ( 400 + position[0], position[1])
    screen.blit(image_button, image_button_rect)
   
def user_save(board: list, score: int) -> list|int:
    """
    Perform user save action in the game.

    Parameters:
    board (list): The current game board to be saved.
    score (int): The current score of the game to be saved.

    Returns:
    tuple: A tuple containing the deep copy of the board and the score.
    """
    play_sound(sound_file_path_save)
    save_board = deepcopy(board)
    save_score = score
    return save_board, save_score

def user_load(board: list, score: int) -> list|int:
    """
    Perform user load action in the game.

    Parameters:
    board (list): The current game board to be loaded.
    score (int): The current score of the game to be loaded.

    Returns:
    tuple: A tuple containing the deep copy of the loaded board and the loaded score.
    """
    play_sound(sound_file_path_load)
    board_values_load = deepcopy(board)
    score_load = score
    return board_values_load, score_load

# Constants
WIDTH = 550
HEIGHT = 500
FPS = 15
winner_score = 2048

# 2048 game color library
colors = {0: (204, 192, 179),
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
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'bg': (187, 173, 160),
          'skils_board': (255, 255, 179),
          'gg': (250, 250, 250)
          }

# URL
file_score_url = "high_score.txt"
icon_image_url = "Images\\icon.png"
mario_save_button_small = "Images\\mario_button\\folder_mario_small.png"
mario_save_button_big = "Images\\mario_button\\folder_mario_big.png"
mario_load_button_big = "Images\\mario_button\\folder_mario_big_load.png"
start_animation_url = "Images\\StartAnimation"
win_animation_url = "Images\\WinAnimation"
sound_file_path_start = "sounds\\sound_start3.mp3"
sound_file_path_move = "sounds\\sound_move1.mp3"
sound_file_path_gg = "sounds\\sound_gg.mp3"
sound_file_path_win = "sounds\\sound_win.mp3"
sound_file_path_save = "sounds\\sound_save.mp3"
sound_file_path_load = "sounds\\sound_load.mp3"
font_one_url = "font//Gropled-Bold.otf"
start_animation_list = listdir(start_animation_url)
win_animation_list = listdir(win_animation_url)


pg.init()

#Create display
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("2048")
icon = pg.image.load(icon_image_url)
pg.display.set_icon(icon)

# Create FPS
clock = pg.time.Clock()
clock.tick(FPS)

#Game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
save_board = deepcopy(board_values)
score = 0
save_score = score
try:
    with open(file_score_url, encoding="utf-8") as file_score:
        high_score = int(file_score.read())
except FileNotFoundError:
    print("Файл не знайдено")
    high_score = 0


#Flags
run = True
running_start_animation = True
frame_index = 0
spawn_new = True
init_count = 0
game_over = False
winner =False
direction = ''
stop = False
save_game = False
load_game = False

#Main loop
while run:

#Ranning start animation Змінити стартуву анімацію
    if running_start_animation:
        play_sound(sound_file_path_start)
        run_animation_full_screen(start_animation_url, start_animation_list)
        running_start_animation = False

    screen.fill('gray')
    keys = pg.key.get_pressed()
    draw_board()
    draw_skils_board()
    draw_pieces(board_values)

# Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_UP:
                direction = 'UP'
            elif event.key == pg.K_DOWN:
                direction = 'DOWN'
            elif event.key == pg.K_LEFT:
                direction = 'LEFT'
            elif event.key == pg.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pg.K_1:
                save_game = True
            elif event.key == pg.K_2:
                load_game = True
                
            if game_over or winner:
                if event.key == pg.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False
                    winner = False
                    stop = False
                    save_board = [[0 for _ in range(4)] for _ in range(4)]
                    save_score = 0

    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1

    if direction != '' and not stop:
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True

    if save_game:
        save_board, save_score = user_save(board_values, score)
        save_game = False

    if load_game:
        if save_board == [[0 for _ in range(4)] for _ in range(4)]:
            if keys[pg.K_2]:
                display_text_message("Збережень немає")
                pg.display.update()
                sleep(2)
        else:
            board_values, score = user_load(save_board, save_score)
            load_game = False
            game_over = False
            stop = False
    
    if any(winner_score in row for row in board_values) and not stop:
        winner = True

    if winner:
        if not stop:
            play_sound(sound_file_path_win)
            run_animation_full_screen(win_animation_url, win_animation_list)
        display_text_message("Ви перемогри)")
        stop = True

    if game_over:
        if not stop:
            play_sound(sound_file_path_gg)
        display_text_message("ГРУ ЗАВЕРШИНО")
        stop = True

    if (game_over or winner) and high_score < score:
        try:
            with open(file_score_url, "w", encoding="utf-8") as file_score:
                file_score.write(str(score))
            high_score = score
        except:
            print("Файл не знайно, рахунок не був оновленний")
            high_score = 0
    
    pg.display.update()
    clock.tick(FPS)

pg.quit()
