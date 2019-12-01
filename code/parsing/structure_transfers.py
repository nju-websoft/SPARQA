from common_structs.ungrounded_graph import UngroundedEdge, UngroundedGraph, UngroundedNode
import copy
from parsing import parsing_utils
from common_structs.graph import Digragh
from common_structs.cycle import DirectedCycle

def _generate_ungrounded_graph(nodes, edges, ungrounded_query_id=1):
    '''ungrounded graph'''
    return UngroundedGraph(
        ungrounded_query_id=ungrounded_query_id, nodes=nodes, edges=edges, important_words_list=[],
        abstract_question=[], grounded_linking=[], grounded_graph_forest=[])

def _generate_ungrounded_node(node_type, nid, friendly_name='blank_node', start_position=0, end_position=0, score=1.0):
    '''ungrounded node'''
    ungrounded_node = UngroundedNode(
        nid=nid, node_type=node_type,
        friendly_name=friendly_name,
        question_node=0, score=score,
        start_position=start_position, end_position=end_position)
    return ungrounded_node

def _generate_ungrounded_edge(start=-1, end=-1, friendly_name='blank_edge', score=1.0):
    '''ungrounded edge'''
    ungrounded_edge = UngroundedEdge(start=start, end=end, friendly_name=friendly_name, score=score)
    return ungrounded_edge

#---------------aggregation-------------------------

def update_ungrounded_graph_count_aggregation(ungrounded_graph):
    '''
    第一种改变: class -> count  转变为class的function是count
    :param ungrounded_graph:
    :return: ungrounded_graph
    '''
    ungrounded_graph_nodes = ungrounded_graph.nodes
    merge_edges = []
    for edge in ungrounded_graph.edges:
        # start_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
        # end_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
        # if ungrounded_generation_helper.is_class_node(start_node) and ungrounded_generation_helper.is_count_node(end_node):
        class_node, count_node = parsing_utils.class_count_node_in_one_edge(ungrounded_graph_nodes, edge)
        if class_node is not None and count_node is not None:
            merge_edges.append(edge)
    new_ungrounded_edges = []
    new_ungrounded_nodes = []
    for edge in ungrounded_graph.edges:
        if edge in merge_edges:
            # class_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            # count_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            class_node, count_node = parsing_utils.class_count_node_in_one_edge(ungrounded_graph_nodes, edge)
            class_node.function = count_node.function
            #first check if it exist
            #if exist, update node information
            #if not exist, add node
            if parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, class_node):
                temp_node = parsing_utils.search_one_node_in_nodes(new_ungrounded_nodes, class_node)
                temp_node.function = count_node.function
            else:
                new_ungrounded_nodes.append(class_node)
        else:
            start_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            end_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            #first check if it exist
            #if exist, no add the node
            #if not exist, add node
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, start_node):
                new_ungrounded_nodes.append(start_node)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, end_node):
                new_ungrounded_nodes.append(end_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))

    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges, ungrounded_query_id=ungrounded_graph.ungrounded_query_id)

