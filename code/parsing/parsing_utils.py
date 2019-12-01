from collections import defaultdict
from nltk.parse import DependencyGraph
import collections
import copy
from common_structs.skeleton import Token
from parsing import parsing_args

def look_for_position(redundancy_span, root_span_node):
    redundancy_tokens = redundancy_span.split(' ')
    j = 0
    start_index = -1
    end_index = -1
    while j < len(root_span_node.tokens):
        common = 0
        for redundancy_index in range(len(redundancy_tokens)):
            if redundancy_tokens[redundancy_index] == root_span_node.tokens[j].value:
                common = common + 1
                j = j + 1
            else:
                j = j - common
                break
        if common == len(redundancy_tokens):
            start_index = root_span_node.tokens[j - common].index
            end_index = root_span_node.tokens[j - 1].index
        j = j + 1
    if start_index == -1 and end_index == -1:
        j = 0
        while j < len(root_span_node.tokens):
            for redundancy_index in range(len(redundancy_tokens)):
                if redundancy_index == 0 \
                        and redundancy_tokens[redundancy_index] == root_span_node.tokens[j].value:
                    start_index = root_span_node.tokens[j].index
                if redundancy_index == len(redundancy_tokens) - 1 \
                        and redundancy_tokens[redundancy_index] == root_span_node.tokens[j].value:
                    end_index = root_span_node.tokens[j].index
            j = j + 1
    # print('#index:\t', start_index, end_index)
    return start_index, end_index

def update_headword_index(tokens, headword_index):
    result = headword_index
    for z_index, z_token in enumerate(tokens):
        if z_index == headword_index:
            result = z_token.index
            break
    return result

def is_leaf(span_tree, span_node):
    '''判断是不是叶子'''
    is_leaf = True
    for id, node in span_tree.nodes.items():
        if node.isRoot: continue
        if node.headword_position is None: continue
        if span_node.start_position <= node.headword_position <= span_node.end_position:
            is_leaf = False
            break
    return is_leaf

def look_for_related_nodes(span_tree, span_node):
    '''找与span node相关联的span nodes'''
    related_nodes = []
    for id, node in span_tree.nodes.items():
        if node.isRoot: continue
        if node.headword_position is None: continue
        # if span_node.start_position <= node.headword_position <= span_node.end_position:
        for token in span_node.tokens:
            if token.index == node.headword_position:
                related_nodes.append(node)
    return related_nodes

def get_tokens(layer_num=None, start_position=None, end_position=None, token_nodes=None):
    '''get tokens between start_position and end_position'''
    # return token_nodes[start_position:end_position+1]
    tokens_result = []
    for i in range(start_position, end_position+1):
        if token_nodes[i].layer == layer_num:
            tokens_result.append(token_nodes[i])
    return tokens_result

def look_for_ancestor(current_layer, current_position, layer_nums_head_tail_position):
    '''寻找祖先layer_num'''
    ancestor_layer_num_list = []
    for candidate_ancestor_layer_num, candidate_ancestor_position in layer_nums_head_tail_position.items():
        if current_layer == candidate_ancestor_layer_num: continue
        if candidate_ancestor_position[0] <= current_position[0] and candidate_ancestor_position[1] >= current_position[1]:
            ancestor_layer_num_list.append(candidate_ancestor_layer_num)
    return ancestor_layer_num_list

def head_tail(layer_nums_list=None):
    '''
    找每层的边界, 并且包含所有的子孙
    segmentation head and tail of subquestions
    return layer: [start_position, end_position]
    '''
    layer_nums_head_tail_position = collections.OrderedDict()
    for i in range(len(layer_nums_list)):
        start_position = i
        end_position = -1
        for j in range(i, len(layer_nums_list)):
            if layer_nums_list[i] < layer_nums_list[j]:
                end_position = j-1
                break
            elif j == len(layer_nums_list)-1:
                end_position = j
        if layer_nums_list[start_position] not in layer_nums_head_tail_position.keys():
            layer_nums_head_tail_position[layer_nums_list[start_position]] = [start_position, end_position]
    return collections.OrderedDict(sorted(layer_nums_head_tail_position.items(), key=lambda t:t[0])) #按key排序

def head_tail_with_content(layer_nums_list=None, token_nodes=None):
    '''
    segmentation head and tail of subquestions
    return layer: [start_position, end_position, content]
    '''
    layer_nums_head_tail_position = collections.OrderedDict()
    for i in range(len(layer_nums_list)):
        start_position = i
        end_position = -1
        for j in range(i, len(layer_nums_list)):
            if layer_nums_list[i] < layer_nums_list[j]:
                end_position = j-1
                break
            elif j == len(layer_nums_list)-1:
                end_position = j

        if layer_nums_list[start_position] not in layer_nums_head_tail_position.keys():
            #get content
            content = ''
            for z in range(start_position, end_position + 1):
                if layer_nums_list[start_position] == layer_nums_list[z]:
                    content = content + ' ' + token_nodes[z].value
            content = content.strip()

            layer_nums_head_tail_position[layer_nums_list[start_position]] = [start_position, end_position, content]
    return collections.OrderedDict(sorted(layer_nums_head_tail_position.items(), key=lambda t:t[0])) #按key排序

def update_layer(tokens_nodes, start_index, end_index, layer_num):
    '''update redundancy tokens layer'''
    for i in range(len(tokens_nodes)):
        if start_index <= i <= end_index and tokens_nodes[i].layer == -1:
            tokens_nodes[i].layer = layer_num
    return tokens_nodes

