import json
from common_structs.grounded_graph import GroundedNode, GroundedEdge
from common import globals_args
from common.hand_files import read_dict

class GraphQuestion:
    '''graphquestion class'''
    def __init__(self):
        self.qid = ''  # int  251000000,
        self.question = ''  # string  "xtracycle is which type of bicycle?",
        self.answer = ''  # list  ["Longtail"]
        self.answer_mid = []
        self.function = ''  # string  "none"
        self.commonness = ''  # float   -19.635822428214723,
        self.num_node = ''  # int  2
        self.num_edge = ''  # int  1
        self.graph_query = ''  # dict
        self.nodes = []  # list
        self.edges = []  # list
        self.sparql_query = ''  # string   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX : <http://rdf.freebase.com/ns/> \nSELECT (?x0 AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \n?x0 :type.object.type :bicycles.bicycle_type . \nVALUES ?x1 { :en.xtracycle } \n?x1 :bicycles.bicycle_model.bicycle_type ?x0 . \nFILTER ( ?x0 != ?x1  )\n}\n}

def read_graph_question_json(filename):
    '''
    function: read graphquestion dataset
    :param filename: filename path file
    :return: graph_question structure list
    '''
    graphquestionsList = list()
    with open(filename, 'rb') as f:
        data = json.load(f)
    for questionAnnotation in data:
        graphq = GraphQuestion()
        graphq.qid = questionAnnotation["qid"]
        graphq.graph_entity_level_paraphrase_id = graphq.qid % 100
        graphq.graph_sentence_level_paraphrase_id = (graphq.qid // 100) % 10000
        graphq.graph_query_id = graphq.qid // 1000000
        # graphq.question = questionAnnotation["question"]
        graphq.question = questionAnnotation["question_normal"]
        graphq.answer = questionAnnotation["answer"]
        graphq.answer_mid = questionAnnotation["answer_mid"]
        graphq.function = questionAnnotation["function"]
        graphq.commonness = questionAnnotation["commonness"]
        graphq.num_node = questionAnnotation["num_node"]
        graphq.num_edge = questionAnnotation["num_edge"]
        graphq.graph_query = questionAnnotation["graph_query"]
        for node in questionAnnotation["graph_query"]["nodes"]:
            graphq.nodes.append(GroundedNode(
                nid=node["nid"], node_type=node["node_type"], type_class=node["class"],
                friendly_name=node["friendly_name"], question_node=node["question_node"],
                function=node["function"], id=node["id"], score=1.0))
        for edge in questionAnnotation["graph_query"]["edges"]:
            graphq.edges.append(GroundedEdge(
                start=edge["start"], end=edge["end"], relation=edge["relation"],
                friendly_name=edge["friendly_name"], score=1.0))
        graphq.sparql_query = questionAnnotation["sparql_query"]
        graphquestionsList.append(graphq)
    return graphquestionsList

test_graph_questions_struct = read_graph_question_json(globals_args.fn_graph_file.graphquestions_testing_dir)
train_graph_questions_struct = read_graph_question_json(globals_args.fn_graph_file.graphquestions_training_dir)

def get_answers_by_question(question=None):
    answers = []
    for data_ann in test_graph_questions_struct:
        if data_ann.question == question:
            answers = data_ann.answer
            break
    for data_ann in train_graph_questions_struct:
        if data_ann.question == question:
            answers = data_ann.answer
    return answers

def get_answers_mid_by_question(question=None):
    answers = []
    for data_ann in test_graph_questions_struct:
        if data_ann.question == question:
            answers = data_ann.answer_mid
            break
    for data_ann in train_graph_questions_struct:
        if data_ann.question == question:
            answers = data_ann.answer_mid
    # [80] -> ['80']
    new_gold_answers_set = set()
    for gold_answer in answers:
        if isinstance(gold_answer, int):
            new_gold_answers_set.add(str(gold_answer))
        else:
            new_gold_answers_set.add(gold_answer)
    return list(new_gold_answers_set)

