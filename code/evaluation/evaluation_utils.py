import os
from common.hand_files import read_structure_file
from common.hand_files import write_json

def search_for_answers_by_id(qid, qid_to_answers_dict):
    # qid = 'webqtrn-'+str(qid)
    qid = 'webqtest-' + str(qid)
    # qid = 'WebQTrn-'+str(qid)
    # qid = 'WebQTest-'+str(qid)
    gold_answers = []
    if qid in qid_to_answers_dict.keys():
        gold_answers = qid_to_answers_dict[qid]
    # else:
    #     print(qid, 'not exist')
    return gold_answers

def get_gold_answers(gold_answers):
    '''get gold answers from structure'''
    gold_answer_mid_set = set()
    for gold_answer_dict in gold_answers:
        gold_answer_mid_set.add(gold_answer_dict['answer_id'])
    return gold_answer_mid_set

def get_gold_qald_answers(gold_answers):
    '''get gold answers from structure'''
    gold_answer_mid_set = set()
    for gold_answer_dict in gold_answers:
        if 'vars' not in gold_answer_dict['head']: continue
        head_var = gold_answer_dict['head']['vars'][0]
        if 'bindings' in gold_answer_dict['results']:
            for answer_uri in gold_answer_dict['results']['bindings']:
                gold_answer_mid_set.add(answer_uri[head_var]['value'])
    return gold_answer_mid_set

def get_denotation_set(grounded_graph_list, grounded_query_id):
    '''get denotation from grounded_graph list'''
    denotation_set = set()
    for grounded_graph in grounded_graph_list:
        if grounded_query_id == grounded_graph.grounded_query_id:
            denotation_set = set(grounded_graph.denotation)
    return denotation_set

def show_f1_given_qids(input_file,qids):
    qid_f1=dict()
    all_data_path = os.listdir(input_file)
    for path in all_data_path:
        if path.split('.')[0] in qids:
            structure_with_grounded_graphq_file = input_file + path
            structure_list = read_structure_file(structure_with_grounded_graphq_file)
            print(path)
            max_f1 = 0
            for structure in structure_list:
                for ungrounded_graph in structure.ungrounded_graph_forest:
                    for grounded_graph in ungrounded_graph.get_grounded_graph_forest():
                        if max_f1 < grounded_graph.f1_score:
                            max_f1 = grounded_graph.f1_score
            qid_f1[path.split('.')[0]]=max_f1
    write_json(qid_f1,'qid_f1.json')

def get_name_by_mid(mid, mid_to_names_dict):
    result = ''
    if mid in mid_to_names_dict:
        names = mid_to_names_dict[mid]
        if len(names) > 0:
            result = names[0]
    return result

