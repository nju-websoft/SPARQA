from common_structs.grounded_graph import GrounedGraph, GroundedNode, GroundedEdge

nodes_sequence_completed_list = []
node_sequence = []
def recursion_generate_grounded_graph(grounding_result_list=None, index=0):
    '''meanwhile multiple nodes grounding, exponent complexity
    :param grounding_result_list [
            (node(barbaro), {'en.barbaro': 1.6}),
            (node(september), {'en.september_11_2001_attacks': 1.0})
    :return: grounded_graph list
    '''
    if index == len(grounding_result_list):
        nodes_sequence_completed_list.append(node_sequence.copy())
        return
    _, grounding_ordered_dict = grounding_result_list[index]
    #grounding_ordered_dict: {'en.barbaro': 1.6, 'en.barba': 1.0, 'en.baro': 1.2}
    for k, v in grounding_ordered_dict.items():
        node_sequence.append((k, v))
        recursion_generate_grounded_graph(grounding_result_list, index+1)
        node_sequence.pop()

def generate_grounded_graph_interface(ungrounded_graph=None, grounding_result_list=None):
    '''
        function: generate 2.1 grounded_graph
        :param ungrounded_graph
        :param grounding_result_list [
            (node(barbaro), {'en.barbaro': 1.6}),
            (node(september), {'en.september_11_2001_attacks': 1.0})
        :return: grounded_graph list
    '''
    grouned_graph_list = []
    if grounding_result_list is None: return grouned_graph_list
    # shut down
    # ungrounded_graph = graph_transformation(ungrounded_graph)
    nodes_sequence_completed_list.clear()
    node_sequence.clear()
    basic_grounded_graph = ungrounded_to_grounded(ungrounded_graph)
    #---------------------------------
    recursion_generate_grounded_graph(grounding_result_list, 0)
    # print('#sequence:', nodes_grounding_list)
    node_list = []
    for grounded_node, _ in grounding_result_list:
        node_list.append(grounded_node)
    grounded_id = 0
    for nodes_grounding in nodes_sequence_completed_list:
        # nodes_grounding: [('en.xtracycle', 1.6), ('freebase.type_profile', 1.0)]
        grounded_id = grounded_id + 1
        new_grounded_graph = basic_grounded_graph.get_copy()
        new_grounded_graph.grounded_query_id = new_grounded_graph.grounded_query_id * 10000 + grounded_id
        for node in new_grounded_graph.nodes:
            correct_index = -1
            for index in range(len(node_list)):
                if node.nid == node_list[index].nid:
                    correct_index = index
            if correct_index != -1:
                node.id = nodes_grounding[correct_index][0]
                node.score = nodes_grounding[correct_index][1]
        grouned_graph_list.append(new_grounded_graph)
        break
    return grouned_graph_list

def ungrounded_to_grounded(ungrounded_graph):
    '''
    convert ungrounded graph to basic grounded graph
    :param ungrounded_graph:
    :return:
    '''
    nodes = []
    edges = []
    for ungrounded_node in ungrounded_graph.nodes:
        nodes.append(GroundedNode(nid=ungrounded_node.nid, node_type=ungrounded_node.node_type, type_class=ungrounded_node.type_class,
                                  friendly_name=ungrounded_node.friendly_name, question_node=ungrounded_node.question_node, function=ungrounded_node.function, score=0))
    for ungrounded_edge in ungrounded_graph.edges:
        edges.append(GroundedEdge(start=ungrounded_edge.start, end=ungrounded_edge.end, friendly_name=ungrounded_edge.friendly_name, score=ungrounded_edge.score))
    return GrounedGraph(grounded_query_id=ungrounded_graph.ungrounded_query_id, type='', nodes=nodes, edges=edges, key_path='', sparql_query='', score=0, denotation='')

