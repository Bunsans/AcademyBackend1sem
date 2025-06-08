from enum import StrEnum
from typing import NamedTuple

RANDOM_SEED = 123

DEBUG = False
SLEEP_TIME_GENERATE = 0.05
SLEEP_TIME_ADD_SURFACE = 0.3
SLEEP_TIME_PATH = 0.3

WEIGHT_BLACK = 50
WEIGHT_SAND = 100
WEIGHT_GOOD = 1


class Surface(NamedTuple):
    """Свойства поверхности."""

    weight: int
    symbol: str


class SurfaceTypes:
    """Типы поверхностей."""

    EMPTY = Surface(weight=50, symbol="  ")
    GOOD = Surface(weight=1, symbol="🟪")
    SAND = Surface(weight=100, symbol="🟫")


class Borders(StrEnum):
    """Типы стен."""

    OUTER = "🟦"
    INNER = "⬜️"


class PathGraphics(StrEnum):
    """Графика пути."""

    PATH = "🟩"
    START_POINT = "🔻"
    END_POINT = "✅"
