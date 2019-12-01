import collections
import random
import mmap
import os

# from common import globals_args
from common.globals_args import root
from common.hand_files import write_json, read_json,read_structure_file
from grounding.ranking.path_match_nn.question_match_interface import QuestionMatchInterface
from datasets_interface.question_interface import questions_utils

resources_cwq=root+'/dataset_cwq_1_1/'
data_question_match=resources_cwq+'data_question_match/'
test_cwq_bgp_filepath=resources_cwq+'/ComplexWebQuestions_test_bgp.txt'
dev_cwq_bgp_filepath=resources_cwq+'/ComplexWebQuestions_dev_bgp.txt'
train_cwq_bgp_filepath=resources_cwq+'/ComplexWebQuestions_train_bgp.txt'

output_path = resources_cwq + '/output_cwq'
# train_structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_all_train_head_0901_0_5000.json'
# train_structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_all_train_head_0901_0_15000.json'
train_structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_all_train_head_0901.json'
# dev_structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_all_dev_head_0901.json'
test_structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_all_test_head_0901.json'

def generate_qid_abstractquestion():
    # dev_2_1 = read_structure_file(dev_structure_with_2_1_grounded_graph_file)
    test_2_1 = read_structure_file(test_structure_with_2_1_grounded_graph_file)
    train_2_1 = read_structure_file(train_structure_with_2_1_grounded_graph_file)
    qid_abstractquestion = dict()
    any_2_1_dict = {'train':train_2_1,'test':test_2_1} #'dev': dev_2_1
    for key in any_2_1_dict:
        any_2_1=any_2_1_dict[key]
        for one in any_2_1:
            qid = key+"_"+str(one.qid)
            question = one.question
            for ungrounded_graph in one.ungrounded_graph_forest:
                question_ = question
                for node in ungrounded_graph.nodes:
                    if node.node_type == 'entity':
                        question_ = question_.replace(node.friendly_name, '<e>')
                qid_abstractquestion[qid]=question_
                break
    # print(len(qid_abstractquestions))
    write_json(qid_abstractquestion,data_question_match+'qid_abstractquestion.json')
    return qid_abstractquestion

def generate_predicate_qids():
    train_qid_to_grounded_graph_dict = questions_utils.extract_grounded_graph_from_jena_freebase(train_cwq_bgp_filepath)
    # dev_qid_to_grounded_graph_dict = questions_utils.extract_grounded_graph_from_jena_freebase(dev_cwq_bgp_filepath)
    test_qid_to_grounded_graph_dict = questions_utils.extract_grounded_graph_from_jena_freebase(test_cwq_bgp_filepath)
    qid_abstractquestions = read_json(data_question_match + 'qid_abstractquestion.json')

    train_predicate_qids = collections.defaultdict(list)
    for qid, grounded_graph in train_qid_to_grounded_graph_dict.items():
        # qid='train_'+str(qid.split('-')[1])
        qid='train_' + qid
        if qid not in qid_abstractquestions:
            continue
        predicates = []
        for edge in grounded_graph.edges:
            predicates.append(edge.friendly_name)
        predicates.sort()
        predicate = '\t'.join(predicates)
        # print(qid)
        if len(qid_abstractquestions[qid]) > 0:
            # print('hi',qid)
            # abstractquestion = qid_abstractquestions[qid]
            train_predicate_qids[predicate].append(qid)
    write_json(train_predicate_qids,data_question_match + 'train_predicate_qids.json')

    test_predicate_qids = collections.defaultdict(list)
    for qid, grounded_graph in test_qid_to_grounded_graph_dict.items():
        # qid = 'test_' + str(qid.split('-')[1])
        qid='test_' + qid
        if qid not in qid_abstractquestions:
            continue
        predicates = []
        for edge in grounded_graph.edges:
            predicates.append(edge.friendly_name)
        predicates.sort()
        predicate = '\t'.join(predicates)
        if len(qid_abstractquestions[qid]) > 0:
            # abstractquestion = qid_abstractquestions[qid]
            test_predicate_qids[predicate].append(qid)
    write_json(test_predicate_qids, data_question_match + 'test_predicate_qids.json')

    # dev_predicate_qids = collections.defaultdict(list)
    # for qid, grounded_graph in dev_qid_to_grounded_graph_dict.items():
    #     # qid = 'dev_' + str(qid.split('-')[1])
    #     qid='dev_' + qid
    #     if qid not in qid_abstractquestions:
    #         continue
    #     predicates = []
    #     for edge in grounded_graph.edges:
    #         predicates.append(edge.friendly_name)
    #     predicates.sort()
    #     predicate = '\t'.join(predicates)
    #     if len(qid_abstractquestions[qid]) > 0:
    #         # abstractquestion = qid_abstractquestions[qid]
    #         dev_predicate_qids[predicate].append(qid)
    # write_json(dev_predicate_qids, data_question_match + 'dev_predicate_qids.json')

    num_intersect=0
    # 2718
    for predicate in test_predicate_qids:
        if predicate in train_predicate_qids:
            num_intersect += len(test_predicate_qids[predicate])
    print(num_intersect)

