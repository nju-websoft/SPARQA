from grounding._2_2_grounded_graph_offline import path_to_graph
from common.hand_files import read_json
from grounding import grounding_utils
from grounding import grounding_args

def get_2_2_graphs_by_type_and_literals(question_type, entities_or_literals):
    result = []
    candidate_graphquerys = []
    if len(entities_or_literals) == 2: # one literal, one entity
        literal_value = None
        entity_value = None
        for entity_or_literal in entities_or_literals:
            if entity_or_literal[1] == 'literal':
                literal_value = entity_or_literal[0]
            else:
                entity_value = entity_or_literal[0]
        if not isinstance(literal_value, str):
            literal_value = str(literal_value)
        if literal_value in grounding_args.literal_to_id_map:
            literal_value_id = str(grounding_args.literal_to_id_map[literal_value])
        else:
            return result
        filename_1 = question_type
        filename_1 += '_entity_' + entity_value
        filename_1 += '_literal_' + literal_value_id
        filename_2 = question_type
        filename_2 += '_literal_' + literal_value_id
        filename_2 += '_entity_' + entity_value
        if filename_1 in grounding_args.oracle_all_files_path_names: #all_oracle_files_path:
            data_dict = read_json(grounding_args.oracle_file_root + filename_1)
            if question_type == 'conjunction':
                if grounding_args.q_mode == 'cwq':
                    candidate_graphquerys = path_to_graph.parser_conjunction_q_cwq_(data_dict=data_dict, s1=entity_value, t1='entity', s2=literal_value_id, t2='literal')
                elif grounding_args.q_mode == 'graphq':
                    candidate_graphquerys = path_to_graph.parser_conjunction_q_graphq(data_dict=data_dict, s1=entity_value, t1='entity', s2=literal_value_id, t2='literal')
        elif filename_2 is not None and filename_2 in grounding_args.oracle_all_files_path_names: #all_oracle_files_path:
            data_dict = read_json(grounding_args.oracle_file_root + filename_2) #file_result
            if grounding_args.q_mode == 'cwq':
                candidate_graphquerys = path_to_graph.parser_conjunction_q_cwq_(data_dict=data_dict, s1=literal_value_id, t1='literal', s2=entity_value, t2='entity')
            elif grounding_args.q_mode == 'graphq':
                candidate_graphquerys = path_to_graph.parser_conjunction_q_graphq(data_dict=data_dict, s1=literal_value_id, t1='literal', s2=entity_value, t2='entity')
    elif len(entities_or_literals) == 1:
        literal_value = None
        for entity_or_literal in entities_or_literals:
            if entity_or_literal[1] == 'literal': literal_value = entity_or_literal[0]
        if not isinstance(literal_value, str): literal_value = str(literal_value)
        if literal_value in grounding_args.literal_to_id_map:
            literal_value_id = str(grounding_args.literal_to_id_map[literal_value])
        else:
            return result
        filename_1 = question_type
        filename_1 += '_literal_' + literal_value_id
        if filename_1 in grounding_args.oracle_all_files_path_names:  # all_oracle_files_path:
            data_dict = read_json(grounding_args.oracle_file_root + filename_1)
            if question_type == 'composition':
                if grounding_args.q_mode == 'cwq':
                    candidate_graphquerys = path_to_graph.parser_composition_q_cwq_(data_dict=data_dict, s1=literal_value, t1='literal')
                elif grounding_args.q_mode == 'graphq':
                    candidate_graphquerys = path_to_graph.parser_composition_q_graphq(data_dict=data_dict, s1=literal_value, t1='literal')
    return grounding_utils.candidate_query_to_grounded_graph(candidate_graphquerys=candidate_graphquerys)