def get_sequence(token_nodes):
    '''get sequence which do not contain shield token'''
    def postprocessing(utterance):
        utterance = utterance.replace('  ', ' ')
        utterance = utterance.replace(', ,', '')
        utterance = utterance.replace(' , ?', ' ?')
        utterance = utterance.replace(' . ?', ' ?')
        if utterance.startswith(' , '):
            utterance = utterance[3:]
        utterance = utterance.replace('  ', ' ')
        utterance = utterance.strip()
        return utterance
    sequence_list = [token_node.value for token_node in token_nodes if token_node.shield is False]
    sequence = ' '.join(sequence_list)
    sequence = postprocessing(sequence)
    return sequence

def shield_redundancy(tokens=None, start_index=None, end_index=None):
    '''shield redundancy tokens'''
    for i in range(len(tokens)):
        if start_index <= i <= end_index:
            tokens[i].shield = True

def open_redundany(tokens=None, start_index=None, end_index=None):
    for i in range(len(tokens)):
        if start_index <= i <= end_index:
            tokens[i].shield = False

def get_redundancy_un_continuous_index(token_nodes, redundancy):
    '''
    look for start of redundancy, and end of redundancy
    token_nodes = where did the conviction of thomas fyshe palmer occur ?
    redundancy = of palmer
    :param token_nodes:
    :param redundancy:
    :return: start_index, end_index
    '''
    redundancy_tokens = redundancy.split(' ')
    j = 0
    start_index = -1
    end_index = -1
    while j < len(token_nodes):
        for redundancy_index in range(len(redundancy_tokens)):
            # start_index == -1 and
            if redundancy_index == 0 and redundancy_tokens[redundancy_index] == token_nodes[j].value \
                    and not token_nodes[j].shield:
                start_index = j
            # end_index==-1 and
            if redundancy_index == len(redundancy_tokens)-1 and redundancy_tokens[redundancy_index] == token_nodes[j].value \
                    and not token_nodes[j].shield:
                end_index = j
        j = j + 1
    return start_index, end_index

def get_redundancy_continuous_index(token_nodes, redundancy):
    '''get redundancy index of tokens'''
    redundancy_tokens = redundancy.split(' ')
    j = 0
    start_index = -1
    end_index = -1
    while j < len(token_nodes):
        common = 0
        for redundancy_index in range(len(redundancy_tokens)):
            if redundancy_tokens[redundancy_index] == token_nodes[j].value and not token_nodes[j].shield:
                common = common + 1
                j = j + 1
            else:
                j = j - common
                break
        if common == len(redundancy_tokens):
            start_index = j - common
            end_index = j - 1
        j = j + 1
    return start_index, end_index

def look_for_max_layer(layer_nums_head_tail_position):
    '''look for root of tree'''
    max_layer_num = -1
    for layer_num in layer_nums_head_tail_position.keys():
        if max_layer_num < layer_num:
            max_layer_num = layer_num
    return max_layer_num

def create_tokens(words):
    '''create node token'''
    # return [Node(index, token) for index, token in enumerate(tokens)]
    tokens = []
    for index, word in enumerate(words):
        if index == len(words)-1 :
            tokens.append(Token(index, word, isEnd=True))
        else:
            tokens.append(Token(index, word, isEnd=False))
    return tokens

def get_sub_tokens(tokens, start_index, end_index):
    sub_tokens = []
    for temp_token in tokens:
        if start_index <= temp_token.index <= end_index:
            sub_tokens.append(temp_token)
    return sub_tokens

def update_span_tree_structure(span_tree, sub_span_node):
    related_span_nodes = look_for_related_nodes(span_tree, sub_span_node)  # look for 相关联的顶点列表
    for related_span_node in related_span_nodes:
        yuanyou_father_span_node = span_tree.get_father_span_by_sonid(related_span_node.id)
        if yuanyou_father_span_node is not None:
            yuanyou_father_span_node.children.remove(related_span_node.id)
        span_tree.add_child_rel_with_headword(
            father_id=sub_span_node.id, son_id=related_span_node.id,
            headword_position=related_span_node.headword_position,
            headword_relation=related_span_node.headword_relation)

def update_span_tree_nodes(span_tree, start_index, end_index):
    # update root span node
    new_root_span_node_tokens = []
    for old_token in span_tree.tokens:
        if start_index <= old_token.index <= end_index:
            continue
        new_root_span_node_tokens.append(old_token)
    span_tree.set_tokens(new_root_span_node_tokens)

def get_friendly_name(tokens, sequence_start, sequence_end):
    '''friendly_name = ' '.join([token.value for token in tokens if sequence_end >= token.index >= sequence_start])'''
    friendly_name = ' '.join([token.value for token in tokens
                              if sequence_end >= token.index >= sequence_start])
    # sequence = 'the united states of america'
    # if friendly_name.startswith('the '):
    #     friendly_name = friendly_name[4:]
    return friendly_name.strip()

def is_exist_edge_in_edges(ungrounded_edges, ungrounded_edge):
    result = False
    for edge in ungrounded_edges:
        if (edge.start == ungrounded_edge.start and edge.end == ungrounded_edge.end) \
                or (edge.start == ungrounded_edge.end and edge.end == ungrounded_edge.start):
            result = True
            break
    return result

def search_for_node_by_index(node_index, dependency_graph):
    result_node = None
    for index, node in dependency_graph.nodes.items():
        if index == node_index:
            result_node = node
    return result_node