def update_ungrounded_graph_superlative_aggregation(ungrounded_graph):
    '''
    第二种改变:
    relation -> superlative  转变为superlative node的function是superlative
    class -> superlative 转变为superlative node 的function 是superlative
    "nid": 1,
	"node_type": "literal",
	"id": "0",
	"class": "type.float",
	friendly_name": "0",
	"question_node": 0,
	"function": "argmin"
    :param ungrounded_graph:
    :return: ungrounded_graph
    '''
    ungrounded_graph_nodes = ungrounded_graph.nodes
    merge_edges = []
    for edge in ungrounded_graph.edges:
        # start_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
        # end_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
        # if (ungrounded_generation_helper.is_relation_node(start_node)
        #     or ungrounded_generation_helper.is_class_node(start_node)) \
        #         and ungrounded_generation_helper.is_superlative_node(end_node):
        #     merge_edges.append(edge)
        relation_node, superlative_node = parsing_utils.relation_superlative_node_in_one_edge(ungrounded_graph_nodes, edge)
        if relation_node is not None and superlative_node is not None:
            merge_edges.append(edge)
        else:
            class_node, superlative_node = parsing_utils.class_superlative_node_in_one_edge(ungrounded_graph_nodes, edge)
            if class_node is not None and superlative_node is not None:
                merge_edges.append(edge)

    new_ungrounded_edges = []
    new_ungrounded_nodes = []
    for edge in ungrounded_graph.edges:
        if edge in merge_edges:
            # other_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            # superlative_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            other_node, superlative_node = parsing_utils.relation_superlative_node_in_one_edge(
                ungrounded_graph_nodes, edge)
            if other_node is None and superlative_node is None:
                other_node, superlative_node = parsing_utils.class_superlative_node_in_one_edge(
                    ungrounded_graph_nodes, edge)
            superlative_node.function = parsing_utils.superlative_to_function(superlative_node.friendly_name)
            superlative_node.node_type = 'literal'
            # superlative_node.friendly_name = '0'
            #first check if it exist
            #if exist, update node information
            #if not exist, add node
            if parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, superlative_node):
                temp_node = parsing_utils.search_one_node_in_nodes(new_ungrounded_nodes, superlative_node)
                temp_node.function = superlative_node.function
                temp_node.node_type = superlative_node.node_type
                temp_node.friendly_name = superlative_node.friendly_name
            else:
                new_ungrounded_nodes.append(superlative_node)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, other_node):
                new_ungrounded_nodes.append(other_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))

        else:
            start_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            end_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            #first check if it exist
            #if exist, no add the node
            #if not exist, add node
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, start_node):
                new_ungrounded_nodes.append(start_node)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, end_node):
                new_ungrounded_nodes.append(end_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))
    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges, ungrounded_query_id=ungrounded_graph.ungrounded_query_id)

def update_ungrounded_graph_comparative_aggregation(ungrounded_graph):
    '''
    第三种改变: literal -> comparative  转变为literal node的function是comparative,
    同时去掉comparative节点
    :param ungrounded_graph:
    :return: ungrounded_graph
    '''
    ungrounded_graph_nodes = ungrounded_graph.nodes
    merge_edges = []
    for edge in ungrounded_graph.edges:
        # start_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
        # end_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
        # if ungrounded_generation_helper.is_literal_node(start_node) \
        #         and ungrounded_generation_helper.is_comparative_node(end_node):
        #     merge_edges.append(edge)
        literal_node, comparative_node = parsing_utils.literal_comparative_node_in_one_edge(
            ungrounded_graph_nodes, edge)
        if literal_node is not None and comparative_node is not None:
            merge_edges.append(edge)

    new_ungrounded_edges = []
    new_ungrounded_nodes = []
    for edge in ungrounded_graph.edges:
        if edge in merge_edges:
            # literal_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            # comparative_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            literal_node, comparative_node = parsing_utils.literal_comparative_node_in_one_edge(
                ungrounded_graph_nodes, edge)

            literal_node.function = comparative_node.function
            #first check if it exist
            #if exist, update node information
            #if not exist, add node
            if parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, literal_node):
                temp_node = parsing_utils.search_one_node_in_nodes(new_ungrounded_nodes, literal_node)
                temp_node.function = comparative_node.function
            else:
                new_ungrounded_nodes.append(literal_node)
            # if not ungrounded_generation_helper.is_exist_in_nodes(new_ungrounded_nodes, comparative_node):
            #     new_ungrounded_nodes.append(comparative_node)
            # new_ungrounded_edges.append(copy.deepcopy(edge)) do not add comparative_node edge
        else:
            start_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            end_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            #first check if it exist
            #if exist, no add the node
            #if not exist, add node
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, start_node):
                new_ungrounded_nodes.append(start_node)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, end_node):
                new_ungrounded_nodes.append(end_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))
    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges,
                                      ungrounded_query_id=ungrounded_graph.ungrounded_query_id)

