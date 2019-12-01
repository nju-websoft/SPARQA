from collections import defaultdict

class DepthFirstSearch:

    def __init__(self, graph, start_vertex):
        self._marked = defaultdict(bool)
        self._edge_to = {}
        self._start = start_vertex
        self._edge_to[start_vertex] = -1 # represent start node
        self._traversal_sequence_list = []
        self.dfs(graph, self._start)
        self.count = 0

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        for w in graph.get_adjacent_vertices(vertex):
            if not self._marked[w]:
                self._edge_to[w] = vertex
                self.dfs(graph, w)
                self._traversal_sequence_list.append((w, vertex))

    def print(self, graph):
        for v in graph.vertices():
            if self._marked[v]:
                print(str(v) + "\tfather:\t" + str(self._edge_to[v]))

# g = Graph()
# tuple_data = [(1, 2), (2, 3)]
# for a, b in tuple_data:
#     g.add_edge(a, b)
# dfs = DepthFirstSearch(g, 1)
