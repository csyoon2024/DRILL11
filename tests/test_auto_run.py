import unittest
from types import SimpleNamespace
from unittest.mock import patch

from boy import Boy
from main import handle_events
from pico2d import SDLK_a, SDL_KEYDOWN


class FakeImage:
    def __init__(self):
        self.draw_calls = []

    def clip_draw(self, *args):
        self.draw_calls.append(args)

    def clip_composite_draw(self, *args):
        self.draw_calls.append(args)


class AutoRunTests(unittest.TestCase):
    def setUp(self):
        self.image = FakeImage()
        with patch('boy.load_image', return_value=self.image):
            self.boy = Boy()

    def test_character_starts_at_standing_height(self):
        self.assertEqual(self.boy.y, 90)

    def test_sleeping_and_waking_updates_character_height(self):
        self.boy.fall_asleep()
        self.assertEqual(self.boy.y, 50)

        self.boy.wake_up()
        self.assertEqual(self.boy.y, 90)

    def test_direction_key_wakes_sleeping_character_at_standing_height(self):
        self.boy.fall_asleep()
        self.boy.on_direction_key_down(1)

        self.assertEqual(self.boy.state, 'RUN')
        self.assertEqual(self.boy.y, 90)

    def start_auto_run(self, start_time=0.0):
        self.boy.on_auto_run_key_down()
        self.boy.auto_run.started_at = start_time
        self.boy.last_update_at = start_time

    def test_auto_run_starts_from_idle_and_is_faster(self):
        self.start_auto_run()

        self.assertEqual(self.boy.state, 'AUTO_RUN')
        with patch('boy.time.monotonic', return_value=0.1):
            self.boy.update()
        self.assertAlmostEqual(self.boy.x, 440.0)

    def test_auto_run_returns_to_idle_after_five_seconds(self):
        self.start_auto_run(start_time=10.0)
        self.boy.last_update_at = 14.9

        with patch('boy.time.monotonic', return_value=15.0):
            self.boy.update()

        self.assertEqual(self.boy.state, 'IDLE')

    def test_auto_run_reverses_at_scaled_screen_boundary(self):
        self.start_auto_run()
        self.boy.x = 724.0

        with patch('boy.time.monotonic', return_value=0.1):
            self.boy.update()

        self.assertEqual(self.boy.x, 725.0)
        self.assertEqual(self.boy.face_dir, -1)

    def test_direction_key_cancels_auto_run_into_normal_run(self):
        self.start_auto_run()

        self.boy.on_direction_key_down(-1)

        self.assertEqual(self.boy.state, 'RUN')
        self.assertEqual(self.boy.face_dir, -1)
        self.assertEqual(self.boy.pressed_directions, [-1])

    def test_auto_run_draws_larger_sprite(self):
        self.start_auto_run()

        self.boy.draw()

        self.assertEqual(self.image.draw_calls[-1][-2:], (150.0, 150.0))

    def test_auto_run_can_only_start_from_idle(self):
        self.boy.on_direction_key_down(1)
        self.boy.on_auto_run_key_down()

        self.assertEqual(self.boy.state, 'RUN')

    def test_a_key_event_starts_auto_run(self):
        event = SimpleNamespace(type=SDL_KEYDOWN, key=SDLK_a)
        with patch('main.get_events', return_value=[event]):
            keep_running = handle_events(self.boy)

        self.assertTrue(keep_running)
        self.assertEqual(self.boy.state, 'AUTO_RUN')


if __name__ == '__main__':
    unittest.main()