def update_ungrounded_graph_contract_relation_node(ungrounded_graph):
    '''
    第四种改变: relation -> class; relation -> entity;  转变为 class -{relation}->entity
    :param ungrounded_graph:
    :return: ungrounded_graph
    '''
    def _constract_relation_node(relation_node, ungrounded_graph):
        '''第四种改变: relation -> class; relation -> entity;  转变为 class -{relation}->entity'''
        # first, search all "relation" nodes
        # second, bianli every "relation" node
        # look for all its adject nodes "args_node"
        # third, add edge between every pair of adject nodes "args_node"
        # adjacent_edges = search_adjacent_edges(node=relation_node, ungrounded_graph=ungrounded_graph)
        adjacent_nodes = parsing_utils.search_adjacent_nodes(
            node=relation_node, ungrounded_graph=ungrounded_graph)
        new_ungrounded_edges = []
        new_ungrounded_nodes = []
        if len(adjacent_nodes) > 1:
            for adjacent_node_a in adjacent_nodes:
                for adjacent_node_b in adjacent_nodes:
                    if adjacent_node_a == adjacent_node_b: continue
                    if adjacent_node_a.nid < adjacent_node_b.nid: continue
                    new_ungrounded_edges.append(
                        _generate_ungrounded_edge(start=adjacent_node_a.nid, end=adjacent_node_b.nid, friendly_name=relation_node.friendly_name))
                    if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, adjacent_node_a):
                        new_ungrounded_nodes.append(adjacent_node_a)
                    if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, adjacent_node_b):
                        new_ungrounded_nodes.append(adjacent_node_b)
        elif len(adjacent_nodes) == 1:
            adjacent_node = adjacent_nodes[0]
            # insert blank node
            max_nid = -1  # look for max nid
            for temp_node in ungrounded_graph.nodes:
                if max_nid < temp_node.nid:
                    max_nid = temp_node.nid
            blank_node_nid = max_nid + 1
            blank_node = _generate_ungrounded_node(node_type='class', nid=blank_node_nid)
            new_ungrounded_nodes.append(blank_node)
            new_ungrounded_nodes.append(adjacent_node)
            ungrounded_edge = _generate_ungrounded_edge(start=adjacent_node.nid, end=blank_node.nid, friendly_name=relation_node.friendly_name)
            new_ungrounded_edges.append(ungrounded_edge)
        return new_ungrounded_nodes, new_ungrounded_edges

    ungrounded_graph_nodes = ungrounded_graph.nodes
    new_ungrounded_edges = []
    new_ungrounded_nodes = []
    for edge in ungrounded_graph.edges:
        relation_node, other_node = parsing_utils.relation_other_node_in_one_edge(ungrounded_graph_nodes, edge)
        if relation_node is not None and other_node is not None:
            constract_new_ungrounded_nodes, constract_new_ungrounded_edges = _constract_relation_node(
                relation_node=relation_node, ungrounded_graph=ungrounded_graph)
            for constract_new_ungrounded_edge in constract_new_ungrounded_edges:
                if not parsing_utils.is_exist_edge_in_edges(ungrounded_edges=new_ungrounded_edges,
                                                            ungrounded_edge=constract_new_ungrounded_edge):
                    new_ungrounded_edges.append(copy.deepcopy(constract_new_ungrounded_edge))
            for constract_new_ungrounded_node in constract_new_ungrounded_nodes:
                if not parsing_utils.is_exist_in_nodes(ungrounded_graph_nodes=new_ungrounded_nodes,
                                                       ungrounded_node=constract_new_ungrounded_node):
                    new_ungrounded_nodes.append(constract_new_ungrounded_node)
        else:
            start_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            end_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, start_node):
                new_ungrounded_nodes.append(start_node)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, end_node):
                new_ungrounded_nodes.append(end_node)
            if not parsing_utils.is_exist_edge_in_edges(ungrounded_edges=new_ungrounded_edges,
                                                        ungrounded_edge=edge):
                new_ungrounded_edges.append(copy.deepcopy(edge))
    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges, ungrounded_query_id=ungrounded_graph.ungrounded_query_id)