def adj_edge_nodes_update(dep_node_index, dependency_graph):
    '''zhao children'''
    dep_result_nodes_index = []
    if dep_node_index is None: return dep_result_nodes_index
    node = search_for_node_by_index(dep_node_index, dependency_graph)
    #chu du
    for _, child_index_list in node['deps'].items():
        for child_index in child_index_list:
            dep_result_nodes_index.append(child_index)
    #ru du
    for node_index_, node in dependency_graph.nodes.items():
        for _, child_index_list in node['deps'].items():
            for child_index in child_index_list:
                if child_index == dep_node_index: #某个顶点的孩子是dep_node, 那么他就是其父亲
                    dep_result_nodes_index.append(node_index_)
    return dep_result_nodes_index

def look_for_surface_tokens_index(dep_index, surface_tokens_to_dep_node_dict):
    result = -1
    for surface_token_index, dep_node_index in surface_tokens_to_dep_node_dict.items():
        if dep_index == dep_node_index:
            result = surface_token_index
            break
    return result

def is_contained_one_node_from_nodes(token_index, ungrounded_nodes):
    result = False
    for ungrounded_node in ungrounded_nodes:
        if ungrounded_node.start_position <= token_index <= ungrounded_node.end_position:
            result = True
            break
    return result

def look_for_one_node_from_nodes(token_index, ungrounded_nodes):
    result = None
    for ungrounded_node in ungrounded_nodes:
        if ungrounded_node.start_position <= token_index <= ungrounded_node.end_position:
            result = ungrounded_node
            break
    return result

def is_contained_one_node(head_node_index, end_node_index, ungrounded_nodes):
    result = False
    for ungrounded_node in ungrounded_nodes:
        if ungrounded_node.start_position <= head_node_index <= ungrounded_node.end_position \
            and ungrounded_node.start_position <= end_node_index <= ungrounded_node.end_position:
            result = True
            break
    return result

def get_friendly_name_by_tokens(tokens, path):
    '''friendly_name = ' '.join([token.value for token in tokens if sequence_end >= token.index >= sequence_start])'''
    copy_path = copy.deepcopy(path)
    if len(copy_path) > 0: del copy_path[-1]
    friendly_name = ''
    for i, token_index in enumerate(sorted(copy_path)):
        friendly_name += ' '.join([token.value for token in tokens if token_index == token.index])+' '
    return friendly_name.strip()

def get_friendly_name_by_dependency(dependency_graph, path):
    '''friendly_name = ' '.join([token.value for token in tokens if sequence_end >= token.index >= sequence_start])'''
    copy_path = copy.deepcopy(path)
    if len(copy_path) > 0: del copy_path[-1]
    friendly_name = ''
    for token_index in sorted(copy_path):
        friendly_name += dependency_graph.nodes[token_index]['word'] + ' '
        # friendly_name += ' '.join([token.value for token in tokens if token_index-1 == token.index])+' '
    # friendly_name += str(copy_path)
    return friendly_name.strip()

def look_for_key_by_value(dict_, value_):
    result = None
    for key, value in dict_.items():
        if value_ == value:
            result = key
            result += 1
            break
    return result

def update_dependencygraph_indexs(old_dependency_graph):
    # surface_tokens_to_dep_node_dict 两个索引的映射表
    surface_tokens_to_dep_node_dict = dict()
    for _, dep_node in old_dependency_graph.nodes.items():
        surface_tokens_to_dep_node_dict[dep_node['feats']] = dep_node['address']

    new_hybrid_dependency_graph = DependencyGraph()
    for _, yuanshi_node in old_dependency_graph.nodes.items():
        new_node_info = copy.deepcopy(yuanshi_node)
        new_node_info['address'] = look_for_key_by_value(dict_=surface_tokens_to_dep_node_dict, value_=new_node_info['address'])
        new_node_info['head'] = look_for_key_by_value(dict_=surface_tokens_to_dep_node_dict, value_=new_node_info['head'])

        new_deps = defaultdict(list)
        for old_dep_rel, old_dep_index_list in yuanshi_node['deps'].items():
            new_dep_index_list = []
            for old_dep_index in old_dep_index_list:
                new_dep_index_list.append(look_for_key_by_value(dict_=surface_tokens_to_dep_node_dict, value_=old_dep_index))
            new_deps[old_dep_rel] = new_dep_index_list
        new_node_info['deps'] = new_deps

        # 更新新地址
        if new_hybrid_dependency_graph.contains_address(new_node_info['address']):
            new_hybrid_dependency_graph.nodes[new_node_info['address']].update(new_node_info)
        else:
            new_hybrid_dependency_graph.add_node(new_node_info)

    if new_hybrid_dependency_graph.nodes[0]['deps']['ROOT']:
        root_address = new_hybrid_dependency_graph.nodes[0]['deps']['ROOT'][0]
        new_hybrid_dependency_graph.root = new_hybrid_dependency_graph.nodes[root_address]
        new_hybrid_dependency_graph.top_relation_label = 'ROOT'
    return new_hybrid_dependency_graph

def is_ordianl(token):
    result = False
    for index, _set in parsing_args.ordinal_lines_dict.items():
        if token == index or token in _set:
            result = True
            break
    return result

def ordinal_normalization(token):
    normal = None
    for index, _set in parsing_args.ordinal_lines_dict.items():
        if token == index or token in _set:
            normal = index
            break
    return normal

