import math
import time

from pico2d import load_image
from transitions import Machine

from auto_run import AutoRun


class Boy:
    IDLE_TIMEOUT = 5.0
    CANVAS_WIDTH = 800
    FRAME_WIDTH = 100
    RUN_SPEED = 200.0
    RUN_FRAME_DURATION = 0.05
    STANDING_Y = 90
    SLEEPING_Y = 50
    MIN_X = FRAME_WIDTH / 2
    MAX_X = CANVAS_WIDTH - FRAME_WIDTH / 2

    def __init__(self):
        self.x, self.y = 400, self.STANDING_Y
        self.frame = 0
        self.face_dir = 1
        self.pressed_directions = []
        self.idle_since = time.monotonic()
        self.last_update_at = self.idle_since
        self.run_animation_elapsed = 0.0
        self.image = load_image('animation_sheet.png')
        self.auto_run = AutoRun(self)
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP', 'AUTO_RUN'],
            initial='IDLE',
            transitions=[
                {'trigger': 'start_run', 'source': 'IDLE', 'dest': 'RUN', 'after': 'reset_run_animation'},
                {'trigger': 'wake_and_run', 'source': 'SLEEP', 'dest': 'RUN', 'after': 'wake_from_sleep_and_run'},
                {'trigger': 'stop_run', 'source': 'RUN', 'dest': 'IDLE', 'after': 'reset_idle_timer'},
                {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP', 'after': 'freeze_sleep_frame'},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE', 'after': 'wake_from_sleep'},
                {'trigger': 'start_auto_run', 'source': 'IDLE', 'dest': 'AUTO_RUN', 'after': 'enter_auto_run'},
                {'trigger': 'cancel_auto_run', 'source': 'AUTO_RUN', 'dest': 'RUN', 'after': 'reset_run_animation'},
                {'trigger': 'finish_auto_run', 'source': 'AUTO_RUN', 'dest': 'IDLE', 'after': 'reset_idle_timer'},
            ],
            auto_transitions=False,
        )

    def update(self):
        now = time.monotonic()
        delta_time = min(now - self.last_update_at, 0.1)
        self.last_update_at = now

        if self.state == 'IDLE':
            if now - self.idle_since >= self.IDLE_TIMEOUT:
                self.fall_asleep()
                return
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.x = max(
                self.MIN_X,
                min(self.MAX_X, self.x + self.face_dir * self.RUN_SPEED * delta_time),
            )
            self.advance_run_animation(delta_time)
        elif self.state == 'AUTO_RUN':
            self.auto_run.update(delta_time, now)

    def on_direction_key_down(self, direction):
        if self.state == 'AUTO_RUN':
            if direction not in self.pressed_directions:
                self.pressed_directions.append(direction)
            self.face_dir = direction
            self.cancel_auto_run()
            return
        if self.state not in ('IDLE', 'RUN', 'SLEEP'):
            return
        if direction not in self.pressed_directions:
            self.pressed_directions.append(direction)
        self.face_dir = direction
        if self.state == 'SLEEP':
            self.wake_and_run()
        elif self.state == 'IDLE':
            self.start_run()

    def on_direction_key_up(self, direction):
        if direction in self.pressed_directions:
            self.pressed_directions.remove(direction)
        if self.state != 'RUN':
            return
        if self.pressed_directions:
            self.face_dir = self.pressed_directions[-1]
        else:
            self.stop_run()

    def on_space(self):
        if self.state == 'SLEEP':
            self.wake_up()

    def on_auto_run_key_down(self):
        if self.state == 'IDLE':
            self.start_auto_run()

    def enter_auto_run(self):
        self.auto_run.enter(time.monotonic())

    def reset_run_animation(self):
        self.frame = 0
        self.run_animation_elapsed = 0.0

    def advance_run_animation(self, delta_time):
        self.run_animation_elapsed += delta_time
        while self.run_animation_elapsed >= self.RUN_FRAME_DURATION:
            self.frame = (self.frame + 1) % 8
            self.run_animation_elapsed -= self.RUN_FRAME_DURATION

    def freeze_sleep_frame(self):
        self.frame = 0
        self.y = self.SLEEPING_Y

    def wake_from_sleep(self):
        self.y = self.STANDING_Y
        self.reset_idle_timer()

    def wake_from_sleep_and_run(self):
        self.y = self.STANDING_Y
        self.reset_run_animation()

    def reset_idle_timer(self):
        self.idle_since = time.monotonic()

    def draw(self):
        if self.state == 'SLEEP':
            sprite_bottom = 300 if self.face_dir == 1 else 200
            self.image.clip_composite_draw(
                self.frame * 100, sprite_bottom, 100, 100,
                math.pi / 2, '', self.x, self.y, 100, 100,
            )
            return

        if self.state in ('RUN', 'AUTO_RUN'):
            sprite_bottom = 100 if self.face_dir == 1 else 0
            if self.state == 'AUTO_RUN':
                draw_size = self.FRAME_WIDTH * self.auto_run.DRAW_SCALE
                self.image.clip_draw(
                    self.frame * 100, sprite_bottom, 100, 100,
                    self.x, self.y, draw_size, draw_size,
                )
            else:
                self.image.clip_draw(
                    self.frame * 100, sprite_bottom, 100, 100, self.x, self.y,
                )
            return

        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
