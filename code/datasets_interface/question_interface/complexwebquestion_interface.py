import json
from common import globals_args

class ComplexWebQuestion:
    '''graphquestion class'''
    def __init__(self):
        self.ID = ''  # int  251000000,
        self.webqsp_ID = ''  # "WebQTrn-3252"
        self.webqsp_question = '' #webqsp_question
        self.machine_question = '' #machine_question
        self.question = '' #question
        self.sparql = '' #sparql
        self.compositionality_type = '' #compositionality_type
        self.answers = ''
        self.created = '' # created time

def _read_complexwebq_question_json(filename):
    complexwebq_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        complexwebq_json_data = json.load(f)
    for complexwebq in complexwebq_json_data:
        complexwebq_struct = ComplexWebQuestion()
        complexwebq_struct.question = complexwebq['question']
        complexwebq_struct.ID = complexwebq['ID']
        complexwebq_struct.answers = complexwebq['answers']
        complexwebq_struct.sparql = complexwebq['sparql']
        complexwebq_struct.compositionality_type = complexwebq['compositionality_type']
        complexwebq_list.append(complexwebq_struct)
    return complexwebq_list

all_complexwebq_list = _read_complexwebq_question_json(globals_args.fn_cwq_file.complexwebquestion_all_questions_dir)
def read_complexwebq_question_json(filename):
    '''
    function: read complexquestion dataset
    :param filename: filename path file
    :return: graph_question structure list
    '''
    complexwebq_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        complexwebq_json_data = json.load(f)
    for complexwebq in complexwebq_json_data:
        complexwebq_struct = ComplexWebQuestion()
        complexwebq_struct.ID = complexwebq['ID']
        complexwebq_struct.webqsp_ID = complexwebq['webqsp_ID']
        complexwebq_struct.webqsp_question = complexwebq['webqsp_question']
        complexwebq_struct.machine_question = complexwebq['machine_question']
        complexwebq_struct.question = complexwebq['question_normal'][0]
        complexwebq_struct.sparql = complexwebq['sparql']
        complexwebq_struct.compositionality_type = complexwebq['compositionality_type']
        if 'answers' in complexwebq:
            complexwebq_struct.answers = complexwebq['answers']
        else:
            complexwebq_struct.answers = look_for_answers_by_id(qid=complexwebq_struct.ID)
        complexwebq_struct.created = complexwebq['created']
        complexwebq_list.append(complexwebq_struct)
    return complexwebq_list

def look_for_answers_by_id(qid):
    answers = "none"
    for complexwebq_struct in all_complexwebq_list:
        if complexwebq_struct.ID == qid:
            answers = complexwebq_struct.answers
            break
    return answers

def look_for_question_by_id(qid):
    question = None
    for complexwebq_struct in all_complexwebq_list:
        if complexwebq_struct.ID == qid:
            question = complexwebq_struct.question
            break
    return question

def look_for_sparql_by_id(qid):
    sparql = None
    for complexwebq_struct in all_complexwebq_list:
        if complexwebq_struct.ID == qid:
            sparql = complexwebq_struct.sparql
            break
    return sparql

def look_for_compositionality_type_by_id(qid):
    compositionality_type = None
    for complexwebq_struct in all_complexwebq_list:
        if complexwebq_struct.ID == qid:
            compositionality_type = complexwebq_struct.compositionality_type
            break
    return compositionality_type

