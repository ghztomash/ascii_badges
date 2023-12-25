import math

class Oscillator:
    def __init__(self, sample_rate, frequency, phase=0):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.phase_offset = phase
        if self.phase_offset > 2 * math.pi:
            self.phase_offset -= 2 * math.pi
        self.phase = 0
        self.phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def tick(self):
        self.phase += self.phase_increment
        if self.phase >= 2 * math.pi:
            self.phase -= 2 * math.pi
        return self

    def get_sin_value(self):
        value = math.sin(self.phase + self.phase_offset)
        return value

    def get_cos_value(self):
        value = math.cos(self.phase + self.phase_offset)
        return value

    def get_square_value(self):
        if self.phase() < math.pi:
            return 1
        else:
            return -1

    def get_sawtooth_value(self):
        value = (self.phase + self.phase_offset) / (2 * math.pi)
        return value

    def get_triangle_value(self):
        value = 1 - (2 * abs((self.phase + self.phase_offset) / (2 * math.pi) - 0.5))
        return value


# convert fps to sample rate
def fps_to_sample_rate(fps):
    return fps * 1000


# convert bpm to frequency
def bpm_to_frequency(bpm):
    return bpm / 60