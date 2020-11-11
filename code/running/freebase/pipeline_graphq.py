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
        tuples_list.append((graphquestion.qid, graphquestion.question, graphquestion.graph_query, graphquestion.answer))
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
    graph_questions_filepath = globals_args.fn_graph_file.graphquestions_testing_dir
    # output file
    output_path = globals_args.fn_graph_file.dataset + 'output_graphq'
    structure_with_1_ungrounded_graphq_file = output_path + '/structures_with_1_ungrounded_graphs_test_spantree.json'
    structure_with_2_1_grounded_graph_file = output_path + '/structures_with_2_1_grounded_graph_test_1111.json'
    structure_with_2_2_grounded_graph_folder = output_path + '/2.2_train/'
    # module
    if module == '1.0':
        run_ungrounded_graph_from_graphq(graph_questions_filepath, structure_with_1_ungrounded_graphq_file)
    elif module == '2.1':
        running_interface.run_grounded_node_grounding_freebase(structure_with_1_ungrounded_graphq_file, structure_with_2_1_grounded_graph_file)
    elif module == '2.2':
        running_interface.run_grounded_graph_generation_by_structure_transformation(structure_with_2_1_grounded_graph_file, structure_with_2_2_grounded_graph_folder)
    elif module == '2.3_word_match':
        running_interface.run_grounding_graph_path_match(structure_with_2_2_grounded_graph_folder)
    elif module == '2.3_add_question_match':
        running_interface.run_grounding_graph_guiyi_add_question_match(structure_with_2_2_grounded_graph_folder)
        # run_grounding_graph_add_question_match(structure_with_2_2_grounded_graph_folder)
    elif module == '3_evaluation':
        running_interface.run_end_to_end_evaluation(structure_with_2_2_grounded_graph_folder, dataset='graphq')
    print("end")

