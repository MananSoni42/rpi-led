import matplotlib.pyplot as plt
from rpi_ws281x import Color
from config import LED_COUNT
import numpy as np

def update(data, cols, brightness, _type, strip=None):
    if _type == 'led':
        strip.setBrightness(int(255*brightness))
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(int(255*cols[i][0]), int(255*cols[i][1]), int(255*cols[i][2])))
        strip.show()
    elif _type == 'plt':
        plt.cla()
        plt.scatter(range(LED_COUNT), data, c=np.array(cols))
        plt.pause(0.01)
