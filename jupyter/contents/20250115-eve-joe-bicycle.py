# %% [markdown]
# Two cyclists are riding on perpendicular streets towards their future intersection.
#
# They are both riding with steady speed.
#
# The faster one (Eve) is doing 40 km/h and is starting at 10 km from the intersection.
#
# The slower one (Joe) is doing 30 km/h and is starting at 20 km from the intersection.
#
# When and where will they be closest to each other?

# %% jupyter={"source_hidden": true}
# below code is copy-paste from here: https://ipywidgets.readthedocs.io/en/8.1.5/examples/Widget%20Events.html#throttling
import asyncio
from time import time

class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback()

    def start(self):
        self._task = asyncio.ensure_future(self._job())

    def cancel(self):
        self._task.cancel()

def throttle(wait):
    """ Decorator that prevents a function from being called
        more than once every wait period. """
    def decorator(fn):
        time_of_last_call = 0
        scheduled, timer = False, None
        new_args, new_kwargs = None, None
        def throttled(*args, **kwargs):
            nonlocal new_args, new_kwargs, time_of_last_call, scheduled, timer
            def call_it():
                nonlocal new_args, new_kwargs, time_of_last_call, scheduled, timer
                time_of_last_call = time()
                fn(*new_args, **new_kwargs)
                scheduled = False
            time_since_last_call = time() - time_of_last_call
            new_args, new_kwargs = args, kwargs
            if not scheduled:
                scheduled = True
                new_wait = max(0, wait - time_since_last_call)
                timer = Timer(new_wait, call_it)
                timer.start()
        return throttled
    return decorator
# copy-paste ends here, below is original content

from ipycanvas import MultiCanvas
from math import sqrt
from ipywidgets import FloatSlider, interact, Layout

mc = MultiCanvas(2, width = 800, height = 400)
[background, canvas] = mc

for layer in [canvas, background]:
    layer.translate(200, 200)
    layer.scale(5, 5)
    layer.font = '4px mono'

background.fill_text('Time:', 30, -30)
background.fill_text('Distance:', 30, -25)
background.fill_text('Eve (green):', 30, -20)
background.fill_text('Joe (blue):', 30, -15)

background.line_width = 0.25
background.stroke_line(-200, 0, 200, 0)
background.stroke_line(0, -200, 0, 200)

canvas = mc[1]

def reset_canvas():
    canvas.clear_rect(-10000, -10000, 20000, 20000)
    canvas.line_width = 1
    canvas.stroke_style = 'black'
    canvas.fill_style = 'black'

def bicycle_position(time, startingpos, velocity):
    return startingpos + velocity * time

@throttle(0.2)
def draw(time):
    reset_canvas()

    joe = bicycle_position(time, 20, -30)
    eve = bicycle_position(time, 10, -40)
    canvas.fill_style = 'blue'
    canvas.fill_circle(joe, 0, 1)
    canvas.fill_style = 'green'
    canvas.fill_circle(0, eve, 1)

    canvas.stroke_style = 'red'
    canvas.line_width = 0.1
    canvas.stroke_line(joe, 0, 0, eve)

    distance = sqrt(joe*joe + eve*eve)

    canvas.fill_style = 'black'

    canvas.fill_text(f'{time:7.2f} hours', 70, -30)
    canvas.fill_text(f'{distance:7.2f} km', 70, -25)
    canvas.fill_text(f'{eve:7.2f} km', 70, -20)
    canvas.fill_text(f'{joe:7.2f} km', 70, -15)

slider = FloatSlider(value = 0, min = -1.2, max = 1.2, step = 0.01, readout = True, readout_format = '.2f', layout=Layout(width='800px'))
interact(draw, time = slider)

display(mc)
draw(0)
