import contextlib
import os
import pytest

from src.structure_graph import Maze
from src.visual.renderer_ import Renderer
import filecmp


TMP_FILE = "./tests/test_graph_structure/to_del_generator_prima.txt"


@pytest.fixture(scope="function", autouse=True)
def del_file():
    filename = TMP_FILE
    yield
    if os.path.exists(filename):
        os.remove(filename)


def write_in_file(renderer: Renderer, maze: Maze, path_test):
    with open(path_test, "w") as f, contextlib.redirect_stdout(f):
        renderer.print_maze(maze)


@pytest.mark.usefixtures("del_file")
@pytest.mark.parametrize(
    "path_test_local, is_add_surface",
    [
        ("./tests/test_generate/case_generator_prima_with_surface.txt", True),
        ("./tests/test_generate/case_generator_prima.txt", False),
    ],
)
def test_generator_prima(
    path_test_local,
    is_add_surface,
    renderer,
    generator_prima,
):
    path_test = TMP_FILE
    maze = generator_prima.generate(renderer, is_add_surface=is_add_surface)
    renderer.print_maze(maze)

    write_in_file(renderer, maze, path_test)
    result = filecmp.cmp(path_test, path_test_local)
    assert result


@pytest.mark.usefixtures("del_file")
@pytest.mark.parametrize(
    "path_test_local, is_add_surface",
    [
        ("./tests/test_generate/case_generator_kruskal_with_surface.txt", True),
        ("./tests/test_generate/case_generator_kruskal.txt", False),
    ],
)
def test_generator_kruskal(
    path_test_local,
    is_add_surface,
    renderer,
    generator_kruskal,
):
    path_test = TMP_FILE
    maze = generator_kruskal.generate(renderer, is_add_surface=is_add_surface)
    renderer.print_maze(maze)

    write_in_file(renderer, maze, path_test)
    result = filecmp.cmp(path_test, path_test_local)
    assert result
