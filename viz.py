import argparse
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from pprint import pprint
from rpi_ws281x import PixelStrip, Color
from config import *
from type.out import update
from type.freq import ledcolors as freq_cols
from type.wave import ledcolors as wave_cols
from scipy.ndimage import gaussian_filter1d

parser = argparse.ArgumentParser()
parser.add_argument("--type" , help="Choose type of visualiztion [wave | freq]")
parser.add_argument("--out" , help="Choose output [led | plt]")
args = parser.parse_args()

bmean, bmin, bmax, bcount, bprev = 0, 1e6, 0, 0, 0.3

def get_brightness(b):
    global bmean, bmin, bmax, bcount, bprev
    w,a = 0.7, 0.75
    bmean = w*bmean + (1-w)*(bcount*bmean + b)/(bcount+1)
    bcount += 1
    bmin = w*bmin + (1-w)*min(bmin,b)
    bmax = w*bmax + (1-w)*max(bmax,b)

    if count < 10:
        return 0.3
    else:
        bcurr = max(min((b - (a*bmean + (1-a)*bmin)) / ((1-a)*(bmax-bmin + 1e-3)), 1), 0)
        bfinal = w*bcurr + (1-w)*bprev
        bprev = bcurr
        return bfinal

strip = None
if args.out == 'led':
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

viz_type = {
    'freq': freq_cols,
    'wave': wave_cols
}

cmap = cm.ScalarMappable(
    norm=colors.Normalize(vmin=0, vmax=1, clip=False),
    cmap='hsv')

cval = lambda i,x: (x+i/60) if (x+i/60) < 1 else (x - 1 + i/60)

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
    while count <= TMAX:
        brightness = np.sqrt((np.sum(np.square(audio))))/audio.shape[0]
        brightness1 = get_brightness(brightness)
        print(count, '/', TMAX, bmin, bmean, bmax)
        print(brightness, brightness1)
        audio = gaussian_filter1d(audio, sigma=50)
        data = viz_type[args.type](audio)
        update(data, brightness1, _type=args.out, strip=strip)
        count += 1
        return False
    return True


print('overflows', start_stream(audio_func))

if args.type == 'led':
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
