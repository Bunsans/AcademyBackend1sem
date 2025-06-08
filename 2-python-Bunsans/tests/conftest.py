import pytest

from src.structure_graph import Maze
from src.visual.menu_ import MenuVisualizer
from src.visual.renderer_ import Renderer
from src.generate_maze import PrimGenerator, KruskalGenerator

RANDOM = 13


@pytest.fixture(scope="session", autouse=True)
def menu_vsiualizer():
    return MenuVisualizer()


@pytest.fixture(scope="session", autouse=True)
def maze():
    return Maze(row_max=13, col_max=17)


@pytest.fixture(scope="session", autouse=True)
def renderer():
    return Renderer(False)


@pytest.fixture(scope="function", autouse=True)
def generator_prima():
    generator_prima_ = PrimGenerator(13, 17)
    generator_prima_.set_random_seed(RANDOM)
    return generator_prima_


@pytest.fixture(scope="function", autouse=True)
def generator_kruskal():
    generator_kruskal_ = KruskalGenerator(13, 17)
    generator_kruskal_.set_random_seed(RANDOM)
    return generator_kruskal_


@pytest.fixture(scope="function", autouse=False)
def maze_with_surface_kruskal(generator_kruskal, renderer):
    maze = generator_kruskal.generate(renderer, is_add_surface=True)
    maze.set_begin(1, 1)
    maze.set_final(11, 15)
    return maze


@pytest.fixture(scope="function", autouse=False)
def maze_with_surface_prima(generator_prima, renderer):
    maze = generator_prima.generate(renderer, is_add_surface=True)
    maze.set_begin(1, 1)
    maze.set_final(11, 15)
    return maze


@pytest.fixture(scope="function", autouse=False)
def maze_wo_surface_kruskal(generator_kruskal, renderer):
    maze = generator_kruskal.generate(renderer, is_add_surface=False)
    maze.set_begin(1, 1)
    maze.set_final(11, 15)
    return maze


@pytest.fixture(scope="function", autouse=False)
def maze_wo_surface_prima(generator_prima, renderer):
    maze = generator_prima.generate(renderer, is_add_surface=False)
    maze.set_begin(1, 1)
    maze.set_final(11, 15)
    return maze
