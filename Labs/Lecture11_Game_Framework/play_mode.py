from pico2d import *
from boy import Boy
from grass import Grass

import game_world
import game_framework
import title_mode
import item_mode

boy = None
running = True

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_mode(item_mode)
        else:
            boy.handle_event(event)

def init():
    global boy
    global running

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass

def pause():pass
def resume():pass


