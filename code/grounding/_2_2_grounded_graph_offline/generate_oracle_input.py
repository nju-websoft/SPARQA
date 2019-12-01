from common.hand_files import read_structure_file
from grounding import grounding_utils

def generate_paths_graphq_interface_from_lcquad_el(structure_with_2_1_grounded_graph_file):
    from datasets_interface.question_interface import lcquad_1_0_interface
    structure_list = read_structure_file(structure_with_2_1_grounded_graph_file)
    error_qid_list = []
    for i, structure in enumerate(structure_list):
        try:
            # entities_list = lcquad_1_0_interface.get_topic_entities_list_by_question(structure.question)
            entities_list = lcquad_1_0_interface.get_topic_entities_list_by_question_from_nn(structure.question)
            new_entities_list = []
            for entity in entities_list:
                new_entities_list.append([entity, 'entity'])
            if len(entities_list) == 1:
                print(('%s\t%s\t%s') % (structure.qid, 'composition', str(new_entities_list)))
            elif len(entities_list) == 2:
                print(('%s\t%s\t%s') % (structure.qid, 'conjunction', str(new_entities_list)))
        except Exception as e:
            error_qid_list.append(structure.qid)
    print ('#error:\t', error_qid_list)

def generate_paths_graphq_interface_from_graph_2_1(structure_with_2_1_grounded_graph_file):
    structure_list = read_structure_file(structure_with_2_1_grounded_graph_file)
    error_qid_list = []

    # structure_list = structure_list[0:1000]
    # structure_list = structure_list[1000:2000]
    # structure_list = structure_list[2000:3000]
    # structure_list = structure_list[3000:4000]
    # structure_list = structure_list[4000:5000]
    # structure_list = structure_list[5000:6000]
    # structure_list = structure_list[6000:7000]
    # structure_list = structure_list[7000:8000]
    # structure_list = structure_list[8000:9000]
    # structure_list = structure_list[9000:10000]

    for i, structure in enumerate(structure_list):
        for ungrounded_graph in structure.ungrounded_graph_forest:
            for _2_1_grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                try:
                    entities_list = grounding_utils.convert_2_1_graph_to_qid_entities(_2_1_graph=_2_1_grounded_graph)
                    if len(entities_list) == 1:
                        print(('%s\t%s\t%s') % (structure.qid, 'composition', str(entities_list)))
                    elif len(entities_list) == 2:
                        print(('%s\t%s\t%s') % (structure.qid, 'conjunction', str(entities_list)))
                except Exception as e:
                    error_qid_list.append(structure.qid)
    print ('#error:\t', error_qid_list)

def generate_paths_graphq_interface_from_graph_2_1_cwq(structure_with_2_1_grounded_graph_file):
    def is_exist(question_type=None, entities_or_literals=None):
        from grounding import grounding_args
        blag = 0
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
        if filename_1 in grounding_args.oracle_all_files_path_names:
            blag = 1
        elif filename_2 is not None and filename_2 in grounding_args.oracle_all_files_path_names:
            blag = 1
        return blag

    structure_list = read_structure_file(structure_with_2_1_grounded_graph_file)
    error_qid_list = []
    # structure_list = structure_list[0:1000]
    for i, structure in enumerate(structure_list):
        for ungrounded_graph in structure.ungrounded_graph_forest:
            for _2_1_grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                try:
                    entities_list = grounding_utils.convert_2_1_graph_to_qid_entities(_2_1_graph=_2_1_grounded_graph)
                    if len(entities_list) == 1:
                        blag = is_exist(question_type='composition', entities_or_literals=entities_list)
                        print(('%s\t%s\t%s\t%d') % (structure.qid, 'composition', str(entities_list), blag))
                    elif len(entities_list) == 2:
                        blag = is_exist(question_type='conjunction', entities_or_literals=entities_list)
                        print(('%s\t%s\t%s\t%d') % (structure.qid, 'conjunction', str(entities_list), blag))
                except Exception as e:
                    error_qid_list.append(structure.qid)
    print ('#error:\t', error_qid_list)

def generate_paths_graphq_interface_from_graph_2_1_graphq(structure_with_2_1_grounded_graph_file):

    def is_exist(question_type=None, entities_or_literals=None):
        from grounding import grounding_args
        blag = 0
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
        if filename_1 in grounding_args.oracle_all_files_path_names:
            blag = 1
        elif filename_2 is not None and filename_2 in grounding_args.oracle_all_files_path_names:
            blag = 1
        return blag

    structure_list = read_structure_file(structure_with_2_1_grounded_graph_file)
    error_qid_list = []
    # structure_list = structure_list[0:1000]
    for i, structure in enumerate(structure_list):
        for ungrounded_graph in structure.ungrounded_graph_forest:
            for _2_1_grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                # try:
                entities_list = grounding_utils.convert_2_1_graph_to_qid_entities(_2_1_graph=_2_1_grounded_graph)
                if len(entities_list) == 1:
                    blag = is_exist(question_type='composition', entities_or_literals=entities_list)
                    if blag == 0:
                        print(('%s\t%s\t%s\t%d') % (structure.qid, 'composition', str(entities_list), blag))
                elif len(entities_list) == 2:
                    blag = is_exist(question_type='conjunction', entities_or_literals=entities_list)
                    if blag == 0:
                        print(('%s\t%s\t%s\t%d') % (structure.qid, 'conjunction', str(entities_list), blag))
                # except Exception as e:
                #     error_qid_list.append(structure.qid)
    print ('#error:\t', error_qid_list)

if __name__ == '__main__':

    # structure_with_2_1_grounded_graph_file = 'D:/dataset/output/2019.07.12_lcquad/2.1/structures_with_2_1_grounded_graphs_test_spantree_joint_0821.json'
    # structure_with_2_1_grounded_graph_file = 'D:/dataset/dataset_lcquad_1_0/output_lcquad/2.1/structures_with_2_1_grounded_graphs_test_spantree_head_0905_joint.json'
    structure_with_2_1_grounded_graph_file = 'D:/dataset/dataset_lcquad_1_0/output_lcquad/2.1/structures_with_2_1_grounded_graphs_train_spantree_head_0905_withcount_gold_node.json'
    generate_paths_graphq_interface_from_lcquad_el(structure_with_2_1_grounded_graph_file)

    # structure_with_2_1_grounded_graph_file = 'D:/dataset/dataset_cwq_1_1/output_cwq/2.1/structures_with_2_1_grounded_graphs_all_train_head_0901_10000_15000.json'
    # generate_paths_graphq_interface_from_graph_2_1_cwq(structure_with_2_1_grounded_graph_file)

    # structure_with_2_1_grounded_graph_file = 'D:/dataset/dataset_graphquestions/output_graphq/2.1/structures_with_2_1_grounded_graph_train_0905.json'
    # generate_paths_graphq_interface_from_graph_2_1_graphq(structure_with_2_1_grounded_graph_file)

    print('end')

