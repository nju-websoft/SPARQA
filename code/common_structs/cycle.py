import copy
from collections import defaultdict
from common_structs.bag import Stack

class Cycle(object):
    """
    Using Depth-First-Search algorithm to check whether a graph has a cycle.
    if a graph is tree-like structure(no cycle), then has_cycle is never reached.
    """
    def __init__(self, graph):
        self._marked = defaultdict(bool) #daoda biaoshi
        self._has_cycle = False
        for vertex in graph.vertices():
            if not self._marked[vertex]:
                self.dfs(graph, vertex, vertex)
        # for vertex in graph.vertices():
        #     print (vertex, self._marked[vertex])

    def dfs(self, graph, vertex_1, vertex_2):
        self._marked[vertex_1] = True
        for adj in graph.get_adjacent_vertices(vertex_1):
            if not self._marked[adj]:
                self.dfs(graph, adj, vertex_1)
            else: #has reach node
                if adj != vertex_2:
                    # print (vertex_1, vertex_2, adj)
                    self._has_cycle = True
    def has_cycle(self):
        return self._has_cycle

# from parsing.structs.graph import Graph
# g = Graph()
# test_data = [(0, 1), (0, 2), (0, 6), (0, 5), (3, 5), (6, 4)]
# test_data = [(1,3), (1,4), (3,4), (1,2)]
# for a, b in test_data:
#    g.add_edge(a, b)
# cycle = Cycle(g)
# has_cycle_arg = cycle.has_cycle()
# print (has_cycle_arg)

# g2 = Graph()
# has_cycle_data = [(0, 1), (0, 2), (1, 2)] #, (1, 4)
# for a, b in has_cycle_data:
#     g2.add_edge(a, b)
# cycle2 = Cycle(g2)
# has_cycle_arg = cycle2.has_cycle()
# print (has_cycle_arg)

class DirectedCycle(object):
    """
    Using Depth-First-Search algorithm to check whether a cycle exists in a directed graph.
    There is an assist attribute call _on_stack,
    if an adjacent vertex is in _on_stack(True), that means a cycle exists.
    """

    def __init__(self, graph):
        self._marked = defaultdict(bool)
        self._edge_to = {}
        self._on_stack = defaultdict(bool)

        self._cycle = Stack()
        self.all_cycles=list()
        for v in graph.vertices():
            if not self._marked[v]:
                self.dfs(graph, v)

    def dfs(self, graph, vertex):
        self._on_stack[vertex] = True
        self._marked[vertex] = True

        for v in graph.get_adjacent_vertices(vertex):
            # if self.has_cycle() :
            #     return

            if self.has_cycle() :
                while self.has_cycle():
                    self._cycle.pop()
            # elif self._cycle.size()==2:
            #     self._cycle.pop()
            #     self._cycle.pop()

            if not self._marked[v]:
                self._edge_to[v] = vertex
                self.dfs(graph, v)
            elif self._on_stack[v]:
                tmp = vertex
                while tmp != v:
                    self._cycle.push(tmp)
                    tmp = self._edge_to[tmp]
                if self._cycle.size()>1:
                    self._cycle.push(v)
                    self._cycle.push(vertex)
                    self.all_cycles.append(copy.deepcopy(self._cycle))
                else:
                    self._cycle.pop()
        self._on_stack[vertex] = False


    def has_cycle(self):
        return not self._cycle.is_empty()

    def cycle(self):
        return self._cycle

# from parsing.structs.graph import Digragh
# graph = Digragh()
# from parsing.structs.graph import Graph
# graph = Graph()
# # test_data = [(4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
# #               (11, 12), (12, 9), (9, 10), (9, 11), (8, 9), (10, 12),
# #               (11, 4), (4, 3), (3, 5), (7, 8), (8, 7), (5, 4), (0, 5),
# #               (6, 4), (6, 9), (7, 6)]
# test_data = [(1,0),(0, 1),  (2,1), (0,2),(1, 2), (2, 0),(4,5),(5,6),(6,7),(7,4)] #,
# test_data = [(1,2), (2,3), (3,1)] #,,  (2,3), (3,2), (1,3),(3,1)
# for a, b in test_data:
#     graph.add_edge(a, b)
#
# dc = DirectedCycle(graph)
# print ('#cycle:\t', dc.has_cycle())
# # for i in dc.cycle():
# #     print (i)
# for cycle in dc.all_cycles:
#     print("he")
#     print('#Size:', cycle.size())
#     for i in cycle:
#         print(i.next_node)