#---------------relation-------------------------

def update_merge_relation_to_relation(ungrounded_graph):
    '''
    relation -> relation    ==>     {relation} -{class mention} -> {relation}
    add blank node'''
    ungrounded_graph_nodes = ungrounded_graph.nodes
    remove_edges = []
    add_edges = []
    for edge in ungrounded_graph.edges:
        start_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
        end_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
        if parsing_utils.is_relation_node(start_node) \
                and parsing_utils.is_relation_node(end_node):
            #look for max nid
            max_nid = -1
            for temp_node in ungrounded_graph.nodes:
                if max_nid < temp_node.nid:
                    max_nid = temp_node.nid
            blank_node_nid = max_nid+1
            blank_node = _generate_ungrounded_node(node_type='class', nid=blank_node_nid)
            ungrounded_graph_nodes.append(blank_node)
            add_edges.append( UngroundedEdge(start=start_node.nid, end=blank_node.nid, friendly_name='blank_edge') )
            add_edges.append( UngroundedEdge(start=blank_node.nid, end=end_node.nid, friendly_name='blank_edge') )
            # add_edges.append(UngroundedEdge(start=start_node.nid, end=blank_node.nid, friendly_name='blank_edge', score=1.0))
            # add_edges.append(UngroundedEdge(start=blank_node.nid, end=end_node.nid, friendly_name='#blank_edge', score=1.0))
            remove_edges.append(edge)
    new_ungrounded_edges = []
    for edge in ungrounded_graph.edges:
        if edge not in remove_edges:
            new_ungrounded_edges.append(copy.deepcopy(edge))
    for edge in add_edges:
        new_ungrounded_edges.append(copy.deepcopy(edge))
    ungrounded_graph.edges = new_ungrounded_edges

    return ungrounded_graph

#---------------operation-------------------------

def update_ungrounded_graph_merge_question_node(ungrounded_graph):
    '''
    第5种改变: class{value:wh-word; question_node:1} -> class  转变为class的question_node:1
    :param ungrounded_graph:
    :return: ungrounded_graph
    '''
    ungrounded_graph = copy.deepcopy(ungrounded_graph)
    ungrounded_graph_nodes = ungrounded_graph.nodes
    merge_edges = []
    for edge in ungrounded_graph.edges:
        #question node=1; class
        class_question_node, class_node = parsing_utils.class_question_node_class_node_in_one_edge(ungrounded_graph_nodes, edge)
        if class_question_node is not None and class_node is not None:
            # friendly_name in wh-words
            is_equal_wh_word = parsing_utils.is_equal_wh_word(class_question_node.friendly_name)
            #chu du == 1
            search_adjacent_edges = parsing_utils.search_adjacent_edges(
                node=class_question_node, ungrounded_graph=ungrounded_graph)
            if is_equal_wh_word and len(search_adjacent_edges) == 1 and (edge.friendly_name == '' or edge.friendly_name == 'name'):
                # 满足上述三种条件以后，才merge
                merge_edges.append(edge)

    if len(merge_edges) == 0: return None

    new_ungrounded_edges = []
    new_ungrounded_nodes = []
    for edge in ungrounded_graph.edges:
        if edge in merge_edges:
            # question node=1; class
            class_question_node, class_node = parsing_utils.class_question_node_class_node_in_one_edge(ungrounded_graph_nodes, edge)
            #first check if it exist
            #if exist, update node information
            #if not exist, add node
            if parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, class_node):
                temp_node = parsing_utils.search_one_node_in_nodes(new_ungrounded_nodes, class_node)
                temp_node.question_node = class_question_node.question_node
            else:
                class_node.question_node = class_question_node.question_node
                new_ungrounded_nodes.append(copy.deepcopy(class_node))
        else:
            start_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            end_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            #first check if it exist
            #if exist, no add the node
            #if not exist, add node
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, start_node):
                new_ungrounded_nodes.append(start_node)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, end_node):
                new_ungrounded_nodes.append(end_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))

    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges,ungrounded_query_id=ungrounded_graph.ungrounded_query_id+1)

