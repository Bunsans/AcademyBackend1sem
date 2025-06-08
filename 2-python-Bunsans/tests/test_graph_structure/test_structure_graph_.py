import contextlib
import os
import pytest

from src.structure_graph import Maze
from src.visual.renderer_ import Renderer
import filecmp
from src.symbols import SurfaceTypes, PathGraphics


TMP_FILE = "./tests/test_graph_structure/to_del_maze_change_color.txt"


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
    "path_test_local, to_change, symbol",
    [
        ("./tests/test_graph_structure/case_maze_full.txt", [], PathGraphics.PATH),
        (
            "./tests/test_graph_structure/case_maze_1_1_empty.txt",
            [(1, 1)],
            SurfaceTypes.EMPTY.symbol,
        ),
        (
            "./tests/test_graph_structure/case_maze_path_2_cell.txt",
            [(1, 1), (2, 2)],
            SurfaceTypes.SAND.symbol,
        ),
    ],
)
def test_change_color(
    path_test_local,
    to_change,
    symbol,
    maze,
    renderer,
):
    path_test = TMP_FILE
    maze.change_color(to_change, type=symbol)
    write_in_file(renderer, maze, path_test)
    result = filecmp.cmp(path_test, path_test_local)
    assert result
