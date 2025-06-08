from src.structure_graph import Maze
from src.symbols import SLEEP_TIME_GENERATE, SLEEP_TIME_PATH, PathGraphics, SurfaceTypes

# random.seed = 123


import os
from time import sleep


class Renderer:
    """
    Class for visual in CLI maze
    """

    def __init__(self, is_show_progress: bool = False):
        self.is_show_progress = is_show_progress

    def _print_num_border(self, col_or_row, col_or_row_max):
        if 1 <= col_or_row < col_or_row_max - 1:
            print(str(col_or_row).rjust(2), end="")
        else:
            print(SurfaceTypes.EMPTY.symbol, end="")

    def _is_path(self, row_col, path):
        if path:
            if row_col in path:
                return True
        return False

    def _print_type_or_path(self, row, col, cell_type, path_set: set):

        if (
            self._is_path((row, col), path_set)
            and cell_type == SurfaceTypes.EMPTY.symbol
        ):
            print(PathGraphics.PATH, end="", sep="")
        else:
            print(cell_type, end="", sep="")

    def print_maze(self, maze: Maze, path: list = None):
        if path:
            path = set(path)
        os.system("clear")
        print(SurfaceTypes.EMPTY.symbol, end="")
        for col in range(maze.col_max):
            self._print_num_border(col, maze.col_max)
        print()
        for row in range(maze.row_max):
            self._print_num_border(row, maze.row_max)
            for col in range(maze.col_max):
                cell_type = maze.get_cell(row, col).type
                self._print_type_or_path(row, col, cell_type, path)
            print()

    def print_progress_generation(self, maze: Maze, time_sleep=SLEEP_TIME_GENERATE):
        if self.is_show_progress:
            sleep(time_sleep)
            self.print_maze(maze)
        else:
            pass

    def print_maze_with_path(self, maze: Maze, path: list):
        if self.is_show_progress:
            for i in range(len(path)):
                sleep(SLEEP_TIME_PATH)
                self.print_maze(maze, path[: i + 1])
        else:
            self.print_maze(maze, path)
