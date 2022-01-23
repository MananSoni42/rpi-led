import matplotlib.pyplot as plt
from matplotlib import cm, colors
from rpi_ws281x import Color
from config import LED_COUNT
import numpy as np

def update(data, brightness, _type, strip, cmap='magma'):
    cmap = cm.ScalarMappable(
    norm=colors.Normalize(vmin=0, vmax=1, clip=False),
    cmap=cmap)

    cols = np.array([cmap.to_rgba(data[i])[:3] for i in range(LED_COUNT)]).reshape(LED_COUNT,3)

    if _type == 'led':
        strip.setBrightness(int(255*brightness))
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(int(255*cols[i][0]), int(255*cols[i][1]), int(255*cols[i][2])))
        strip.show()
    elif _type == 'comp':
        plt.cla()
        
        plt.subplot(211)
        plt.gca().set_facecolor((0,0,0))
        plt.scatter(range(LED_COUNT), [0.5]*LED_COUNT, c=cols, alpha=brightness)
        
        plt.subplot(212)
        plt.plot(range(LED_COUNT), data)

        plt.pause(0.01)
