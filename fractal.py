import time
import numpy as np

import pxng
from pxng.keys import KEY_SPACE, KEY_1, KEY_2
from pxng.keys import KEY_Q, KEY_Z, KEY_X, KEY_J, KEY_I

from fractal import Range2D
from fractal import py_create_fractal
from fractal._fractal import create_fractal as rust_create_fractal


def handle_input(window, context):
    context['mouse'] = window.mouse.x, window.mouse.y

    context['mouse_delta'] = window.mouse.dx, window.mouse.dy

    if window.mouse.hover and window.mouse.button_left.held:
        context['panning'] = True
        context['dirty'] = True
    elif window.mouse.hover and window.mouse.button_left.released:
        context['panning'] = False
        context['dirty'] = True

    if window.key_state(KEY_SPACE).pressed:
        context['iterations'] = 128
        context['world'] = WorldSpace(0, 0, window.width, window.height, -2, -1, 1, 1)
        context['dirty'] = True

    if window.key_state(KEY_Q).pressed:
        window.close_window()

    if window.key_state(KEY_1).pressed:
        context['method'] = 1
        context['dirty'] = True

    if window.key_state(KEY_2).pressed:
        context['method'] = 2
        context['dirty'] = True

    if window.key_state(KEY_I).pressed:
        iterations = context['iterations']
        iterations += 64 if iterations >= 64 else 16
        iterations = min(2048, iterations)
        context['iterations'] = iterations
        context['dirty'] = True

    if window.key_state(KEY_J).pressed:
        iterations = context['iterations']
        iterations -= 64 if iterations >= 128 else 16
        iterations = max(16, iterations)
        context['iterations'] = iterations
        context['dirty'] = True

    scroll_dy = window.mouse.scroll_dy
    if window.key_state(KEY_Z).held or scroll_dy > 0:
        context['world'].zoom(1.1)
        context['dirty'] = True

    if window.key_state(KEY_X).held or scroll_dy < 0:
        context['world'].zoom(0.9)
        context['dirty'] = True


def update(window: pxng.Window):
    handle_input(window, window.context)

    if window.context['dirty']:
        render_fractal(window)

    sprite = window.context['sprite']
    window.draw_sprite(0, 0, sprite, scale=1)

    window.draw_text(0, 0, 'Fractal Renderer', scale=2)
    rendering_time = window.context["rendering_time"]
    iterations = window.context["iterations"]
    window.draw_text(0, 18, f'Iterations: {iterations}')
    window.draw_text(0, 28, f'Time Taken: {rendering_time :.04f} s.')
    if window.context['method'] == 1:
        method = 'Rust'
    elif window.context['method'] == 2:
        method = 'Python'
    else:
        method = 'Unknown'
    window.draw_text(0, 36, f'Method: {method}')


class WorldSpace:
    def __init__(self, sx1, sy1, sx2, sy2, wx1, wy1, wx2, wy2):
        self.sx1 = sx1
        self.sy1 = sy1
        self.sx2 = sx2
        self.sy2 = sy2
        self.wx1 = wx1
        self.wy1 = wy1
        self.wx2 = wx2
        self.wy2 = wy2

        self._x_scale = (self.sx2 - self.sx1) / (self.wx2 - self.wx1)
        self._y_scale = (self.sy2 - self.sy1) / (self.wy2 - self.wy1)
        self._offset_x = self.wx1
        self._offset_y = self.wy1
        self._zoom = 1

    def screen_to_world(self, x1, y1):
        x = x1 / self._x_scale + self._offset_x
        y = y1 / self._y_scale + self._offset_y
        return x, y

    def screen_to_world_units(self, dx, dy):
        x = dx / self._x_scale
        y = dy / self._y_scale
        return x, y

    def apply_zoom(self):
        self._x_scale *= self._zoom
        self._y_scale *= self._zoom
        self._zoom = 1

    def zoom(self, zoom_factor):
        self._zoom *= zoom_factor

    def adjust_offset(self, dx, dy):
        self._offset_x += dx
        self._offset_y += dy


def render_fractal(window: pxng.Window):
    iterations = window.context['iterations']
    sprite = window.context['sprite']
    world: WorldSpace = window.context['world']

    if window.context['panning']:
        dx, dy = window.context['mouse_delta']
        dx, dy = world.screen_to_world_units(dx, dy)
        world.adjust_offset(dx, dy)

    mx, my = window.context['mouse']
    pzmx, pzmy = world.screen_to_world(mx, my)
    world.apply_zoom()
    zmx, zmy = world.screen_to_world(mx, my)
    world.adjust_offset(pzmx - zmx, pzmy - zmy)

    fx1, fy1 = world.screen_to_world(0, 0)
    fx2, fy2 = world.screen_to_world(window.width, window.height)

    frac = Range2D(fx1, fy1, fx2, fy2)

    now = time.time()
    pix = Range2D(0, 0, w, h)
    if window.context['method'] == 1:
        rust_create_fractal(pix, frac, iterations=iterations, data=sprite._data)
        sprite.update()
    elif window.context['method'] == 2:
        py_create_fractal(pix, frac, iterations=iterations, data=sprite)

    window.context['rendering_time'] = time.time() - now
    window.context['dirty'] = False


if __name__ == "__main__":
    w = 1280
    h = 720
    sprite = pxng.Sprite(np.zeros((h, w, 3), dtype=np.uint8))
    window = pxng.Window(w, h, 'Fractal', scale=1)

    window.context = {
        'sprite': sprite,
        'count': 0,
        'dirty': True,
        'iterations': 128,
        'rendering_time': 0,
        'method': 1,  # 1 = rust, 2 = python
        'world': WorldSpace(0, 0, w, h, -2, -1, 1, 1),
        'panning': False,
        'mouse': (0, 0),
        'mouse_delta': (0, 0),
    }
    render_fractal(window)
    window.set_update_handler(update)
    window.start_event_loop()
