import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from scipy.signal import savgol_filter
import librosa
import librosa.display
from pprint import pprint
from rpi_ws281x import PixelStrip, Color
import time

# LED strip configuration:
LED_COUNT = 60        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

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
    global cmap, cval
    norm_data = np.mean(data, axis=1)
    ydata,cols = np.zeros(BINS), np.zeros(BINS)
    ydata = np.repeat(norm_data, BINS/norm_data.shape[0])
    cols = [cmap.to_rgba(cval(i,ydata[i]))[:3] for i in range(BINS)]
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
    global count, strip
    while audio.shape[0] > 0 and count <= TMAX:
        print(count)
        chroma = librosa.feature.chroma_stft(audio, sr=MIC_RATE)
        _, cols = ledcolors(chroma)
        for i in range(BINS):
            strip.setPixelColor(i, Color(*cols[i]))
        count += 1
        return False
    return True


print('overflows', start_stream(audio_func))

