import re
from parsing.models.fine_tuning_based_on_bert_interface import token_classifier_interface
from parsing import parsing_args
from common_structs.ungrounded_graph import UngroundedNode
from parsing import parsing_utils
from common import globals_args

def generate_nodes(question_normal, qid=None, tokens=None):
    '''recognize nodes'''
    # bert ner
    bert_sequence_ner_tag_dict = run_generate_bert_ner_tag_dict(question_normal)
    print('#bert ner:\t', bert_sequence_ner_tag_dict)

    # generate sutime annotation
    sutime_dict = run_generate_sutime_tag_dict(question_normal)
    print('#sutime:\t', sutime_dict)

    # generate corenlp ner
    corenlp_sequence_ner_tag_dict = run_generate_ner_corenlp_tag_dict(question_normal)
    print('#corenlp ner:\t', corenlp_sequence_ner_tag_dict)

    # generate ngram el annotation
    el_node_ngram_dict = run_generate_ngram_el_dict(qid)
    print('#ngram el\t', el_node_ngram_dict)

    quotation_mark_el_dict = run_generate_quotation_mark_ner_dict(question_normal)
    # print('#quotation_mark_el:\t', quotation_mark_el_dict)

    '''construct nodes'''
    nid = 0
    #bert
    # if bert_sequence_ner_tag_dict is not None and len(bert_sequence_ner_tag_dict) > 0:
    nodes, nid = add_bert_ner_dict(nid=nid, bert_sequence_ner_tag_dict=bert_sequence_ner_tag_dict, yuanshi_tokens=tokens)
    #sutime
    if sutime_dict is not None : #and len(sutime_dict) > 0
        nodes, nid = add_sutime_ner_dict(nid=nid, sutime_dict=sutime_dict, yuanshi_nodes=nodes)
    #corenlp ner
    # if corenlp_sequence_ner_tag_dict is not None and len(corenlp_sequence_ner_tag_dict) > 0:
    nodes, nid = add_corenlp_ner_dict(nid=nid, corenlp_sequence_ner_tag_dict=corenlp_sequence_ner_tag_dict, yuanshi_nodes=nodes, yuanshi_tokens=tokens)

    # if el_node_ngram_dict is not None and len(el_node_ngram_dict) > 0:
    nodes, nid = add_el_node_ngram_or_quotation_dict(nid=nid, el_node_ngram_dict=el_node_ngram_dict, yuanshi_nodes=nodes, yuanshi_tokens=tokens)

    # if quotation_mark_el_dict is not None and len(quotation_mark_el_dict) > 0:
    nodes, nid = add_el_node_ngram_or_quotation_dict(nid=nid, el_node_ngram_dict=quotation_mark_el_dict, yuanshi_nodes=nodes, yuanshi_tokens=tokens)

    # 后处理: 暂时关闭
    # if len(nodes)==1:
    #     blank_node = add_wh_words(tokens=tokens, nid=nid+1, nodes=nodes)
    #     if blank_node is not None:
    #         nodes.append(blank_node)
    #后处理: question node
    ungrounded_nodes = parsing_utils.set_question_node(nodes)
    return ungrounded_nodes

#----------------------------------------

def run_generate_bert_ner_tag_dict(question_normal):
    '''ner node mention recognize'''
    sentence_annotation = token_classifier_interface.process(sequence=question_normal)
    sequence_ner_tag_dict = parsing_utils.merge_ner_sequence(sentence_annotation)
    return sequence_ner_tag_dict

def run_generate_ner_corenlp_tag_dict(question_normal):
    '''ner corenlp
    # corenlp_sequence_ner_tag_dict = node_recognition_interface.corenlp_ner_annotation(qustion_normal)
    # print('#corenlp ner result:\t', sequence_ner_list)
    # print('#after merge result:\t', sequence_ner_tag_dict)
    '''
    sequence_ner_list = parsing_args.nltk_nlp.get_ner(question_normal)
    corenlp_sequence_ner_tag_dict = parsing_utils.merge_ner_sequence(sequence_ner_list)
    return corenlp_sequence_ner_tag_dict

