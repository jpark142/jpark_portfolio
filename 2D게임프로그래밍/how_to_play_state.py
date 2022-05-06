import game_framework
from pico2d import *
import main

name = "HowToPlay"
image = None

show_time = 0.0


def enter():
    global image
    image = load_image('res\\how_to_play.png')


def exit():
    global image
    del image
    pass


def update():
    global show_time
    if show_time > 1.0:
        show_time = 0
        game_framework.change_state(main)
    delay(0.03)
    show_time += 0.01



def handle_events():
    events = get_events()
    pass


def draw():
    global image
    clear_canvas()
    image.draw(500, 300)
    update_canvas()
    pass


