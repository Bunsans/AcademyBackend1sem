import itertools
import random
from time import sleep
from loguru import logger

from src.structure_graph import Maze
from src.visual.renderer_ import Renderer

from src.symbols import (
    SLEEP_TIME_GENERATE,
    WEIGHT_BLACK,
    WEIGHT_SAND,
    WEIGHT_GOOD,
    DEBUG,
    RANDOM_SEED,
    SurfaceTypes,
)

from abc import ABC, abstractmethod

random.seed(13)


class Generator(ABC):
    """Класс генерации лабиринта."""

    maze: Maze

    def set_random_seed(self, seed_=RANDOM_SEED):
        random.seed(seed_)

    def change_color(
        self,
        to_change,
        type=SurfaceTypes.EMPTY.symbol,
        weight=WEIGHT_BLACK,
    ):
        self.maze.change_color(to_change, type=type, weight=weight)

    def get_begin_pos(self):
        begin_pos = (
            random.choice([i for i in range(self.row_max - 2) if i % 2 == 1]),
            random.choice([i for i in range(self.col_max - 2) if i % 2 == 1]),
        )
        return begin_pos

    def _set_walls_and_nodes(self):
        self.maze.set_walls_and_nodes(visited=self.visited, betweneers=self.betweeners)

    def _make_not_ideal_maze(self):
        self._break_walls()
        self._add_surface()

    def _break_walls(self):
        num_break = int(len(self.maze.walls) / 10)
        breaked = {random.choice(list(self.maze.walls)) for _ in range(num_break)}
        self.maze.walls -= breaked
        self.maze.nodes |= breaked
        self.change_color(to_change=breaked, type=SurfaceTypes.EMPTY.symbol)

    def _add_surface(self):
        num_sand = int(len(self.maze.nodes) / 20)
        num_good = int(len(self.maze.nodes) / 20)
        sand = [random.choice(list(self.maze.nodes)) for _ in range(num_sand)]
        self.change_color(
            to_change=sand, type=SurfaceTypes.SAND.symbol, weight=WEIGHT_SAND
        )
        good = [random.choice(list(self.maze.nodes)) for _ in range(num_good)]
        self.change_color(
            to_change=good, type=SurfaceTypes.GOOD.symbol, weight=WEIGHT_GOOD
        )

    def print_progress(self, renderer: Renderer):
        renderer.print_progress_generation(self.maze, time_sleep=SLEEP_TIME_GENERATE)

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate(self) -> Maze:
        """Сгенерировать лабириринт."""
        pass


class PrimGenerator(Generator):
    """Генератор Прима."""

    maze: Maze

    def __init__(self, row_max, col_max):

        self.row_max = row_max
        self.col_max = col_max
        self.candidates = dict()
        self.visited = set()
        self.betweeners = set()
        self.maze = Maze(row_max, col_max)
        # init begin pos
        begin_pos = self.get_begin_pos()
        self.maze.set_type(*begin_pos, SurfaceTypes.EMPTY.symbol)
        self.visited.add(begin_pos)
        self._add_candidates_pos(*begin_pos)
        if DEBUG:
            logger.info(f"Begin pos: {begin_pos}")
            logger.info(f"set_visited: {self.visited}")

    def _add_candidates_pos(self, row, col) -> dict[tuple:list]:
        """
        vector of direction from (row, col) to this candidate
        "left" "right" "up" "down"
        """
        neighbours = {
            (row, col - 2): ["left"],
            (row, col + 2): ["right"],
            (row - 2, col): ["up"],
            (row + 2, col): ["down"],
        }
        for pos, direct in neighbours.items():
            if self.maze.is_inside(*pos) and (pos not in self.visited):
                if pos not in self.candidates:
                    self.candidates[pos] = direct
                else:
                    self.candidates[pos] += direct

    def _get_between(self, row, col, direct):
        if direct == "left":
            return (row, col + 1)
        elif direct == "right":
            return (row, col - 1)
        elif direct == "up":
            return (row + 1, col)
        elif direct == "down":
            return (row - 1, col)

    def generate(self, renderer, is_add_surface) -> Maze:
        """Сгенерировать лабириринт."""
        if DEBUG:
            logger.info(
                f"Candidates: {self.maze.candidates}\nVasited: {self.maze.visited}\n"
            )

        while self.candidates:
            self.print_progress(renderer)
            if DEBUG:
                sleep(SLEEP_TIME_GENERATE)
                renderer.print_matrix(self.maze)
                sleep(SLEEP_TIME_GENERATE)

            pos, directs = random.choice(list(self.candidates.items()))
            self.candidates.pop(pos)
            self.maze.set_type(*pos, SurfaceTypes.EMPTY.symbol)
            self.visited.add(pos)
            if DEBUG:
                sleep(SLEEP_TIME_GENERATE)
                renderer.print_matrix(self.maze)
                sleep(SLEEP_TIME_GENERATE)
            # update +- 1
            direct = random.choice(directs)
            pos_between = self._get_between(*pos, direct)
            self.maze.set_type(*pos_between, SurfaceTypes.EMPTY.symbol)
            self.betweeners.add(pos_between)
            # update candidates
            self._add_candidates_pos(*pos)

        self._set_walls_and_nodes()
        if is_add_surface:
            self._make_not_ideal_maze()

        return self.maze


