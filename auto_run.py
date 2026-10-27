class AutoRun:
    DURATION = 5.0
    SPEED_MULTIPLIER = 2.0
    DRAW_SCALE = 1.5

    def __init__(self, boy):
        self.boy = boy
        self.started_at = None

    def enter(self, now):
        self.started_at = now
        self.boy.reset_run_animation()

    def update(self, delta_time, now):
        if self.started_at is None:
            raise RuntimeError('AutoRun must be entered before it can update.')

        if now - self.started_at >= self.DURATION:
            self.boy.finish_auto_run()
            return

        half_width = self.boy.FRAME_WIDTH * self.DRAW_SCALE / 2
        min_x = half_width
        max_x = self.boy.CANVAS_WIDTH - half_width
        next_x = self.boy.x + (
            self.boy.face_dir
            * self.boy.RUN_SPEED
            * self.SPEED_MULTIPLIER
            * delta_time
        )

        if next_x <= min_x:
            self.boy.x = min_x
            self.boy.face_dir = 1
        elif next_x >= max_x:
            self.boy.x = max_x
            self.boy.face_dir = -1
        else:
            self.boy.x = next_x

        self.boy.advance_run_animation(delta_time)
