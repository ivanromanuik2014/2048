import pygame as pg
from os import listdir, path

def run_animation(animation_frames: dict, frame_index: int, running_animation: bool) -> int:
    if running_animation:
        play_sound(sound_file_path)
        frame = pg.image.load(path.join(StartAnimationPath, animation_frames[frame_index]))
        screen.blit(frame, (-40, 40))
        frame_index += 1
        if frame_index >= len(listdir(StartAnimationPath)):
            running_animation = False  # Встановлюємо прапорець вимкнення анімації
    return frame_index, running_animation  # Повертаємо оновлений frame_index та running_animation

def play_sound(path: str) -> None:
    sound = pg.mixer.Sound(path)
    sound.play()

# draw background for the board
def draw_board() -> None:
    """
    Draws the game board and its elements on the screen.

    Args:
        screen (Surface): The surface to draw on.
        colors (dict): A dictionary of color values.
        font_one (Font): The font to use for text.
        board_values (list): A 2D list representing the game board.
        score (int): The current score.
        high_score (int): The high score.

    Returns:
        None

    """
    pg.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font_one.render(f'Рахунок: {score}', True, 'black')
    high_score_text = font_one.render(f'Найкращий рахунок: {high_score}', True, 'black')
    screen.blit(score_text, (10, 415))
    screen.blit(high_score_text, (10, 460))
    pass


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
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# URL
icon_image_url = "Images\\icon.png"
StartAnimationPath = "Images\\StartAnimation"
start_animation = listdir(StartAnimationPath)
sound_file_path = "sounds\\sound_start3.mp3"  # Шлях до вашого звукового файлу
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

#Main loop
while run:

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False

    # Start Animation
    while running_animation:
        frame_index, running_animation = run_animation(start_animation, frame_index, running_animation)
        pg.display.update()
        clock.tick(FPS)
        
    screen.fill('gray')
    draw_board()
    
    # Update
    pg.display.update()

    # Оновлення FPS
    clock.tick(FPS)

pg.quit()
