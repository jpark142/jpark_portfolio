import game_framework
from pico2d import *
import how_to_play_state

name = "TitleState"
image = None
bgm_title = None


def enter():
    global image, bgm_title
    image = load_image('res\\my_title.png')
    bgm_title = load_music('sound\\Christmas synths.ogg')
    bgm_title.set_volume(64)
    bgm_title.repeat_play()


def exit():
    global image, bgm_title

    bgm_title.stop()
    del image
    del bgm_title



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(how_to_play_state)


def draw():
    clear_canvas()
    image.draw(500, 300)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






