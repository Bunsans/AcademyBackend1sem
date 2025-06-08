import numpy as np
from tqdm import tqdm

from utils.time_ import timeit
from constants import GAMMA


class FractalImage:
    image: np.array
    data_corrected: np.array

    def __init__(self, width: int, height: int):
        self.image = np.zeros((height, width, 3), dtype=np.uint8)
        self.counter = np.zeros((height, width), dtype=np.uint64)
        self.count_max = 0

    def __add__(self, other):
        self.image = ((self.image + other.image) / 2).astype(np.uint8)
        self.counter = self.counter + other.counter
        self.count_max = np.max(self.counter)
        return self

    @timeit
    def calc_counter_norm(self):
        count_max_for_corr_norm = np.log10(self.count_max)
        return (np.log10(self.counter) / count_max_for_corr_norm) ** (1 / GAMMA)

    @timeit
    def correction(self):
        self.counter[self.counter == 0] = 1
        counter_norm = self.calc_counter_norm()
        counter_norm[self.counter < 0] = 0
        for color in tqdm(range(3)):
            self.image[:, :, color] = self.image[:, :, color] * counter_norm
        return self.image

    def change_color_and_increase_hit(self, x_pos, y_pos, color):
        count = self.counter[y_pos][x_pos]
        if count == 0:
            self.image[y_pos][x_pos][:] = color
        else:
            self.image[y_pos][x_pos][:] = (self.image[y_pos][x_pos][:] + color) / 2
        self.counter[y_pos][x_pos] += 1
        count += 1
        if count > self.count_max:
            self.count_max = count
