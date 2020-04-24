from parsing import parsing_args
from parsing import parsing_utils

def is_comparative_funct(serialization_list):
    '''is_count_funct(serialization_list)'''
    is_comarative = False
    for element in serialization_list:
        if element in parsing_args.comparative_ner_tags:
            is_comarative = True
            break
    return is_comarative

def comparative_serialization(question):
    question_tokens_list = question.split(' ')
    serialization_list = ['O' for _ in question_tokens_list]
    for mention in parsing_args.dayu_phrases:
        if mention not in question: continue
        serialization_list = parsing_utils.serialization_mention(
            question_tokens_list, mention.split(' '), ner_tag='>')
    for mention in parsing_args.dayu_dengyu_phrases:
        if mention not in question: continue
        serialization_list = parsing_utils.serialization_mention(
            question_tokens_list, mention.split(' '), ner_tag='>=')
    for mention in parsing_args.xiaoyu_phrases:
        if mention not in question: continue
        serialization_list = parsing_utils.serialization_mention(
            question_tokens_list, mention.split(' '), ner_tag='<')
    for mention in parsing_args.xiaoyu_dengyu_phrases:
        if mention not in question: continue
        serialization_list = parsing_utils.serialization_mention(
            question_tokens_list, mention.split(' '), ner_tag='<=')
    return serialization_list

def is_comparative_by_token_ner_tag(token):
    result = False
    if token.ner_tag is not None and token.ner_tag in parsing_args.comparative_ner_tags:
        result = True
    return result

# comparative
def comparative_ground(_2_2_graph, comparative):
    '''
    :param _2_2_graph:
    :param comparative:
    :return: denotation
    '''
    # "question": "which company builds bipropellant rocket engines with at least 2361800 n sea level trust ?",
    # "qid": 455000001,
    # "function": ">=",
    for edge in ungrounded_graph.edges:
        if edge in merge_edges:
            # literal_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
            # comparative_node = ungrounded_generation_helper.search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
            literal_node, comparative_node = transformations_helper.literal_comparative_node_in_one_edge(
                ungrounded_graph_nodes, edge)

            literal_node.function = comparative_node.function
            #first check if it exist
            #if exist, update node information
            #if not exist, add node
            if transformations_helper.is_exist_in_nodes(new_ungrounded_nodes, literal_node):
                temp_node = transformations_helper.search_one_node_in_nodes(new_ungrounded_nodes, literal_node)
                temp_node.function = comparative_node.function
            else:
                new_ungrounded_nodes.append(literal_node)
            # if not ungrounded_generation_helper.is_exist_in_nodes(new_ungrounded_nodes, comparative_node):
            #     new_ungrounded_nodes.append(comparative_node)
            # new_ungrounded_edges.append(copy.deepcopy(edge)) do not add comparative_node edge
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
    return _generate_ungrounded_graph(new_ungrounded_nodes, new_ungrounded_edges,
                                      ungrounded_query_id=ungrounded_graph.ungrounded_query_id)