def is_comparative(token):
    token = token.lower()
    if token in parsing_args.dayu_dengyu_phrases \
        or token in parsing_args.dayu_phrases \
        or token in parsing_args.xiaoyu_phrases \
        or token in parsing_args.xiaoyu_dengyu_phrases:
        return True
    else:
        return False

def is_superlative(token):
    result = False
    # for index, _set in superlative_lines_dict.items():
    #     if token == index or token in _set:
    #         result = True
    #         break
    token = token.lower()
    if token in parsing_args.argmax_phrases \
            or token in parsing_args.argmin_phrases:
        result = True
    return result

def superlative_normalization(token):
    normal = 'none'
    # for index, _set in superlative_lines_dict.items():
    #     if token == index or token in _set:
    #         normal = index
    #         break
    token = token.lower()
    if token in parsing_args.argmax_phrases:
        normal = 'argmax'
    elif token in parsing_args.argmin_phrases:
        normal = 'argmin'
    return normal

def set_class_ordinal_superlative_function(ungrounded_nodes=None, span_tree_hybrid_dependency_graph=None,surface_tokens=None):
    '''set ordinal function of class'''
    for ungrounded_node in ungrounded_nodes:
        # 只有class, literal上面设置聚合属性
        if ungrounded_node.node_type != 'class' and ungrounded_node.node_type != 'literal':
            continue
        start_position = ungrounded_node.start_position
        end_position = ungrounded_node.end_position
        for surface_index in range(start_position, end_position+1):
            # 遍历node的每个word, 检测它的所有出边
            adj_vertexs = adj_edge_nodes_update(surface_index, span_tree_hybrid_dependency_graph)
            if adj_vertexs is None: continue
            for adj_vertex_index in adj_vertexs:
                adj_token = surface_tokens[adj_vertex_index].value
                if is_ordianl(adj_token):
                    ungrounded_node.ordinal = ordinal_normalization(adj_token)
                elif is_superlative(adj_token):
                    ungrounded_node.function = superlative_normalization(adj_token)
                elif is_comparative(adj_token):
                    ungrounded_node.function = comparative_to_function(adj_token)
                # elif is_count_by_token_ner_tag(adj_vertex_index, tokens=surface_tokens):
                #     ungrounded_node.function = 'count'
                # print ('#children:\t', surface_tokens[adj_vertex_index].value)
    return ungrounded_nodes

def comparative_to_function(comparative_friendly_name):
    '''> , >=, <, <='''
    if comparative_friendly_name in parsing_args.dayu_phrases:
        return '>'
    elif comparative_friendly_name in parsing_args.dayu_dengyu_phrases:
        return '>='
    # elif comparative_friendly_name in dengyu_phrases:
    #     return '=='
    elif comparative_friendly_name in parsing_args.xiaoyu_phrases:
        return '<'
    elif comparative_friendly_name in parsing_args.xiaoyu_dengyu_phrases:
        return '<='
    else:
        return 'none'

def superlative_to_function(superlative_friendly_name):
    '''argmax, argmin'''
    if superlative_friendly_name in parsing_args.argmin_phrases:
        return 'argmin'
    elif superlative_friendly_name in parsing_args.argmax_phrases:
        return 'argmax'
    else:
        return 'none' #'=='

def count_to_function(count_friendly_name):
    '''count'''
    if count_friendly_name in parsing_args.count_phrases:
        return 'count'
    else:
        return 'none'

def ner_to_function(friendly_name, ner_tag):
    node_function = 'none'
    if ner_tag == 'superlative':
        node_function = superlative_to_function(friendly_name)
    elif ner_tag == 'comparative':
        node_function = comparative_to_function(friendly_name)
    elif ner_tag == 'count':
        node_function = count_to_function(friendly_name)
    return node_function

def get_literal_classifier(friendly_name, is_sutime=False):
    '''type.int, type.float, type.datetime'''
    if is_sutime:
        return 'type.datetime'
    if '.' in friendly_name or '+' in friendly_name:
        return 'type.float'
    else:
        return 'type.int'

def is_question_node_by_words(node_mention):
    '''interaction between wh-word and node mention, then the node is question node'''
    result = False
    if node_mention is None: return result
    for word in node_mention.split(' '):
        if word.lower() in parsing_args.wh_words_set:
            result = True
    return result

def is_wh_question_node(node):
    '''node's id is wh-word'''
    result = False
    if node is None: return result
    if node.id in parsing_args.wh_words_set:
        result = True
    return result

def set_question_node(ungrounded_nodes):
    '''recogniatize question node'''
    #1. overlap
    is_has = False
    for ungrounded_node in ungrounded_nodes:
        if ungrounded_node.node_type == 'class' and is_question_node_by_words(ungrounded_node.friendly_name):
            ungrounded_node.question_node = 1
            is_has = True
            break
    if not is_has:
        class_nodes_list = []
        for ungrounded_node in ungrounded_nodes:
            if ungrounded_node.node_type == 'class':
                class_nodes_list.append(ungrounded_node)
        if len(class_nodes_list) == 1:
            for class_node in class_nodes_list:
                class_node.question_node = 1
        elif len(class_nodes_list) > 1: # start_position is smaller, is question node
            min_start_position = 100000
            for class_node in class_nodes_list:
                if min_start_position > class_node.start_position:
                    min_start_position = class_node.start_position
            for ungrounded_node in ungrounded_nodes:
                if ungrounded_node.start_position == min_start_position:
                    ungrounded_node.question_node = 1
                    break
    return ungrounded_nodes

