from common_structs.ungrounded_graph import UngroundedEdge, UngroundedGraph
from parsing import parsing_utils

visit_set = set()
ungrounded_edges = []
path = []

def generate_ungrounded_graph(ungrounded_nodes=None, span_tree_hybrid_dependency_graph=None):
    '''
    :param ungrounded_nodes:
    :param span_tree_hybrid_dependency_graph:
    :return: path: ungrounded edges
    '''
    visit_set.clear()
    global ungrounded_edges
    ungrounded_edges = []
    path.clear()
    construct_edges(ungrounded_nodes=ungrounded_nodes, span_tree_hybrid_dependency_graph=span_tree_hybrid_dependency_graph)
    ungrounded_graph = UngroundedGraph(
        ungrounded_query_id=1, nodes=ungrounded_nodes, edges=ungrounded_edges,
        important_words_list=[], abstract_question=[], grounded_linking=[], grounded_graph_forest=[])
    return ungrounded_graph

def construct_edges(ungrounded_nodes=None, span_tree_hybrid_dependency_graph=None):
    # 输入: question sentence N, Nodes set V, dependency tree Y.
    # 输出: a super semantic query graph
    # for u in V:
    # 	Initialize visit as an empty set
    # 	Expand (u,u)
    # tokens = question_normal.split(' ')
    for ungrounded_node in ungrounded_nodes:
        visit_set.clear() # initialize visit as an empty set
        # 把node的最后一个位置当作node的核心词
        expand(head_index_in_dep=ungrounded_node.end_position+1,
            end_index_in_dep=ungrounded_node.end_position+1,
            ungrounded_nodes=ungrounded_nodes,
            dependency_graph=span_tree_hybrid_dependency_graph)

def expand(head_index_in_dep=None, end_index_in_dep=None, ungrounded_nodes=None, dependency_graph=None):
    # Expand(head, u)
    # 	visit <- u
    # 	if u 属于 V:
    # 		connect head and u
    # 		return
    # 	for each vertex v connected with u in Y do:
    # 		if v 不属于visit:
    # 			Expand(head, v)
    visit_set.add(end_index_in_dep)
    if parsing_utils.is_contained_one_node_from_nodes(end_index_in_dep - 1, ungrounded_nodes) \
            and not parsing_utils.is_contained_one_node(head_index_in_dep - 1, end_index_in_dep - 1, ungrounded_nodes):
        # do not in one same node 属于一个node, 但是不是当前的node
        start_node = parsing_utils.look_for_one_node_from_nodes(head_index_in_dep - 1, ungrounded_nodes)
        end_node = parsing_utils.look_for_one_node_from_nodes(end_index_in_dep - 1, ungrounded_nodes)
        friendly_name = parsing_utils.get_friendly_name_by_dependency(dependency_graph=dependency_graph, path=path)
        # connect head an u
        temp_edge = UngroundedEdge(start=start_node.nid, end=end_node.nid,friendly_name=friendly_name, score=1.0)
        if not parsing_utils.is_exist_edge_in_edges(ungrounded_edges=ungrounded_edges, ungrounded_edge=temp_edge):
            # 如果ungrounded_edges不存在这样的edge, 则追加
            ungrounded_edges.append(temp_edge)
        return

    # 递归扩张邻居顶点
    adj_vertexs = parsing_utils.adj_edge_nodes_update(end_index_in_dep, dependency_graph)
    if adj_vertexs is not None:
        for adj_vertex_index in adj_vertexs:
            if adj_vertex_index not in visit_set:
                path.append(adj_vertex_index)
                expand(head_index_in_dep=head_index_in_dep, end_index_in_dep=adj_vertex_index,
                       ungrounded_nodes=ungrounded_nodes, dependency_graph=dependency_graph)
                path.pop()
