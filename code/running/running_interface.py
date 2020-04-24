from common.hand_files import write_structure_file, read_structure_file, read_json

# 1.0
def run_query_graph_generation_lcquad(tuples_list):
    from parsing import query_graph_generator_el_gold
    structure_list = []
    error_qid_list = []
    for i, (qid, question_normal, gold_sparql_query, gold_answer) in enumerate(tuples_list):
        print(('%d\t%s') % (i, question_normal))
        try:
            structure = query_graph_generator_el_gold.run_ungrounded_graph_interface(
                qid=qid, question_normal=question_normal, gold_sparql_query=gold_sparql_query, gold_answer=gold_answer)
            structure_list.append(structure)
        except Exception as e:
            print('#Error:', i, e)
            error_qid_list.append(i)
    print('Error:', error_qid_list)
    return structure_list

# 1.0
def run_query_graph_generation(tuples_list):
    from parsing import query_graph_generator
    structure_list = []
    error_qid_list = []
    for i, (qid, question_normal, gold_sparql_query, gold_answer) in enumerate(tuples_list):
        print(('%d\t%s') % (i, question_normal))
        try:
            structure = query_graph_generator.run_ungrounded_graph_interface(
                qid=qid, question_normal=question_normal, gold_sparql_query=gold_sparql_query, gold_answer=gold_answer)  # , gold_graph_query=gold_graph_query
            structure_list.append(structure)
        except Exception as e:
            print('#Error:', i, e)
            error_qid_list.append(i)
    print('Error:', error_qid_list)
    return structure_list

# 2.1
def run_grounded_node_grounding_dbpedia(structure_with_ungrounded_graphq_file, output_file):
    '''
     #2.1
    function: 1.0 ungrounded query  ->  2.1 grounded query
    input: structure_ungrounded_graphq_file
    :return: grounded graph with entity linking
    '''
    from grounding._2_1_grounded_graph import node_linking_interface_dbpedia
    from grounding._2_1_grounded_graph.grounded_graph_2_1_generation import generate_grounded_graph_interface
    structure_list = read_structure_file(structure_with_ungrounded_graphq_file)
    for structure in structure_list:
        print(structure.qid)
        for i, ungrounded_graph in enumerate(structure.get_ungrounded_graph_forest()):
            if i == len(structure.get_ungrounded_graph_forest()) - 1:
                grounding_result_list = []
                if len(ungrounded_graph.nodes) > 4:
                    continue
                for node in ungrounded_graph.nodes:
                    grounding_result_list.append((node, node_linking_interface_dbpedia.node_linking(qid=structure.qid, node=node)))
                grouned_graph_list = generate_grounded_graph_interface(ungrounded_graph=ungrounded_graph, grounding_result_list=grounding_result_list)
                ungrounded_graph.set_grounded_linking(grounding_result_list)
                ungrounded_graph.set_grounded_graph_forest(grouned_graph_list)
        break
    write_structure_file(structure_list, output_file)

# 2.1
def run_grounded_node_grounding_dbpedia_gold(structure_with_ungrounded_graphq_file, output_file):
    '''
     #2.1
    function: 1.0 ungrounded query  ->  2.1 grounded query
    input: structure_ungrounded_graphq_file
    :return: grounded graph with entity linking
    '''
    from datasets_interface.question_interface import lcquad_1_0_interface
    from grounding._2_1_grounded_graph.grounded_graph_2_1_generation import generate_grounded_graph_interface
    structure_list = read_structure_file(structure_with_ungrounded_graphq_file)
    for structure in structure_list:
        print(structure.qid)
        for i, ungrounded_graph in enumerate(structure.get_ungrounded_graph_forest()):
            if i == len(structure.get_ungrounded_graph_forest()) - 1:
                grounding_result_list = []
                for node in ungrounded_graph.nodes:
                    # (node(barbaro), {'en.barbaro': 1.6}), get_el_result(question=structure.question, nid=node.nid)
                    grounding_result_list.append((node,  lcquad_1_0_interface.get_topic_entities_list_by_question_and_nodemention(
                        question=structure.question, mention=node.friendly_name)))
                grouned_graph_list = generate_grounded_graph_interface(ungrounded_graph=ungrounded_graph, grounding_result_list=grounding_result_list)
                ungrounded_graph.set_grounded_linking(grounding_result_list)
                ungrounded_graph.set_grounded_graph_forest(grouned_graph_list)
    write_structure_file(structure_list, output_file)

# 2.1

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

    from grounding._2_2_grounded_graph import graph_2_1_to_2_2_by_transfer
    from grounding.grounded_graph_to_sparql import grounded_graph_to_sparql_CWQ
    import os

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
    # structure_list = structure_list[3000:3500]
    for i, structure in enumerate(structure_list):

        if str(structure.qid) + '.json' in os.listdir(output_file):
            print ('exist...', structure.qid)
            continue

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

        # if i > 10:
        #     break

    print('Error qid list:', error_qid_list)

#2.3_path match
def run_grounding_graph_path_match(input_file_folder):
    '''path candidate grounding graph'''
    from grounding.ranking.path_match_nn.path_match_interface import PathMatchByLexicalNN
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