def is_equal_wh_word(node_mention):
    '''equal between wh-word and node mention'''
    result = False
    if node_mention is None: return result
    if node_mention.lower() in parsing_args.wh_words_set:
        result = True
    return result

def class_count_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''class and count组合成edge'''
    class_node = None
    count_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_class_node(start_node) and is_count_node(end_node):
        class_node = start_node
        count_node = end_node
    elif is_class_node(end_node) and is_count_node(start_node):
        class_node = end_node
        count_node = start_node
    return class_node, count_node

def relation_other_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''relation and other组合成edge'''
    relation_node = None
    other_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_relation_node(start_node) and not is_relation_node(end_node):
        relation_node = start_node
        other_node = end_node
    elif is_relation_node(end_node) and not is_relation_node(start_node):
        relation_node = end_node
        other_node = start_node
    return relation_node, other_node

def class_superlative_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''class and superlative组合成edge'''
    class_node = None
    superlative_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_class_node(start_node) and is_superlative_node(end_node):
        class_node = start_node
        superlative_node = end_node
    elif is_class_node(end_node) and is_superlative_node(start_node):
        class_node = end_node
        superlative_node = start_node
    return class_node, superlative_node

def class_question_node_class_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''class and class组合成edge'''
    class_question_node = None
    class_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_class_node(start_node) and is_question_node(start_node) and is_class_node(end_node):
        class_question_node = start_node
        class_node = end_node
    elif is_class_node(end_node) and is_question_node(end_node) and is_class_node(start_node):
        class_question_node = end_node
        class_node = start_node
    return class_question_node, class_node

def class_class_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''class and class组合成edge'''
    class_a_node = None
    class_b_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_class_node(start_node) and is_class_node(end_node):
        class_a_node = start_node
        class_b_node = end_node
    return class_a_node, class_b_node

def entity_class_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''entity , class 组合成的edge'''
    entity_node = None
    class_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_entity_node(start_node) and is_class_node(end_node):
        entity_node = start_node
        class_node = end_node
    elif is_class_node(start_node) and is_entity_node(end_node):
        entity_node = end_node
        class_node = start_node
    return entity_node, class_node

