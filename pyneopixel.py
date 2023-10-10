# NeoPixel driver for MicroPython

from machine import bitstream, Pin
import time


class NeoPixel:
    # G R B W
    ORDER = (1, 0, 2, 3)

    def __init__(self, pin, n, brightness=255, bpp=3, timing=1):
        self.pin = pin
        self.n = n  # led's num
        self.brightness = brightness
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin = Pin(pin, Pin.OUT)
        # Timing arg can either be 1 for 800kHz or 0 for 400kHz,
        # or a user-specified timing ns tuple (high_0, low_0, high_1, low_1).
        self.timing = (
            ((400, 850, 800, 450) if timing else (800, 1700, 1600, 900))
            if isinstance(timing, int)
            else timing
        )

    def __len__(self):
        return self.n

    def __setitem__(self, i, v):  # v:color
        offset = i * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = v[i]

    def __getitem__(self, i):
        offset = i * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]] for i in range(self.bpp))

    def fill(self, v):
        b = self.buf
        l = len(self.buf)
        bpp = self.bpp
        for i in range(bpp):
            c = v[i]
            j = self.ORDER[i]
            while j < l:
                b[j] = c
                j += bpp

    def clear(self):
        self.buf = bytearray(len(self.buf))  #
        self.write()

    def write(self, array=None):
        if array is None:
            array = self.buf
        bitstream(self.pin, 0, self.timing, array)

    def set_brightness(self, brightness):
        if 0 <= brightness <= 255:
            for i in range(len(self.buf)):
                self[i] = int(self[i] * brightness / 255)
        else:
            raise ValueError("Brightness should be in the range 0-255")

    def blink(self, color, repeat=3, durian=500): 
        for i in range(repeat):
            self.fill(color)
            self.write()
            time.sleep_ms(durian)
            self.clear()
            time.sleep_ms(durian)

    def blink_fun(self, color=None, array=None, durian=None):  # universal function in blink
        if color == None:
            self.write(array)
            time.sleep_ms(durian)
            self.clear()
            time.sleep_ms(durian)

        else:
            self.fill(color)
            self.write()
            time.sleep_ms(durian)
            self.clear()
            time.sleep_ms(durian)

    def blink_infinite(self, color=None, durian=500):
        b = self.buf
        while True:
            self.blink_fun(color, b, durian)

    def blink_full(self, mode=True, color=None, repeat=3, durian=500):  # fully functional; mode: 1 for finite
        b = self.buf
        if mode:
            for i in range(repeat):
                self.blink_fun(color, b, durian)
        else:
            while True:
                self.blink_fun(color, b, durian)

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.n):
                rc_index = (i * 256 // self.n) + j
                self.__setitem__(i, self.wheel(rc_index & 255))
            self.write()
            time.sleep(wait)

    def hsv2rgb(self, h, s, v):  # h:0~360;s:0~1;v:0~1
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        elif 240 <= h < 360:
            r, g, b = c, 0, x

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)
        return r, g, b

    def rainbow(self, wait=10):
        while True:
            for i in range(360):
                hue = i % 360
                for j in range(self.n):
                    color = self.hsv2rgb(hue, 1, 1)
                    self[j] = color
                self.write()
                time.sleep_ms(wait)

#     def random_color(self):
#         import random
#         r = random.randint(0, 255)
#         g = random.randint(0, 255)
#         b = random.randint(0, 255)
#         return (r, g, b)
#
#     def random_pos(self):
#         import random
#         pos = random.randint(0, self.n)
#         return pos

