from pico2d import *
from player import *
from grass import *
from background import *

from platforms import *
import game_framework
import blue_win_state
import green_win_state

name = "MainState"

bgm_main = None

def get_blue():
    return blue


def get_green():
    return green


def collide_check():
    global green, blue, grass, platforms
    if blue.collide_check is True:
        if blue.y <= grass.y + 40:
            blue.y = grass.y + 40
            if blue.vel_y < 0:
                blue.vel_y = 0
            blue.jumping = False

        if blue.x > 1000:
            blue.x = 0
        if blue.x < 0:
            blue.x = 1000

        if blue.vel_y < 0:
            if collide_p2_pf1(blue, platforms):
                blue.y = platforms.py1 + 45
                blue.vel_y = 0
                blue.jumping = False
                blue.x += platforms.dx / 2

            if collide_p2_pf2(blue, platforms):
                blue.y = platforms.py2 + 45
                blue.vel_y = 0
                blue.jumping = False

            if collide_p2_pf3(blue, platforms):
                blue.y = platforms.py3 + 45
                blue.vel_y = 0
                blue.jumping = False

            if collide_p2_pf4(blue, platforms):
                blue.y = platforms.py4 + 45
                blue.vel_y = 0
                blue.jumping = False

            if collide_p2_pf5(blue, platforms):
                blue.y = platforms.py5 + 45
                blue.vel_y = 0
                blue.jumping = False

    if green.collide_check is True:
        if green.y <= grass.y + 40:
            green.y = grass.y + 40
            if green.vel_y < 0:
                green.vel_y = 0
            green.jumping = False

        if green.x > 1000:
            green.x = 0
        if green.x < 0:
            green.x = 1000

        if green.vel_y < 0:
            if collide_p1_pf1(green, platforms):
                green.y = platforms.py1 + 45
                green.vel_y = 0
                green.jumping = False
                green.x += platforms.dx / 2

            if collide_p1_pf2(green, platforms):
                green.y = platforms.py2 + 45
                green.vel_y = 0
                green.jumping = False

            if collide_p1_pf3(green, platforms):
                green.y = platforms.py3 + 45
                green.vel_y = 0
                green.jumping = False

            if collide_p1_pf4(green, platforms):
                green.y = platforms.py4 + 45
                green.vel_y = 0
                green.jumping = False

            if collide_p1_pf5(green, platforms):
                green.y = platforms.py5 + 45
                green.vel_y = 0
                green.jumping = False


#  충돌체크 함수s -p1
def collide_p1_pf1(green, platforms):
    left_p1, bottom_p1, right_p1, top_p1 = green.get_bb_green()
    # 플랫폼1
    left_pf1, bottom_pf1, right_pf1, top_pf1 = platforms.get_bb()

    if left_p1 > right_pf1: return False
    if right_p1 < left_pf1: return False
    if top_p1 < bottom_pf1: return False
    if bottom_p1 > top_pf1: return False
    if green.is_in_bubble is True: return False  # 2021-09-07 추가(green, blue)
    return True


def collide_p1_pf2(green, platforms):
    left_p1, bottom_p1, right_p1, top_p1 = green.get_bb_green()
    # 플랫폼2
    left_pf2, bottom_pf2, right_pf2, top_pf2 = platforms.get_bb2()

    if left_p1 > right_pf2: return False
    if right_p1 < left_pf2: return False
    if top_p1 < bottom_pf2: return False
    if bottom_p1 > top_pf2: return False
    if green.is_in_bubble is True: return False
    return True


def collide_p1_pf3(green, platforms):
    left_p1, bottom_p1, right_p1, top_p1 = green.get_bb_green()
    # 플랫폼3
    left_pf3, bottom_pf3, right_pf3, top_pf3 = platforms.get_bb3()
    if left_p1 > right_pf3: return False
    if right_p1 < left_pf3: return False
    if top_p1 < bottom_pf3: return False
    if bottom_p1 > top_pf3: return False
    if green.is_in_bubble is True: return False
    return True


def collide_p1_pf4(green, platforms):
    left_p1, bottom_p1, right_p1, top_p1 = green.get_bb_green()
    # 플랫폼4
    left_pf4, bottom_pf4, right_pf4, top_pf4 = platforms.get_bb4()
    if left_p1 > right_pf4: return False
    if right_p1 < left_pf4: return False
    if top_p1 < bottom_pf4: return False
    if bottom_p1 > top_pf4: return False
    if green.is_in_bubble is True: return False
    return True


def collide_p1_pf5(green, platforms):
    left_p1, bottom_p1, right_p1, top_p1 = green.get_bb_green()
    # 플랫폼5
    left_pf5, bottom_pf5, right_pf5, top_pf5 = platforms.get_bb5()
    if left_p1 > right_pf5: return False
    if right_p1 < left_pf5: return False
    if top_p1 < bottom_pf5: return False
    if bottom_p1 > top_pf5: return False
    if green.is_in_bubble is True: return False
    return True