def run_generate_ngram_el_dict(qid):
    '''ngram el, entity mention
      qid = 267000000
      filename = './2018.02.25_graphq_test_ngram_el.txt'
    '''
    result_dict = {}
    if qid is None \
            or globals_args.fn_graph_file.ngram_el_qid_to_position_grounding_result_dict is None:
        return result_dict
    if qid in globals_args.fn_graph_file.ngram_el_qid_to_position_grounding_result_dict.keys() \
            and globals_args.q_mode == 'graphq':
        result_dict = globals_args.fn_graph_file.ngram_el_qid_to_position_grounding_result_dict[qid]
    return result_dict

def run_generate_quotation_mark_ner_dict(question_normal):
    '''What is the name of the capital of Australia where the film \" The Squatter \'s Daughter \" was made ?'''
    quotation_mark_dict = dict()
    def sub_string(utterance):
        rule = r'.*\"(.*)\".*'
        result = re.findall(rule, utterance)
        return result

    result = sub_string(utterance=question_normal)
    tokens = question_normal.split(' ')
    for x in result:
        x = x.strip()
        mention_word_list = x.split(' ')
        for i in range(len(tokens)):
            for j in range(len(tokens)):
                if tokens[i:j] == mention_word_list:
                    start_index = i
                    end_index = j - 1
                    quotation_mark_dict[str(start_index)+'\t'+str(end_index)] = 'entity'
    return quotation_mark_dict

def run_generate_sutime_tag_dict(question_normal):
    '''sutime dict list
        :return 9\t9  {'text': '07/16/1902', 'value': '1902-07-16', 'type': 'DATE'}
        '''
    sutime_result = parsing_args.sutime.parse(question_normal)
    '''[{'start': 86, 'end': 100, 'text': 'March 4 , 1933', 'type': 'DATE', 'value': '1933-03-04'}]'''
    result_dict = dict()
    for time_mention in sutime_result:
        simple_sutime = dict()
        simple_sutime['text'] = time_mention['text']
        simple_sutime['value'] = time_mention['value']
        simple_sutime['type'] = time_mention['type']
        start_char = time_mention['start']
        end_char = time_mention['end']
        start_token_index, end_token_index = parsing_utils.char_index_to_token_index(
            question_normal, start_char, end_char)
        start_end_index = str(start_token_index) + '\t' + str(end_token_index)
        result_dict[start_end_index] = simple_sutime
    return result_dict

#-----------------------------

def add_bert_ner_dict(nid, bert_sequence_ner_tag_dict, yuanshi_tokens):
    nodes = []
    for sequence_start_end, ner_tag in bert_sequence_ner_tag_dict.items():
        # if ner_tag not in ['class', 'entity', 'literal', 'comparative',
        # 'count', 'superlative', 'target']: continue
        if ner_tag not in ['class', 'entity', 'literal']:
            continue
        nid += 1
        sequence_start = int(sequence_start_end.split('\t')[0])
        sequence_end = int(sequence_start_end.split('\t')[1])
        friendly_name = parsing_utils.get_friendly_name(
            tokens=yuanshi_tokens, sequence_start=sequence_start, sequence_end=sequence_end)
        node = UngroundedNode(nid=nid, node_type=ner_tag, friendly_name=friendly_name,
                              question_node=0, score=1.0,
                              start_position=sequence_start,
                              end_position=sequence_end)
        if node.node_type == 'literal':
            node.type_class = parsing_utils.get_literal_classifier(friendly_name)
        # node.function = parser_utils.ner_to_function(friendly_name, ner_tag)
        # if ner_tag == 'target': node.node_type = 'class'
        # graphquestions
        # if friendly_name == 'the' or friendly_name == 'a': continue  # postprocessing the class
        nodes.append(node)
    return nodes, nid

