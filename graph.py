import copy
from random import shuffle, random

class Node:

    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.links= []

    def add_connection(self, node, distance):
        self.links.append((node, distance))

    def __repr__(self):
        return self.name

class Path:

    def __init__(self, nodes):
        self.nodes = nodes
        self.score = self.calculate_value()
        self.length = len(nodes)
        self.normalize_score = None
        self.prob = None


    def calculate_value(self):
        total_score = 0
        for node in self.nodes:
            total_score += node.score
        return total_score

    def normalize(self, max_score):
        self.normalize_score = self.score/max_score

    def add_probability(self, total_score):
        self.prob = self.score / total_score

class Graph:

    def __init__(self):
        self.nodes = []

    def add_node(self, new_node):
        self.nodes.append(new_node)

    #this function is implemented to use before use binary_search function
    def sort_nodes(self):
        self.nodes.sort(key = lambda node: node.name)

    def find_node(self, node_name, bsearch= False):
        if bsearch:
            return self.binary_search(node_name, 0, len(self.nodes)-1)

        for node in self.nodes:
            if node.name == node_name:
                return node
        return None

    def binary_search(self, node_name, s, e):
        current_index = (s+e)//2
        #base cases
        if node_name == self.nodes[current_index].name:
            return self.nodes[current_index]
        elif s >= e:
            return None

        #Recurrent cases
        if node_name > self.nodes[current_index].name:
            return self.binary_search(node_name, current_index + 1, e)
        elif node_name < self.nodes[current_index].name:
            return self.binary_search(node_name, s, current_index - 1)

    def add_connection(self, node_name1, node_name2, distance):
        node1 = self.find_node(node_name1)
        node2 = self.find_node(node_name2)
        node1.add_connection(node2, distance)
        node2.add_connection(node1, distance)

    #this function get the first random path that see in deep first search
    def get_random_path(self, start, end, bsearch = False,  visited = []):
        current = self.find_node(start, bsearch = bsearch)
        visited.append(current)

        if current.name == end:
            return [current]

        order = [i for i in range(0, len(current.links))]
        shuffle(order)

        for i in order:
            nb = current.links[i]
            if nb[0] not in visited:
                visited2 = copy.copy(visited)
                sub_path = self.get_random_path(nb[0].name, end, bsearch, visited2)
                if sub_path != None:
                    sub_path.append(current)
                    return sub_path
        return None

    def different(self, a, b):
        if len(a) != len(b):
            return True
        else:
            for i in range(len(a)):
                if a[i] != b[i]:
                    return True
            return False

    def mutate_path(self, path, mut_rate):
        print("starting mutation with prob path: {0}, score path: {1} normalize score: {2}".format(path.prob, path.score, path.normalize_score))
        i = (path.length)//2 - 1
        start = path.nodes[0].name
        end = path.nodes[-1].name


        score = path.normalize_score*mut_rate
        #print("path prob chosen: {0}".format(path.prob))

        while i > 0:
            r = random()
            print("iteration {0} random : {1} score : {2}".format(i, r, score))
            #print("random: {0}, score: {1}".format(r, score))
            if r > score:
                new_left = self.get_random_path(start, path.nodes[i].name, visited = path.nodes[i+1:])[::-1]
                if self.different(new_left, path.nodes[0:i+1]):
                    new_path = Path(new_left + path.nodes[i+1:])
                    return new_path
                new_right = self.get_random_path(end, path.nodes[i].name, visited = path.nodes[:i])
                if self.different(new_right, path.nodes[i:]):
                    new_path = Path(path.nodes[:i] + new_right)
                    return new_path
            i -= 1

        print("fail to find new")
        return path




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

    rp1 = Path(region.get_random_path("1", "8", True))
    rp1.score = 0.5
    print("nodes: {0} score: {1}".format(rp1.nodes, rp1.score))
    new = region.mutate_path(rp1)
    print(new)
