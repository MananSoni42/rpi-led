import numpy as np
from pprint import pprint
from config import MIC_RATE, LED_COUNT
import librosa

def ledcolors(audio):
    data = librosa.feature.chroma_stft(audio, sr=MIC_RATE)
    norm_data = np.mean(data, axis=1)
    ydata = np.repeat(norm_data, LED_COUNT/norm_data.shape[0])
    return ydata
