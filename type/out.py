import matplotlib.pyplot as plt
from rpi_ws281x import Color
from config import LED_COUNT, cmap, cval
import numpy as np

def update(data, brightness, _type, strip):
    cols = [cmap.to_rgba(cval(i,data[i]))[:3] for i in range(LED_COUNT)]
    if _type == 'led':
        strip.setBrightness(int(255*brightness))
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(int(255*cols[i][0]), int(255*cols[i][1]), int(255*cols[i][2])))
        strip.show()
    elif _type == 'plt':
        plt.cla()
        plt.gca().set_ylim((0,1))
        plt.scatter(range(LED_COUNT), [brightness]*LED_COUNT, c=np.array(cols))
        #plt.scatter(0.1, brightness,  c='k')
        plt.pause(0.01)
