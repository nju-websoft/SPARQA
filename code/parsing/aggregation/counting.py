from parsing import parsing_utils
from parsing import parsing_args

def is_count_funct(serialization_list):
    '''is_count_funct(serialization_list)'''
    is_count = False
    for element in serialization_list:
        if element in parsing_args.count_ner_tags:
            is_count = True
            break
    return is_count

def count_serialization(question):
    question_tokens_list = question.split(' ')
    serialization_list = ['O' for _ in question_tokens_list]
    for count_mention in parsing_args.count_phrases:
        if count_mention not in question:
            continue
        serialization_list = parsing_utils.serialization_mention(question_tokens_list, count_mention.split(' '), ner_tag='count')
    return serialization_list

def counting_recognition_interface():
    pass

def counting_binding():
    pass

def grounded_to_answers():
    pass

def grounded_graph_to_sparql():
    pass

def is_count_by_token_ner_tag(token):
    result = False
    if token.ner_tag is not None and token.ner_tag == 'count':
        result = True
    return result