class KruskalGenerator(Generator):
    """Генератор краскал."""

    def __init__(self, row_max, col_max):
        self.row_max = row_max
        self.col_max = col_max
        self.candidates = dict()
        self.visited = set()
        self.betweeners = set()
        self.maze = Maze(row_max, col_max)
        begin_pos = self.get_begin_pos()
        self.maze.set_type(*begin_pos, type=SurfaceTypes.EMPTY.symbol)

    def _get_neighbours(self, row, col):
        neighbours = [
            (row, col + 2),
            (row + 2, col),
        ]
        return [pos for pos in neighbours if self.maze.is_inside(*pos)]

    def _find_list_set(self, row, col):
        """
        Find index in list of spans(sets), in which span
        """
        for i, nodes_set in enumerate(self.min_spans):
            if (row, col) in nodes_set:
                return i
        return None

    def _get_between(self, node_1, node_2):
        return int((node_1[0] + node_2[0]) / 2), int((node_1[1] + node_2[1]) / 2)

    def generate(self, renderer: Renderer, is_add_surface) -> Maze:
        """Сгенерировать лабиринт."""
        # preparing
        # rename to visited
        nodes = list(
            itertools.product(
                [i for i in range(self.row_max) if i % 2 == 1],
                [i for i in range(self.col_max) if i % 2 == 1],
            )
        )
        for node in nodes:
            self.maze.set_type(*node, type=SurfaceTypes.EMPTY.symbol)
            self.visited.add(node)
        self.edges = []
        for node in nodes:
            for neighbour in self._get_neighbours(*node):
                self.edges.append((neighbour, node))
        random.shuffle(self.edges)
        # min_spans -- list of spans (as type set)
        self.min_spans = list(map(lambda v: set([v]), nodes))
        # start generating
        for node_1, node_2 in self.edges:
            renderer.print_progress_generation(
                self.maze, time_sleep=SLEEP_TIME_GENERATE
            )

            if len(self.min_spans) == 1:
                break
            node_1_indx = self._find_list_set(*node_1)
            node_2_indx = self._find_list_set(*node_2)
            if (
                node_1_indx is not None
                and node_2_indx is not None
                and node_1_indx != node_2_indx
            ):
                # union in first
                self.min_spans[node_1_indx] = self.min_spans[node_1_indx].union(
                    self.min_spans[node_2_indx]
                )
                # remove second
                self.min_spans.pop(node_2_indx)
                pos_between = self._get_between(node_1, node_2)
                self.betweeners.add(pos_between)
                self.maze.set_type(*pos_between, SurfaceTypes.EMPTY.symbol)

        self._set_walls_and_nodes()
        if is_add_surface:
            self._make_not_ideal_maze()
        return self.maze
