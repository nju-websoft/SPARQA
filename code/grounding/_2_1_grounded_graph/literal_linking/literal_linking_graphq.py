from common import globals_args
from common.globals_args import fn_graph_file
# from execute_freebase import kb_interface
from common.hand_files import write_set,read_structure_file

file_literal=fn_graph_file.grounded_graph_file+'oracle_grounded_graph_test_group_2/literals/'

def get_s_p_byliteral(i, literal_value):
    '''获取literal值的s_p'''
    s_p = kb_interface.get_s_p_literal_none(literal_value)
    write_set(s_p, file_literal + str(i))
    return s_p

def get_s_p_by_literal_none(literal_value):
    s_p = kb_interface.get_s_p_literal_none(literal_value)
    return s_p

def get_s_p_literal_function(literal_value, literal_function, literaltype):
    s_p = kb_interface.get_s_p_literal_function(
        literal_value, literal_function, literaltype)
    return s_p

if __name__ == '__main__':

    # output file
    output_path = globals_args.argument_parser.output
    output_folder_name = '/2019.05.17_graphq'
    output_file_folder = output_path + output_folder_name
    structure_with_2_1_grounded_graph_file = output_file_folder + '/2.1/' + 'structures_with_2_1_grounded_graph_train.json'

    structure_list = read_structure_file(structure_with_2_1_grounded_graph_file)
    literal_node_set = set()
    literal_count = 0
    for i, structure in enumerate(structure_list):
        print(i, structure.qid, structure.question)
        for ungrounded_graph in structure.ungrounded_graph_forest:
            grounded_graph_forest = []
            for _2_1_grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                for _2_1_grounded_graph_node in _2_1_grounded_graph.nodes:
                    if _2_1_grounded_graph_node.node_type == 'literal':
                        literal_node_set.add(_2_1_grounded_graph_node.id)
                        literal_count += 1
                        print (_2_1_grounded_graph_node.id, _2_1_grounded_graph_node.type_class)
    print ('-------------------')
    print (literal_count)

    literal_node_list = list(literal_node_set)
    for i, nodeid in enumerate(literal_node_list):
        if nodeid in filter_list: continue
        print (i, nodeid)
        s_p = get_s_p_byliteral(i+100, nodeid)
        print ('#size:\t', i+100, nodeid, len(s_p))

    literal = '"2"^^<http://www.w3.org/2001/XMLSchema#int>'

    # type.datetime
    literal = '"1902-07-16"^^<http://www.w3.org/2001/XMLSchema#datetime>'

    # ?x1 > 1.524
    s_p_set = get_s_p_literal_function('1.524',
                                       literal_function='>',
                                       literaltype=None)
    print (s_p_set)

    #type.int
    # ?x1 < 74
    s_p_set = get_s_p_literal_function('1.524',
                                       literal_function='<',
                                       literaltype='type.int')
    print ('end')