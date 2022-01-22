import numpy as np
from pprint import pprint
from config import LED_COUNT
from scipy.ndimage import gaussian_filter1d

def ledcolors(audio):
    ydata, _ = np.histogram(audio, bins=LED_COUNT)
    ydata += np.min(ydata)
    ydata = ydata.astype(np.float32)/np.max(ydata)
    
    return ydata
