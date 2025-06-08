import itertools
import pickle
import random
from typing import Callable, Dict, List, Tuple
from loguru import logger

import numpy as np
from tqdm import tqdm
from fractal_image import FractalImage
from linear_generator import (
    CoefLinear,
    LinearTransformGenerator,
    linear_transform,
)
from non_linear_func import non_liniear_funcs
from constants import (
    NUM_COLORS,
    RESOL_X_MAX,
    RESOL_Y_MAX,
    ITERATION,
    SAMPLES,
    SEED,
    X_MAX,
    X_MIN,
    Y_MAX,
    Y_MIN,
    COEF_SYMETRY,
    Color,
)

np.random.seed(SEED)


def linear_rotation(x, y, i, coef_symetry):
    alpha = i * (2 * np.pi) / coef_symetry
    x_rot = np.cos(alpha) * x + np.sin(alpha) * y
    y_rot = -np.sin(alpha) * x + np.cos(alpha) * y
    # should improve
    return x_rot, y_rot


def dihedral_symmetry(
    x,
    y,
):
    return -x, y

class Generator:
    def __init__(
        self,
        samples: int = SAMPLES,
        iterations: int = ITERATION,
        coef_symetry: int = COEF_SYMETRY,
        resol_x_max: int = RESOL_X_MAX,
        resol_y_max: int = RESOL_Y_MAX,
        num_colors: int = NUM_COLORS,
    ) -> None:
        self.samples = samples
        self.iterations = iterations
        self.coef_symetry = coef_symetry
        self.resol_x_max = resol_x_max
        self.resol_y_max = resol_y_max
        self.fractal_image = FractalImage(resol_x_max, resol_y_max)


        
        self.list_colors_liniear_funcs: List[Tuple[Color, Callable]] = LinearTransformGenerator().get_list_linear_funcs(
            num_colors=num_colors
        )
        self.list_non_liniear_funcs: List[Callable] = non_liniear_funcs

    # def _get_linear_transform(self) -> Tuple[np.array, CoefLinear]:
    #     """
    #     color: np.array, linear_coefs
    #     """
    #     return random.choice(self.list_liniear)

    # def _get_non_linear_transform(self):
    #     return random.choice(self.non_liniear_funcs)
    def _get_list_of_coordinates(self):
        x = np.random.uniform(X_MIN, X_MAX, size=(self.samples, 1))
        y = np.random.uniform(Y_MIN, Y_MAX, size=(self.samples, 1))
        return np.concatenate((x, y), axis=1)

    def get_pos_on_image(self, x: float, y: float) -> Tuple[int, int]:
        # minus because positions and x, y are not
        x_pos = self.resol_x_max - round(
            (X_MAX - x) / (X_MAX - X_MIN) * self.resol_x_max
        )
        y_pos = self.resol_y_max - round(
            (Y_MAX - y) / (Y_MAX - Y_MIN) * self.resol_y_max
        )
        if x_pos == self.resol_x_max:
            x_pos = self.resol_x_max - 1
        if y_pos == self.resol_y_max:
            y_pos = self.resol_y_max - 1
        return x_pos, y_pos

    def is_inside_image(self, x_pos: int, y_pos: int):
        return 0 < x_pos < self.resol_x_max and 0 < y_pos < self.resol_y_max

    def _is_inside_space(self, x: float, y: float):
        return X_MIN < x < X_MAX and Y_MIN < y < Y_MAX

    def transform_pixel(
        self, x: float, y: float, index: int = None
    ) -> Tuple[float, float, np.array] | None:
        linear_func, non_linear_func = self.list_linear_and_non[index]
        color, linear_coefs = linear_func
        x_linear, y_linear = linear_transform(x, y, linear_coefs)
        x_non_linear, y_non_linear = non_linear_func(x_linear, y_linear, linear_coefs)
        return x_non_linear, y_non_linear, color


    # def _get_random_coordinates(self):
    #     x = np.random.uniform(X_MIN, X_MAX)
    #     y = np.random.uniform(Y_MIN, Y_MAX)
    #     return x, y

    # def add_symmetry(self, x: float, y: float, color, iteration: int):

    #     if iteration > 20:
    #         x_pos, y_pos = self.get_pos_on_image(x_rot, y_rot)
    #         if not self.is_inside_image(x_pos, y_pos):
    #             continue
    #         self.fractal_image.change_color_and_increase_hit(x_pos, y_pos, color)
    #         if self.coef_symetry < 0:
    #             x_dih, y_dih = dihedral_symmetry(x_rot, y_rot)
    #             x_pos_dih, y_pos_dih = self.get_pos_on_image(x_dih, y_dih)
    #             if not self.is_inside_image(x_pos_dih, y_pos_dih):
    #                 continue
    #             self.fractal_image.change_color_and_increase_hit(
    #                 x_pos_dih, y_pos_dih, color
    #             )

    def _check_coordinates(self, x: float, y: float, ):
        if not self._is_inside_space(x, y):
            return False
        x_pos, y_pos = self.get_pos_on_image(x, y)
        if not self.is_inside_image(x_pos, y_pos):
            return False
        return x_pos, y_pos

    def get_all_possible_positions(self, x: float, y: float, linear_and_non):
        possible_pos_at_sample: Dict[Color, List[int, int]] = []

        for color, linear_func in self.list_colors_liniear_funcs:
            possible_pos_curr: List[Tuple[int, int]] = []

            x_linear, y_linear = linear_func(x, y)
            for non_linear_func in self.list_non_liniear_funcs:
                x_non_linear, y_non_linear = non_linear_func(x_linear, y_linear)

                for i in range(abs(self.coef_symetry)):
                    x_rot, y_rot = linear_rotation(x_non_linear, y_non_linear, i, self.coef_symetry)

                    res_of_check_coordinates = self._check_coordinates(x_rot, y_rot)
                    if res_of_check_coordinates == False: 
                        continue
                    x_pos, y_pos = res_of_check_coordinates
                    possible_pos_curr.append((x_pos, y_pos))

                    if self.coef_symetry < 0:
                        x_dih, y_dih = dihedral_symmetry(x_rot, y_rot)
                        res_of_check_coordinates = self._check_coordinates(x_dih, y_dih)
                        if res_of_check_coordinates == False: 
                            continue
                        x_pos, y_pos = res_of_check_coordinates
                        possible_pos_curr.append((x_pos, y_pos))

            possible_pos_at_sample[color] = possible_pos_curr

        

    def generate(self):
        for x, y in self._get_list_of_coordinates():
            # calc all possible positions after transforming
            
                self.get_all_possible_positions(x, y, linear_and_non)
            for iteration in range(self.iterations):
                if not self._is_inside_space(x_non_linear, y_non_linear):
                    continue
                self.add_symmetry(x_non_linear, y_non_linear, color, iteration)
        return self.fractal_image