def add_sutime_ner_dict(nid, sutime_dict, yuanshi_nodes):
    remove_nodes = []
    for sequence_start_end, time_dict in sutime_dict.items():
        if time_dict['type'] != 'DATE':
            continue  # 只处理date
        # sutime:	 {'6\t6': {'text': 'recently', 'value': 'PAST_REF', 'type': 'DATE'}}

        if time_dict['value'] in ['PAST_REF', 'FUTURE_REF', 'PRESENT_REF']:
            continue # 类似once

        nid += 1
        sequence_start = int(sequence_start_end.split('\t')[0])
        sequence_end = int(sequence_start_end.split('\t')[1])
        is_contain_or_overlap = False
        for node in yuanshi_nodes:
            if node.start_position <= sequence_start and sequence_end <= node.end_position:
                #bert包含literal
                is_contain_or_overlap = True
            if node.start_position == sequence_start and node.end_position == sequence_end:
                node.normalization_value = sutime_dict[sequence_start_end]['value'] + '^^http://www.w3.org/2001/XMLSchema#datetime'
                node.node_type = 'literal'  # sutime_dict[sequence_start_end]['type']
                node.type_class = parsing_utils.get_literal_classifier(node.friendly_name, is_sutime=True)
        if is_contain_or_overlap:
            continue

        # init
        node = UngroundedNode(nid=nid, node_type='literal',
                              friendly_name=sutime_dict[sequence_start_end]['text'],
                              question_node=0, score=1.0,
                              start_position=sequence_start, end_position=sequence_end)
        node.normalization_value = sutime_dict[sequence_start_end]['value'] + '^^http://www.w3.org/2001/XMLSchema#datetime'
        node.type_class = parsing_utils.get_literal_classifier(sutime_dict[sequence_start_end]['text'], is_sutime=True)
        yuanshi_nodes.append(node)

        # sutime包含其他node的话, 则删除
        for node in yuanshi_nodes:
            if (sequence_start <= node.start_position and node.end_position < sequence_end) \
                    or (sequence_start < node.start_position and node.end_position <= sequence_end):
                remove_nodes.append(node)
    # remove remove_node
    new_nodes = []
    for temp in yuanshi_nodes:
        if temp not in remove_nodes:
            new_nodes.append(temp)
    return new_nodes, nid

def add_corenlp_ner_dict(nid, corenlp_sequence_ner_tag_dict, yuanshi_nodes, yuanshi_tokens):
    remove_nodes = []
    add_nodes = []
    for sequence_start_end, ner_tag in corenlp_sequence_ner_tag_dict.items():
        nid += 1
        sequence_start = int(sequence_start_end.split('\t')[0])
        sequence_end = int(sequence_start_end.split('\t')[1])

        # if ner_tag != 'DATE': continue  # only process date
        if ner_tag == 'DATE':
            node_type = 'literal'
        elif ner_tag in ['PERSON', 'LOCATION', 'ORGANIZATION', 'MISC',
                         'NATIONALITY', 'CITY', 'COUNTRY']:
            node_type = 'entity'
        else:
            continue

        # NER等于其他node的话, 则更新信息
        is_equal = False
        for node in yuanshi_nodes:
            if node.start_position == sequence_start and node.end_position == sequence_end:
                if node_type == 'literal':
                    node.type_class = 'type.datetime'
                    node.node_type = 'literal'
                elif node_type == 'entity':
                    node.node_type = 'entity'
                is_equal = True
                break
        if is_equal:
            continue

        ##recently, once corenlp ner:	 {'2\t3': 'PERSON', '6\t6': 'DATE'}
        friendly_name = parsing_utils.get_friendly_name(tokens=yuanshi_tokens, sequence_start=sequence_start, sequence_end=sequence_end)
        filter_values = ['once', 'recently', 'now', 'recent', 'current', 'currently']
        if friendly_name in filter_values:
            continue

        ner_node = UngroundedNode(nid=nid, node_type=node_type, friendly_name=friendly_name, question_node=0, score=1.0,
                                  start_position=sequence_start, end_position=sequence_end)

        # NER包含其他node的话, 则替换
        is_add_ner_node = False
        is_overlap = False
        for node in yuanshi_nodes:
            if (sequence_start <= node.start_position and node.end_position < sequence_end) or (sequence_start < node.start_position and node.end_position <= sequence_end):
                remove_nodes.append(node)
                is_add_ner_node = True
            else:
                for i in range(node.start_position, node.end_position+1):
                    for j in range(sequence_start, sequence_end+1):
                        if i == j:
                            is_overlap = True
        # 如果包括其他的node, 或者跟其他没有overlap，就追加
        if is_add_ner_node or not is_overlap:
            add_nodes.append(ner_node)

    new_nodes = []
    for temp in yuanshi_nodes:
        if temp not in remove_nodes:
            new_nodes.append(temp)
    for new_temp in add_nodes:
        new_nodes.append(new_temp)
    return new_nodes, nid

