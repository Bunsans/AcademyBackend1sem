import logging

from src.generate_maze import Generator
from src.structure_graph import Graph, Maze
from src.visual.menu_ import MenuVisualizer
from src.mappers import (
    mapper_generator_maze_mapper,
    type_solver_mapper,
    solver_path_mapper,
)
from src.solver import Solver
import pickle

from src.visual.renderer_ import Renderer


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    menu_visualizer = MenuVisualizer()
    pos_max, is_add_surface, is_show_progress, type_of_generation = (
        menu_visualizer.show_menu()
    )
    generator: Generator = mapper_generator_maze_mapper[type_of_generation](*pos_max)
    renderer = Renderer(is_show_progress)
    maze: Maze = generator.generate(renderer, is_add_surface=is_add_surface)
    begin, final = menu_visualizer.show_choose_begin_final(*pos_max, renderer, maze)
    maze.set_begin(*begin)
    maze.set_final(*final)
    renderer.print_maze(maze)

    with open("./maze.pickle", "wb") as f:
        pickle.dump(maze, f)

    graph = Graph(
        maze,
        is_add_surface=is_add_surface,
    )
    type_solver = type_solver_mapper[is_add_surface]
    solver: Solver = solver_path_mapper[type_solver](graph)

    path = solver.solve(begin, final)
    renderer.print_maze_with_path(maze, path)


if __name__ == "__main__":
    main()
