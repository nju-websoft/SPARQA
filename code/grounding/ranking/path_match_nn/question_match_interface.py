
from common.hand_files import read_json
from common import globals_args
from common.globals_args import fn_cwq_file, fn_lcquad_file, root, q_mode as mode
from datasets_interface.question_interface.questions_utils import extract_grounded_graph_from_jena_freebase, extract_grounded_graph_from_jena_dbpedia
from grounding.grounded_graph_to_sparql import sparql_to_denotation_dbpedia, sparql_to_denotation_freebase,  grounded_graph_to_sparql_CWQ, grounded_graph_to_sparql_LcQuAD

'''cwq,292道question match对了但是path match不对'''


class QuestionMatchInterface():

    def __init__(self):
        if mode=='cwq':
            self.train_qid_to_grounded_graph_dict = extract_grounded_graph_from_jena_freebase(globals_args.fn_cwq_file.complexwebquestion_train_bgp_dir)
            self.testqid_trainqid_bertmax=read_json(fn_cwq_file.question_match_dir +'testqid_trainqid_bertmax.json')
            self.testqid_correspondingtrainqid_denotations=read_json(fn_cwq_file.question_match_dir+'testqid_correspondingtrainqid_denotations.json')

        elif mode=='lcquad':
            self.train_qid_to_grounded_graph_dict = extract_grounded_graph_from_jena_dbpedia(fn_lcquad_file.lcquad_train_bgp_dir)
            self.testqid_trainqid_bertmax=read_json(fn_lcquad_file.question_match_dir +'testqid_trainqid_bertmax.json')
            self.testqid_correspondingtrainqid_denotations=read_json(fn_lcquad_file.question_match_dir+'testqid_correspondingtrainqid_denotations.json')
            # self.testqid_correspondingtrainqid_denotations={}

        elif mode=='webq':
            resources_webq = root + '/resources_webq/'
            data_question_match = resources_webq + 'data_question_match/'
            train_webq_bgp_filepath = root + '\dataset_questions\webquestions/2019.06.04_wsp_train_bgp.txt'
            self.train_qid_to_grounded_graph_dict = extract_grounded_graph_from_jena_freebase(train_webq_bgp_filepath)
            self.testqid_trainqid_bertmax = read_json(data_question_match + 'testqid_trainqid_bertmax.json')
            self.testqid_correspondingtrainqid_denotations = read_json(data_question_match+'testqid_correspondingtrainqid_denotations.json')


    def get_denotation_by_testqid_nodes_freebase(self, testqid, nodes):

        if mode=='cwq':
            if testqid in self.testqid_correspondingtrainqid_denotations:
                return self.testqid_correspondingtrainqid_denotations[testqid]

            if (testqid) not in self.testqid_trainqid_bertmax:
                return []

            trainqid = self.testqid_trainqid_bertmax[testqid]
            if trainqid not in self.train_qid_to_grounded_graph_dict:
                return []

        elif mode=='webq':
            print(testqid)
            print('test_' + str(testqid))
            if testqid in self.testqid_correspondingtrainqid_denotations:
                return self.testqid_correspondingtrainqid_denotations[testqid]
            if 'test_'+str(testqid) not in self.testqid_trainqid_bertmax:
                return []
            trainqid='WebQTrn-'+self.testqid_trainqid_bertmax['test_'+str(testqid)].split('_')[-1]
            print(trainqid)
            if trainqid not in self.train_qid_to_grounded_graph_dict:
                return []

        train_grounded_graph = self.train_qid_to_grounded_graph_dict[trainqid]  #获得所对应的最匹配的training grounded graph
        print (trainqid)
        # print(train_grounded_graph)
        # 测试问句中的entity 和 literal信息
        entitys = list()
        literals = list()
        for node in nodes:
            if node.node_type=='literal':
                literals.append(node.id)
            elif node.node_type=='entity':
                entitys.append(node.id)

        # 训练集问句中的entity 和 literal信息
        train_entitys = list()
        train_literals = list()
        for node in train_grounded_graph.nodes:
            if node.node_type=='literal':
                train_literals.append(node.id)
            elif node.node_type=='entity':
                train_entitys.append(node.id)
        print(train_entitys)
        print(entitys)
        print(train_literals)
        print(literals)

        # 如果个数不相等, 直接更新testqid_correspondingtrainqid_denotations, 然后跳出来
        if len(train_entitys) != len(entitys) or len(train_literals) != len(literals):
            self.testqid_correspondingtrainqid_denotations[testqid]=[]
            print('not equal nodes')
            return []

        # 复制training grounded graph图
        graph = train_grounded_graph.get_copy()

        if len(train_entitys) == 1:
            # 重新复制
            for node in graph.nodes:
                if node.node_type == 'entity':
                    node.id = entitys[0]

            if len(train_literals)>0:
                for node in graph.nodes:
                    if node.node_type == 'literal':
                        node.id = literals[0]
            print(graph)

            sparql = grounded_graph_to_sparql_CWQ(graph)
            print(sparql)
            denotation = sparql_to_denotation_freebase(sparql)
            self.testqid_correspondingtrainqid_denotations[testqid] = list(denotation)
            return denotation

        elif len(train_entitys)==0:
            if len(train_literals) > 0:
                for node in graph.nodes:
                    if node.node_type == 'literal':
                        node.id = literals[0]
            print(graph)
            sparql = grounded_graph_to_sparql_CWQ(graph)
            print(sparql)
            denotation = sparql_to_denotation_freebase(sparql)
            self.testqid_correspondingtrainqid_denotations[testqid] = list(denotation)
            return denotation

        else:
            firstused=False
            for node in graph.nodes:
                if node.node_type=='entity':
                    if firstused:
                        node.id = entitys[1]
                    else:
                        node.id=entitys[0]
                        firstused=True
            # print(train_grounded_graph)
            print(graph)

            sparql = grounded_graph_to_sparql_CWQ(graph)
            print(sparql)
            denotation = sparql_to_denotation_freebase(sparql)
            if len(denotation)==0:
                firstused = False
                for node in graph.nodes:
                    if node.node_type == 'entity':
                        if firstused:
                            node.id = entitys[0]
                        else:
                            node.id = entitys[1]
                            firstused = True
                print(graph)
                sparql = grounded_graph_to_sparql_CWQ(graph)
                print(sparql)
                denotation = sparql_to_denotation_freebase(sparql)
            self.testqid_correspondingtrainqid_denotations[testqid] = list(denotation)
            return denotation


    def get_denotation_by_testqid_nodes_dbpedia(self, testqid, nodes):

        if mode == 'lcquad':
            if testqid in self.testqid_correspondingtrainqid_denotations:
                return self.testqid_correspondingtrainqid_denotations[testqid]
            if (testqid) not in self.testqid_trainqid_bertmax:
                return []

            trainqid = self.testqid_trainqid_bertmax[testqid]
            if trainqid not in self.train_qid_to_grounded_graph_dict:
                return []

        train_grounded_graph = self.train_qid_to_grounded_graph_dict[trainqid]
        print (trainqid)

        # print(train_grounded_graph)
        entitys = list()
        literals = list()
        for node in nodes:
            if node.node_type=='literal':
                literals.append(node.id)
            elif node.node_type=='entity':
                entitys.append(node.id)

        train_entitys = list()
        train_literals = list()
        for node in train_grounded_graph.nodes:
            if node.node_type=='literal':
                train_literals.append(node.id)
            elif node.node_type=='entity':
                train_entitys.append(node.id)

        print(train_entitys)
        print(entitys)
        print(train_literals)
        print(literals)
        if len(train_entitys) != len(entitys) or len(train_literals) != len(literals):
            self.testqid_correspondingtrainqid_denotations[testqid]=[]
            print('not equal nodes')
            return []

        graph = train_grounded_graph.get_copy()
        if len(train_entitys) == 1:

            for node in graph.nodes:
                if node.node_type == 'entity':
                    node.id = entitys[0]

            if len(train_literals)>0:
                for node in graph.nodes:
                    if node.node_type == 'literal':
                        node.id = literals[0]
            print(graph)

            sparql = grounded_graph_to_sparql_LcQuAD(graph)
            print(sparql)
            denotation = sparql_to_denotation_dbpedia(sparql)
            self.testqid_correspondingtrainqid_denotations[testqid] = list(denotation)
            return denotation

        elif len(train_entitys)==0:
            if len(train_literals) > 0:
                for node in graph.nodes:
                    if node.node_type == 'literal':
                        node.id = literals[0]
            print(graph)
            sparql = grounded_graph_to_sparql_LcQuAD(graph)
            print(sparql)
            denotation = sparql_to_denotation_dbpedia(sparql)
            self.testqid_correspondingtrainqid_denotations[testqid] = list(denotation)
            return denotation

        else:
            firstused=False
            for node in graph.nodes:
                if node.node_type=='entity':
                    if firstused:
                        node.id = entitys[1]
                    else:
                        node.id=entitys[0]
                        firstused=True
            # print(train_grounded_graph)
            print(graph)

            sparql = grounded_graph_to_sparql_LcQuAD(graph)
            print(sparql)
            denotation = sparql_to_denotation_dbpedia(sparql)
            if len(denotation)==0:
                firstused = False
                for node in graph.nodes:
                    if node.node_type == 'entity':
                        if firstused:
                            node.id = entitys[0]
                        else:
                            node.id = entitys[1]
                            firstused = True
                print(graph)
                sparql = grounded_graph_to_sparql_LcQuAD(graph)
                print(sparql)
                denotation = sparql_to_denotation_dbpedia(sparql)
            self.testqid_correspondingtrainqid_denotations[testqid] = list(denotation)
            return denotation


    def get_score(self,testqid, denotations):
        testqid=str(testqid)
        testqid=str('test_'+testqid)
        if testqid in self.testqid_correspondingtrainqid_denotations:
            if len(self.testqid_correspondingtrainqid_denotations[testqid]) > 0:
                if len(set(denotations)-set(self.testqid_correspondingtrainqid_denotations[testqid]))==0 and \
                    len(set(self.testqid_correspondingtrainqid_denotations[testqid])-set(denotations))==0:
                    return 1
        return 0


# def read_test_data_bert_output(filepath):
#     diction = dict()
#     with open(filepath, 'r') as f:
#         mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
#         line = mm.readline()
#         while line:
#             cols = line.decode().strip().split('\t')
#             input_pair='\t'.join([cols[0],cols[1]])
#             diction[input_pair] = float(cols[3])
#             line = mm.readline()
#     mm.close()
#     f.close()
#     return diction
# qid_abstractquestions = read_json(fn_cwq_file.question_match_dir + 'qid_abstractquestion.json')
# outpupair_pro=read_test_data_bert_output(fn_cwq_file.question_match_dir + 'testdata_predicatematch_v1_forbert_result.json')

# def get_predicatematch_v1_bert_score(test_qid,predicate_path):
#     if test_qid not in qid_abstractquestions:
#         return 0
#     abstractquestion=qid_abstractquestions[test_qid]
#     predicate_path=' '.join(predicate_path.split('\t'))
#     pair='\t'.join([abstractquestion,predicate_path])
#     if pair in outpupair_pro:
#         # print(pair)
#         return outpupair_pro[pair]
#     return 0