def generate_trainset():
    trainset=[]
    train_predicate_qids = read_json(data_question_match + 'train_predicate_qids.json')
    qid_abstractquestions = read_json(data_question_match + 'qid_abstractquestion.json')

    abstractquestion_all=set()
    for predicate in train_predicate_qids:
        for qid in train_predicate_qids[predicate]:
            #"train_WebQTrn-3513_7c4117891abf63781b892537979054c6",
            if qid in qid_abstractquestions:
                abstractquestion_all.add(qid_abstractquestions[qid])

    for k, predicate in enumerate(train_predicate_qids):
        print(k, predicate)

        same_abstractquestions = set()
        for qid in train_predicate_qids[predicate]:
            if qid in qid_abstractquestions:
                same_abstractquestions.add(qid_abstractquestions[qid])

        residu_abstractquestions=(list(abstractquestion_all-same_abstractquestions))
        same_abstractquestions=list(same_abstractquestions)[:10]

        for first, current in enumerate(same_abstractquestions):
            for second, gold in enumerate(same_abstractquestions):
                if current != gold:
                    random.shuffle(residu_abstractquestions)
                    neg_samples = residu_abstractquestions[:50]
                    trainset.append([current, gold, 1])
                    for neg in neg_samples:
                        trainset.append([current, neg, 0])

        # if len(same_abstractquestions)>1:
        #     current=list(same_abstractquestions)[0]
        #     gold=list(same_abstractquestions)[1]
        #     random.shuffle(residu_abstractquestions)
        #     neg_samples = residu_abstractquestions[:20]
        #     trainset.append([current,gold,1])
        #     for neg in neg_samples:
        #         trainset.append([current, neg, 0])
        #     # trainset.append([current, gold, neg_samples])
        #     current = list(same_abstractquestions)[1]
        #     gold = list(same_abstractquestions)[0]
        #     random.shuffle(residu_abstractquestions)
        #     neg_samples = residu_abstractquestions[:20]
        #     trainset.append([current, gold, 1])
        #     for neg in neg_samples:
        #         trainset.append([current, neg, 0])
        #     # trainset.append([current, gold, neg_samples])

    write_json(trainset,data_question_match + 'trainset.json')

def generate_testset():
    testset=[]
    test_2_1 = read_structure_file(test_structure_with_2_1_grounded_graph_file)
    train_predicate_qids = read_json(data_question_match + 'train_predicate_qids.json')
    qid_abstractquestions = read_json(data_question_match + 'qid_abstractquestion.json')

    train_abstractquestion = set()
    for predicate in train_predicate_qids:
        for qid in train_predicate_qids[predicate]:
            if qid in qid_abstractquestions:
                train_abstractquestion.add(qid_abstractquestions[qid])

    test_abstractquestions=set()
    for one in test_2_1:
        if 'test_'+str(one.qid) in qid_abstractquestions:
            abstractquestion=qid_abstractquestions['test_'+str(one.qid)]
            test_abstractquestions.add(abstractquestion)

    for abstractquestion in test_abstractquestions:
        for ta in train_abstractquestion:
            testset.append([abstractquestion, ta])
    write_json(testset, data_question_match+ 'testset.json')

