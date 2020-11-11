from common.hand_files import write_structure_file, read_structure_file, read_json
import os

# 1.0
def run_query_graph_generation(tuples_list):
    from parsing import query_graph_generator
    structure_list = []
    error_qid_list = []
    for i, (qid, question_normal, gold_sparql_query, gold_answer) in enumerate(tuples_list):
        print(('%d\t%s') % (i, question_normal))
        try:
            structure = query_graph_generator.run_ungrounded_graph_interface(qid=qid, question_normal=question_normal, gold_sparql_query=gold_sparql_query, gold_answer=gold_answer)  # , gold_graph_query=gold_graph_query
            structure_list.append(structure)
        except Exception as e:
            print('#Error:', i, e)
            error_qid_list.append(i)
    print('Error:', error_qid_list)
    return structure_list

def run_grounded_node_grounding_freebase(structure_with_ungrounded_graphq_file, output_file):
    '''
     #2.1
    function: 1.0 ungrounded query  ->  2.1 grounded query
    input: structure_ungrounded_graphq_file
    :return: grounded graph with entity linking
    '''
    from grounding._2_1_grounded_graph import node_linking_interface_freebase
    from grounding._2_1_grounded_graph.grounded_graph_2_1_generation import generate_grounded_graph_interface
    structure_list = read_structure_file(structure_with_ungrounded_graphq_file)
    for structure in structure_list:
        print(structure.qid)
        for i, ungrounded_graph in enumerate(structure.get_ungrounded_graph_forest()):
            if i == len(structure.get_ungrounded_graph_forest())-1:
                grounding_result_list = []
                for node in ungrounded_graph.nodes:
                    grounding_result_list.append((node, node_linking_interface_freebase.node_linking(qid=structure.qid, node=node)))
                grouned_graph_list = generate_grounded_graph_interface(ungrounded_graph=ungrounded_graph, grounding_result_list=grounding_result_list)
                ungrounded_graph.set_grounded_linking(grounding_result_list)
                ungrounded_graph.set_grounded_graph_forest(grouned_graph_list)
    write_structure_file(structure_list, output_file)

# 2.2 structure_transformation
def run_grounded_graph_generation_by_structure_transformation(structure_with_grounded_graphq_node_grounding_file, output_file):
    from grounding._2_2_grounded_graph_offline import graph_2_1_to_2_2_by_transfer
    from grounding.grounded_graph_to_sparql import grounded_graph_to_sparql_CWQ
    def count_denotation_to_num(grounded_graph):
        '''
        # counting
        # how many softwares are developed by google?
        '''
        num = 0
        denotation_set = grounded_graph.denotation
        if denotation_set is not None:
            num = len(denotation_set)
        return [num]

    structure_list = read_structure_file(structure_with_grounded_graphq_node_grounding_file)
    new_structure_list = []
    error_qid_list = []
    for i, structure in enumerate(structure_list):
        if str(structure.qid) + '.json' in os.listdir(output_file): continue
        new_structure_list.clear()
        print(i, structure.qid, structure.question)
        is_print = False
        for ungrounded_graph in structure.ungrounded_graph_forest:
            grounded_graph_forest = []
            for _2_1_grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                try:
                    grounded_graph_forest.extend(graph_2_1_to_2_2_by_transfer.generate_candidates_by_2_1_grounded_graph_interface(_2_1_grounded_graph=_2_1_grounded_graph))
                except Exception as e:
                    print('#Error:', structure.qid, e)
                    error_qid_list.append(structure.qid)
                # break
            if len(grounded_graph_forest) > 0:
                is_print = True
                print('#Size:', len(grounded_graph_forest))
            for z in range(len(grounded_graph_forest)):
                grounded_graph_forest[z].grounded_query_id = ungrounded_graph.ungrounded_query_id * 100000 + z
                grounded_graph_forest[z].sparql_query = grounded_graph_to_sparql_CWQ(grounded_graph_forest[z])
                if structure.function == 'count':
                    grounded_graph_forest[z].denotation = count_denotation_to_num(grounded_graph_forest[z])
            ungrounded_graph.set_grounded_graph_forest(grounded_graph_forest)
        if is_print:
            new_structure_list.append(structure)
            write_structure_file(new_structure_list, output_file + str(structure.qid) + '.json')
    print('Error qid list:', error_qid_list)

