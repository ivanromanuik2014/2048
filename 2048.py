import pygame as pg
from os import listdir, path
import random

def run_animation(animation_frames: list, frame_index: int, running_animation: bool) -> int:
    """
    Runs an animation.

    Parameters:
    animation_frames (list): A list of animation frames.
    frame_index (int): The current frame index.
    running_animation (bool): A flag indicating whether the animation is running.

    Returns:
    int: The updated frame index.
    bool: A flag indicating whether the animation is running.
    """
    if running_animation:
        play_sound(sound_file_path_start)
        frame = pg.image.load(path.join(StartAnimationPath, animation_frames[frame_index]))
        screen.blit(frame, (-40, 40))
        frame_index += 1
        if frame_index >= len(listdir(StartAnimationPath)):
            running_animation = False  # Встановлюємо прапорець вимкнення анімації
    return frame_index, running_animation  # Повертаємо оновлений frame_index та running_animation

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
    score_text = font_one.render(f'Рахунок: {score}', True, 'black')
    high_score_text = font_one.render(f'Найкращий рахунок: {high_score}', True, 'black')
    screen.blit(score_text, (10, 415))
    screen.blit(high_score_text, (10, 460))
    pass

def draw_skils_board() ->None:
    pg.draw.rect(screen, colors['skils_board'], [400, 0, 150, HEIGHT], 0)
    pass

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
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pg.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# spawn in new pieces randomly when turns start
def new_pieces(board):
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
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# take your turn based on direction
def take_turn(direc, board):
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

# Constants
WIDTH = 550
HEIGHT = 500
FPS = 15

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
          'skils_board': (255, 255, 179)
          }

# URL
icon_image_url = "Images\\icon.png"
StartAnimationPath = "Images\\StartAnimation"
start_animation = listdir(StartAnimationPath)
sound_file_path_start = "sounds\\sound_start3.mp3"  # Шлях до вашого звукового файлу
sound_file_path_move = "sounds\\sound_move1.mp3"
font_one_url = "font//Gropled-Bold.otf"


pg.init()

#Create display
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("2048")
icon = pg.image.load(icon_image_url)
pg.display.set_icon(icon)

#Fonts
font_one = pg.font.Font( font_one_url , 24)

# Create FPS
clock = pg.time.Clock()
clock.tick(FPS)

#Game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
score = 0
high_score = 0

#Flags
run = True
running_animation = True
frame_index = 0
spawn_new = True
init_count = 0
game_over = False
direction = ''

#Main loop
while run:
  
# Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            if event.key == pg.K_UP:
                direction = 'UP'
            elif event.key == pg.K_DOWN:
                direction = 'DOWN'
            elif event.key == pg.K_LEFT:
                direction = 'LEFT'
            elif event.key == pg.K_RIGHT:
                direction = 'RIGHT'

# Start Animation
    while running_animation:
        frame_index, running_animation = run_animation(start_animation, frame_index, running_animation)
        pg.display.update()
        clock.tick(FPS)
        
    screen.fill('gray')
    draw_board()
    draw_skils_board()
    draw_pieces(board_values)

    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    
    
    # Update
    pg.display.update()

    # Оновлення FPS
    clock.tick(FPS)

pg.quit()
