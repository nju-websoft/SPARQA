import os
from common.hand_files import read_structure_file, write_structure_file, write_json, read_list
import collections
from evaluation import sempre_evaluation
from evaluation import evaluation_utils

def computed_every_grounded_graph_f1_lcquad(input_file):
    from datasets_interface.question_interface import lcquad_1_0_interface
    all_structure_path = os.listdir(input_file)
    for structure_path in all_structure_path:
        structure_with_grounded_graphq_file = input_file + structure_path
        print(structure_path)
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            gold_answer_mid_set = lcquad_1_0_interface.get_answers_by_question(structure.question)
            print('#gold answer:\t', gold_answer_mid_set)
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    system_denotation_set = set(grounded_graph.denotation)
                    recall, precision, f1 = sempre_evaluation.computeF1(gold_answer_mid_set, system_denotation_set)
                    grounded_graph.f1_score = f1
                    if f1 > 0 :
                        print (f1)
        write_structure_file(structure_list, input_file + structure_path)

def computed_every_grounded_graph_f1_qald(input_file):
    all_structure_path = os.listdir(input_file)
    for structure_path in all_structure_path:
        structure_with_grounded_graphq_file = input_file + structure_path
        print(structure_path)
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            gold_answer_mid_set = evaluation_utils.get_gold_qald_answers(structure.gold_answer)
            print('#gold answer:\t', gold_answer_mid_set)
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    system_denotation_set = set(grounded_graph.denotation)
                    recall, precision, f1 = sempre_evaluation.computeF1(gold_answer_mid_set, system_denotation_set)
                    grounded_graph.f1_score = f1
                    if f1 > 0:
                        print (f1)
        write_structure_file(structure_list, input_file + structure_path)

def computed_every_grounded_graph_f1_webq_mid(input_file, answer_file):
    #read qid-to-answers
    all_structure_path = os.listdir(input_file)
    for structure_path in all_structure_path:
        structure_with_grounded_graphq_file = input_file + structure_path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            qid = structure.qid
            gold_answer_mid_set = evaluation_utils.search_for_answers_by_id(qid, qid_to_answers_dict)
            print(structure_path, gold_answer_mid_set)
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    system_denotation_set = set(grounded_graph.denotation)
                    recall, precision, f1 = sempre_evaluation.computeF1(gold_answer_mid_set, system_denotation_set)
                    grounded_graph.f1_score = f1
        write_structure_file(structure_list, input_file + structure_path)

def computed_every_grounded_graph_f1_webq_name(input_file, answer_file, mid_to_names_file):
    # from datasets_interface.freebase import webquestions_interface
    # from evaluation.webq_denotation import webq_mid_to_names_process
    #------------------------------------------------
    #read qid-to-answers
    qid_to_answers_dict = dict()
    lines = read_list(answer_file)
    for line in lines:
        cols = line.split('\t')
        qid_to_answers_dict[cols[0]] = eval(cols[2])
    #------------------------------------------------
    # mid to names dict
    mid_to_names_dict = dict()
    lines = read_list(mid_to_names_file)
    for line in lines:
        cols = line.split('\t')
        mid = cols[1]
        names = list(eval(cols[2]))
        mid_to_names_dict[mid] = names
    #------------------------------------------------
    all_structure_path = os.listdir(input_file)
    for structure_path in all_structure_path:
        structure_with_grounded_graphq_file = input_file + structure_path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        for structure in structure_list:
            qid = structure.qid
            gold_answer_names_set = evaluation_utils.search_for_answers_by_id(qid, qid_to_answers_dict)

            print(structure_path, '#gold:\t', gold_answer_names_set)
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    system_denotation_names_set = set()
                    for denotation_mid in grounded_graph.denotation:
                        denotation_name = evaluation_utils.get_name_by_mid(denotation_mid, mid_to_names_dict)
                        print ('###denotation:\t', denotation_mid, denotation_name)
                        if denotation_name is not None:
                            system_denotation_names_set.add(denotation_name)
                        else:
                            print(denotation_mid, '#####error!!!', denotation_name)
                    print('#gold:\t', gold_answer_names_set, '#system:\t', system_denotation_names_set)
                    recall, precision, f1 = sempre_evaluation.computeF1(gold_answer_names_set, system_denotation_names_set)
                    if f1 > 0.0:
                        print ('#result:\t', f1)
                    grounded_graph.f1_score = f1
        write_structure_file(structure_list, input_file + structure_path)

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

    from grounding.grounding_args import test_qid_to_answers_mid_dict, train_qid_to_answers_mid_dict
    for structure_path in os.listdir(input_file): #all_structure_path
        structure_with_grounded_graphq_file = input_file + structure_path
        print(structure_path)
        structure_list = read_structure_file(structure_with_grounded_graphq_file)

        for structure in structure_list:
            gold_answers_mid_set = []
            qid = structure.qid
            if qid in test_qid_to_answers_mid_dict:
                gold_answers_mid_set = test_qid_to_answers_mid_dict[qid]
            elif qid in train_qid_to_answers_mid_dict:
                gold_answers_mid_set = train_qid_to_answers_mid_dict[qid]

            #[80] -> ['80']
            new_gold_answers_set = set()
            for gold_answer in gold_answers_mid_set:
                if isinstance(gold_answer, int):
                    new_gold_answers_set.add(str(gold_answer))
                else:
                    new_gold_answers_set.add(gold_answer)
            gold_answers_mid_set = list(new_gold_answers_set)

            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    system_denotation_set = set(grounded_graph.denotation)
                    new_system_answers_set = set()
                    for system_answer in system_denotation_set:
                        if isinstance(system_answer, int):
                            new_system_answers_set.add(str(system_answer))
                        else:
                            new_system_answers_set.add(system_answer)
                    new_system_answers_set = list(new_system_answers_set)

                    recall, precision, f1 = sempre_evaluation.computeF1(gold_answers_mid_set, new_system_answers_set)
                    print (structure_path, gold_answers_mid_set, new_system_answers_set, f1)
                    grounded_graph.f1_score = f1
                    if f1 > 0:
                        print (f1)
            # update answers by answer mid list   ["Kimberly-Clark"]  ['en.kimberly-clark']
            structure.gold_answer = gold_answers_mid_set
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

