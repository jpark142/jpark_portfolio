from pico2d import *

class Platforms:
    def __init__(self):
        self.image = load_image('res\\platform.png')
        self.px1, self.py1 = 500, 150
        self.px2, self.py2 = 200, 300
        self.px3, self.py3 = 800, 300
        self.px4, self.py4 = 350, 450
        self.px5, self.py5 = 650, 450
        self.dx = 1

    def update(self):
        self.px1 += self.dx
        if self.px1 > 820:
            self.dx = -1
        if self.px1 < 180:
            self.dx = 1

    def draw(self):
        # 플랫폼1의 크기는 가로400 세로50 / 위치는 (500, 150)
        self.image.clip_draw(0, 30, 400, 50, self.px1, self.py1)
        # 플랫폼2의 크기는 가로200 세로50 / 위치는 (200, 300)
        self.image.clip_draw(0, 30, 200, 50, self.px2, self.py2)
        # 플랫폼3의 크기는 가로200 세로50 / 위치는 (800, 300)
        self.image.clip_draw(0, 30, 200, 50, self.px3, self.py3)

        self.image.clip_draw(20, 30, 100, 50, self.px4, self.py4)
        self.image.clip_draw(20, 30, 100, 50, self.px5, self.py5)

    def get_bb(self):
        return self.px1-180, self.py1+25, self.px1 + 180, self.py1+25

    def get_bb2(self):
        return self.px2-80, self.py2+25, self.px2 + 80, self.py2+25

    def get_bb3(self):
        return self.px3-80, self.py3+25, self.px3 + 80, self.py3+25

    def get_bb4(self):
        return self.px4-30, self.py4+25, self.px4 +30, self.py4+25

    def get_bb5(self):
        return self.px5-30, self.py5+25, self.px5 +30, self.py5+25
