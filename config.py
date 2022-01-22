from matplotlib import cm, colors

# LED strip configuration:
LED_COUNT = 60        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 42  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

MIC_RATE = 44100
FPS = 40
TMAX = 1000
count = 1

# hsv, seismic, autumn, magma
cmap = cm.ScalarMappable(
    norm=colors.Normalize(vmin=0, vmax=1, clip=False),
    cmap='magma')

#cval = lambda i,x: (x+i/60) if (x+i/60) < 1 else (x - 1 + i/60)
cval = lambda i,x: x