def add_el_node_ngram_or_quotation_dict(nid, el_node_ngram_dict, yuanshi_nodes, yuanshi_tokens):
    '''
    entity linking by ngram  or quotation, all tag is entity
    el_node_dict: {'en.my_heart_will_go_on': 1.061931253785453}
    '''
    remove_nodes = []
    for sequence_start_end, _ in el_node_ngram_dict.items():
        nid += 1
        sequence_start = int(sequence_start_end.split('\t')[0])
        sequence_end = int(sequence_start_end.split('\t')[1])

        is_bujia = False # 缺省是追加的, 下面来检测不加的情况

        # ngram包含其他node的话, 则替换
        # quotation mark 包含其他node的话, 则替换
        for node in yuanshi_nodes:
            if node.start_position == sequence_start and node.end_position == sequence_end:
                # 存在完全重叠的顶点，则不追加
                is_bujia = True
                break
            elif (sequence_start <= node.start_position and node.end_position < sequence_end) \
                    or (sequence_start < node.start_position and node.end_position <= sequence_end):
                #包含别人, 加自己, 删别人
                remove_nodes.append(node)
            elif sequence_start < node.start_position < sequence_end \
                    or sequence_start < node.end_position < sequence_end \
                    or node.start_position < sequence_start < node.end_position \
                    or node.start_position < sequence_end < node.end_position:
                # 与别人有overlap, 保留边界最宽的那个,
                # 举例: such as [the {royal arms] of the united kingdom}
                if node.end_position - node.start_position < sequence_end - sequence_start:
                    remove_nodes.append(node)
                else: #自己边界小，则不加
                    is_bujia = True
            elif sequence_start == node.end_position or sequence_end == node.start_position:
                # 边界重叠, 则不加
                is_bujia = True

        if is_bujia:
            continue

        friendly_name = parsing_utils.get_friendly_name(tokens=yuanshi_tokens, sequence_start=sequence_start, sequence_end=sequence_end)
        ngram_el_ner_node = UngroundedNode(
            nid=nid, node_type='entity', friendly_name=friendly_name,
            question_node=0, score=1.0, start_position=sequence_start,end_position=sequence_end)
        yuanshi_nodes.append(ngram_el_ner_node)

    # update nodes
    new_nodes = []
    for temp in yuanshi_nodes:
        if temp not in remove_nodes:
            new_nodes.append(temp)
    return new_nodes, nid

# def add_wh_words(tokens, nid, nodes):
#     blank_node = None
#     for i, token in enumerate(tokens):
#         #do not contain nodes
#         is_contain = False
#         for node in nodes:
#             if node.start_position<=i<=node.end_position:
#                 is_contain = True
#                 break
#         if is_contain: continue
#         if token.value in node_helper.globals_args.wh_words_set:
#             blank_node = generate_blank_node(
#                 node_type='class', nid=nid, friendly_name=token.value,start_position=i, end_position=i, score=1.0)
#             break
#     return blank_node


