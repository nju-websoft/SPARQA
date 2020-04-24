import copy
from collections import defaultdict
from common_structs.bag import Bag

class Graph(object):

    '''Undirected graph implementation. The cost of space is proportional to O(V + E)
    (V is the number of vertices and E is the number of edges). Adding
    an edge only takes constant time. The running time of
    Checking if node v is adjacent to w and traveling all adjacent point of v
    is related to the degree of v. This implementation supports multiple'''

    def __init__(self, input_file=None, graph=None):
        self._edges_size = 0
        self._adj = defaultdict(Bag)
        # 4.1.3 practice, add a graph parameter for constructor method.
        if graph:
            self._adj = copy.deepcopy(graph._adj)
            self._edges_size = graph.edges_size()


    def vertices_size(self):
        return len(self._adj.keys())


    def edges_size(self):
        return self._edges_size


    def add_edge(self, vertext_a, vertext_b):
        # 4.1.5 practice, no self cycle or parallel edges.
        if self.has_edge(vertext_a, vertext_b) or vertext_a == vertext_b:
            return
        self._adj[vertext_a].add(vertext_b)
        self._adj[vertext_b].add(vertext_a)
        self._edges_size += 1


    # 4.1.4 practice, add has_edge method
    def has_edge(self, vertext_a, vertext_b):
        if vertext_a not in self._adj or vertext_b not in self._adj:
            return False
        edge = next((i for i in self._adj[vertext_a] if i == vertext_b), None)
        return edge is not None


    def get_adjacent_vertices(self, vertex):
        return self._adj[vertex]


    def vertices(self):
        return self._adj.keys()


    def degree(self, vertex):
        assert vertex in self._adj
        return self._adj[vertex].size()


    def max_degree(self):
        result = 0
        for vertex in self._adj:
            v_degree = self.degree(vertex)
            if v_degree > result:
                result = v_degree
        return result


    def avg_degree(self):
        return float(2 * self._edges_size) / self.vertices_size()


    def number_of_self_loops(self):
        count = 0
        for k in self._adj:
            for vertex in self._adj[k]:
                if vertex == k:
                    count += 1
        return int(count / 2)


    # 4.1.31 check the number of parallel edges with linear running time.
    def number_of_parallel_edges(self):
        count = 0
        for k in self._adj:
            tmp = set()
            for vertex in self._adj[k]:
                if vertex not in tmp:
                    tmp.add(vertex)
                else:
                    count += 1
        return int(count / 2)


    def __repr__(self):
        '''to string'''
        s = str(self.vertices_size()) + ' vertices, ' + str(self._edges_size) + ' edges\n'
        for k in self._adj:
            try:
                lst = ' '.join([vertex for vertex in self._adj[k]])
            except TypeError:
                lst = ' '.join([str(vertex) for vertex in self._adj[k]])
            s += '{}: {}\n'.format(k, lst)
        return s

#
# g = Graph()
# test_data = [(0, 5), (4, 3), (0, 1), (9, 12), (6, 4), (5, 4), (0, 2),  # from book tinyG.txt
#                   (11, 12), (9, 10), (0, 6), (7, 8), (9, 11), (5, 3)]
# for a, b in test_data:
#     g.add_edge(a, b)
#
# print (g.vertices()) #vertices
# print (g.vertices_size())
# print (g.max_degree())
# print (g.degree(9))
# print (g)
#
# adj_list = [i for i in g.get_adjacent_vertices(4)]
# print (adj_list)

class Digragh(object):

    """
      Directed graph implementation. Every edges is directed, so if v is
    reachable from w, w might not be reachable from v.There would ba an
    assist data structure to mark all available vertices, because
    self._adj.keys() is only for the vertices which outdegree is not 0.
    Directed graph is almost the same with Undirected graph,many codes
    from Gragh can be reusable.
    >>> # 4.2.6 practice
    >>> graph = Digragh()
    >>> test_data = [(4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (8, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (7, 8), (8, 7), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6)]
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> graph.vertices_size()
    13
    >>> graph.edges_size()
    22
    >>> [i for i in graph.get_adjacent_vertices(2)]
    [0, 3]
    >>> [j for j in graph.get_adjacent_vertices(6)]
    [9, 4, 0]
    >>> [v for v in graph.vertices()]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    >>> graph
    13 vertices, 22 edges
    0: 5 1
    2: 0 3
    3: 5 2
    4: 3 2
    5: 4
    6: 9 4 0
    7: 6 8
    8: 7 9
    9: 11 10
    10: 12
    11: 4 12
    12: 9
    <BLANKLINE>
    >>>
    """

    def __init__(self, graph=None):
        self._edges_size = 0
        self._adj = defaultdict(Bag)
        self._vertices = set()

        # 4.2.3 practice, generate graph from another graph.
        if graph:
            self._adj = copy.deepcopy(graph._adj)
            self._vertices_size = graph.vertices_size()
            self._edges_size = graph.edges_size()
            self._vertices = copy.copy(graph.vertices())

    def vertices_size(self):
        return len(self._vertices)

    def edges_size(self):
        return self._edges_size

    def add_edge(self, start, end):
        # 4.2.5 practice, parallel edge and self cycle are not allowed
        if self.has_edge(start, end) or start == end:
            return
        self._vertices.add(start)
        self._vertices.add(end)
        self._adj[start].add(end)
        self._edges_size += 1

    def get_adjacent_vertices(self, vertex):
        return self._adj[vertex]

    def vertices(self):
        return self._vertices

    def reverse(self):
        reverse_graph = Digragh()
        for vertex in self.vertices():
            for adjacent_vertex in self.get_adjacent_vertices(vertex):
                reverse_graph.add_edge(adjacent_vertex, vertex)
        return reverse_graph

    # 4.2.4 practice, add has_edge method for Digraph
    def has_edge(self, start, end):
        edge = next((i for i in self._adj[start] if i == end), None)
        return edge is not None

    def __repr__(self):
        s = str(len(self._vertices)) + ' vertices, ' + str(self._edges_size) + ' edges\n'
        for k in self._adj:
            try:
                lst = ' '.join([vertex for vertex in self._adj[k]])
            except TypeError:
                lst = ' '.join([str(vertex) for vertex in self._adj[k]])
            s += '{}: {}\n'.format(k, lst)
        return s