def update_ungrounded_graph_ec(ungrounded_graph):
    '''entity-class  entity-{class}-_blank_node  s,p,? entity's class class -> entity: [where] did the [conviction] of [thomas fyshe palmer] occur'''
    ungrounded_graph = copy.deepcopy(ungrounded_graph)

    ungrounded_graph_nodes = ungrounded_graph.nodes
    operation_edges = []
    for edge in ungrounded_graph.edges:
        # entity; class
        entity_node, class_node = parsing_utils.entity_class_node_in_one_edge(ungrounded_graph_nodes, edge)
        if entity_node is not None and class_node is not None:
            if not parsing_utils.is_question_node(class_node): #class node 不能是question node
                operation_edges.append(edge)

    if len(operation_edges) == 0: return None

    new_ungrounded_edges = []
    new_ungrounded_nodes = []
    for edge in ungrounded_graph.edges:
        if edge in operation_edges:
            # entity; class
            entity_node, class_node = parsing_utils.entity_class_node_in_one_edge(ungrounded_graph_nodes, edge)
            # entity-{class}-_blank_node
            _blank_node = _generate_ungrounded_node(node_type='class', nid=class_node.nid, friendly_name='blank_node',
                                                    start_position=class_node.start_position, end_position=class_node.end_position)
            new_edge = _generate_ungrounded_edge(start=edge.start, end=edge.end, friendly_name=class_node.friendly_name)

            # first check if it exist
            # if exist, update node information
            # if not exist, add node
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, entity_node):
                new_ungrounded_nodes.append(entity_node)
            if parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, _blank_node):
                # 已经存在了, 则更新原来的顶点，（边信息不变）
                yijing_exist_class_node = parsing_utils.search_one_node_in_nodes(new_ungrounded_nodes, _blank_node)
                new_ungrounded_nodes.remove(yijing_exist_class_node)
                new_ungrounded_nodes.append(_blank_node)
            else: # 如果没有存在, 则追加
                new_ungrounded_nodes.append(_blank_node)
            new_ungrounded_edges.append(new_edge)

        else:
            start_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            end_node = parsing_utils.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            # first check if it exist
            # if exist, no add the node
            # if not exist, add node
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, start_node):
                new_ungrounded_nodes.append(start_node)
            if not parsing_utils.is_exist_in_nodes(new_ungrounded_nodes, end_node):
                new_ungrounded_nodes.append(end_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))

    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges, ungrounded_query_id=ungrounded_graph.ungrounded_query_id + 1)

def undate_ungrounded_graph_del_cycle(ungrounded_graph):
    '''破圈操作:  包含e-e或e-l或l-l的圈，要把它们破开。有圈情况:  event型问句,
    比如what were the compositions made by bach in 1749; O并列;  VP 并列; 修饰疑问短语，挂到了动词身上'''
    ungrounded_graph_edges = ungrounded_graph.edges
    di_graph = Digragh()
    for edge in ungrounded_graph_edges:
        di_graph.add_edge(edge.start, edge.end)
        di_graph.add_edge(edge.end, edge.start)
    directed_cycle = DirectedCycle(di_graph)
    if len(directed_cycle.all_cycles) > 0:
        return parsing_utils.del_edge_in_ungrounded_edge(ungrounded_graph, directed_cycle)
    else:
        return None

#---------------operation-------------------------

def graph_transformation(ungrounded_graph):
    # check cycle, and delete cycle
    del_cycle_ungrounded_graph = undate_ungrounded_graph_del_cycle(ungrounded_graph)
    if del_cycle_ungrounded_graph is not None:
        ungrounded_graph = del_cycle_ungrounded_graph
    # class{value:wh-word; question_node:1} -> class  转变为class的question_node:1
    qc_ungrounded_graph = update_ungrounded_graph_merge_question_node(ungrounded_graph)
    if qc_ungrounded_graph is not None:
        ungrounded_graph = qc_ungrounded_graph

    return ungrounded_graph