def score_testquestion_bert():

    def reverse(path):
        data = read_json(path)
        res = dict()
        for key in data:
            for val in data[key]:
                res[val] = key
        return res

    # def read_abstractquestionpair_pro():
    #     diction = dict()
    #     with open(data_question_match + '09_03_cwq_test_gpu.log', 'r') as f: #'05_10_test.log'
    #         mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    #         line = mm.readline()
    #         while line:
    #             cols = line.decode().strip().split('\t')
    #             abstractquestion_pair = '\t'.join([cols[0], cols[1]])
    #             if float(cols[3]) > 0:
    #                 diction[abstractquestion_pair] = float(cols[3])
    #             line = mm.readline()
    #     mm.close()
    #     f.close()
    #     return

    def read_abstractquestionpair_pro():
        diction = dict()
        with open(data_question_match + '09_03_cwq_test_gpu.log', 'r') as f: #'05_10_test.log'
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            line = mm.readline()
            while line:
                cols = line.decode().strip().split('\t')
                abstractquestion_pair = '\t'.join([cols[1], cols[2]])
                if float(cols[4]) > 0:
                    diction[abstractquestion_pair] = float(cols[4])
                line = mm.readline()
        mm.close()
        f.close()
        return diction


    abstractquestionpair_pro = read_abstractquestionpair_pro()
    # print(abstractquestionpair_pro)
    testqid_trainqidmax = dict()
    test_qid_trainqid_pro = dict()
    qid_abstractquestion = read_json(data_question_match + 'qid_abstractquestion.json')
    test_2_1 = read_structure_file(test_structure_with_2_1_grounded_graph_file)
    train_2_1 = read_structure_file(train_structure_with_2_1_grounded_graph_file)
    test_qid_predicate=reverse(data_question_match+'test_predicate_qids.json')
    train_qid_predicate=reverse(data_question_match+'train_predicate_qids.json')

    for one in test_2_1:
        qid='test_'+str(one.qid)
        print(qid)
        if qid not in qid_abstractquestion:
            continue
        abstractquestion = qid_abstractquestion[qid]

        trainqid_pro = dict()
        for train_one in train_2_1:
            train_one_qid = 'train_'+str(train_one.qid)
            if train_one_qid not in qid_abstractquestion:
                continue

            train_abstractquestion = qid_abstractquestion[train_one_qid]
            if '\t'.join([abstractquestion,train_abstractquestion]) in abstractquestionpair_pro:
                # print('\t'.join([abstractquestion,train_abstractquestion]))
                sim = abstractquestionpair_pro[('\t'.join([abstractquestion,train_abstractquestion]))]
                trainqid_pro[train_one_qid] = float(sim)

        trainqid_pro=dict(sorted(trainqid_pro.items(),key=lambda d:d[1],reverse=True))
        if len(trainqid_pro)==0:
            continue

        if qid in test_qid_predicate:
            if list(trainqid_pro.keys())[0] in train_qid_predicate:
                if test_qid_predicate[qid] == train_qid_predicate[list(trainqid_pro.keys())[0]]:
                    print('yeah')

        test_qid_trainqid_pro[qid] = trainqid_pro
        if len( list(trainqid_pro.keys())) > 0:
            testqid_trainqidmax[qid] = list(trainqid_pro.keys())[0]
    write_json(test_qid_trainqid_pro,data_question_match+'test_qid_trainqid_pro_bert')
    write_json(testqid_trainqidmax,data_question_match+'testqid_trainqid_bertmax.json')


def investigate_denotation_same():

    testqid_trainqid_bertmax = read_json(data_question_match + 'testqid_trainqid_bertmax.json')
    qmi = QuestionMatchInterface()
    structure_2_2_files = '/2.2_test_span_transfer_wo_wordlevel/'
    all_data_path = os.listdir(output_path+structure_2_2_files)
    for path in all_data_path:
        print(path)
        test_qid = path.split('.')[0]
        test_qid = 'test_' + str(test_qid)
        # if 'test_'+str(test_qid) not in testqid_trainqid_bertmax:
        if test_qid not in testqid_trainqid_bertmax:
            continue
        # structure_with_grounded_graphq_file = output_path + structure_2_2_files + path
        structure_list = read_structure_file(output_path + structure_2_2_files + path)
        for structure in structure_list:
            for ungrounded_graph in structure.ungrounded_graph_forest:
                nodes = []
                for groundedgraph in ungrounded_graph.get_grounded_graph_forest():
                    nodes = groundedgraph.nodes
                    break
                # print(test_qid)
                # denotation = set(qmi.get_denotation_by_testqid_nodes(test_qid, nodes))
                denotation = set(qmi.get_denotation_by_testqid_nodes_freebase(test_qid, nodes))
                print('denotations:', denotation)
                # gold_mids = set()
                # for one in structure.gold_answer:
                #     gold_mids.add(one['answer_id'])
                #
                # if  (len(denotation-gold_mids)==0 and len(gold_mids-denotation)==0):
                #     print('oh no',test_qid)
                #     if test_qid in qmunique_qids:
                #         print('double oh no')
    write_json(qmi.testqid_correspondingtrainqid_denotations, data_question_match+'testqid_correspondingtrainqid_denotations.json')


if __name__=='__main__':

    '''1'''
    # generate_qid_abstractquestion()

    '''2'''
    # "education.educational_institution.sports_teams\tlocation.mailing_address.state_province_region\torganization.organization.headquarters": [
       # "train_WebQTrn-3513_7c4117891abf63781b892537979054c6",
       #  "train_WebQTrn-2348_7c4117891abf63781b892537979054c6",
    # ],
    # generate_predicate_qids()

    '''3'''
    # [
    #     "What state is they university where the <e> located ?",
    #     "What location of the <e> is the place in which the local time zone is <e> ?",
    #     0
    # ],
    # generate_trainset()
    # [
    #     "In which movies , does <e> act in , that was released after Jan 22 , 2004 ?",
    #     "Who portrayed <e> in the movie with another character called <e> ?"
    # ],
    # generate_testset()

    '''4'''
    score_testquestion_bert()
    # investigate_denotation_same()
