
from common.hand_files import read_json
from common import globals_args
from common.globals_args import fn_cwq_file, root, q_mode as mode
from datasets_interface.question_interface.questions_utils import extract_grounded_graph_from_jena_freebase
from grounding.grounded_graph_to_sparql import sparql_to_denotation_freebase,  grounded_graph_to_sparql_CWQ

class QuestionMatchInterface():

    def __init__(self):
        if mode=='cwq':
            self.train_qid_to_grounded_graph_dict = extract_grounded_graph_from_jena_freebase(globals_args.fn_cwq_file.complexwebquestion_train_bgp_dir)
            self.testqid_trainqid_bertmax=read_json(fn_cwq_file.question_match_dir +'testqid_trainqid_bertmax.json')
            self.testqid_correspondingtrainqid_denotations=read_json(fn_cwq_file.question_match_dir+'testqid_correspondingtrainqid_denotations.json')

    def get_denotation_by_testqid_nodes_freebase(self, testqid, nodes):
        if mode=='cwq':
            if testqid in self.testqid_correspondingtrainqid_denotations:
                return self.testqid_correspondingtrainqid_denotations[testqid]
            if (testqid) not in self.testqid_trainqid_bertmax:
                return []
            trainqid = self.testqid_trainqid_bertmax[testqid]
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

    def get_score(self,testqid, denotations):
        testqid=str(testqid)
        testqid=str('test_'+testqid)
        if testqid in self.testqid_correspondingtrainqid_denotations:
            if len(self.testqid_correspondingtrainqid_denotations[testqid]) > 0:
                if len(set(denotations)-set(self.testqid_correspondingtrainqid_denotations[testqid]))==0 and \
                    len(set(self.testqid_correspondingtrainqid_denotations[testqid])-set(denotations))==0:
                    return 1
        return 0

