
from collections import defaultdict
from common_structs.graph import Graph
from common_structs.stack import Stack

def get_path_every_two_node(tuple_data):
    g = Graph()
    result = []
    for start, end in tuple_data:
        g.add_edge(start, end)
    for node_a in g.vertices():
        for node_b in g.vertices():
            if node_a > node_b:
                path_list = get_path_from_a_to_b(graph=g, a=node_a, b=node_b)
                result.append((node_a, node_b, path_list))
    return result

def get_path_from_a_to_b(graph=None, a=None, b=None):
    dfp = DepthFirstPaths(graph, a)
    path_list = None
    if dfp.has_path_to(b):
        path_list = [i for i in dfp.path_to(b)]
    return path_list

class DepthFirstPaths():
    '''Undirected graph depth-first searching algorithms implementation.
    Depth-First-Search recurvisely reaching all vertices
    that are adjacent to it,
    and then treat these adjacent_vertices as start_vertex and searching again util all the
    connected vertices is marked.'''

    def __init__(self, graph, start_vertex):
        self._marked = defaultdict(bool)
        self._edge_to = {}
        self._start = start_vertex
        self.dfs(graph, self._start)

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        for v in graph.get_adjacent_vertices(vertex):
            if not self._marked[v]:
                self._edge_to[v] = vertex
                self.dfs(graph, v)

    def has_path_to(self, vertex):
        return self._marked[vertex]

    def vertices_size(self):
        return len(self._marked.keys())

    def path_to(self, vertex):
        if not self.has_path_to(vertex):
            return None
        tmp = vertex
        path = Stack()
        while tmp != self._start:
            path.push(tmp)
            tmp = self._edge_to[tmp]
        path.push(self._start)
        return path

# g = Graph()
# tuple_data = [(1, 0), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
# for a, b in tuple_data:
#     g.add_edge(a, b)
# dfp = DepthFirstPaths(g, 7)
# has_path_list = [dfp.has_path_to(i) for i in range(6)]
# # print (has_path_list)
# path_to_list = [i for i in dfp.path_to(4)]
# # print (path_to_list)
# for i in range(7):
#     if dfp.has_path_to(i):
#         path = dfp.path_to(i)
#         path_to_list = [i for i in path]
#         print(path_to_list)
