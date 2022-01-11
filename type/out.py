import matplotlib.pyplot as plt
from rpi_ws281x import Color
from config import LED_COUNT
import numpy as np

def update(data, cols, _type, strip=None):
    if _type == 'led':
        print('led')
        for i in range(LED_COUNT):
            print(i, (int(255*cols[i][0]), int(255*cols[i][1]), int(255*cols[i][2])))
            strip.setPixelColor(i, Color(int(255*cols[i][0]), int(255*cols[i][1]), int(255*cols[i][2])))
            strip.show()
            print('\t',i, 'done')
    elif _type == 'plt':
        plt.cla()
        plt.scatter(range(LED_COUNT), data, c=np.array(cols))
        plt.pause(0.01)
