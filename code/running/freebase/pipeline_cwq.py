from common import globals_args
from running import running_interface

# 1.0 parsing
def run_ungrounded_graph_from_complexwebquestion(complexquestin_filepath, structure_with_1_ungrounded_cwq_file):
    from datasets_interface.question_interface import complexwebquestion_interface
    from common.hand_files import write_structure_file
    complexwebq_list = complexwebquestion_interface.read_complexwebq_question_json(complexquestin_filepath)
    tuples_list = []
    for i, complexwebq_struct in enumerate(complexwebq_list):
        tuples_list.append((complexwebq_struct.ID, complexwebq_struct.question, complexwebq_struct.sparql, complexwebq_struct.answers))
    print (len(tuples_list))
    structure_list = running_interface.run_query_graph_generation(tuples_list=tuples_list)
    write_structure_file(structure_list, structure_with_1_ungrounded_cwq_file)


if __name__ == '__main__':
    module = "3_evaluation"
    #1.0  utterance -> span tree -> ungrounded graph
    #2.1  node linking
    #2.2  grounded graph
    #2.2_oracle
    #2.3_word_match     2.3_add_question_match
    #3_evaluation
    print ('#module:', module)

    #complexwebquestion
    complexwebquestion_filepath = globals_args.fn_cwq_file.complexwebquestion_train_dir
    # output file
    output_path = globals_args.fn_cwq_file.dataset + 'output_cwq'
    # output_folder_name = '/2019.08.02_cwq'
    # output_file_folder = output_path + output_folder_name
    structure_with_1_ungrounded_graphq_file = output_path + '/1/' + 'structures_with_1_ungrounded_graphs_all_train_head_0901_10000_15000.json'
    # structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_all_train_head_0901_0_5000.json'
    # structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graphs_all_train_head_0901_5000_10000.json'
    structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graphs_all_test_head_0901_dep.json'
    structure_with_2_2_grounded_graph_folder = output_path + '/2.2_test_span_transfer_wo_wordlevel/'

    # module
    if module == '1.0':
        run_ungrounded_graph_from_complexwebquestion(complexwebquestion_filepath,structure_with_1_ungrounded_graphq_file)
    elif module == '2.1':
        running_interface.run_grounded_node_grounding_freebase(structure_with_1_ungrounded_graphq_file, structure_with_2_1_grounded_graph_file)
    elif module == '2.2':
        running_interface.run_grounded_graph_generation_by_structure_transformation(structure_with_2_1_grounded_graph_file, structure_with_2_2_grounded_graph_folder)
    elif module == '2.3_word_match':
        running_interface.run_grounding_graph_path_match(structure_with_2_2_grounded_graph_folder)
        # run_grounding_graph_cnn_match(structure_with_2_2_grounded_graph_folder)
    elif module == '2.3_add_question_match':
        # running_interface.run_grounding_graph_guiyi_add_question_match(structure_with_2_2_grounded_graph_folder)
        running_interface.run_grounding_graph_question_match_minus(structure_with_2_2_grounded_graph_folder)
        # running_interface.run_grounding_graph_add_question_match(structure_with_2_2_grounded_graph_folder)
    elif module == '3_evaluation':  # evaluation
        running_interface.run_end_to_end_evaluation(structure_with_2_2_grounded_graph_folder, dataset='cwq')

    print("end")
