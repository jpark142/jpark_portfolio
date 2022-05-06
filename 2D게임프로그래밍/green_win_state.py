import game_framework
from pico2d import *
import title_state

name = "GreenWinState"
image = None

bgm_green_win = None


def enter():
    global image, bgm_green_win
    image = load_image('res\\ending_green_win.png')
    bgm_green_win = load_music('sound\\happy_winner.wav')
    bgm_green_win.set_volume(64)
    bgm_green_win.repeat_play()


def exit():
    global image, bgm_green_win
    bgm_green_win.stop()
    del image
    del bgm_green_win



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)


def draw():
    global image
    #clear_canvas()
    image.draw(500, 300)
    update_canvas()
    pass


def update():
    pass

