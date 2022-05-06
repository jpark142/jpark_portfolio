from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('res\\grass.png')
        self.x, self.y = 400, 30



    def update(self):
        pass


    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(800, 30)

