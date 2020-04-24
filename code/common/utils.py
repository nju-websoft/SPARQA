from common_structs.graph import Graph
import random

def get_gold_entity_or_class(gold_grounded_graph, node_type='entity'):
    gold_set_result = set()
    if gold_grounded_graph is None:return gold_set_result
    for gold_node in gold_grounded_graph.nodes:
        if gold_node.node_type == node_type:
            gold_set_result.add(gold_node.id)
    return gold_set_result

def get_gold_entity_or_class_by_json(gold_grounded_graph, node_type='entity'):
    gold_set_result = set()
    if gold_grounded_graph is None:
        return gold_set_result
    for gold_node in gold_grounded_graph['nodes']:
        if gold_node['node_type'] == node_type:
            gold_set_result.add(gold_node['id'])
    return gold_set_result

def get_nid_by_id(nodes, id):
    result_nid = None
    for node in nodes:
        if id == node.id:
            result_nid = node.nid
    return result_nid

def get_edge_by_nodes(edges, node_a, node_b):
    result = None
    for edge in edges:
        if (edge.start == node_a.nid and edge.end == node_b.nid) \
            or (edge.start == node_b.nid and edge.end == node_a.nid):
            result = edge
    return result

def is_literal_node(nodes, nid):
    result = False
    for node in nodes:
        if (nid == node.nid and node.node_type == 'literal') or nid in ['?num', '?sk0']:
            result = True
    return result

def has_literal_node(nodes):
    '''literal node'''
    has_literal = False
    for node in nodes:
        if node.node_type == 'literal':
            has_literal = True
    return has_literal

def convert_triples_to_graph(grounded_edges):
    '''convert triples to graph'''
    g = Graph()
    for edge in grounded_edges:
        g.add_edge(edge.start, edge.end)
    return g

def search_one_node_in_nodes_by_nid(nodes, nid):
    '''get specific node'''
    result = None
    for node in nodes:
        if node.nid == nid:
            result = node
            break
    return result

def print_span_tree(span_tree):
    '''print span tree'''
    root_node = span_tree.get_root_span_node()
    # preorder(root_node,tree)
    # print_str = root_node.show(0, tree)
    return root_node.show_line(span_tree)

def print_ungrounded_graph(ungrounded_graph):
    for node in ungrounded_graph.nodes:
        print (node)
    for edge in ungrounded_graph.edges:
        print (edge)

def print_grounded_graph(grounded_graph):
    print ('\t\t', grounded_graph.type)
    for node in grounded_graph.nodes:
        print ('\t\t', node)
    for edge in grounded_graph.edges:
        print ('\t\t', edge)

def random_int_list(start, stop, length):
    '''generate random'''
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        rand_temp = random.randint(start, stop)
        # 如果在里面了, 就继续随机
        while rand_temp in random_list:
            rand_temp = random.randint(start, stop)
        random_list.append(rand_temp)
    return random_list

def search_ungrounded_graph(qid, structure_list):
    qid_ungrounded_graph_result = None
    for structure in structure_list:
        for i, ungrounded_graph in enumerate(structure.get_ungrounded_graph_forest()):
            if qid == structure.qid:
                qid_ungrounded_graph_result = ungrounded_graph
                break
    return qid_ungrounded_graph_result

def get_node_by_id(nodes, id):
    result_node = None
    for node in nodes:
        if id == node.id:
            result_node = node
    return result_node

def get_unground_node_by_id(nodes, id):
    result_node = None
    for node in nodes:
        if id == node.nid:
            result_node = node
    return result_node

import numpy as np
def Normalize(data):
    if len(data)==0:
        return []
    m = np.mean(data)
    mx = max(data)
    mn = min(data)
    return [(float(i) - m) / (mx - mn) for i in data]


