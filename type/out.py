import matplotlib.pyplot as plt
from rpi_ws281x import Color
from config import LED_COUNT
import numpy as np

def update(data, cols, type, strip=None):
    if type == 'led':
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(*cols[i]))
    elif type == 'plt':
        plt.cla()
        plt.scatter(range(LED_COUNT), data, c=np.array(cols))
        plt.pause(0.01)
