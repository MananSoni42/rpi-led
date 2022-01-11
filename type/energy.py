import numpy as np
from pprint import pprint
from config import MIC_RATE, LED_COUNT, cmap, cval
import librosa

def ledcolors(audio):
    global cmap, cval
    data = librosa.feature.chroma_stft(audio, sr=MIC_RATE)
    norm_data = np.mean(data, axis=1)
    ydata = np.repeat(norm_data, LED_COUNT/norm_data.shape[0])
    cols = [cmap.to_rgba(cval(i,ydata[i]))[:3] for i in range(LED_COUNT)]
    return ydata, cols
