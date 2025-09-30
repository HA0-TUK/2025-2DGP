from pico2d import *
import random


# Game object class here
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
    

    def draw(self):
       self.image.draw(400, 30)
    
    def update(self):
        pass

class Boy:
    def __init__(self):
        self.image = load_image('run_animation.png')
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

    def update(self):
        self.x += 5
        self.frame = (self.frame + 1) % 8

class Zombie:
    def __init__(self):
        self.image = load_image('zombie_run_animation.png')
        self.x, self.y = 100, 170
        self.frame = 0

    def draw(self):
        frame_width = self.image.w // 10
        frame_height = self.image.h
        self.image.clip_draw(self.frame * frame_width, 0, frame_width, frame_height, self.x, self.y, frame_width//2, frame_height//2)
    
    def update(self):
        self.x += 5
        self.frame = (self.frame + 1) % 10

class Girl:
    pass

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running 
    running = True

    global world
    world = []

    grass = Grass()
    world.append(grass)

    characters = [Boy() for i in range(10)]
    world += characters

    zombie = Zombie()
    world.append(zombie)



def update_world():
    for obj in world:
        obj.update()


def render_world():
    clear_canvas()

    for obj in world:
        obj.draw()


    update_canvas()

open_canvas()

reset_world()
    
while running:
    #입력처리
    handle_events()

    # 게임 로직
    update_world()
    # 게임 렌더링
    render_world()
    delay(0.05)

    #

close_canvas()
