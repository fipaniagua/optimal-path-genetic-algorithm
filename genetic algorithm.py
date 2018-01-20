from graph import Graph, Node, Path
from random import random
from copy import copy

class Pool:

    def __init__(self, graph, n, start, end):
        self.graph = graph
        self.n = n
        self.paths = []
        self.start = start
        self.end = end
        self.solution = None
        self.max = 0

    def generate_initial_population(self):
        for i in range(self.n):
            new_path = Path(self.graph.get_random_path(self.start, self.end, bsearch = True))
            self.paths.append(new_path)

    def normalize_scores(self):
        new_solution = max(self.paths, key = lambda path: path.score)
        if new_solution.score > self.max:
            self.max = new_solution.score
            self.solution = new_solution
        for path in self.paths:
            path.normalize(self.max)

    def add_probabilities(self):
        total_score = sum(path.score for path in self.paths)
        for path in self.paths:
            path.add_probability(total_score)

    def pick_one(self):
        index = 0
        r = random()
        while r > 0:
            r -= self.paths[index].prob
            index += 1
        return self.paths[index-1].nodes

    def generate_new_population(self):
        news_paths = []
        for i in range(self.n):
            new_path = Path(copy(self.pick_one()))
            new_path = self.graph.mutate_path(new_path)
            news_paths.append(new_path)

        self.paths = news_paths

    def run(self):

        previus_max = 0
        self.generate_initial_population()
        print(sum(path.score for path in self.paths))
        self.normalize_scores()
        self.add_probabilities()
        while self.max != previus_max:
            previus_max = self.max
            self.generate_new_population()
            print(sum(path.score for path in self.paths))
            self.normalize_scores()
            self.add_probabilities()



if __name__ == "__main__":
    region = Graph()

    region.add_node(Node("4", 6))
    region.add_node(Node("1", 1))
    region.add_node(Node("2", 10))
    region.add_node(Node("3", 9))
    region.add_node(Node("6", 8))
    region.add_node(Node("7", 7))
    region.add_node(Node("5", 5))
    region.add_node(Node("8", 1))
    region.add_node(Node("9", 4))
    region.add_node(Node("10", 10))
    region.add_node(Node("11", 1))
    region.add_connection("1", "2", 4)
    region.add_connection("1", "3", 3)
    region.add_connection("1", "4", 1)
    region.add_connection("3", "4", 1)
    region.add_connection("3", "6", 8)
    region.add_connection("6", "8", 1)
    region.add_connection("2", "7", 1)
    region.add_connection("2", "5", 2)
    region.add_connection("7", "5", 1)
    region.add_connection("7", "8", 4)
    region.add_connection("5", "8", 1)
    region.add_connection("3", "7", 2)
    region.add_connection("10", "2", 2)
    region.add_connection("9", "6", 1)
    region.add_connection("11", "8", 2)
    region.add_connection("4", "6", 3)
    region.add_connection("4", "9", 1)
    region.sort_nodes()

    pool = Pool(region, 5, "1", "8")
    pool.run()
