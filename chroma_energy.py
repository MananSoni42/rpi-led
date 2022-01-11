import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from scipy.signal import savgol_filter
import librosa
import librosa.display
from pprint import pprint

fig, ax = plt.subplots()

MIC_RATE = 44100
FPS = 30
BINS = 60
TMAX = 100
count = 1

cmap = cm.ScalarMappable(
    norm=colors.Normalize(vmin=0, vmax=1, clip=False),
    cmap='hsv')

cval = lambda i,x: (x+i/60) if (x+i/60) < 1 else (x - 1 + i/60)

def ledcolors(data):
    norm_data = np.mean(data, axis=1)
    ydata,cols = np.zeros(BINS), np.zeros(BINS)
    ydata = np.repeat(norm_data, BINS/norm_data.shape[0])
    cols = [cval(i,ydata[i]) for i in range(BINS)]
    return ydata, cols

    

def start_stream(callback):
    p = pyaudio.PyAudio()
    frames_per_buffer = int(MIC_RATE / FPS)
    print('Frames per buffer: ', frames_per_buffer)
    overflows = 0
    finished = False
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer)
    while not finished:
        try:
            y = np.frombuffer(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16).astype(np.float32)
            stream.read(stream.get_read_available(), exception_on_overflow=False)
            finished = callback(y)
            
        except IOError:
            overflows += 1

    stream.stop_stream()
    stream.close()
    p.terminate()

    return overflows

def audio_func(audio):
    global count
    while audio.shape[0] > 0 and count <= TMAX:
        print(count)
        chroma = librosa.feature.chroma_stft(audio, sr=MIC_RATE)
        plt.cla()
        data, cols = ledcolors(chroma)
        plt.scatter(range(BINS), data, c=cols)
        plt.pause(0.01)
        count += 1
        return False
    return True


print('overflows', start_stream(audio_func))
plt.show()