def relation_superlative_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''relation and superlative组合成edge'''
    relation_node = None
    superlative_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_relation_node(start_node) and is_superlative_node(end_node):
        relation_node = start_node
        superlative_node = end_node
    elif is_relation_node(end_node) and is_superlative_node(start_node):
        relation_node = end_node
        superlative_node = start_node
    return relation_node, superlative_node

def literal_comparative_node_in_one_edge(ungrounded_graph_nodes, edge):
    '''literal and comparative组合成edge'''
    literal_node = None
    comparative_node = None
    start_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.start)
    end_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, edge.end)
    if is_literal_node(start_node) and is_comparative_node(end_node):
        literal_node = start_node
        comparative_node = end_node
    elif is_literal_node(end_node) and is_comparative_node(start_node):
        literal_node = end_node
        comparative_node = start_node
    return literal_node, comparative_node

def is_exist_in_nodes(ungrounded_graph_nodes, ungrounded_node):
    ''''''
    result = False
    for node in ungrounded_graph_nodes:
        if node.nid == ungrounded_node.nid:
            result = True
            break
    return result

def search_one_node_in_nodes(ungrounded_graph_nodes, ungrounded_node):
    ''''''
    result = None
    for node in ungrounded_graph_nodes:
        if node.nid == ungrounded_node.nid:
            result = node
            break
    return result

def search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, nid):
    result = None
    for node in ungrounded_graph_nodes:
        if node.nid == nid:
            result = node
            break
    return result

def is_property_node(ungrounded_node):
    '''check if node is property'''
    property_type_list = ["comparative", "count", "superlative", "neg"]
    if ungrounded_node.node_type in property_type_list:
        return True
    else:
        return False

def is_comparative_node(ungrounded_node):
    '''check if node is superlative node'''
    comparative_list = ["comparative"]
    if ungrounded_node.node_type in comparative_list:
        return True
    else:
        return False

def is_literal_node(ungrounded_node):
    '''check if node is literal node'''
    literal_list = ["literal"]
    if ungrounded_node.node_type in literal_list:
        return True
    else:
        return False

def is_superlative_node(ungrounded_node):
    '''check if node is superlative node'''
    superlative_list = ["superlative"]
    function_list = ['argmin', 'argmax', '==']
    if ungrounded_node.node_type in superlative_list or \
            (ungrounded_node.function is not None and ungrounded_node.function in function_list):
        return True
    else:
        return False

def is_count_node(ungrounded_node):
    '''check if node is count node'''
    count_list = ["count"]
    if ungrounded_node.node_type in count_list:
        return True
    else:
        return False

def is_class_node(ungrounded_node):
    '''check if node is class node'''
    class_list = ["class"]
    if ungrounded_node.node_type in class_list:
        return True
    else:
        return False

def is_entity_node(ungrounded_node):
    '''check if node is entity node'''
    class_list = ["entity"]
    if ungrounded_node.node_type in class_list:
        return True
    else:
        return False

def is_question_node(ungrounded_node):
    '''check if node is class node'''
    class_list = ["class"]
    if ungrounded_node.node_type in class_list and ungrounded_node.question_node == 1:
        return True
    else:
        return False

def is_relation_node(ungrounded_node):
    '''check if node is class node'''
    relation_list = ["relation"]
    if ungrounded_node.node_type in relation_list:
        return True
    else:
        return False

def search_adjacent_edges(node, ungrounded_graph):
    ''''''
    adjacent_edges = []
    for edge in ungrounded_graph.edges:
        if edge.start == node.nid or edge.end == node.nid:
            adjacent_edges.append(edge)
    return adjacent_edges

def search_adjacent_nodes(node, ungrounded_graph):
    ''''''
    adjacent_nodes = []
    nodes = ungrounded_graph.nodes
    for edge in ungrounded_graph.edges:
        if edge.start == node.nid:
            adjacent_nodes.append(search_one_node_in_nodes_by_nid(nodes, edge.end))
        elif edge.end == node.nid:
            adjacent_nodes.append(search_one_node_in_nodes_by_nid(nodes, edge.start))
    return adjacent_nodes

def del_edge_in_ungrounded_edge(ungrounded_graph, directed_cycle):
    '''
    :param ungrounded_graph:
    :param directed_cycle:
    :return: ungrounded_graph
    '''
    ungrounded_graph = copy.deepcopy(ungrounded_graph)

    edge_nodes_pair = []
    edge_nodes_pair.append(('literal', 'entity'))
    edge_nodes_pair.append(('entity', 'literal'))
    edge_nodes_pair.append(('literal', 'literal'))
    edge_nodes_pair.append(('entity', 'entity'))

    # node_type
    ungrounded_graph_nodes = ungrounded_graph.nodes
    ungrounded_graph_edges = ungrounded_graph.edges
    remove_edges = []

    for cycle in directed_cycle.all_cycles:
        cycle_index_list = []
        for temp_index in cycle:
            cycle_index_list.append(temp_index)

        before_node_index = None
        current_node_index = None
        for i, index in enumerate(cycle_index_list):
            if i == 0:
                before_node_index = index
                continue
            else:
                current_node_index = index
                temp_edge = search_special_edge_in_edges(ungrounded_graph_edges, before_node_index, current_node_index)
                if temp_edge is not None:
                    before_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, before_node_index)
                    current_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, current_node_index)
                    if is_nosiy_edge(edge_nodes_pair=edge_nodes_pair, node_a=before_node, node_b=current_node):
                        remove_edges.append(temp_edge)
                before_node_index = current_node_index

        if len(remove_edges) == 0:
            #if class_1 - class_2{question_node=1} - entity|literal
            #断开 class_2{question_node} - entity|literal
            before_node_index = None
            for i, index in enumerate(cycle_index_list):
                if i == 0:
                    before_node_index = index
                    continue
                else:
                    current_node_index = index
                    current_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, current_node_index)
                    if current_node.node_type == 'entity' or current_node.node_type == 'literal':
                        before_edge = search_special_edge_in_edges(ungrounded_graph_edges, before_node_index, current_node_index)
                        before_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, before_node_index)
                        if before_edge is not None and before_node.node_type == 'class':
                            if len(cycle_index_list) > i+1:
                                next_edge = search_special_edge_in_edges(ungrounded_graph_edges, current_node_index, cycle_index_list[i+1])
                                next_node = search_one_node_in_nodes_by_nid(ungrounded_graph_nodes, cycle_index_list[i+1])
                                if next_edge is not None and next_node.node_type == 'class':
                                    if before_node.question_node == 1 and next_node.question_node == 0:
                                        remove_edges.append(before_edge)
                                    elif before_node.question_node == 0 and next_node.question_node == 1:
                                        remove_edges.append(next_edge)
                    before_node_index = current_node_index
        break  #default one cycle

    new_ungrounded_edges = []
    for edge in ungrounded_graph.edges:
        if edge not in remove_edges:
            new_ungrounded_edges.append(copy.deepcopy(edge))
    ungrounded_graph.edges = new_ungrounded_edges
    ungrounded_graph.ungrounded_query_id = ungrounded_graph.ungrounded_query_id+1
    return ungrounded_graph

def search_special_edge_in_edges(ungrounded_edges, nid_a, nid_b):
    ''''''
    result = None
    for edge in ungrounded_edges:
        if (edge.start == nid_a and edge.end == nid_b) or (edge.start == nid_b and edge.end == nid_a):
            result = edge
            break
    return result

def is_nosiy_edge(edge_nodes_pair, node_a, node_b):
    result = False
    for edge_node_pair_start, edge_node_pair_end in edge_nodes_pair:
        if node_a.node_type == edge_node_pair_start and node_b.node_type == edge_node_pair_end:
            result = True
    return result

def abstract_question_word_generation(tokens, ungrounded_nodes):
    '''
    replace entity mention and class mention to entity and class
    '''
    i = 0
    abstract_question_word = []
    while i < len(tokens):
        is_contained = False
        # for sequence_start_end, ner_tag in sequence_ner_tag_dict.items():
        #     if ner_tag not in ['entity', 'literal', 'class']: continue
        #     sequence_start = int(sequence_start_end.split('\t')[0])
        #     sequence_end = int(sequence_start_end.split('\t')[1])
        #     if sequence_start <= i <= sequence_end:
        #         # self.abstract_question_word.append('NP')
        #         # self.abstract_question_pos.append('NP')
        #         abstract_question_word.append(ner_tag)
        #         # self.abstract_question_pos.append(node_type)
        #         is_contained = True
        #         i += (sequence_end - sequence_start + 1)
        #         break
        for ungrounded_node in ungrounded_nodes:
            sequence_start = ungrounded_node.start_position
            sequence_end = ungrounded_node.end_position
            ner_tag = ungrounded_node.node_type
            if ner_tag not in ['entity', 'literal', 'class']:
                continue
            if sequence_start <= i <= sequence_end:
                abstract_question_word.append(ner_tag)
                is_contained = True
                i += (sequence_end - sequence_start + 1)
                break
        if not is_contained:
            abstract_question_word.append(tokens[i].value)
            i += 1
    return abstract_question_word

def get_nertag_sequence(ungrounded_nodes):
    indexs_to_nertag_dict = dict()
    for ungrounded_node in ungrounded_nodes:
        sequence_start = ungrounded_node.start_position
        sequence_end = ungrounded_node.end_position
        ner_tag = ungrounded_node.node_type
        indexs_to_nertag_dict[str(sequence_start) + '\t' + str(sequence_end)] = ner_tag
    return indexs_to_nertag_dict

def is_whitespace(c):
    if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
        return True
    return False

def char_index_to_token_index(question, start_char, end_char):
    doc_tokens = []
    char_to_word_offset = []
    prev_is_whitespace = True
    for i, char in enumerate(question):
        if is_whitespace(char):
            prev_is_whitespace = True
        else:
            if prev_is_whitespace:
                doc_tokens.append(char)
            else:
                doc_tokens[-1] += char
            prev_is_whitespace = False
        char_to_word_offset.append(len(doc_tokens) - 1)
    # print('#doc_tokens:\t', doc_tokens)
    # print('#char_to_word_offset:\t', char_to_word_offset)
    start_token_index = char_to_word_offset[start_char]
    if end_char >= len(char_to_word_offset):
        end_token_index = char_to_word_offset[-1]
    else:
        end_token_index = char_to_word_offset[end_char]
    return start_token_index, end_token_index

def serialization_class_whnp(whnp_phrase_tree_leaves_list, question_word_list, ner_tag='class'):
    serialization_list = serialization_mention(question_word_list, mention_word_list=whnp_phrase_tree_leaves_list, is_lower=True, ner_tag=ner_tag)
    return serialization_list

def serialization_mention_corenlp(question_word_list, corenlp_ner_dict, ner_tag='literal'):
    '''{'7\t7': 'NUMBER', '9\t10': 'PERSON'}'''
    serialization_list = ['O' for i in question_word_list]
    for sequence_start_end, _ner_tag in corenlp_ner_dict.items():
        if _ner_tag != 'DATE' and _ner_tag != 'NUMBER': continue  # only process date
        sequence_start = int(sequence_start_end.split('\t')[0])
        sequence_end = int(sequence_start_end.split('\t')[1])
        for i in range(len(question_word_list)):
            if sequence_start <= i <= sequence_end:
                serialization_list[i] = ner_tag
    return serialization_list

def serialization_mention_sutime(question_word_list, sutime_dict, ner_tag='literal'):
    '''
        input: question_string and sutime_dict  {'5\t5': {'text': '2004', 'value': '2004', 'type': 'DATE'}}
        output: O O Date  O O O O serialization
        '''
    serialization_list = ['O' for i in question_word_list]
    for sequence_start_end, time_dict in sutime_dict.items():
        if time_dict['type'] != 'DATE': continue  # 只处理date
        sequence_start = int(sequence_start_end.split('\t')[0])
        sequence_end = int(sequence_start_end.split('\t')[1])
        for i in range(len(question_word_list)):
            if sequence_start <= i <= sequence_end:
                serialization_list[i] = ner_tag
    return serialization_list

def serialization_mention(question_word_list, mention_word_list, is_lower=False, ner_tag='I'):
    '''
    input: question_string and entity_mention
    output: O O I I O O O O serialization
    example: 'find me tablet computers from apple inc.' and 'apple inc.'
    example output: O O O O O I I
    question = 'which presidents of the u.s. weighed 80.0 kilograms or more ?'
    class_mention = 'presidents of the u.s.'
    '''
    serialization_list = list()
    start_index = -1
    end_index = -1
    if is_lower:
        new_question_word_list = []
        for question_word in question_word_list:
            new_question_word_list.append(question_word.lower())
        question_word_list = new_question_word_list
        new_mention_word_list = []
        for mention_word in mention_word_list:
            new_mention_word_list.append(mention_word.lower())
        mention_word_list = new_mention_word_list
    for i in range(len(question_word_list)):
        for j in range(len(question_word_list)):
            if question_word_list[i:j] == mention_word_list:
                start_index = i
                end_index = j-1
    for i in range(len(question_word_list)):
        if start_index <= i <= end_index:
            serialization_list.append(ner_tag)
        else:
            serialization_list.append('O')
    return serialization_list

def serialization_entity_mention(question_string, entity_mention):
    '''input: question_string and entity_mention
    example: 'find me tablet computers from apple inc.' and 'apple inc.'
    example output: O O O O O I I
    '''
    question_token_list = globals_args.corenlp_parser.get_token(question_string)
    entity_token_list = globals_args.corenlp_parser.get_token(entity_mention)
    serialization = ''
    question_string_new = ''
    for question_token in question_token_list:
        is_tag = False
        for entity_token in entity_token_list:
            if question_token.word == entity_token.word or question_token.lemma == entity_token.word:
                is_tag = True
        if is_tag:
            serialization += 'I '
        else:
            serialization += 'O '
        question_string_new += question_token.word+' '
    # old method
    # question_string = question_string.replace(',',' ,').replace('?',' ?').replace('.',' .')
    # question_tokens = question_string.split(' ')
    # entity_mention_tokens = entity_mention.split(' ')
    # serialization = ''
    # for token in question_tokens:
    #     if token in entity_mention_tokens:
    #         serialization += 'I '
    #     else:
    #         serialization += 'O '
    serialization = serialization.strip()
    question_string_new = question_string_new.strip()
    return question_string_new, serialization

def search_question_node_nid(nodes):
    '''question node index'''
    question_node_index = None
    for node in nodes:
        if is_question_node(node):
            question_node_index = node.nid
    return question_node_index

def merge_ner_sequence(ner_sequence):
    '''
    merge ner type, input ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'O']
    return startIndex\tendIndex -> nerType
    '''
    ner_dict = dict()
    ner_type = None
    start_index = 0
    end_index = 0
    is_meet = False
    for index in range(len(ner_sequence)):
        current_tag = ner_sequence[index]
        if '0' != current_tag and 'O' != current_tag:
            if is_meet and ner_type == current_tag: #过程中
                if index != len(ner_sequence) - 1: #没有到达句尾, 过程中
                    continue
            elif is_meet and ner_type != current_tag: # 上一下与下一个不一样了'class', 'relation'
                end_index = index - 1
                # is_meet = False
                ner_dict[str(start_index) + '\t' + str(end_index)] = ner_type
                # ner_type= None
                #相当于又到了一个新mention的开头
                is_meet = True
                start_index = index
                ner_type = current_tag
            else:
                is_meet = True #到了mention的开头
                start_index = index
                ner_type = current_tag

            if index == len(ner_sequence) - 1: # 到达了句尾, 要把当前的mention，追加到ner_dict中
                end_index = index
                ner_dict[str(start_index) + '\t' + str(end_index)] = ner_type

        else:
            if is_meet: #到了mention尾部
                end_index = index - 1
                is_meet = False
                ner_dict[str(start_index) + '\t' + str(end_index)] = ner_type
                ner_type = None
            else:
                continue
    return ner_dict

#---------------------------------------------------------------------

def importantwords_by_unimportant_abstractq(abstractquestion):
    if isinstance(abstractquestion, list):
        abstractquestion = ' '.join(abstractquestion)
    abstractquestion_remove_version = abstractquestion.lower()
    for unimportantphrase in parsing_args.unimportantphrases:
        abstractquestion_remove_version = abstractquestion_remove_version.replace(unimportantphrase, "")
    importantwords = []
    for word in abstractquestion_remove_version.split(" "):
        if len(word) > 0 and word not in parsing_args.unimportantwords and word not in parsing_args.stopwords_dict:
            importantwords.append(word)
    # importantwords = set(abstractquestion_remove_version.split(" ")) - unimportantwords - stopwords
    # for word in importantwords:
    #     if "entity" in word:
    #         print("error")
    return importantwords

def extract_importantwords_from_question(question, ungrounded_graph):
    for node in ungrounded_graph.nodes:
        if node.node_type == 'entity':
            question = question.replace(node.friendly_name, '')
    words = question.split(' ')
    if words[-1] == '?' or words[-1] == '.':
        del words[-1]
    abstractquestion_list = []  #变成了list
    for word in words:
        if len(word) > 0:
            abstractquestion_list.append(word)
    return importantwords_by_unimportant_abstractq(abstractquestion_list)

def extract_importantwords_from_cnn(question, ungrounded_graph):
    for node in ungrounded_graph.nodes:
        if node.node_type == 'entity':
            question_ = question.replace(node.friendly_name, '')
    return question

def get_importantwords_byabstractquestion(question_):
    words = question_.split()
    if len(words)==0:
        return []
    if words[-1] == '?' or words[-1] == '.':
        del words[-1]
    importantwords_list = list()
    for word in words:
        if len(word) > 0 and '<e>' not in word:
            importantwords_list.append(word)
    return importantwords_by_unimportant_abstractq(importantwords_list)


def print_dependency_graph_tree(dependency_graph):
    '''print dependency graph'''
    # print('#dependency graph:')
    # dependency_graph.tree().draw()
    # for node_index, node in dependency_graph.nodes.items():
    #     print(node_index, node)
    # dg = dependency_graph.nx_graph()
    # g_labels = dependency_graph.nx_labels #<class 'dict'>
    # for i, label in g_labels.items():
    #     print(i, label)
    # print(dg.edges) #[(1, 3, 'det'), (2, 3, 'amod'), (3, 4, 'nsubj'), (5, 6, 'case'), (6, 4, 'nmod'), (7, 4, 'punct')]
    # print(dg.node) [1, 2, 3, 4, 5, 6, 7]
    # for node_index, node in span_tree_hybrid_dependency_graph.nodes.items():
    #     print(node_index, node)
    #     word = span_tree_hybrid_dependency_graph._word(node)
    #     tree = span_tree_hybrid_dependency_graph._tree(node_index)
    #     head = span_tree_hybrid_dependency_graph._hd(node_index)
    #     print('#head:\t', head)
    #     # look for relation
    #     rel = span_tree_hybrid_dependency_graph._rel(node_index)
    #     print('#rel:\t', rel)
    #     children = chain.from_iterable(node['deps'].values())
    #     for child in children:
    #         print('#child:\t', child)

    print('----------------------start---------------------------')
    # print(print_struct.print_span_tree(span_tree))
    # utils_helpers.print_dependency_graph(span_tree_hybrid_dependency_graph)
    dependency_graph.tree().pretty_print()
    print(dependency_graph.to_conll(10))
    # for _, dep_node in dependency_graph.nodes.items():
    #     print(dep_node)
    print('----------------------end---------------------------')

