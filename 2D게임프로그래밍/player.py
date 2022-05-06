from pico2d import *
from bubble import *
from grass import Grass

import game_world
import game_framework
import time
import main


PLAYER_GRAVITY = -0.01

BUBBLE_SPEED = 180.0

# Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 30.0  # km / hour
RUN_SPEED_MPM = 0
RUN_SPEED_MPS = 0
RUN_SPEED_PPS = 250.0

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5
FRAMES_PER_ACTION = 32

STAND_FRAMES_PER_ACTION = 8


RIGHT_DOWN_p1, LEFT_DOWN_p1, RIGHT_UP_p1, LEFT_UP_p1, UP_UP_p1, UP_DOWN_p1, BUBBLE_SHOT_p1,\
    RIGHT_DOWN_p2, LEFT_DOWN_p2, RIGHT_UP_p2, LEFT_UP_p2, UP_UP_p2, UP_DOWN_p2, BUBBLE_SHOT_p2,\
    DOWN_DOWN_p1, DOWN_UP_p1, DOWN_DOWN_p2, DOWN_UP_p2, BUBBLE_HIT, BUBBLE_SHOT_p1_UP,\
    BUBBLE_SHOT_p2_UP = range(21)

key_event_table = {
    # 플레이어1 키 입력
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN_p1,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN_p1,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP_p1,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP_p1,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN_p1,
    (SDL_KEYUP, SDLK_UP): UP_UP_p1,
    (SDL_KEYDOWN, SDLK_RSHIFT): BUBBLE_SHOT_p1,
    (SDL_KEYUP, SDLK_RSHIFT): BUBBLE_SHOT_p1_UP,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN_p1,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP_p1
}
key_event_table2 = {
    # 플레이어2 키 입력
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN_p2,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN_p2,
    (SDL_KEYUP, SDLK_d): RIGHT_UP_p2,
    (SDL_KEYUP, SDLK_a): LEFT_UP_p2,
    (SDL_KEYDOWN, SDLK_w): UP_DOWN_p2,
    (SDL_KEYUP, SDLK_w): UP_UP_p2,
    (SDL_KEYDOWN, SDLK_LSHIFT): BUBBLE_SHOT_p2,
    (SDL_KEYUP, SDLK_LSHIFT): BUBBLE_SHOT_p2_UP,
    (SDL_KEYDOWN, SDLK_s): DOWN_DOWN_p2,
    (SDL_KEYUP, SDLK_s): DOWN_UP_p2
}


