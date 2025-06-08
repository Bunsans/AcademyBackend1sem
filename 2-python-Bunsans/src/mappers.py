from typing import Dict
from src.solver import Solver, SolverBFS, SolverDijkstra
from src.generate_maze import Generator, PrimGenerator, KruskalGenerator

mapper_generator_maze_mapper: Dict[str, Generator] = {
    "prima": PrimGenerator,
    "kruskal": KruskalGenerator,
}

type_solver_mapper = {True: "dijkstra", False: "bfs"}
solver_path_mapper: Dict[str, Solver] = {"bfs": SolverBFS, "dijkstra": SolverDijkstra}
