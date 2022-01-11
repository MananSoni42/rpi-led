import argparse
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from pprint import pprint
from rpi_ws281x import PixelStrip, Color
from config import *
from type.out import update
#from type.energy import ledcolors as energy_cols
from type.freq import ledcolors as freq_cols

parser = argparse.ArgumentParser()
parser.add_argument("--type" , help="Choose type of visualiztion [energy | freq]")
parser.add_argument("--out" , help="Choose output [led | plt]")
args = parser.parse_args()

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

viz_type = {
    'energy': freq_cols,
    'freq': freq_cols,
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
    while audio.shape[0] > 0 and count <= TMAX:
        print(count)
        data, cols = viz_type[args.type](audio)
        #update(data, cols, _type=args.out, strip=strip)
        for i in range(LED_COUNT):
            print('\t', i, (int(255*cols[i][0]), int(255*cols[i][1]), int(255*cols[i][2])))
            strip.setPixelColor(i, Color(int(255*cols[i][0]), int(255*cols[i][1]), int(255*cols[i][2])))
            strip.show()
        count += 1
        return False
    return True


print('overflows', start_stream(audio_func))

