from PIL import Image
import numpy as np
from utils.time_ import timeit


class Renderer:
    image_maker: Image

    def __init__(self, path_to_save: str):
        self.path_to_save = path_to_save

    @timeit
    def make_image(self, data_to_image: np.array):
        self.image = Image.fromarray(data_to_image)

    @timeit
    def show_image(self):
        self.image.show()

    @timeit
    def save_image(self):
        self.image.save(self.path_to_save)
