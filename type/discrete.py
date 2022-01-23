import numpy as np
from pprint import pprint
from config import LED_COUNT
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

def ledcolors(audio):
    data = np.absolute(np.fft.fft(audio))
    m,M = min(data), max(data)
    ydata, _ = np.histogram(data,  bins=10 ** np.linspace(np.log10(m), np.log10(M), 1+LED_COUNT//2))
    ydata = np.concatenate([ydata[::-1], ydata])
    print(ydata.shape)
    ydata = gaussian_filter1d(ydata, sigma=1)
    ydata = ydata.astype(np.float32)/np.max(ydata)
    return ydata, 'magma'