# all questions, top-k, f1 score
def get_top_k_grounded_graphs_by_score_standard(input_file):
    count_number = 0
    all_f1_score = 0
    correctqids_top1 = list()
    correctqids_top3 = list()
    correctqids_top5 = list()
    correctqids_top10 = list()
    for structure_path in os.listdir(input_file):
        count_number += 1
        structure_list = read_structure_file(input_file + structure_path)

        totalscore_queryid_sparql = collections.defaultdict(list)
        grounded_graph_list = []
        # gold_answer_mid_set = set()
        grounded_query_id_denotation = collections.defaultdict(set)
        # denotations_all=set()

        f1_1_query_id_set = set()
        for structure in structure_list:
            # gold_answers = structure.gold_answer
            # for gold_answer_dict in gold_answers:
            #     gold_answer_mid_set.add(gold_answer_dict['answer_id'])
            for ungrounded_graph in structure.ungrounded_graph_forest:
                # ungrounded_graph_edges_num = len(ungrounded_graph.edges)
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    # edge constaints
                    # grounded_graph_edges_num = len(grounded_graph.edges)
                    # if grounded_graph_edges_num != ungrounded_graph_edges_num: continue
                    # totalscore_queryid_sparql[grounded_graph.total_score].append(grounded_graph.grounded_query_id)
                    totalscore_queryid_sparql[grounded_graph.score].append(grounded_graph.grounded_query_id)
                    grounded_query_id_denotation[grounded_graph.grounded_query_id] = grounded_graph.f1_score
                    # totalscore_queryid_sparql[grounded_graph.total_score].append(grounded_graph.grounded_query_id)

                    if grounded_graph.f1_score == 1.0:
                        f1_1_query_id_set.add(grounded_graph.grounded_query_id)

                    grounded_graph_list.append(grounded_graph)

        totalscore_queryid_sparql = dict(sorted(totalscore_queryid_sparql.items(), key=lambda d: d[0], reverse=True))
        for totalscore, grounded_query_ids in totalscore_queryid_sparql.items():
            for grounded_query_id in grounded_query_ids:
                f1_score = grounded_query_id_denotation[grounded_query_id]
                all_f1_score += f1_score
                print(('%s\t%s\t%s\t%s') % (structure_path, f1_score, grounded_query_id, f1_1_query_id_set))
                break
            break

        num = 0
        find = False
        now = []
        for totalscore, grounded_query_ids in totalscore_queryid_sparql.items():
            if num >= 10 or find:
                break

            for grounded_query_id in grounded_query_ids:
                if num >= 10 or find:
                    break
                f1_score = grounded_query_id_denotation[grounded_query_id]
                now.append([structure_path.split('.')[0], grounded_query_id])
                if f1_score == 1:
                    find=True
                    if num < 1:
                        correctqids_top1.append(now)
                    elif num < 3:
                        correctqids_top3.append(now)
                    elif num < 5:
                        correctqids_top5.append(now)
                    elif num < 10:
                        correctqids_top10.append(now)
                num += 1

    print('#all_f1_score:\t', all_f1_score)
    print('#count_number:\t', count_number)
    write_json(correctqids_top1, './correctqids_top1_.json')
    write_json(correctqids_top3, './correctqids_top3_.json')
    write_json(correctqids_top5,'./correctqids_top5_.json')
    write_json(correctqids_top10,'./correctqids_top10_.json')
    # print(path_match_correctqids)