#2.3_path match
def run_grounding_graph_path_match(input_file_folder):
    '''path candidate grounding graph'''
    from grounding.ranking.path_match_word_level.path_match_interface import PathMatchByLexicalNN
    import os
    from parsing.parsing_utils import extract_importantwords_from_question
    all_data_path = os.listdir(input_file_folder)
    pml = PathMatchByLexicalNN()
    for path in all_data_path:
        print(path)
        structure_with_grounded_graphq_file = input_file_folder + path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            question = structure.question
            for ungrounded_graph in structure.ungrounded_graph_forest:
                importantwords_list = extract_importantwords_from_question(question=question, ungrounded_graph=ungrounded_graph)
                print(importantwords_list, len(ungrounded_graph.get_grounded_graph_forest()))
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    grounded_graph.score = pml.get_path_pro(grounded_graph.key_path, importantwords_list) # '\t'.join(grounded_graph.key_path),
                    print (grounded_graph.key_path, importantwords_list, grounded_graph.score)
        write_structure_file(structure_list,structure_with_grounded_graphq_file)

def run_grounding_graph_add_question_match(input_file_folder):
    '''path candidate grounding graph'''
    all_data_path = os.listdir(input_file_folder)
    from grounding.ranking.path_match_sentence_level.question_match_interface import QuestionMatchInterface
    qmi = QuestionMatchInterface()
    for path in all_data_path:
        print(path)
        structure_with_grounded_graphq_file = input_file_folder + path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            qid = structure.qid
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    grounded_graph.total_score = grounded_graph.score+qmi.get_score(qid, grounded_graph.denotation)
        write_structure_file(structure_list, structure_with_grounded_graphq_file)

def run_grounding_graph_guiyi_add_question_match(input_file_folder):
    '''path candidate grounding graph'''
    from common import utils
    from grounding.ranking.path_match_sentence_level.question_match_interface import QuestionMatchInterface
    qmi = QuestionMatchInterface()
    for path in os.listdir(input_file_folder):
        print(path)
        structure_with_grounded_graphq_file = input_file_folder + path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        all_score=[]
        for structure in structure_list:
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    all_score.append(grounded_graph.score)

        all_score_guiyi = utils.Normalize(all_score)
        score_guiyi = dict()
        for i, score_ori in enumerate(all_score):
            score_guiyi[score_ori] = all_score_guiyi[i]

        for structure in structure_list:
            qid = structure.qid
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    # 3.单独跑 question match
                    # grounded_graph.total_score = qmi.get_score(qid, grounded_graph.denotation)
                    # if grounded_graph.total_score > 0:
                    #     print ('\t\t', grounded_graph.total_score)
                    # 4.单独跑 question match
                    grounded_graph.score = qmi.get_score(qid, grounded_graph.denotation)
                    if grounded_graph.score > 0:
                        print('\t\t', grounded_graph.score)
                    # 4.跑word match+question match
                    # grounded_graph.total_score = score_guiyi[grounded_graph.score] + qmi.get_score(qid, grounded_graph.denotation)
                    # return
        write_structure_file(structure_list, structure_with_grounded_graphq_file)

def run_end_to_end_evaluation(structure_with_2_2_grounded_graph_folder, dataset='qald'):
    from evaluation import kbcqa_evaluation
    if dataset == 'cwq':
        from evaluation import kbcqa_evaluation
        # every grounded graph's f1
        # kbcqa_evaluation.computed_every_grounded_graph_f1_cwq(structure_with_2_2_grounded_graph_folder)
        # kbcqa_evaluation.compute_all_questions_recall(structure_with_2_2_grounded_graph_folder)
        # kbcqa_evaluation.grounded_graphes_by_score_standard_ywsun(input_file=structure_with_2_2_grounded_graph_folder)
        kbcqa_evaluation.grounded_graphes_by_score_standard_ywsun_prediction_test(input_file=structure_with_2_2_grounded_graph_folder)
    elif dataset == 'graphq':
        #step1: every grounded graph's f1
        # kbcqa_evaluation.computed_every_grounded_graph_f1_graphq(structure_with_2_2_grounded_graph_folder)
        #step2: upbound
        kbcqa_evaluation.compute_all_questions_recall(structure_with_2_2_grounded_graph_folder)
        #step3: evaluation
        # kbcqa_evaluation.grounded_graphes_by_score_standard_ywsun(input_file=structure_with_2_2_grounded_graph_folder)

