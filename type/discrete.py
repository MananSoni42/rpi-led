import numpy as np
from config import LED_COUNT
from scipy.signal import find_peaks, peak_prominences
from scipy.ndimage import gaussian_filter1d

gaussian = lambda x,mu,sigma: np.exp(-0.5*(np.square((x-mu)/sigma))) / (np.sqrt(2*np.pi)*sigma)

def get_combined_gaussian(data, peaks):
    total = sum([data[p] for p in peaks])
    return lambda x: sum([data[p]/(1e-3 + total)*gaussian(x, p, 10/6)/gaussian(p,p,10/6) for p in peaks])

def ledcolors(audio):
    data = np.absolute(np.fft.fft(audio))
    m,M = min(data), max(data)
    ydata, _ = np.histogram(data,  bins=10 ** np.linspace(np.log10(m), np.log10(M), 1+LED_COUNT))
    ydata = gaussian_filter1d(ydata, sigma=1)
    peaks, _ = find_peaks(ydata)

    val = get_combined_gaussian(data, peaks)
    
    finalData = [val(i) for i in range(LED_COUNT)]
    
    return finalData, 'magma'
