import numpy as np
from pprint import pprint
from config import MIC_RATE, LED_COUNT, cmap, cval
from scipy.ndimage import gaussian_filter1d

MAX_IND = 1

def ledcolors(audio):
    global cmap, cval
    data = np.absolute(np.fft.fft(audio))
    ydata, _ = np.histogram(data, bins=LED_COUNT//2)
    ydata = np.concatenate([ydata[::-1], ydata])
    ydata = gaussian_filter1d(np.log(1+ydata), sigma=5)
    ydata = ydata.astype(np.float32)/np.max(ydata)
    brightness = max( np.mean(np.absolute(audio)) / np.max(np.absolute(audio)), 0)
    cols = [cmap.to_rgba(cval(i,ydata[i]))[:3] for i in range(LED_COUNT)]
    return ydata, cols, brightness
