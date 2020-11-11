import os
from common.hand_files import read_structure_file, write_structure_file, write_json, read_list
import collections
from evaluation import sempre_evaluation
from evaluation import evaluation_utils

def computed_every_grounded_graph_f1_cwq(input_file):
    all_structure_path = os.listdir(input_file)
    for structure_path in all_structure_path:
        structure_with_grounded_graphq_file = input_file + structure_path
        print(structure_path)
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            gold_answer_mid_set = evaluation_utils.get_gold_answers(structure.gold_answer)
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    system_denotation_set = set(grounded_graph.denotation)
                    recall, precision, f1 = sempre_evaluation.computeF1(gold_answer_mid_set, system_denotation_set)
                    grounded_graph.f1_score = f1
                    if f1 > 0:
                        print (f1)
        write_structure_file(structure_list, input_file + structure_path)

def computed_every_grounded_graph_f1_graphq(input_file):
    from datasets_interface.question_interface import graphquestion_interface
    for structure_path in os.listdir(input_file):
        structure_with_grounded_graphq_file = input_file + structure_path
        print(structure_path)
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            gold_answers_mid_set = graphquestion_interface.get_answers_mid_by_question(structure.question)
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    system_denotation_set = set(grounded_graph.denotation)
                    new_system_answers_set = set()
                    for system_answer in system_denotation_set:
                        if isinstance(system_answer, int): new_system_answers_set.add(str(system_answer))
                        else: new_system_answers_set.add(system_answer)
                    new_system_answers_set = list(new_system_answers_set)
                    recall, precision, f1 = sempre_evaluation.computeF1(gold_answers_mid_set, new_system_answers_set)
                    print (structure_path, gold_answers_mid_set, new_system_answers_set, f1)
                    grounded_graph.f1_score = f1
                    if f1 > 0:
                        print (f1)
            structure.gold_answer = gold_answers_mid_set # update answers by answer mid list   ["Kimberly-Clark"]  ['en.kimberly-clark']
        write_structure_file(structure_list, input_file + structure_path)

# oracle all recall by max f1
def compute_all_questions_recall(input_file):
    '''
    # structure_with_2_2_grounded_graph_folder = output_file_folder + '/2.2_0_500/'
    # compute_recall(input_file=structure_with_2_2_grounded_graph_folder)
    :param input_file:
    :return:
    '''
    all_data_path = os.listdir(input_file)
    all_recall = 0
    for path in all_data_path:
        structure_with_grounded_graphq_file = input_file + path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        max_f1 = 0
        for structure in structure_list:
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    if max_f1 < grounded_graph.f1_score:
                        max_f1 = grounded_graph.f1_score
        all_recall += max_f1
        print(('%s\t%s') % (path, str(max_f1)))
    print(all_recall, len(all_data_path))

def grounded_graphes_by_score_standard_ywsun(input_file):
    all_structure_path = os.listdir(input_file)
    count_number = 0
    all_f1_score = 0
    qid_f1_top1id_correctidlist__list = []
    for structure_path in all_structure_path:
        print(structure_path)
        count_number += 1
        structure_with_grounded_graphq_file = input_file + structure_path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        score_to_queryid_sparql = collections.defaultdict(list)
        grounded_query_id_to_f1_denotation = collections.defaultdict(set)
        grounded_query_id_to_sparql_query = collections.defaultdict(set)

        qid = None
        for structure in structure_list:
            qid = structure.qid
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    score_to_queryid_sparql[grounded_graph.score].append(grounded_graph.grounded_query_id)
                    # score_to_queryid_sparql[grounded_graph.total_score].append(grounded_graph.grounded_query_id)
                    grounded_query_id_to_f1_denotation[grounded_graph.grounded_query_id] = grounded_graph.f1_score
                    grounded_query_id_to_sparql_query[grounded_graph.grounded_query_id] = grounded_graph.sparql_query

        qid_f1_score = 0.0
        top1id = None
        score_to_queryid_sparql = dict(sorted(score_to_queryid_sparql.items(), key=lambda d: d[0], reverse=True))
        for totalscore, grounded_query_ids in score_to_queryid_sparql.items():
            for grounded_query_id in grounded_query_ids:
                f1_score = grounded_query_id_to_f1_denotation[grounded_query_id]
                all_f1_score += f1_score
                top1id = grounded_query_id
                qid_f1_score = f1_score
                break
            break

        correctlist = []
        for score, grounded_query_ids in score_to_queryid_sparql.items():
            for grounded_query_id in grounded_query_ids:
                f1_score = grounded_query_id_to_f1_denotation[grounded_query_id]
                if f1_score == 1.0:
                    correctlist.append([grounded_query_id, score])
        qid_f1_top1id_correctidlist__list.append((qid, qid_f1_score, top1id, correctlist))

    print('#all_f1_score:\t', all_f1_score)
    print('#count_number:\t', count_number)
    fi = open('./every_q_result.txt', "w", encoding="utf-8")
    for (qid, qid_f1_score, top1id, correctlist) in qid_f1_top1id_correctidlist__list:
        fi.write('#qid:'+str(qid))
        fi.write("\t")
        fi.write('#f1:'+str(qid_f1_score))
        fi.write("\t")
        fi.write('#answer:'+str(top1id))
        fi.write("\t")
        fi.write('#shiji:'+str(correctlist))
        fi.write("\n")
    fi.close()

def grounded_graphes_by_score_standard_ywsun_prediction_test(input_file):
    from common.hand_files import write_json
    all_structure_path = os.listdir(input_file)
    # all_f1_score = 0
    prediction_list = []
    for structure_path in all_structure_path:
        print(structure_path)
        structure_list = read_structure_file(input_file + structure_path)
        score_to_queryid_sparql = collections.defaultdict(list)
        # grounded_query_id_to_f1_denotation = collections.defaultdict(set)
        grounded_query_id_to_denotation = collections.defaultdict(set)
        qid = None
        for structure in structure_list:
            qid = structure.qid
            for ungrounded_graph in structure.ungrounded_graph_forest:
                # ungrounded_graph_edges_num = len(ungrounded_graph.edges)
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    # grounded_graph_edges_num = len(grounded_graph.edges)
                    # edge constaints
                    # if grounded_graph_edges_num != ungrounded_graph_edges_num: continue
                    # score_to_queryid_sparql[grounded_graph.score].append(grounded_graph.grounded_query_id) #word level matcher
                    score_to_queryid_sparql[grounded_graph.total_score].append(grounded_graph.grounded_query_id)
                    # grounded_query_id_to_f1_denotation[grounded_graph.grounded_query_id] = grounded_graph.f1_score
                    grounded_query_id_to_denotation[grounded_graph.grounded_query_id] = grounded_graph.denotation
        answers = []
        score_to_queryid_sparql = dict(sorted(score_to_queryid_sparql.items(), key=lambda d: d[0], reverse=True))
        for totalscore, grounded_query_ids in score_to_queryid_sparql.items():
            for grounded_query_id in grounded_query_ids:
                answers = grounded_query_id_to_denotation[grounded_query_id]
                # all_f1_score += f1_score
                # top1id = grounded_query_id
                break
            break
        q_dict = dict()
        q_dict['ID'] = qid
        q_dict['answers_id'] = answers
        prediction_list.append(q_dict)
    write_json(prediction_list, './20191113_cwq_wo_wordlevel_prediction_test.json')

