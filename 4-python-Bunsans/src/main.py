from multiprocessing import Pool
import os
from typing import List
import numpy as np

from generator_ import Generator
from visualize import Renderer
from utils.arg_parser_ import arg_parse_decorator
from utils.time_ import timeit
from constants import SEED
from fractal_image import FractalImage

np.random.seed(SEED)


def generate_image(args):
    generator = Generator(
        samples=args.sample_degree,
        iterations=args.iter_degree,
        coef_symetry=args.symetry_coef,
        resol_x_max=args.resol_x,
        resol_y_max=args.resol_y,
        num_colors=args.colors_num,
    )
    fractal_image = generator.generate()
    return fractal_image


@timeit
def generate(args):
    num_workers = args.num_workers
    with Pool(num_workers) as pool:
        list_of_images: List[FractalImage] = pool.map(
            generate_image, [args for _ in range(num_workers)]
        )
        return list_of_images


@arg_parse_decorator
@timeit
def main(args):
    print(f"\nargs is:\n{args}")
    renderer = Renderer(f"./images/{args.path}.png")
    list_of_images = generate(args=args)
    # костыль
    image_main = list_of_images[0]
    for i in range(1, len(list_of_images)):
        image_main = image_main + list_of_images[i]

    data_to_image = image_main.correction()
    print(f"count_max is: {image_main.count_max}")
    renderer.make_image(data_to_image)
    renderer.save_image()
    renderer.show_image()


if __name__ == "__main__":
    main()