class IdleState:
    @staticmethod
    def enter_p1(green, event):
        green.isShot = False
        green.is_in_bubble = False

        # 플레이어1
        if event == RIGHT_DOWN_p1:
            green.vel_x += green.run_speed
            green.dir = 1
            green.cur_state = RunState

        elif event == LEFT_DOWN_p1:
            green.vel_x -= green.run_speed
            green.dir = -1
            green.cur_state = RunState

        elif event == RIGHT_UP_p1:
            green.vel_x -= green.run_speed

            green.cur_state = IdleState

        elif event == LEFT_UP_p1:
            green.vel_x += green.run_speed

            green.cur_state = IdleState

        elif event == UP_DOWN_p1 and green.jumping is False:
            green.vel_y = 2
            green.jumping = True
            green.jump_sound.play()

        elif event == UP_UP_p1:
            green.jumping = True

        elif event == DOWN_DOWN_p1:
            pass
        elif event == DOWN_UP_p1:
            pass

    @staticmethod
    def enter_p2(blue, event2):
        blue.isShot = False
        blue.is_in_bubble = False

        if event2 == RIGHT_DOWN_p2:
            blue.vel_x += blue.run_speed
            blue.dir = 1

            blue.cur_state = RunState

        elif event2 == LEFT_DOWN_p2:
            blue.vel_x -= blue.run_speed
            blue.dir = -1

            blue.cur_state = RunState

        elif event2 == RIGHT_UP_p2:
            blue.vel_x -= blue.run_speed
            blue.cur_state = IdleState

        elif event2 == LEFT_UP_p2:
            blue.vel_x += blue.run_speed
            blue.cur_state = IdleState

        elif event2 == UP_DOWN_p2 and blue.jumping is False:
            blue.vel_y = 2
            blue.jumping = True
            blue.jump_sound.play()

        elif event2 == UP_UP_p2:
            blue.jumping = True

        elif event2 == DOWN_DOWN_p2:
            pass
        elif event2 == DOWN_UP_p2:
            pass



    @staticmethod
    def exit_p1(green, event):
        if event == BUBBLE_SHOT_p1:
            green.bubble_shot()

    @staticmethod
    def exit_p2(blue, event2):
        if event2 == BUBBLE_SHOT_p2:
            blue.bubble_shot()

    @staticmethod
    def do_p1(green):
        print(green.vel_x, "idlestate")

        green.timer = 10

        # 플레이어1
        green.frame1 = (green.frame1 + STAND_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        green.x += green.vel_x * game_framework.frame_time
        green.y += green.vel_y
        green.vel_y += green.acc_y

        if green.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            green.add_event(BUBBLE_HIT)
            green.isHit = False
            green.is_in_bubble = True

    @staticmethod
    def do_p2(blue):
        blue.timer = 10

        # 플레이어2
        blue.frame2 = (blue.frame2 + STAND_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        blue.x += blue.vel_x * game_framework.frame_time
        blue.y += blue.vel_y
        blue.vel_y += blue.acc_y

        if blue.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            blue.add_event(BUBBLE_HIT)
            blue.isHit = False
            blue.is_in_bubble = True

    @staticmethod
    def draw_p1(green):
        # 플레이어1
        if green.vel_x == 0 and green.dir == -1:  # 왼쪽보고 가만히 있기

            green.sheet_line = 180
        elif green.vel_x == 0 and green.dir == 1:  # 오른쪽보고 가만히 있기

            green.sheet_line = 120
        elif green.vel_y >= 0 and green.dir == 1:
            green.sheet_line = 120
        elif green.vel_y >= 0 and green.dir == -1:
            green.sheet_line = 180

        elif green.isShot is True:
            green.attack.clip_draw(0, 0, 60, 60, green.x, green.y)
            green.isShot = False

    @staticmethod
    def draw_p2(blue):
        # 플레이어2
        if blue.dir == 1:  # 오른쪽보고 가만히 있기
            blue.sheet_line = 120

        elif blue.dir == -1:  # 왼쪽보고 가만히 있기
            blue.sheet_line = 180


class RunState:
    @staticmethod
    def enter_p1(green, event):

        green.isShot = False
        green.is_in_bubble = False

        if event == RIGHT_DOWN_p1:
            green.vel_x += green.run_speed
            green.dir = 1

        elif event == LEFT_DOWN_p1:
            green.vel_x -= green.run_speed
            green.dir = -1

        elif event == RIGHT_UP_p1:
            if green.x == 950:
                green.cur_state = IdleState
            else:
                green.vel_x -= green.run_speed
                green.dir = -1
                if green.vel_x != 0:
                    green.vel_x = 0
                    green.cur_state = RunState

        elif event == LEFT_UP_p1:
            if green.x == 950:
                green.cur_state = IdleState
            else:
                green.vel_x += green.run_speed
                green.dir = 1
                if green.vel_x != 0:
                    green.vel_x = 0
                    green.cur_state = RunState

        elif event == UP_DOWN_p1 and green.jumping is False:
            green.vel_y = 2
            green.jumping = True
            green.jump_sound.play()

        elif event == UP_UP_p1:
            # 다시 시작 에러 수정2(2021-09-18)
            if green.x == 950:
                green.cur_state = IdleState
            green.jumping = True

        elif event == DOWN_DOWN_p1:
            pass
        elif event == DOWN_UP_p1:
            pass


    @staticmethod
    def enter_p2(blue, event2):
        blue.isShot = False
        blue.is_in_bubble = False

        # 플레이어2
        if event2 == RIGHT_DOWN_p2:
            blue.vel_x += blue.run_speed
            blue.dir = 1
        elif event2 == LEFT_DOWN_p2:
            blue.vel_x -= blue.run_speed
            blue.dir = -1

        elif event2 == RIGHT_UP_p2:
            # 다시 시작 에러 수정(2021-09-18)
            if blue.x == 50:
                blue.cur_state = IdleState
            else:
                blue.vel_x -= blue.run_speed
                blue.dir = -1
                if blue.vel_x != 0:
                    blue.vel_x = 0
                    blue.cur_state = RunState

        elif event2 == LEFT_UP_p2:
            # 다시 시작 에러 수정(2021-09-18)
            if blue.x == 50:
                blue.cur_state = IdleState
            else:
                blue.vel_x += blue.run_speed
                blue.dir = 1
                if blue.vel_x != 0:
                    blue.vel_x = 0
                    blue.cur_state = RunState

        elif event2 == UP_DOWN_p2 and blue.jumping is False:
            blue.vel_y = 2
            blue.jumping = True
            blue.jump_sound.play()

        elif event2 == UP_UP_p2:
            blue.jumping = True

        elif event2 == DOWN_DOWN_p2:
            pass
        elif event2 == DOWN_UP_p2:
            pass


    @staticmethod
    def exit_p1(green, event):
        if event == BUBBLE_SHOT_p1:
            green.bubble_shot()


    @staticmethod
    def exit_p2(blue, event2):
        if event2 == BUBBLE_SHOT_p2:
            blue.bubble_shot()

    @staticmethod
    def do_p1(green):
        print(green.vel_x, "runstate")
        green.timer = 10

        # 플레이어1
        green.frame1 = (green.frame1 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        green.x += green.vel_x * game_framework.frame_time
        green.y += green.vel_y
        green.vel_y += green.acc_y
        if green.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            green.add_event(BUBBLE_HIT)

            green.is_in_bubble = True
            # 수정(2021-09-17)
            if green.vel_x < 0:
                green.vel_x += 70
            elif green.vel_x > 0:
                green.vel_x -= 70

    @staticmethod
    def do_p2(blue):
        blue.timer = 10

        # 플레이어2
        blue.frame2 = (blue.frame2 + + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        blue.x += blue.vel_x * game_framework.frame_time
        blue.y += blue.vel_y
        blue.vel_y += blue.acc_y
        if blue.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            blue.add_event(BUBBLE_HIT)

            blue.is_in_bubble = True
            # 수정(2021-09-17)
            if blue.vel_x < 0:
                blue.vel_x += 70
            elif blue.vel_x > 0:
                blue.vel_x -= 70

    @staticmethod
    def draw_p1(green):
        # 플레이어1
        if green.vel_x == 0 and green.dir == -1:  # 왼쪽보고 가만히 있기

            green.sheet_line = 180
        elif green.vel_x == 0 and green.dir == 1:  # 오른쪽보고 가만히 있기
            green.sheet_line = 120

        if green.vel_x > 0:

            green.sheet_line = 0
        elif green.vel_x < 0:

            green.sheet_line = 60

        if green.isShot is True:
            green.attack.clip_draw(0, 0, 60, 60, green.x, green.y)
            green.isShot = False

    @staticmethod
    def draw_p2(blue):
        # 플레이어2
        if blue.vel_x > 0:
            blue.sheet_line = 0

        elif blue.vel_x < 0:
            blue.sheet_line = 60

        if blue.vel_x == 0 and blue.dir == 1:  # 오른쪽보고 가만히 있기
            blue.sheet_line = 120

        elif blue.vel_x == 0 and blue.dir == -1:  # 왼쪽보고 가만히 있기
            blue.sheet_line = 180


class InBubbleState:

    @staticmethod
    def enter_p1(green, event):
        # 플레이어1
        if event == RIGHT_DOWN_p1:
            green.vel_x += green.bubble_speed

        elif event == LEFT_DOWN_p1:
            green.vel_x -= green.bubble_speed

        elif event == RIGHT_UP_p1:
            green.vel_x -= green.bubble_speed

        elif event == LEFT_UP_p1:
            green.vel_x += green.bubble_speed

        green.acc_y = 0  # 중력은 없애준다

        # 위아래
        if event == DOWN_DOWN_p1:
            green.vel_y = PLAYER_GRAVITY
            green.vel_y -= 0.5
        elif event == DOWN_UP_p1:
            green.vel_y = PLAYER_GRAVITY

        elif event == UP_DOWN_p1:
            green.vel_y = PLAYER_GRAVITY

            green.vel_y += 0.5

        elif event == UP_UP_p1:
            green.vel_y = PLAYER_GRAVITY

        elif event == BUBBLE_SHOT_p1:
            pass
        elif event == BUBBLE_SHOT_p1_UP:
            pass

        green.frame1 = 0

    @staticmethod
    def enter_p2(blue, event):
        # 플레이어2
        if event == RIGHT_DOWN_p2:
            blue.vel_x += blue.bubble_speed

        elif event == LEFT_DOWN_p2:
            blue.vel_x -= blue.bubble_speed

        elif event == RIGHT_UP_p2:
            blue.vel_x -= blue.bubble_speed

        elif event == LEFT_UP_p2:
            blue.vel_x += blue.bubble_speed

        blue.acc_y = 0  # 중력은 없애준다

        # 위아래
        if event == DOWN_DOWN_p2:
            blue.vel_y = PLAYER_GRAVITY
            blue.vel_y -= 0.5
        elif event == DOWN_UP_p2:
            blue.vel_y = PLAYER_GRAVITY
            # player1.vel_y += 0.5
        elif event == UP_DOWN_p2:
            blue.vel_y = PLAYER_GRAVITY

            blue.vel_y += 0.5

        elif event == UP_UP_p2:
            blue.vel_y = PLAYER_GRAVITY
            # player1.vel_y -= 0.5

        elif event == BUBBLE_SHOT_p2:
            pass
        elif event == BUBBLE_SHOT_p2_UP:
            pass

    @staticmethod
    def exit_p1(green, event):

        pass

    @staticmethod
    def exit_p2(blue, event):

        pass

    @staticmethod
    def do_p1(green):

        green.isHit = False
        # 플레이어1
        green.frame1 = (green.frame1 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        green.timer -= 1.5/1000
        #print(green.vel_x, "inbubblestate")
        #print(green.timer)

        if green.timer < 0:  # 만약에 일정 시간이 다 되면

            green.acc_y = PLAYER_GRAVITY
            if green.vel_x != 0.0 or green.vel_y != 0.0:
                # 수정(2021-09-17)
                if green.vel_x < 0:
                    green.vel_x -= 70
                elif green.vel_x > 0:
                    green.vel_x += 70

                green.cur_state = RunState  # 물방울에서 빠져나온다. -> RunState

            if green.vel_x == 0.0 and green.vel_y == 0.0:

                green.cur_state = IdleState  # 물방울에서 빠져나온다. -> IdleState

            elif green.vel_x != 0.0 and green.vel_y > 0.0:  # 어쩔 수가 없음(보류)

                green.cur_state = IdleState
            elif green.vel_x == 0.0 and green.vel_y < 0.0:

                green.cur_state = IdleState

        blue = main.get_blue()
        if blue.is_in_bubble is False and green.is_in_bubble is True:
            if final_collide(green, blue):
                # 수정(2021-09-18)
                green.run_speed = 0
                green.bubble_speed = 0
                blue.run_speed = 0
                blue.bubble_speed = 0
                green.explosion_sound.play()
                green.cur_state = GreenDefeatState
                blue.cur_state = GreenDefeatState
                print("Blue Win!!")
                blue.win = True
                green.defeat = True

        green.x += green.vel_x * game_framework.frame_time
        green.y += green.vel_y
        green.vel_y += green.acc_y

        if green.y > 550:
            green.y = 550

    @staticmethod
    def do_p2(blue):
        blue.isHit = False

        # 플레이어2
        blue.frame2 = (blue.frame2 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        blue.timer -= 1.5/1000

        print(blue.timer)

        if blue.timer < 0:  # 만약에 일정 시간이 다 되면
            blue.acc_y = PLAYER_GRAVITY
            print(blue.vel_x)
            if blue.vel_x != 0.0 or blue.vel_y != 0.0:
                if blue.vel_x < 0:
                    blue.vel_x -= 70
                elif blue.vel_x > 0:
                    blue.vel_x += 70
                blue.cur_state = RunState  # 물방울에서 빠져나온다. -> RunState
            if blue.vel_x == 0.0 and blue.vel_y == 0.0:
                blue.cur_state = IdleState  # 물방울에서 빠져나온다. -> IdleState
            elif blue.vel_x != 0.0 and blue.vel_y > 0.0:
                blue.cur_state = IdleState
            elif blue.vel_x == 0.0 and blue.vel_y < 0.0:
                blue.cur_state = IdleState

        green = main.get_green()

        if green.is_in_bubble is False and blue.is_in_bubble is True:
            if final_collide(green, blue):
                green.run_speed = 0
                green.bubble_speed = 0
                blue.run_speed = 0
                blue.bubble_speed = 0

                blue.explosion_sound.play()
                blue.cur_state = BlueDefeatState
                green.cur_state = BlueDefeatState
                print("Green Win!!")
                green.win = True
                blue.defeat = True

        blue.x += blue.vel_x * game_framework.frame_time
        blue.y += blue.vel_y
        blue.vel_y += blue.acc_y

        if blue.y > 550:
            blue.y = 550

    @staticmethod
    def draw_p1(green):
        green.in_bubble.clip_draw(int(green.frame1) * 80, 80, 80, 80, green.x, green.y)
        if 10 > green.timer > 6:
            green.font.draw(green.x - 45, green.y + 50, '(Time: %3.2f)' % green.timer, (0, 255, 0))
        elif 6 > green.timer > 3:
            green.font.draw(green.x - 45, green.y + 50, '(Time: %3.2f)' % green.timer, (255, 255, 0))
        else:
            green.font.draw(green.x - 45, green.y + 50, '(Time: %3.2f)' % green.timer, (255, 0, 0))

    @staticmethod
    def draw_p2(blue):
        blue.in_bubble.clip_draw(int(blue.frame2) * 80, 0, 80, 80, blue.x, blue.y)
        if 10 > blue.timer > 6:
            blue.font.draw(blue.x - 45, blue.y + 50, '(Time: %3.2f)' % blue.timer, (0, 255, 0))
        elif 6 > blue.timer > 3:
            blue.font.draw(blue.x - 45, blue.y + 50, '(Time: %3.2f)' % blue.timer, (255, 255, 0))
        else:
            blue.font.draw(blue.x - 45, blue.y + 50, '(Time: %3.2f)' % blue.timer, (255, 0, 0))


class GreenDefeatState:
    @staticmethod
    def enter_p1(green, event):

        print("Game Over..")
        pass

    @staticmethod
    def enter_p2(blue, event):
        pass

    @staticmethod
    def exit_p1(green, event):
        pass

    @staticmethod
    def exit_p2(blue, event):
        pass

    @staticmethod
    def do_p1(green):

        green.frame1 = (green.frame1 + 5 * ACTION_PER_TIME * game_framework.frame_time) % 6
        green.y -= 0.2
        green.collide_check = False

    @staticmethod
    def do_p2(blue):

        blue.frame2 = (blue.frame2 + 5 * ACTION_PER_TIME * game_framework.frame_time) % 12
        blue.y -= 0.1

        blue.ceremony_time += 0.01

    @staticmethod
    def draw_p1(green):
        green.die.clip_draw(int(green.frame1)*60, 60, 60, 60, green.x, green.y)
        pass

    @staticmethod
    def draw_p2(blue):
        blue.win_ceremony.clip_draw(int(blue.frame2)*60, 0, 60, 60, blue.x, blue.y)
        blue.font.draw(blue.x - 40, blue.y + 40, 'Oh Yeah!^-^', (0, 255, 255))


class BlueDefeatState:
    @staticmethod
    def enter_p1(green, event):

        pass

    @staticmethod
    def enter_p2(blue, event):

        print("Game Over..")
        pass

    @staticmethod
    def exit_p1(green, event):

        pass

    @staticmethod
    def exit_p2(blue, event):
        pass

    @staticmethod
    def do_p1(green):
        green.frame1 = (green.frame1 + 5 * ACTION_PER_TIME * game_framework.frame_time) % 12
        green.y -= 0.1
        green.ceremony_time += 0.01

    @staticmethod
    def do_p2(blue):
        blue.frame2 = (blue.frame2 + 5 * ACTION_PER_TIME * game_framework.frame_time) % 6
        blue.y -= 0.2
        blue.collide_check = False

    @staticmethod
    def draw_p1(green):
        green.win_ceremony.clip_draw(int(green.frame1) * 60, 0, 60, 60, green.x, green.y)
        green.font.draw(green.x - 30, green.y + 40, 'So E...Z...', (0, 255, 0))

    @staticmethod
    def draw_p2(blue):
        blue.die.clip_draw(int(blue.frame2) * 60, 0, 60, 60, blue.x, blue.y)


class GreenAttackIdleState:
    @staticmethod
    def enter_p1(green, event):
        green.isShot = True
        if event == RIGHT_DOWN_p1:
            green.vel_x += green.run_speed
            green.dir = 1
            green.cur_state = RunState

        elif event == LEFT_DOWN_p1:
            green.vel_x -= green.run_speed
            green.dir = -1
            green.cur_state = RunState

        elif event == RIGHT_UP_p1:
            green.vel_x -= green.run_speed
            green.dir = -1
            green.cur_state = IdleState

        elif event == LEFT_UP_p1:
            green.vel_x += green.run_speed
            green.dir = 1
            green.cur_state = IdleState


        elif event == UP_DOWN_p1 and green.jumping is False:
            green.vel_y = 2
            green.jumping = True

        elif event == UP_UP_p1:
            green.jumping = True

        elif event == DOWN_DOWN_p1:
            pass
        elif event == DOWN_UP_p1:
            pass

        elif event == BUBBLE_SHOT_p1:
            pass
        elif event == BUBBLE_SHOT_p1_UP:
            pass

    @staticmethod
    def exit_p1(green, event):
        pass

    @staticmethod
    def do_p1(green):
        green.frame1 = (green.frame1 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        green.x += green.vel_x * game_framework.frame_time
        green.y += green.vel_y
        green.vel_y += green.acc_y

        if green.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            green.add_event(BUBBLE_HIT)
            green.isHit = False
            green.is_in_bubble = True
        pass

    @staticmethod
    def draw_p1(green):
        if green.dir == 1:
            green.attack.clip_draw(int(green.frame1) * 60, 0, 60, 60, green.x, green.y)
        elif green.dir == -1:
            green.attack.clip_draw(int(green.frame1) * 60, 60, 60, 60, green.x, green.y)

        pass


class GreenAttackRunState:
    @staticmethod
    def enter_p1(green, event):
        green.isShot = True
        if event == RIGHT_DOWN_p1:
            green.vel_x += green.run_speed
            green.dir = 1
        elif event == LEFT_DOWN_p1:
            green.vel_x -= green.run_speed
            green.dir = -1
        elif event == RIGHT_UP_p1:
            # 다시 시작 에러 수정(2021-09-18)
            if green.x == 950:
                green.cur_state = IdleState
            else:
                green.vel_x -= green.run_speed
                green.dir = -1

                if green.vel_x != 0:
                    green.vel_x = 0
                    green.cur_state = RunState

        elif event == LEFT_UP_p1:
            # 다시 시작 에러 수정(2021-09-18)
            if green.x == 950:
                green.cur_state = IdleState
            else:
                green.vel_x += green.run_speed
                green.dir = 1

                if green.vel_x != 0:
                    green.vel_x = 0
                    green.cur_state = RunState

        elif event == UP_DOWN_p1 and green.jumping is False:
            green.vel_y = 2
            green.jumping = True

        elif event == UP_UP_p1:
            green.jumping = True

        elif event == DOWN_DOWN_p1:
            pass
        elif event == DOWN_UP_p1:
            pass

        elif event == BUBBLE_SHOT_p1:
            pass
        elif event == BUBBLE_SHOT_p1_UP:
            pass

    @staticmethod
    def exit_p1(green, event):
        pass

    @staticmethod
    def do_p1(green):
        green.frame1 = (green.frame1 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        green.x += green.vel_x * game_framework.frame_time
        green.y += green.vel_y
        green.vel_y += green.acc_y

        if green.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            green.add_event(BUBBLE_HIT)
            green.isHit = False
            green.is_in_bubble = True
            # 수정(2021-09-17)
            if green.vel_x < 0:
                green.vel_x += 70
            elif green.vel_x > 0:
                green.vel_x -= 70

    @staticmethod
    def draw_p1(green):
        if green.dir == 1:
            green.attack.clip_draw(int(green.frame1) * 60, 0, 60, 60, green.x, green.y)
        elif green.dir == -1:
            green.attack.clip_draw(int(green.frame1) * 60, 60, 60, 60, green.x, green.y)


class BlueAttackIdleState:
    @staticmethod
    def enter_p2(blue, event):
        blue.isShot = True
        if event == RIGHT_DOWN_p2:
            blue.vel_x += blue.run_speed
            blue.dir = 1
            blue.cur_state = RunState
        elif event == LEFT_DOWN_p2:
            blue.vel_x -= blue.run_speed
            blue.dir = -1
            blue.cur_state = RunState

        elif event == RIGHT_UP_p2:
            blue.vel_x -= blue.run_speed
            blue.dir = -1
            blue.cur_state = IdleState

        elif event == LEFT_UP_p2:
            blue.vel_x += blue.run_speed
            blue.dir = 1
            blue.cur_state = IdleState

        elif event == UP_DOWN_p2 and blue.jumping is False:
            blue.vel_y = 2
            blue.jumping = True

        elif event == UP_UP_p2:
            blue.jumping = True

        elif event == DOWN_DOWN_p2:
            pass
        elif event == DOWN_UP_p2:
            pass

        elif event == BUBBLE_SHOT_p2:
            pass
        elif event == BUBBLE_SHOT_p2_UP:
            pass

    @staticmethod
    def exit_p2(blue, event):
        pass

    @staticmethod
    def do_p2(blue):
        blue.frame2 = (blue.frame2 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        blue.x += blue.vel_x * game_framework.frame_time
        blue.y += blue.vel_y
        blue.vel_y += blue.acc_y

        if blue.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            blue.add_event(BUBBLE_HIT)
            blue.isHit = False
            blue.is_in_bubble = True

    @staticmethod
    def draw_p2(blue):
        if blue.dir == 1:
            blue.attack.clip_draw(int(blue.frame2) * 60, 0, 60, 60, blue.x, blue.y)
        elif blue.dir == -1:
            blue.attack.clip_draw(int(blue.frame2) * 60, 60, 60, 60, blue.x, blue.y)


class BlueAttackRunState:
    @staticmethod
    def enter_p2(blue, event):
        blue.isShot = True
        if event == RIGHT_DOWN_p2:
            blue.vel_x += blue.run_speed
            blue.dir = 1
        elif event == LEFT_DOWN_p2:
            blue.vel_x -= blue.run_speed
            blue.dir = -1
        elif event == RIGHT_UP_p2:
            # 다시 시작 에러 수정(2021-09-18)
            if blue.x == 50:
                blue.cur_state = IdleState
            else:
                blue.vel_x -= blue.run_speed
                blue.dir = -1
                if blue.vel_x != 0:
                    blue.vel_x = 0
                    blue.cur_state = RunState

        elif event == LEFT_UP_p2:
            # 다시 시작 에러 수정(2021-09-18)
            if blue.x == 50:
                blue.cur_state = IdleState
            else:
                blue.vel_x += blue.run_speed
                blue.dir = 1
                if blue.vel_x != 0:
                    blue.vel_x = 0
                    blue.cur_state = RunState

        elif event == UP_DOWN_p2 and blue.jumping is False:
            blue.vel_y = 2
            blue.jumping = True

        elif event == UP_UP_p2:
            blue.jumping = True

        elif event == DOWN_DOWN_p2:
            pass
        elif event == DOWN_UP_p2:
            pass

        elif event == BUBBLE_SHOT_p2:
            pass
        elif event == BUBBLE_SHOT_p2_UP:
            pass

    @staticmethod
    def exit_p2(blue, event):
        pass

    @staticmethod
    def do_p2(blue):
        blue.frame2 = (blue.frame2 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        blue.x += blue.vel_x * game_framework.frame_time
        blue.y += blue.vel_y
        blue.vel_y += blue.acc_y

        if blue.isHit is True:
            print("inBubbleState 상태로 바뀌었습니다.")
            blue.add_event(BUBBLE_HIT)
            blue.isHit = False
            blue.is_in_bubble = True
            # 수정(2021-09-17)
            if blue.vel_x < 0:
                blue.vel_x += 70
            elif blue.vel_x > 0:
                blue.vel_x -= 70

    @staticmethod
    def draw_p2(blue):
        if blue.dir == 1:
            blue.attack.clip_draw(int(blue.frame1) * 60, 0, 60, 60, blue.x, blue.y)
        elif blue.dir == -1:
            blue.attack.clip_draw(int(blue.frame1) * 60, 60, 60, 60, blue.x, blue.y)


def final_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb_green()
    left_b, bottom_b, right_b, top_b = b.get_bb_blue()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


next_state_table = {
    IdleState: {RIGHT_UP_p1: RunState, LEFT_UP_p1: RunState,
                RIGHT_DOWN_p1: RunState, LEFT_DOWN_p1: RunState,
                UP_UP_p1: RunState, UP_DOWN_p1: RunState,
                BUBBLE_SHOT_p1: GreenAttackIdleState,
                BUBBLE_SHOT_p1_UP: IdleState,
                BUBBLE_HIT: InBubbleState,
                DOWN_UP_p1: IdleState, DOWN_DOWN_p1: IdleState},
    RunState: {RIGHT_UP_p1: IdleState, LEFT_UP_p1: IdleState,
               LEFT_DOWN_p1: IdleState, RIGHT_DOWN_p1: IdleState,
               UP_UP_p1: IdleState, UP_DOWN_p1: IdleState,
               BUBBLE_SHOT_p1: GreenAttackRunState,
               BUBBLE_SHOT_p1_UP: RunState,
               BUBBLE_HIT: InBubbleState,
               DOWN_UP_p1: RunState, DOWN_DOWN_p1: RunState},
    InBubbleState: {RIGHT_UP_p1: InBubbleState, LEFT_UP_p1: InBubbleState,
                    LEFT_DOWN_p1: InBubbleState, RIGHT_DOWN_p1: InBubbleState,
                    UP_UP_p1: InBubbleState, UP_DOWN_p1: InBubbleState,
                    DOWN_UP_p1: InBubbleState, DOWN_DOWN_p1: InBubbleState,
                    BUBBLE_SHOT_p1: InBubbleState,
                    BUBBLE_SHOT_p1_UP: InBubbleState},
    GreenDefeatState: {RIGHT_UP_p1: GreenDefeatState, LEFT_UP_p1: GreenDefeatState,
                       LEFT_DOWN_p1: GreenDefeatState, RIGHT_DOWN_p1: GreenDefeatState,
                       UP_UP_p1: GreenDefeatState, UP_DOWN_p1: GreenDefeatState,
                       DOWN_UP_p1: GreenDefeatState, DOWN_DOWN_p1: GreenDefeatState,
                       BUBBLE_SHOT_p1: GreenDefeatState,
                       BUBBLE_SHOT_p1_UP: GreenDefeatState},
    BlueDefeatState: {RIGHT_UP_p1: BlueDefeatState, LEFT_UP_p1: BlueDefeatState,
                      LEFT_DOWN_p1: BlueDefeatState, RIGHT_DOWN_p1: BlueDefeatState,
                      UP_UP_p1: BlueDefeatState, UP_DOWN_p1: BlueDefeatState,
                      DOWN_UP_p1: BlueDefeatState, DOWN_DOWN_p1: BlueDefeatState,
                      BUBBLE_SHOT_p1: BlueDefeatState,
                      BUBBLE_SHOT_p1_UP: BlueDefeatState},
    GreenAttackIdleState: {BUBBLE_SHOT_p1_UP: IdleState,
                           RIGHT_UP_p1: RunState, LEFT_UP_p1: RunState,
                           LEFT_DOWN_p1: RunState, RIGHT_DOWN_p1: RunState,
                           UP_UP_p1: RunState, UP_DOWN_p1: RunState,
                           DOWN_UP_p1: GreenAttackIdleState, DOWN_DOWN_p1: GreenAttackIdleState,
                           BUBBLE_SHOT_p1: GreenAttackIdleState,
                           BUBBLE_HIT: InBubbleState},
    GreenAttackRunState: {BUBBLE_SHOT_p1_UP: RunState,
                          RIGHT_UP_p1: IdleState, LEFT_UP_p1: IdleState,
                          LEFT_DOWN_p1: IdleState, RIGHT_DOWN_p1: IdleState,
                          UP_UP_p1: IdleState, UP_DOWN_p1: IdleState,
                          DOWN_UP_p1: GreenAttackRunState, DOWN_DOWN_p1: GreenAttackRunState,
                          BUBBLE_SHOT_p1: GreenAttackRunState,
                          BUBBLE_HIT: InBubbleState}
}
next_state_table2 = {
    IdleState: {
        RIGHT_UP_p2: RunState, LEFT_UP_p2: RunState,
        RIGHT_DOWN_p2: RunState, LEFT_DOWN_p2: RunState,
        UP_UP_p2: RunState, UP_DOWN_p2: RunState,
        BUBBLE_SHOT_p2: BlueAttackIdleState,
        BUBBLE_SHOT_p2_UP: IdleState,
        BUBBLE_HIT: InBubbleState,
        DOWN_UP_p2: IdleState, DOWN_DOWN_p2: IdleState},
    RunState: {
        RIGHT_UP_p2: IdleState, LEFT_UP_p2: IdleState,
        LEFT_DOWN_p2: IdleState, RIGHT_DOWN_p2: IdleState,
        UP_UP_p2: IdleState, UP_DOWN_p2: IdleState,
        BUBBLE_SHOT_p2: RunState,
        BUBBLE_SHOT_p2_UP: RunState,
        BUBBLE_HIT: InBubbleState,
        DOWN_UP_p2: RunState, DOWN_DOWN_p2: RunState},
    InBubbleState: {RIGHT_UP_p2: InBubbleState, LEFT_UP_p2: InBubbleState,
                    LEFT_DOWN_p2: InBubbleState, RIGHT_DOWN_p2: InBubbleState,
                    UP_UP_p2: InBubbleState, UP_DOWN_p2: InBubbleState,
                    DOWN_UP_p2: InBubbleState, DOWN_DOWN_p2: InBubbleState,
                    BUBBLE_SHOT_p2: InBubbleState,
                    BUBBLE_SHOT_p2_UP: InBubbleState},
    GreenDefeatState: {RIGHT_UP_p2: GreenDefeatState, LEFT_UP_p2: GreenDefeatState,
                       LEFT_DOWN_p2: GreenDefeatState, RIGHT_DOWN_p2: GreenDefeatState,
                       UP_UP_p2: GreenDefeatState, UP_DOWN_p2: GreenDefeatState,
                       DOWN_UP_p2: GreenDefeatState, DOWN_DOWN_p2: GreenDefeatState,
                       BUBBLE_SHOT_p2: GreenDefeatState,
                       BUBBLE_SHOT_p2_UP: GreenDefeatState},
    BlueDefeatState: {RIGHT_UP_p2: BlueDefeatState, LEFT_UP_p2: BlueDefeatState,
                      LEFT_DOWN_p2: BlueDefeatState, RIGHT_DOWN_p2: BlueDefeatState,
                      UP_UP_p2: BlueDefeatState, UP_DOWN_p2: BlueDefeatState,
                      DOWN_UP_p2: BlueDefeatState, DOWN_DOWN_p2: BlueDefeatState,
                      BUBBLE_SHOT_p2: BlueDefeatState,
                      BUBBLE_SHOT_p2_UP: BlueDefeatState},
    BlueAttackIdleState: {BUBBLE_SHOT_p2_UP: IdleState,
                          RIGHT_UP_p2: RunState, LEFT_UP_p2: RunState,
                          LEFT_DOWN_p2: RunState, RIGHT_DOWN_p2: RunState,
                          UP_UP_p2: RunState, UP_DOWN_p2: RunState,
                          DOWN_UP_p2: BlueAttackIdleState, DOWN_DOWN_p2: BlueAttackIdleState,
                          BUBBLE_SHOT_p2: BlueAttackIdleState,
                          BUBBLE_HIT: InBubbleState},
    BlueAttackRunState: {BUBBLE_SHOT_p2_UP: RunState,
                         RIGHT_UP_p2: IdleState, LEFT_UP_p2: IdleState,
                         LEFT_DOWN_p2: IdleState, RIGHT_DOWN_p2: IdleState,
                         UP_UP_p2: IdleState, UP_DOWN_p2: IdleState,
                         DOWN_UP_p2: BlueAttackRunState, DOWN_DOWN_p2: BlueAttackRunState,
                         BUBBLE_SHOT_p2: BlueAttackRunState,
                         BUBBLE_HIT: InBubbleState}
}

class Green:
    def __init__(self):
        self.x, self.y = (950, 600 / 2)
        self.vel_x, self.vel_y = 0, 0
        self.bubble_vel_x = 0
        self.acc_x, self.acc_y = 0, PLAYER_GRAVITY
        self.dy = 0
        self.frame1 = 0
        self.image = load_image('res\\character.png')
        self.attack = load_image('res\\attack_p1.png')
        self.in_bubble = load_image('res\\in_bubble.png')
        self.win_ceremony = load_image('res\\green_win_ceremony.png')
        self.die = load_image('res\\die.png')
        self.font = load_font('test.ttf', 16)

        self.timer = 10
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter_p1(self, None)
        self.dir = -1
        self.jumping = False
        self.sheet_line = 180
        self.isShot = False  # 물방울을 발사 했냐
        self.isHit = False  # 물발울에 맞았냐
        self.collide_check = True
        self.win = False
        self.defeat = False
        self.ceremony_time = 0.0
        self.is_in_bubble = False

        self.shot_sound = load_wav('sound\\bubble.wav')
        self.shot_sound.set_volume(32)
        self.jump_sound = load_wav('sound\\jump.wav')
        self.jump_sound.set_volume(32)
        self.explosion_sound = load_wav('sound\\ddukbaegi.wav')
        self.explosion_sound.set_volume(54)

        self.run_speed = 250
        self.bubble_speed = 180
        self.can_bubble_shot = False
        #self.can_move = False

        # 공용
        self.ingametimer = 4
        self.font_timer = load_font('test.ttf', 50)


    def bubble_shot(self):
        if self.can_bubble_shot is True:
            bubble = Bubble(self.x, self.y, self.dir * 3)
            grass = Grass()  # grass 객체를 가져옴

            game_world.bubble1_objects.append(bubble)

            if bubble.y <= grass.y + 40:  # 물방울이 중력때문에 화면 밖으로 내려가지 않게 함
                bubble.y = grass.y + 40

            self.shot_sound.play()  # 물방울 발사 이펙트 사운드

    def add_event(self, event):
        self.event_que.insert(0, event)


    def update(self):
        self.ingametimer -= 1/1000
        self.cur_state.do_p1(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit_p1(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter_p1(self, event)

    def draw(self):

        if self.defeat is False and self.win is False and self.isShot is False:
            self.image.clip_draw(int(self.frame1) * 60, self.sheet_line, 60, 60, self.x, self.y)
        self.cur_state.draw_p1(self)

        # 시작 전 타이머 그리기
        if self.ingametimer > 0:
            self.font_timer.draw(500, 300, '%d' % self.ingametimer, (0, 0, 0))
        # draw_rectangle(*self.get_bb_green())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


    # collide box
    def get_bb_green(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25


class Blue:
    def __init__(self):
        self.x, self.y = (50, 600 / 2)
        self.vel_x, self.vel_y = 0, 0
        self.acc_x, self.acc_y = 0, PLAYER_GRAVITY
        self.frame2 = 0
        self.image = load_image('res\\character2.png')
        self.in_bubble = load_image('res\\in_bubble.png')
        self.attack = load_image('res\\attack_p2.png')
        self.win_ceremony = load_image('res\\blue_win_ceremony.png')
        self.die = load_image('res\\die.png')

        self.font = load_font('test.ttf', 16)
        self.timer = 10
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter_p2(self, None)
        self.dir = 1
        self.jumping = False
        self.sheet_line = 120
        self.isShot = False
        self.isHit = False
        self.collide_check = True
        self.win = False
        self.defeat = False
        self.ceremony_time = 0.0
        self.is_in_bubble = False

        self.shot_sound = load_wav('sound\\bubble.wav')
        self.shot_sound.set_volume(32)
        self.jump_sound = load_wav('sound\\jump.wav')
        self.jump_sound.set_volume(32)
        self.explosion_sound = load_wav('sound\\ddukbaegi.wav')
        self.explosion_sound.set_volume(54)

        self.run_speed = 250
        self.bubble_speed = 180

        self.can_bubble_shot = False

    def bubble_shot(self):
        if self.can_bubble_shot is True:
            bubble2 = Bubble2(self.x, self.y, self.dir * 3)  # 발사 시작 위치
            grass = Grass()  # grass 객체를 가져옴

            game_world.bubble2_objects.append(bubble2)

            if bubble2.y <= grass.y + 40:  # 물방울이 중력때문에 화면 밖으로 내려가지 않게 함
                bubble2.y = grass.y + 40
            self.shot_sound.play()


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do_p2(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit_p2(self, event)
            self.cur_state = next_state_table2[self.cur_state][event]
            self.cur_state.enter_p2(self, event)

    def draw(self):
        if self.defeat is False and self.win is False and self.isShot is False:
            self.image.clip_draw(int(self.frame2) * 60, self.sheet_line, 60, 60, self.x, self.y)
        self.cur_state.draw_p2(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table2:
            key_event2 = key_event_table2[(event.type, event.key)]
            self.add_event(key_event2)

    # collide box
    def get_bb_blue(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25





