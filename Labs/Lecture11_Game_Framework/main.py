from pico2d import *
import game_framework
import logo_mode as start_mode
import play_mode


open_canvas()
game_framework.run(play_mode)
close_canvas()