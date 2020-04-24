from common.hand_files import write_structure_file
from common import globals_args
from running import running_interface

#parsing
def run_ungrounded_graph_from_graphq(graph_questions_filepath, output_file):
    from datasets_interface.question_interface import graphquestion_interface
    graph_questions_struct = graphquestion_interface.read_graph_question_json(graph_questions_filepath)
    tuples_list = []
    for i in range(len(graph_questions_struct)):
        graphquestion = graph_questions_struct[i]
        q_normal = graphquestion_interface.look_for_q_normal_by_qid(graphquestion.qid)
        tuples_list.append((graphquestion.qid, q_normal, graphquestion.graph_query, graphquestion.answer))
    structure_list = running_interface.run_query_graph_generation(tuples_list=tuples_list)
    write_structure_file(structure_list, output_file)


if __name__ == '__main__':
    module = "3_evaluation"
    #1.0  utterance -> span tree -> ungrounded graph
    #2.1  node linking
    #2.2  grounded graph
    #2.3_word_match     2.3_add_question_match
    #3_evaluation
    print ('#module:', module)

    import sys
    from supplementary.logger_test import Logger

    sys.stdout = Logger('./2019.09.06_graphq_output.log', sys.stdout)

    #graphquestions
    # graph_questions_struct = globals_args.graph_questions
    graph_questions_filepath = globals_args.fn_graph_file.graphquestions_testing_dir
    # question_testing_qid_normal_filepath = globals_args.fn_graph_file.question_testing_qid_normal_dict
    # graph_questions_filepath = globals_args.fn_graph_file.graphquestions_training_dir
    # question_testing_qid_normal_filepath = globals_args.fn_graph_file.question_training_qid_normal_dict

    # output file
    output_path = globals_args.fn_graph_file.dataset + 'output_graphq'

    # output file
    # output_path = globals_args.argument_parser.output
    # output_file_folder = output_path + output_folder_name
    structure_with_1_ungrounded_graphq_file = output_path + '/1/' + 'structures_with_1_ungrounded_graphs_test_0906.json'
    structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_test_0906.json'
    structure_with_2_2_grounded_graph_folder = output_path + '/2.2_test/'

    # module
    if module == '1.0':
        run_ungrounded_graph_from_graphq(graph_questions_filepath, structure_with_1_ungrounded_graphq_file)
    elif module == '2.1':
        running_interface.run_grounded_node_grounding_freebase(structure_with_1_ungrounded_graphq_file, structure_with_2_1_grounded_graph_file)
    elif module == '2.2':
        running_interface.run_grounded_graph_generation_by_structure_transformation(structure_with_2_1_grounded_graph_file, structure_with_2_2_grounded_graph_folder)
    elif module == '2.3_word_match':
        running_interface.run_grounding_graph_path_match(structure_with_2_2_grounded_graph_folder)
        # running_interface.run_grounding_graph_cnn_match(structure_with_2_2_grounded_graph_folder)
    elif module == '2.3_add_question_match':
        pass
        # run_grounding_graph_guiyi_add_question_match(structure_with_2_2_grounded_graph_folder)
        # run_grounding_graph_add_question_match(structure_with_2_2_grounded_graph_folder)
    elif module == '3_evaluation': #ranking
        running_interface.run_end_to_end_evaluation(structure_with_2_2_grounded_graph_folder, dataset='graphq')
    print("end")

