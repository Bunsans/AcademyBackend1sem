import itertools
from typing import Iterable, Tuple
from loguru import logger
from src.symbols import (
    DEBUG,
    Borders,
    SurfaceTypes,
    PathGraphics,
)


class Cell:
    """
    contain:
        type
        pos in matrix
        weight
    """

    def __init__(self, row, col, type=Borders.INNER, weight=SurfaceTypes.EMPTY.weight):
        self.type = type
        self.row = row
        self.col = col
        self.weight = weight

    def set_type(self, type):
        self.type = type

    def set_weight(self, weight):
        self.weight = weight


class Maze:
    """
    Maze with size: width, lengh
    """

    nodes: set
    walls: set

    def __init__(self, row_max, col_max):
        self.row_max = row_max
        self.col_max = col_max
        self.maze = [
            [Cell(row=y, col=x) for x in range(col_max)] for y in range(row_max)
        ]
        self._set_border()
        if DEBUG:
            logger.info(f"Matrix: {self.all_matrix_pos}")
        if DEBUG:
            logger.info(f"Matrix: {self.walls}")

    def _set_border(self):
        """
        (0, :), (:, 0), (row_max - 1, :), (:, col_max)
        """
        border = (
            [(0, i) for i in range(self.col_max)]
            + [(self.row_max - 1, i) for i in range(self.col_max)]
            + [(i, 0) for i in range(self.row_max)]
            + [(i, self.col_max - 1) for i in range(self.row_max)]
        )
        if DEBUG:
            logger.info(f"border: {border}")
        for pos in border:
            self.get_cell(*pos).set_type(Borders.OUTER)

    def set_type(self, row, col, type):
        self.get_cell(row, col).set_type(type)

    def set_begin(self, row, col):
        self.set_type(row, col, PathGraphics.START_POINT)

    def set_final(self, row, col):
        self.set_type(row, col, PathGraphics.END_POINT)

    def set_walls_and_nodes(self, visited: set, betweneers: set):
        all_matrix_pos = set(
            itertools.product(
                [i for i in range(1, self.row_max - 1)],
                [i for i in range(1, self.col_max - 1)],
            )
        )
        self.nodes = visited | betweneers
        self.walls = all_matrix_pos - self.nodes

    def get_cell(self, row, col) -> Cell:
        return self.maze[row][col]

    def change_color(
        self,
        to_change: Iterable[Tuple[int, int]],
        type=PathGraphics.PATH,
        weight=SurfaceTypes.EMPTY.weight,
    ):
        """ """
        for pos in to_change:
            cell = self.get_cell(*pos)
            if type == PathGraphics.PATH and cell.type != SurfaceTypes.EMPTY.symbol:
                continue
            cell.set_type(type)
            cell.set_weight(weight)

    def is_inside(self, row, col):
        """Check is in border"""
        if row < self.row_max - 1 and row > 0 and col > 0 and col < self.col_max - 1:
            return True
        else:
            return False


class Graph:
    def __init__(
        self,
        maze: Maze,
        is_add_surface: bool = False,
    ):
        self.maze = maze
        self.is_add_surface = is_add_surface
        self.visited_in_graph = set()

    def add_visited(self, row, col):
        self.visited_in_graph.add((row, col))

    def get_neighbours(self, row, col):
        neighbours = [
            (row, col - 1),
            (row, col + 1),
            (row - 1, col),
            (row + 1, col),
        ]
        return [n for n in neighbours if n in self.maze.nodes]