def _get_2_2_graphs_by_structure_and_type_only_entities(question_type=None, entities_or_literals=None, _2_1_graph=None, constraint='0'):
    filename_1 = question_type
    filename_2 = None
    if len(entities_or_literals) == 1:
        filename_1 += '_' + entities_or_literals[0][1] + '_' + entities_or_literals[0][0]
    elif len(entities_or_literals) == 2:
        filename_1 += '_' + entities_or_literals[0][1] + '_' + entities_or_literals[0][0]
        filename_1 += '_' + entities_or_literals[1][1] + '_' + entities_or_literals[1][0]
        filename_2 = question_type
        filename_2 += '_' + entities_or_literals[1][1] + '_' + entities_or_literals[1][0]
        filename_2 += '_' + entities_or_literals[0][1] + '_' + entities_or_literals[0][0]
    candidate_graphquerys = []
    if filename_1 in grounding_args.oracle_all_files_path_names:
        data_dict = read_json(grounding_args.oracle_file_root + filename_1)
        if question_type == 'composition':
            if constraint == '1': is_constraint = True
            else: is_constraint = False
            if grounding_args.q_mode == 'cwq':
                candidate_graphquerys = path_to_graph.parser_composition_q_cwq_(data_dict=data_dict, s1=entities_or_literals[0][0], t1=entities_or_literals[0][1], constaint=is_constraint)
            elif grounding_args.q_mode == 'graphq':
                candidate_graphquerys = path_to_graph.parser_composition_q_graphq(data_dict=data_dict, s1=entities_or_literals[0][0], t1=entities_or_literals[0][1], constaint=is_constraint)
        elif question_type == 'conjunction':
            if grounding_args.q_mode == 'cwq':
                candidate_graphquerys = path_to_graph.parser_conjunction_q_cwq_(data_dict=data_dict,s1=entities_or_literals[0][0], t1=entities_or_literals[0][1], s2=entities_or_literals[1][0], t2=entities_or_literals[1][1])
            elif grounding_args.q_mode == 'graphq':
                candidate_graphquerys = path_to_graph.parser_conjunction_q_graphq(data_dict=data_dict, s1=entities_or_literals[0][0], t1=entities_or_literals[0][1], s2=entities_or_literals[1][0], t2=entities_or_literals[1][1])
    elif filename_2 is not None and filename_2 in grounding_args.oracle_all_files_path_names:
        data_dict = read_json(grounding_args.oracle_file_root + filename_2)
        if grounding_args.q_mode == 'cwq':
            candidate_graphquerys = path_to_graph.parser_conjunction_q_cwq_(data_dict=data_dict, s1=entities_or_literals[1][0], t1=entities_or_literals[1][1], s2=entities_or_literals[0][0], t2=entities_or_literals[0][1])
        elif grounding_args.q_mode == 'graphq':
            candidate_graphquerys = path_to_graph.parser_conjunction_q_graphq(data_dict=data_dict, s1=entities_or_literals[1][0], t1=entities_or_literals[1][1], s2=entities_or_literals[0][0], t2=entities_or_literals[0][1])
    return grounding_utils.candidate_query_to_grounded_graph(candidate_graphquerys=candidate_graphquerys)


def generate_candidates_by_2_1_grounded_graph_interface(_2_1_grounded_graph=None):
    '''
    :param _2_1_grounded_graph:
    :return: _2_2 grounded graphs
    '''
    category, path_list = grounding_utils.analysis_structure_category(_2_1_graph=_2_1_grounded_graph)
    entities_list = []
    literals_list = []
    for node in _2_1_grounded_graph.nodes:
        if node.node_type == 'entity':
            entities_list.append([node.id.replace('http://dbpedia.org/resource/', ''), node.node_type])
        elif node.node_type == 'literal':
            literals_list.append([node.id, node.node_type])
    oracle_graphs = []
    if category == 'composition-0':
        if len(entities_list) == 1:
            oracle_graphs = _get_2_2_graphs_by_structure_and_type_only_entities(question_type='composition', entities_or_literals=entities_list, _2_1_graph=_2_1_grounded_graph, constraint='1')
        else:
            print('#only one literal', literals_list)
            oracle_graphs = get_2_2_graphs_by_type_and_literals(question_type='composition', entities_or_literals=literals_list) #, constraint='1'
    elif category == 'composition-1':
        if len(entities_list) == 1:
            oracle_graphs = _get_2_2_graphs_by_structure_and_type_only_entities(question_type='composition', entities_or_literals=entities_list, _2_1_graph=_2_1_grounded_graph, constraint='0')
        else:
            print('#only one literal', literals_list)
            oracle_graphs = get_2_2_graphs_by_type_and_literals(question_type='composition', entities_or_literals=literals_list) #, constraint='0'
    elif category == 'conjunction':
        if len(entities_list) == 2:
            oracle_graphs = _get_2_2_graphs_by_structure_and_type_only_entities(question_type='conjunction', entities_or_literals=entities_list, _2_1_graph=_2_1_grounded_graph, constraint='0')
        elif len(entities_list) == 1 and len(literals_list) == 1:
            print('#literal', entities_list, literals_list)
            entities_list.append(literals_list[0])
            oracle_graphs = get_2_2_graphs_by_type_and_literals(question_type='conjunction', entities_or_literals=entities_list)
        elif len(literals_list) == 2: # do not process
            pass
    else:
        print('---#other structure---')
    return oracle_graphs