def run_grounding_graph_cnn_match(input_file_folder):
    '''path candidate grounding graph'''
    import os
    from grounding.ranking.path_match_cnn.cnn_match_interface import CNNMatchInterface
    from parsing import parsing_utils
    cmi = CNNMatchInterface()
    for path in os.listdir(input_file_folder):
        print(path)
        structure_with_grounded_graphq_file = input_file_folder + path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            question=structure.question
            for ungrounded_graph in structure.ungrounded_graph_forest:
                question = parsing_utils.extract_importantwords_from_cnn(question, ungrounded_graph)
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    grounded_graph.score=cmi.get_path_pro((grounded_graph.key_path), question)
                    print(grounded_graph.key_path, question, grounded_graph.score)
        write_structure_file(structure_list,structure_with_grounded_graphq_file)

def run_grounding_graph_add_question_match(input_file_folder):
    '''path candidate grounding graph'''
    import os
    all_data_path = os.listdir(input_file_folder)
    from grounding.ranking.path_match_nn.question_match_interface import QuestionMatchInterface
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
    import os
    from common import utils
    from grounding.ranking.path_match_nn.question_match_interface import QuestionMatchInterface
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

def run_grounding_graph_question_match_minus(input_file_folder):
    '''path candidate grounding graph'''
    import os
    from common import utils
    for path in os.listdir(input_file_folder):
        print(path)
        structure_with_grounded_graphq_file = input_file_folder + path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        all_score = []
        for structure in structure_list:
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    all_score.append(grounded_graph.score)

        all_score_guiyi = utils.Normalize(all_score)
        score_guiyi = dict()
        for i, score_ori in enumerate(all_score):
            score_guiyi[score_ori] = all_score_guiyi[i]

        for structure in structure_list:
            # qid = structure.qid
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    # 4.跑 total - score_guiyi
                    # grounded_graph.total_score = score_guiyi[grounded_graph.score] + qmi.get_score(qid, grounded_graph.denotation)
                    grounded_graph.total_score = grounded_graph.total_score - score_guiyi[grounded_graph.score]
                    # return
        write_structure_file(structure_list, structure_with_grounded_graphq_file)


def run_end_to_end_evaluation(structure_with_2_2_grounded_graph_folder, dataset='qald'):
    from evaluation import kbcqa_evaluation
    if dataset == 'cwq':
        from evaluation import kbcqa_evaluation
        # every grounded graph's f1
        # kbcqa_evaluation.computed_every_grounded_graph_f1_cwq(structure_with_2_2_grounded_graph_folder)
        # kbcqa_evaluation.compute_all_questions_recall(structure_with_2_2_grounded_graph_folder)

        # all questions recall
        # qids=read_set(fn_cwq_file.dataset+'test_composition_等.txt')
        # qids|=read_set(fn_cwq_file.dataset+'test_conjunction_等.txt')
        # kbcqa_evaluation.show_f1_given_qids(structure_with_2_2_grounded_graph_folder,qids=qids)
        # kbcqa_evaluation.compute_recall(structure_with_2_2_grounded_graph_folder)
        # is equal or not
        # kbcqa_evaluation.get_top_k_grounded_graphes_by_path_match(structure_with_2_2_grounded_graph_folder)
        # evaluate log linear model
        # kbcqa_evaluation.grounded_graphes_by_score_standard_ywsun(input_file=structure_with_2_2_grounded_graph_folder)
        kbcqa_evaluation.grounded_graphes_by_score_standard_ywsun_prediction_test(input_file=structure_with_2_2_grounded_graph_folder)
        # kbcqa_evaluation.grounded_graphes_by_score_standard_no_aggregation(input_file=structure_with_2_2_grounded_graph_folder)

    elif dataset == 'graphq':
        # 3 evalution
        # from evaluation import kbcqa_evaluation
        # every grounded graph's f1
        # kbcqa_evaluation.computed_every_grounded_graph_f1_graphq(structure_with_2_2_grounded_graph_folder)
        # kbcqa_evaluation.computed_every_grounded_graph_f1(structure_with_2_2_grounded_graph_folder)

        # kbcqa_evaluation.compute_all_questions_recall(structure_with_2_2_grounded_graph_folder)
        # all questions recall
        # qids=read_set(fn_cwq_file.dataset+'test_composition_等.txt')
        # qids|=read_set(fn_cwq_file.dataset+'test_conjunction_等.txt')
        # kbcqa_evaluation.show_f1_given_qids(structure_with_2_2_grounded_graph_folder,qids=qids)

        # kbcqa_evaluation.compute_recall(structure_with_2_2_grounded_graph_folder)
        # is equal or not
        # kbcqa_evaluation.get_top_k_grounded_graphes_by_path_match(structure_with_2_2_grounded_graph_folder)
        # evaluate log linear model
        # kbcqa_evaluation.get_top_k_grounded_graphs_by_rank_linear(
        #     structure_with_2_2_grounded_graph_folder, top_k=10)
        # kbcqa_evaluation.get_top_k_grounded_graphs_by_score_standard(structure_with_2_2_grounded_graph_folder)
        kbcqa_evaluation.grounded_graphes_by_score_standard_ywsun(input_file=structure_with_2_2_grounded_graph_folder)
        pass