# path match score, and oracle questions
def get_top_k_grounded_graphes_by_path_match_equal_or_not(input_file, top_k=1):
    all_structure_path = os.listdir(input_file)
    correct = 0
    count_number = 0
    oracle=0
    for structure_path in all_structure_path:
        isoracle=False
        structure_with_grounded_graphq_file = input_file + structure_path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        # print(structure_path)
        totalscore_queryid_sparql = collections.defaultdict(list)
        grounded_graph_list = []
        gold_answer_mid_set = set()
        grounded_query_id_denotation=collections.defaultdict(set)
        # denotations_all=set()
        for structure in structure_list:
            gold_answers = structure.gold_answer
            for gold_answer_dict in gold_answers:
                gold_answer_mid_set.add(gold_answer_dict['answer_id'])
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    totalscore_queryid_sparql[grounded_graph.score].append(grounded_graph.grounded_query_id)
                    grounded_query_id_denotation[grounded_graph.grounded_query_id]=set(grounded_graph.denotation)
                    if (len(gold_answer_mid_set - set(grounded_graph.denotation)) == 0) & (len(set(grounded_graph.denotation)-gold_answer_mid_set  ) == 0):
                        isoracle=True
                    # totalscore_queryid_sparql[grounded_graph.total_score].append(grounded_graph.grounded_query_id)
                    grounded_graph_list.append(grounded_graph)
                    # denotations_all|=set(grounded_graph.denotation)
        # print('gold_answer:', gold_answer_mid_set)
        totalscore_queryid_sparql = dict(sorted(totalscore_queryid_sparql.items(), key=lambda d: d[0], reverse=True))
        is_recall = False
        for totalscore, grounded_query_ids in totalscore_queryid_sparql.items():
            # print(totalscore, grounded_query_ids)
            # count_number += 1
            # denotation_set=set()
            for grounded_query_id in grounded_query_ids:
                denotation_set= grounded_query_id_denotation[grounded_query_id]
                # denotation_set= get_denotation_set(grounded_graph_list, grounded_query_id)
                if (len(gold_answer_mid_set - denotation_set) == 0) & (len(denotation_set-gold_answer_mid_set ) == 0):
                # if len(gold_answer_mid_set &denotation_set)>0:
                    is_recall = True
            break
        if isoracle:
            oracle+=1
        if is_recall==False:
            if isoracle:
                print('error', structure_path, list(totalscore_queryid_sparql.keys())[0])
            # if len(gold_answer_mid_set&denotations_all)>0:
            #     print('error',structure_path,list(totalscore_queryid_sparql.keys())[0])
        else:
            print('true',structure_path,list(totalscore_queryid_sparql.keys())[0])
        if is_recall:
            correct += 1
    #41,101,254
    print(correct, oracle)

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

        qid = None
        for structure in structure_list:
            qid = structure.qid
            for ungrounded_graph in structure.ungrounded_graph_forest:
                ungrounded_graph_edges_num = len(ungrounded_graph.edges)
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    # grounded_graph_edges_num = len(grounded_graph.edges)
                    # edge constaints
                    # if grounded_graph_edges_num != ungrounded_graph_edges_num: continue

                    score_to_queryid_sparql[grounded_graph.score].append(grounded_graph.grounded_query_id)
                    # score_to_queryid_sparql[grounded_graph.total_score].append(grounded_graph.grounded_query_id)
                    grounded_query_id_to_f1_denotation[grounded_graph.grounded_query_id] = grounded_graph.f1_score

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

def grounded_graphes_by_score_standard_no_aggregation(input_file):
    from datasets_interface.question_interface.complexwebquestion_interface import look_for_compositionality_type_by_id

    all_structure_path = os.listdir(input_file)
    count_number = 0
    all_f1_score = 0
    qid_f1_top1id_correctidlist__list = []
    for structure_path in all_structure_path:
        qid = structure_path.replace('.json', '')
        q_type = look_for_compositionality_type_by_id(qid=qid)
        if q_type in ['comparative', 'superlative']:
            continue
        print(structure_path, q_type)

        count_number += 1
        structure_with_grounded_graphq_file = input_file + structure_path
        structure_list = read_structure_file(structure_with_grounded_graphq_file)
        score_to_queryid_sparql = collections.defaultdict(list)
        grounded_query_id_to_f1_denotation = collections.defaultdict(set)
        qid = None

        for structure in structure_list:
            qid = structure.qid
            for ungrounded_graph in structure.ungrounded_graph_forest:
                # ungrounded_graph_edges_num = len(ungrounded_graph.edges)
                for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                    # grounded_graph_edges_num = len(grounded_graph.edges)
                    # edge constaints
                    # if grounded_graph_edges_num != ungrounded_graph_edges_num: continue
                    # score_to_queryid_sparql[grounded_graph.score].append(grounded_graph.grounded_query_id)
                    score_to_queryid_sparql[grounded_graph.total_score].append(grounded_graph.grounded_query_id)
                    grounded_query_id_to_f1_denotation[grounded_graph.grounded_query_id] = grounded_graph.f1_score

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