# 충돌체크 함수s -p2
def collide_p2_pf1(blue, platforms):
    left_p2, bottom_p2, right_p2, top_p2 = blue.get_bb_blue()
    # 플랫폼1
    left_pf1, bottom_pf1, right_pf1, top_pf1 = platforms.get_bb()

    if left_p2 > right_pf1: return False
    if right_p2 < left_pf1: return False
    if top_p2 < bottom_pf1: return False
    if bottom_p2 > top_pf1: return False
    if blue.is_in_bubble is True: return False
    return True


def collide_p2_pf2(blue, platforms):
    left_p2, bottom_p2, right_p2, top_p2 = blue.get_bb_blue()
    # 플랫폼2
    left_pf2, bottom_pf2, right_pf2, top_pf2 = platforms.get_bb2()

    if left_p2 > right_pf2: return False
    if right_p2 < left_pf2: return False
    if top_p2 < bottom_pf2: return False
    if bottom_p2 > top_pf2: return False
    if blue.is_in_bubble is True: return False
    return True


def collide_p2_pf3(blue, platforms):
    left_p2, bottom_p2, right_p2, top_p2 = blue.get_bb_blue()
    # 플랫폼3
    left_pf3, bottom_pf3, right_pf3, top_pf3 = platforms.get_bb3()
    if left_p2 > right_pf3: return False
    if right_p2 < left_pf3: return False
    if top_p2 < bottom_pf3: return False
    if bottom_p2 > top_pf3: return False
    if blue.is_in_bubble is True: return False
    return True


def collide_p2_pf4(blue, platforms):
    left_p2, bottom_p2, right_p2, top_p2 = blue.get_bb_blue()
    # 플랫폼4
    left_pf4, bottom_pf4, right_pf4, top_pf4 = platforms.get_bb4()
    if left_p2 > right_pf4: return False
    if right_p2 < left_pf4: return False
    if top_p2 < bottom_pf4: return False
    if bottom_p2 > top_pf4: return False
    if blue.is_in_bubble is True: return False
    return True


def collide_p2_pf5(blue, platforms):
    left_p2, bottom_p2, right_p2, top_p2 = blue.get_bb_blue()
    # 플랫폼5
    left_pf5, bottom_pf5, right_pf5, top_pf5 = platforms.get_bb5()
    if left_p2 > right_pf5: return False
    if right_p2 < left_pf5: return False
    if top_p2 < bottom_pf5: return False
    if bottom_p2 > top_pf5: return False
    if blue.is_in_bubble is True: return False
    return True


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            green.handle_event(event)
            blue.handle_event(event)


background = None
grass = None
green = None
blue = None
bubble = None
bubble2 = None
platforms = None

running = True


def enter():
    global green, blue, grass, background, bubble, bubble2, platforms, bgm_main
    green = Green()
    blue = Blue()
    grass = Grass()
    bubble = Bubble()
    bubble2 = Bubble2()
    background = Background()
    platforms = Platforms()

    game_world.add_object(background, 0)
    game_world.add_object(grass, 1)
    game_world.add_object(platforms, 2)
    game_world.add_object(green, 3)
    game_world.add_object(blue, 4)

    bgm_main = load_music('sound\\happy2.mp3')
    bgm_main.set_volume(64)
    bgm_main.repeat_play()


def exit():
    global bgm_main
    game_world.clear()
    bgm_main.stop()
    del bgm_main


def update():
    global green, bubble2, blue, bubble
    green.update()
    blue.update()

    if green.ingametimer > 0:
        green.cur_state = IdleState
        green.vel_x = 0
        green.vel_y = 0

        blue.cur_state = IdleState
        blue.vel_x = 0
        blue.vel_y = 0
    else:
        green.can_bubble_shot = True
        blue.can_bubble_shot = True

    for game_object in game_world.all_objects():
        game_object.update()
        collide_check()

    for b2 in game_world.bubble2_objects:  # 버블2를 가져온다
        b2.update(green)
        if is_bubble_hit_green(green, b2):
            game_world.bubble2_objects.remove(b2)

    for b1 in game_world.bubble1_objects:
        b1.update(blue)
        if is_bubble_hit_blue(blue, b1):
            game_world.bubble1_objects.remove(b1)

    if blue.ceremony_time > 40.0:
        green.ingametimer = 4  # 공용
        blue.ceremony_time = 0
        game_framework.change_state(blue_win_state)

    elif green.ceremony_time > 40.0:
        green.ingametimer = 4
        green.ceremony_time = 0
        game_framework.change_state(green_win_state)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for game_object in game_world.bubble2_objects:
        game_object.draw()
    for game_object in game_world.bubble1_objects:
        game_object.draw()

    update_canvas()



