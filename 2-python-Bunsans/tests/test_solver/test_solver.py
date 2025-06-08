import contextlib
import filecmp
import os

import pytest
from src.mappers import solver_path_mapper
from src.structure_graph import Graph, Maze
from src.visual.renderer_ import Renderer

TMP_FILE = "./tests/test_solver/to_del_solver.txt"


@pytest.fixture(scope="function", autouse=True)
def del_file():
    filename = TMP_FILE
    yield
    if os.path.exists(filename):
        os.remove(filename)


def write_in_file(renderer: Renderer, maze: Maze, solve, path_test):
    with open(path_test, "w") as f, contextlib.redirect_stdout(f):
        renderer.print_maze_with_path(maze, solve)


@pytest.mark.usefixtures("del_file")
def test_solver_BFS_kruskal(renderer, maze_wo_surface_kruskal):
    graph = Graph(
        maze_wo_surface_kruskal,
        is_add_surface=True,
    )
    solver = solver_path_mapper["bfs"](graph)
    path = solver.solve((1, 1), (11, 15))

    path_test_local = "tests/test_solver/test_solver_BFS_kruskal.txt"
    path_test = TMP_FILE
    write_in_file(renderer, maze_wo_surface_kruskal, solve=path, path_test=path_test)
    result = filecmp.cmp(path_test, path_test_local)
    assert result


@pytest.mark.usefixtures("del_file")
def test_solver_dijkstra_kruskal(renderer, maze_with_surface_kruskal):
    graph = Graph(
        maze_with_surface_kruskal,
        is_add_surface=True,
    )
    solver = solver_path_mapper["dijkstra"](graph)
    path = solver.solve((1, 1), (11, 15))
    path_test_local = "tests/test_solver/test_solver_dijkstra_kruskal.txt"
    path_test = TMP_FILE
    write_in_file(renderer, maze_with_surface_kruskal, solve=path, path_test=path_test)
    result = filecmp.cmp(path_test, path_test_local)
    assert result


@pytest.mark.usefixtures("del_file")
def test_solver_BFS_prima(renderer, maze_wo_surface_prima):
    graph = Graph(
        maze_wo_surface_prima,
        is_add_surface=True,
    )
    solver = solver_path_mapper["bfs"](graph)
    path = solver.solve((1, 1), (11, 15))
    path_test_local = "tests/test_solver/test_solver_BFS_prima.txt"
    path_test = TMP_FILE
    write_in_file(renderer, maze_wo_surface_prima, solve=path, path_test=path_test)
    result = filecmp.cmp(path_test, path_test_local)
    assert result


@pytest.mark.usefixtures("del_file")
def test_solver_dijkstra_prima(renderer, maze_with_surface_prima):
    graph = Graph(
        maze_with_surface_prima,
        is_add_surface=True,
    )
    solver = solver_path_mapper["dijkstra"](graph)
    path = solver.solve((1, 1), (11, 15))

    path_test_local = "tests/test_solver/test_solver_dijkstra_prima.txt"
    path_test = TMP_FILE
    write_in_file(renderer, maze_with_surface_prima, solve=path, path_test=path_test)
    result = filecmp.cmp(path_test, path_test_local)
    assert result
