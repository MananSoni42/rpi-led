import numpy as np
from pprint import pprint
from config import MIC_RATE, LED_COUNT, cmap, cval
from scipy.ndimage import gaussian_filter1d

MAX_IND = 1

brightness_levels = [
    (0.0, 300, 0.01),
    (300, 500, 0.25),
    (500, 700, 0.75),
    (700, 2000, 1.0),
]

discrete_brightness = lambda b: sum([b_[2] if b_[0] <= b < b_[1] else 0 for b_ in brightness_levels])

def ledcolors(audio):
    global cmap, cval
    data = np.absolute(np.fft.fft(audio))
    ydata, _ = np.histogram(data, bins=LED_COUNT//2)
    ydata = np.concatenate([ydata[::-1], ydata])
    ydata = gaussian_filter1d(np.log(1+ydata), sigma=5)
    ydata = ydata.astype(np.float32)/np.max(ydata)
    brightness = np.sqrt(np.sum(np.square(audio)))/audio.shape[0]
    cols = [cmap.to_rgba(cval(i,ydata[i]))[:3] for i in range(LED_COUNT)]
    
    #print(brightness, discrete_brightness(brightness))
    return ydata, cols, discrete_brightness(brightness)
    #return ydata, cols, brightness
