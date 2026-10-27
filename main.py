from pico2d import *

from boy import Boy
from grass import Grass


def handle_events(boy):
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                return False
            if event.key == SDLK_SPACE:
                boy.on_space()
            elif event.key == SDLK_LEFT:
                boy.on_direction_key_down(-1)
            elif event.key == SDLK_RIGHT:
                boy.on_direction_key_down(1)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                boy.on_direction_key_up(-1)
            elif event.key == SDLK_RIGHT:
                boy.on_direction_key_up(1)
    return True


def run():
    open_canvas(800, 600)
    boy = Boy()
    world = [Grass(), boy]
    running = True

    while running:
        running = handle_events(boy)
        for game_object in world:
            game_object.update()
        clear_canvas()
        for game_object in world:
            game_object.draw()
        update_canvas()
        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    run()
