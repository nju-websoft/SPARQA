from parsing.aggregation import counting
from parsing.aggregation import superlative
from parsing.aggregation import comparative
from parsing import parsing_utils

def aggregation_interface(question_normal):
    '''
    # is_agg, serialization_list = aggregation_process.aggregation_interface(question_normal=question_normal)
    '''
    question_normal = question_normal.lower()
    count_serialization_list = counting.count_serialization(question=question_normal)
    is_count = counting.is_count_funct(count_serialization_list)
    superlative_serialization_list = superlative.superlative_serialization(question=question_normal)
    is_superlative = superlative.is_superlative_funct(superlative_serialization_list)
    comparative_serialization_list = comparative.comparative_serialization(question=question_normal)
    is_comparative = comparative.is_comparative_funct(comparative_serialization_list)
    if is_count:
        return 'count', count_serialization_list
    elif is_superlative:
        return 'superlative', superlative_serialization_list
    elif is_comparative:
        return 'comparative', comparative_serialization_list
    else:
        return 'none', None

def set_class_aggregation_function(ungrounded_nodes=None, dependency_graph=None, surface_tokens=None):
    '''set ordinal function of class'''
    for ungrounded_node in ungrounded_nodes:
        # 只有class, literal上面设置聚合属性
        if ungrounded_node.node_type != 'class' and ungrounded_node.node_type != 'literal':
            continue
        for surface_index in range(ungrounded_node.start_position, ungrounded_node.end_position+1):
            # 遍历node的每个word, 检测它的所有出边
            adj_vertexs = parsing_utils.adj_edge_nodes_update(surface_index + 1, dependency_graph)
            for adj_vertex_index in adj_vertexs:
                adj_token = surface_tokens[adj_vertex_index-1]
                if counting.is_count_by_token_ner_tag(adj_token):
                    ungrounded_node.function = 'count'
                elif superlative.is_superlative_by_token_ner_tag(adj_token):
                    ungrounded_node.function = adj_token.ner_tag
                elif comparative.is_comparative_by_token_ner_tag(adj_token):
                    ungrounded_node.function = adj_token.ner_tag
                else: # 再走一层
                    pass
                    # adj_adj_vertexs = parsing_utils.adj_edge_nodes_update(adj_vertex_index, dependency_graph)
                    # if adj_adj_vertexs is None:
                    #     continue
                    # for adj_adj_vertex_index in adj_adj_vertexs:
                    #     adj_adj_token = surface_tokens[adj_adj_vertex_index-1]
                    #     if counting.is_count_by_token_ner_tag(adj_adj_token):
                    #         ungrounded_node.function = 'count'
                    #     elif superlative.is_superlative_by_token_ner_tag(adj_adj_token):
                    #         ungrounded_node.function = adj_adj_token.ner_tag
                    #     elif comparative.is_comparative_by_token_ner_tag(adj_adj_token):
                    #         ungrounded_node.function = adj_adj_token.ner_tag
    return ungrounded_nodes

if __name__ == '__main__':
    question_1 = 'what is the largest casino ?'
    question_2 = 'what us presidents has a weight of at least 80.0 kg.'
    question_3 = 'how many firefighters are employed with the fdny ?'
    question_4 = 'find the count of firefighters in the new york city fire department'
    question_5 = 'can you give the number of cameras produced by hp ?'
    # node_function = parser_utils.ner_to_function('how many', ner_tag='count')
    question_6 = 'How many other battles have the military person fought whose one of the battles is World War II ?'
    serialization_list = aggregation_interface(question_normal=question_6)


