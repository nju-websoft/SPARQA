from parsing import parsing_args
from parsing import parsing_utils

def is_superlative_funct(serialization_list):
    is_superlative = False
    for element in serialization_list:
        if element in parsing_args.arg_ner_tags:
            is_superlative = True
            break
    return is_superlative

def superlative_serialization(question):
    question_tokens_list = question.split(' ')
    serialization_list = ['O' for _ in question_tokens_list]
    for arg_mention in parsing_args.argmin_phrases:
        if arg_mention not in question: continue
        serialization_list = parsing_utils.serialization_mention(
            question_tokens_list, arg_mention.split(' '), ner_tag='argmin')
    for arg_mention in parsing_args.argmax_phrases:
        if arg_mention not in question: continue
        serialization_list = parsing_utils.serialization_mention(
            question_tokens_list, arg_mention.split(' '), ner_tag='argmax')
    return serialization_list

def is_superlative_by_token_ner_tag(token):
    result = False
    if token.ner_tag is not None and token.ner_tag in parsing_args.arg_ner_tags:
        result = True
    return result

# superlative
def superlative_ground(_2_2_graph, superlative):
    '''
    :param _2_2_graph:
    :param superlative:
    :return: denotation
    '''
    # "question": "which is the smallest roller coasters designed by walt disney imagineering ?",
    # "qid": 442000100,
    # self.function = 'argmax or argmin'
    # 最 442000100	which is the smallest roller coasters designed by walt disney imagineering?	argmin	2
    for edge in ungrounded_graph.edges:
        if edge in merge_edges:
            # other_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            # superlative_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            other_node, superlative_node = transformations_helper.relation_superlative_node_in_one_edge(
                ungrounded_graph_nodes, edge)
            if other_node is None and superlative_node is None:
                other_node, superlative_node = transformations_helper.class_superlative_node_in_one_edge(
                    ungrounded_graph_nodes, edge)
            superlative_node.function = node_helper.superlative_to_function(superlative_node.friendly_name)
            superlative_node.node_type = 'literal'
            # superlative_node.friendly_name = '0'
            #first check if it exist
            #if exist, update node information
            #if not exist, add node
            if transformations_helper.is_exist_in_nodes(new_ungrounded_nodes, superlative_node):
                temp_node = transformations_helper.search_one_node_in_nodes(new_ungrounded_nodes, superlative_node)
                temp_node.function = superlative_node.function
                temp_node.node_type = superlative_node.node_type
                temp_node.friendly_name = superlative_node.friendly_name
            else:
                new_ungrounded_nodes.append(superlative_node)
            if not transformations_helper.is_exist_in_nodes(new_ungrounded_nodes, other_node):
                new_ungrounded_nodes.append(other_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))

        else:
            start_node = transformations_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            end_node = transformations_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            #first check if it exist
            #if exist, no add the node
            #if not exist, add node
            if not transformations_helper.is_exist_in_nodes(new_ungrounded_nodes, start_node):
                new_ungrounded_nodes.append(start_node)
            if not transformations_helper.is_exist_in_nodes(new_ungrounded_nodes, end_node):
                new_ungrounded_nodes.append(end_node)
            new_ungrounded_edges.append(copy.deepcopy(edge))
    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges, ungrounded_query_id=ungrounded_graph.ungrounded_query_id)

