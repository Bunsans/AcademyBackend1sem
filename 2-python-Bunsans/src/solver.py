from abc import ABC, abstractmethod
import sys
from collections import deque
from src.structure_graph import Graph


class Solver(ABC):
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    @abstractmethod
    def solve(self, start_node, final_node):
        pass

    def get_neighbours(self, row, col):
        return self.graph.get_neighbours(row, col)

    def get_cell(self, row, col):
        return self.graph.maze.get_cell(row, col)


class SolverBFS(Solver):
    def solve(self, start_node, final_node):
        queue = deque([(start_node, [start_node])])
        while queue:
            current_node, path = queue.popleft()
            neighbors = self.get_neighbours(*current_node)
            for node in set(neighbors) - set(path):
                if node == final_node:
                    return path + [node]
                else:
                    queue.append((node, path + [node]))


class SolverDijkstra(Solver):
    def get_unvisited_nodes(self):
        return self.graph.maze.nodes

    def solve(self, start_node, final_node):
        unvisited_nodes = self.get_unvisited_nodes()
        shortest_path = {}
        previous_nodes = {}
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        shortest_path[start_node] = 0
        while unvisited_nodes:
            current_min_node = None
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node is None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node
            neighbors = self.get_neighbours(*current_min_node)
            for neighbor in neighbors:
                tentative_value = (
                    shortest_path[current_min_node] + self.get_cell(*neighbor).weight
                )
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    previous_nodes[neighbor] = current_min_node
            unvisited_nodes.remove(current_min_node)
        path = []
        node = final_node

        while node != start_node:
            path.append(node)
            node = previous_nodes[node]
        return list(reversed(path[1:]))
