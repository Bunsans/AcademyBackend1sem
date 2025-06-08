import numpy as np
from numpy import sin, cos
from constants import SEED, X_MAX, Y_MAX

np.random.seed(SEED)


def _theta(x, y):
    arctan = np.arctan(x / y)
    return arctan


def _radius(x, y):
    return np.sqrt(x**2 + y**2)


def _fi(x, y):
    arctan = np.arctan(y / x)
    return arctan


def non_linear_(x, y, linear_coefs=None):
    return x, y


def non_linear_sphere(x, y, linear_coefs=None):
    r_2 = x**2 + y**2
    return x / r_2, y / r_2


def non_linear_heart(x, y, linear_coefs=None):
    # x *= 0.8
    # y *= 0.8
    r = _radius(x, y)
    theta_ = _theta(x, y)
    return 0.5 * r * sin(theta_ * r), 0.5 * -r * cos(theta_ * r)


def non_linear_polar(x, y, linear_coefs=None):
    r = _radius(x, y)
    theta_ = _theta(x, y)
    x = theta_ / np.pi * 2 * X_MAX
    y = r - Y_MAX
    return x, y


def non_linear_sin(x, y, linear_coefs=None):
    return np.sin(x), np.sin(y)


def non_linear_swirl(x, y, linear_coefs=None):
    # x *= 0.5
    # y *= 0.5
    r_2 = x**2 + y**2
    return x * np.sin(r_2) - y * np.cos(r_2), x * np.cos(r_2) + y * np.sin(r_2)


def non_linear_horseshoe(x, y, linear_coefs=None):
    r = np.sqrt(x**2 + y**2)
    return 1 / r * (x - y) * (x + y), 1 / r * 2 * x * y


def non_linear_disk(x, y, linear_coefs=None):
    arctan = np.arctan(y / x)
    r = np.sqrt(x**2 + y**2)
    return 1 / np.pi * arctan * np.sin(np.pi * r), 1 / np.pi * arctan * np.cos(
        np.pi * r
    )


def non_linear_hyperbolic(x, y, linear_coefs=None):
    theta_ = _theta(x, y)
    r = _radius(x, y)
    return np.sin(theta_) / r, r * np.sin(theta_)  # 0.8 * Y_MAX *  0.8 * X_MAX *


# @rotate_90
# def non_linear_hyperbolic_rotate_90(x, y):
#     x, y = non_linear_hyperbolic(x, y)
#     return x, y  # 0.8 * Y_MAX *  0.8 * X_MAX *


# @rotate_120
# def non_linear_hyperbolic_rotate_120(x, y):
#     x, y = non_linear_hyperbolic(x, y)
#     return x, y


def non_linear_diamond(x, y, linear_coefs=None):
    theta_ = _theta(x, y)
    r = _radius(x, y)
    return sin(theta_) * cos(r), sin(r) * cos(theta_)


# @rotate_120
# def non_linear_diamond_rotate_120(x, y):
#     x, y = non_linear_diamond(x, y)
#     return x, y


def non_linear_fisheye(x, y, linear_coefs=None):
    r = _radius(x, y)
    x, y = 2 * y / (r + 1), 2 * x / (r + 1)
    return x, y


# @rotate_120
# def non_linear_fisheye_rotate_120(x, y):
#     x, y = non_linear_fisheye(x, y)
#     return x, y


def non_linear_EX(x, y, linear_coefs=None):
    theta_ = _theta(x, y)
    r = _radius(x, y)
    p_0 = sin(theta_ + r)
    p_1 = cos(theta_ - r)
    return r * (p_0**3 + p_1**3), r * (p_0**3 - p_1**3)


# @rotate_120
# def non_linear_EX_rotate_120(x, y):
#     x, y = non_linear_EX(x, y)
#     return x, y


# not interesting
possible_shift = np.random.uniform(-1, 1, size=4)


def non_linear_blur(x, y, linear_coefs=None):
    psi_1 = np.random.uniform(0, 1)
    psi_2 = np.random.uniform(0, 1)
    shift_x = np.random.choice(possible_shift)
    shift_y = np.random.choice(possible_shift)
    return shift_x + psi_1 * cos(2 * np.pi * psi_2), shift_y + psi_1 * sin(
        2 * np.pi * psi_2
    )


def non_linear_exponential(x, y, linear_coefs=None):
    exp_ = np.exp(x - 1)
    return exp_ * cos(np.pi * y), exp_ * sin(np.pi * y)


def non_linear_julia(x, y, linear_coefs=None):
    # √r · (cos(θ/2 + Ω),sin(θ/2 + Ω)
    r = _radius(x, y)
    sq_r = np.sqrt(r)
    Omega = np.random.choice([0, np.pi])
    theta_ = _theta(x, y)
    return sq_r * cos(theta_ / 2 + Omega), sq_r * sin(theta_ / 2 + Omega)


# @rotate_90
# def non_linear_julia_rotate_90(x, y):
#     # √r · (cos(θ/2 + Ω),sin(θ/2 + Ω)
#     x, y = non_linear_julia(x, y)
#     return x, y


# @rotate_120
# def non_linear_julia_rotate_120(x, y):
#     # √r · (cos(θ/2 + Ω),sin(θ/2 + Ω)
#     x, y = non_linear_julia(x, y)
#     return x, y


# @rotate_180
# def non_linear_julia_rotate_180(x, y):
#     # √r · (cos(θ/2 + Ω),sin(θ/2 + Ω)
#     x, y = non_linear_julia(x, y)
#     return x, y


def non_linear_popcorn_depended(x, y, linear_coefs):
    C = linear_coefs.C
    F = linear_coefs.F
    return (x + C * sin(np.tan(3 * y)), y + F * sin(np.tan(3 * x)))


def non_linear_waves_depended(x, y, linear_coefs):
    B = linear_coefs.B
    C = linear_coefs.C
    E = linear_coefs.E
    F = linear_coefs.F
    return (x + B * sin(y / (C**2)), y + E * sin(x / (F**2)))


non_liniear_funcs = [
    # non_linear_,
    # non_linear_diamond,
    non_linear_sphere,
    # non_linear_heart,
    # non_linear_blur,
    # non_linear_disk,
    # non_linear_swirl,
    # non_linear_horseshoe,
    # non_linear_polar,
    # non_linear_fisheye,
    non_linear_hyperbolic,
    # non_linear_EX,
    # non_linear_blur,
    # non_linear_exponential,
    # non_linear_julia,
    # non_linear_popcorn_depended,
    # non_linear_waves_depended,
]  # non_liniear_funcs
