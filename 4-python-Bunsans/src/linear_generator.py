from dataclasses import dataclass
import random
from typing import Callable, Dict, List, Tuple
from loguru import logger
import numpy as np

from constants import (
    COLORS,
    NUM_COLORS,
    IS_FIXED_COLORS,
    SEED,
    IS_FIXED_LINEAR,
    LINEAR_FUNCS,
    CoefLinear,
    Color,
)

np.random.seed(SEED)


class LinearTransformGenerator:
    def _is_in_circle(self, x, y):
        """first and second conditions"""
        return x**2 + y**2 < 1

    # think about naming
    def _is_in_4D_circle(self, a, b, d, e):
        """fird condition"""
        return a**2 + b**2 + d**2 + e**2 < 1 + (a * e - b * d) ** 2

    def _is_possible_coef(self, coef_rand: np.array):
        a, b, d, e = coef_rand
        return (
            self._is_in_circle(a, d)
            and self._is_in_circle(b, e)
            and self._is_in_4D_circle(a, b, d, e)
        )

    def _get_coef(self):
        NUM_ITER = 10000
        # think about more efficient, may be inf loop
        count_not_normal = 0
        for i in range(NUM_ITER):
            # a,b,d,e
            coef_linear = np.random.uniform(-1.5, 1.5, size=4)
            # c, f
            coef_shift = np.random.uniform(-2, 2, size=2)
            if self._is_possible_coef(coef_linear):
                break
            ### may be problems should find default coefs which possible, also for test
            elif i == NUM_ITER - 1:
                count_not_normal += 1
                logger.debug(f"not_found normal coefs:{count_not_normal}")
                coef_linear = np.random.uniform(-0.25, 1, size=4)
                # c, f
                coef_shift = np.random.uniform(-0.5, 0.5, size=2)
        return CoefLinear(*coef_linear, *coef_shift)

    def get_list_linear_funcs(
        self, num_colors: int = NUM_COLORS
    ) -> List[Tuple[Color, Callable]]:
        colors: List[Color] = []
        if IS_FIXED_COLORS:
            colors = COLORS[:num_colors]
        else:
            for _ in range(num_colors):
                colors.append(random.choice(COLORS))
        list_color_linear_funcs = []

        if IS_FIXED_LINEAR:
            for color, coef in zip(colors, LINEAR_FUNCS[:num_colors]):
                list_color_linear_funcs.append((color, get_linear_func(color, coef)))
        else:
            for color in colors:
                coef = self._get_coef()
                list_color_linear_funcs.append((color, get_linear_func(color, coef)))

        return list_color_linear_funcs


def linear_transform(x, y, coef: CoefLinear):
    x_new = coef.A * x + coef.B * y + coef.C
    y_new = coef.D * x + coef.E * y + coef.F
    return x_new, y_new


def get_linear_func(coef: CoefLinear):
    return lambda x, y: linear_transform(x, y, coef)


LinearTransformGenerator().get_list_linear_funcs(num_colors=10)
