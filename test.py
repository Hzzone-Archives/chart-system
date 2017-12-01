import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Create some random data
x = np.linspace(0,100,1000)
y = np.sin(x) * np.cos(x)

left, bottom, width, height = 0.15, 0.02, 0.7, 0.10

fig, ax = plt.subplots()

plt.subplots_adjust(left=left, bottom=0.25) # Make space for the slider

ax.plot(x,y)

# Set the starting x limits
xlims = [0, 1]
ax.set_xlim(*xlims)

# Create a plt.axes object to hold the slider
slider_ax = plt.axes([left, bottom, width, height])
# Add a slider to the plt.axes object
slider = Slider(slider_ax, 'x-limits', valmin=0.0, valmax=100.0, valinit=xlims[1])

# Define a function to run whenever the slider changes its value.
def update(val):
    xlims[1] = val
    ax.set_xlim(*xlims)

    fig.canvas.draw_idle()

# Register the function update to run when the slider changes value
slider.on_changed(update)

plt.show()