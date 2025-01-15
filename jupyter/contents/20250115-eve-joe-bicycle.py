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
from ipycanvas import MultiCanvas, hold_canvas
from math import sqrt
from ipywidgets import FloatSlider, interact, Layout

# 2 image layers:
#   - 0: background with non-changing coordinate system
#   - 1: the cyclists and all the data that is changing
mc = MultiCanvas(2, width = 800, height = 400)
[background, canvas] = mc

# Make everything a bit bigger, and centered around the origin
for layer in [canvas, background]:
    layer.translate(200, 200)
    layer.scale(5, 5)

# Our xy coordinate system
background.line_width = 0.25
background.stroke_line(-100, 0, 100, 0)
background.stroke_line(0, -100, 0, 100)

# The color and width of the line between the cyclists
canvas.line_width = 0.1
canvas.stroke_style = 'red'

# The font used for printing the data
canvas.font = '4px mono'

def bicycle_position(time, startingpos, velocity):
    return startingpos + velocity * time

def color_circle(x, y, color):
    canvas.save()
    canvas.fill_style = color
    canvas.fill_circle(x, y, 1)
    canvas.restore()

def update(time):
    joe = bicycle_position(time, 20, -30)
    eve = bicycle_position(time, 10, -40)
    distance = sqrt(joe*joe + eve*eve)

    with hold_canvas():
        canvas.clear_rect(-100, -100, 200, 200)

        color_circle(joe, 0, 'blue')
        color_circle(0, eve, 'green')
        canvas.stroke_line(joe, 0, 0, eve)

        canvas.fill_text(f'Time:        {time:7.2f} hours', 30, -30)
        canvas.fill_text(f'Distance:    {distance:7.2f} km', 30, -25)
        canvas.fill_text(f'Eve (green): {eve:7.2f} km', 30, -20)
        canvas.fill_text(f'Joe (blue):  {joe:7.2f} km', 30, -15)

slider = FloatSlider(value = 0, min = -0.7, max = 1.2, step = 0.01, readout = True, readout_format = '.2f', layout=Layout(width='800px'))
interact(update, time = slider)
mc
