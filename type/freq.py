import numpy as np
from pprint import pprint
from config import LED_COUNT
from scipy.ndimage import gaussian_filter1d

def ledcolors(audio):
    data = np.absolute(np.fft.fft(audio))
    ydata, _ = np.histogram(data, bins=LED_COUNT//2)
    ydata = np.concatenate([ydata[::-1], ydata])
    ydata = gaussian_filter1d(np.log(1+ydata), sigma=5)
    
    return ydata
