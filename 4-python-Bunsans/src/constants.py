from dataclasses import dataclass
import numpy as np


SEED = 1254
IS_FIXED_LINEAR = True
IS_FIXED_COLORS = True
NUM_COLORS = 5
SAMPLES_DEGREE = 3  # 10000
ITERATION_DEGREE = 2

COEF_SYMETRY = 10

SAMPLES = 2 * 10**SAMPLES_DEGREE
ITERATION = 4 * 1 * 10**ITERATION_DEGREE

RESOL_X_MAX = 1920
RESOL_Y_MAX = 1080

X_MAX = 1
Y_MAX = 1

X_MIN = -X_MAX
Y_MIN = -Y_MAX


GAMMA = 2.2


@dataclass
class Color:
    red: int
    green: int
    blue: int


COLORS = [
    Color(204, 51, 51),
    Color(254, 40, 162),
    Color(248, 23, 62),
    Color(255, 255, 255),
    Color(120, 81, 169),
    Color(153, 102, 204),
    Color(202, 44, 146),
    Color(255, 240, 245),
    Color(255, 229, 180),
    Color(230, 214, 144),
    Color(234, 224, 200),
    Color(202, 1, 71),
    Color(155, 45, 48),
    Color(227, 38, 54),
    Color(243, 71, 35),
    Color(229, 43, 80),
    Color(230, 230, 250),
    Color(253, 244, 227),
    Color(245, 255, 250),
    Color(245, 245, 220),
    Color(250, 235, 215),
    Color(255, 255, 255),
    Color(62, 180, 137),
    Color(80, 200, 120),
    Color(172, 229, 238),
    Color(204, 204, 255),
    Color(144, 0, 32),
    Color(72, 6, 7),
    Color(189, 51, 164),
    Color(169, 32, 62),
    Color(196, 30, 58),
    Color(219, 112, 147),
    Color(246, 100, 175),
    Color(220, 20, 60),
    Color(114, 115, 161),
    Color(199, 252, 236),
    Color(134, 115, 161),
    Color(42, 100, 120),
    Color(218, 112, 214),
    Color(204, 119, 34),
    Color(0, 168, 107),
    Color(218, 112, 214),
    Color(50, 18, 122),
    Color(254, 40, 162),
    Color(248, 23, 62),
    Color(128, 0, 128),
    Color(37, 109, 123),
    Color(0, 166, 147),
    Color(50, 18, 122),
    Color(33, 66, 30),
    Color(153, 51, 102),
    Color(37, 109, 123),
    Color(116, 66, 200),
    Color(65, 105, 225),
]


@dataclass
class CoefLinear:
    A: float
    B: float
    C: float
    D: float
    E: float
    F: float


LINEAR_FUNCS = [
    CoefLinear(
        A=np.float64(-0.2639242918266681),
        B=np.float64(0.3337399590577439),
        C=np.float64(-0.06683381786995135),
        D=np.float64(0.7295615603691242),
        E=np.float64(0.8092738890916427),
        F=np.float64(1.025070821411307),
    ),
    CoefLinear(
        A=np.float64(-0.23817338261738208),
        B=np.float64(-0.05444324897510755),
        C=np.float64(0.05371500287868014),
        D=np.float64(-0.9124018867273085),
        E=np.float64(0.10230556286736014),
        F=np.float64(0.5398881430488807),
    ),
    CoefLinear(
        A=np.float64(0.6340415760008229),
        B=np.float64(-0.35697898892695623),
        C=np.float64(-0.18216996680244402),
        D=np.float64(-0.4243261345681182),
        E=np.float64(0.5987411267990277),
        F=np.float64(-0.8616729227951097),
    ),
    CoefLinear(
        A=np.float64(-0.1709933950933129),
        B=np.float64(-0.21438693140500786),
        C=np.float64(0.23095919929685815),
        D=np.float64(0.5123335113436892),
        E=np.float64(-1.6382565170220076),
        F=np.float64(-0.782774436065635),
    ),
    CoefLinear(
        A=np.float64(0.22564273120471445),
        B=np.float64(-0.8597876948314338),
        C=np.float64(0.541242363103679),
        D=np.float64(0.39178715922189833),
        E=np.float64(1.9476918083341466),
        F=np.float64(1.0476663211150514),
    ),
    CoefLinear(
        A=np.float64(-0.4351665155683563),
        B=np.float64(0.12205230061165806),
        C=np.float64(-0.2919803799592151),
        D=np.float64(-0.141735313720738),
        E=np.float64(-0.04061728095223893),
        F=np.float64(0.5429558468197562),
    ),
    CoefLinear(
        A=np.float64(-0.42391064484243945),
        B=np.float64(-0.5839416191271956),
        C=np.float64(0.010508268116427355),
        D=np.float64(-0.7493569623060254),
        E=np.float64(0.531799728003385),
        F=np.float64(-0.9310359339236753),
    ),
    CoefLinear(
        A=np.float64(0.31724825907903464),
        B=np.float64(-0.23282167201769277),
        C=np.float64(-0.20531501286997256),
        D=np.float64(-0.8517268500445438),
        E=np.float64(-0.24319518811699892),
        F=np.float64(0.301063752202118),
    ),
    CoefLinear(
        A=np.float64(-0.6095144346197353),
        B=np.float64(-0.15830649130608254),
        C=np.float64(-0.04038328139393099),
        D=np.float64(0.5466843247405506),
        E=np.float64(0.8690415784724008),
        F=np.float64(-0.26393750258783566),
    ),
    CoefLinear(
        A=np.float64(0.25710889016812266),
        B=np.float64(-0.7116771809297668),
        C=np.float64(-0.09965647519677945),
        D=np.float64(-0.6125547971627259),
        E=np.float64(1.7298415346001295),
        F=np.float64(-1.6351763836167081),
    ),
]
