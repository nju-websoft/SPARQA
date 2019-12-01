from collections import defaultdict
import copy
from nltk.parse import DependencyGraph
from parsing.parsing_args import nltk_nlp

def span_tree_to_hybrid_dependency_graph_interface(span_tree=None):
    '''span tree to hybrid dependency graph interface '''
    skeleton_span_node = span_tree.get_root_span_node()
    if len(span_tree.nodes) == 1: #simple question
        surface_tokens = span_tree.tokens
        hybrid_dependency_graph = nltk_nlp.generate_dependency_graph(skeleton_span_node.content)
        # feats 暂时存放索引位置
        for address, node_dict in hybrid_dependency_graph.nodes.items():
            if address == 0:
                node_dict['feats'] = -1
            else:
                node_dict['feats'] = surface_tokens[address-1].index
    else: #complex question
        hybrid_dependency_graph = span_tree_to_dependency_graph_recursion(span_tree=span_tree, current_span_node=skeleton_span_node)
    return hybrid_dependency_graph

def span_tree_to_dependency_graph_recursion(span_tree=None, current_span_node=None):
    '''recursion method generate hybrid dependency graph'''
    current_span_node_dependency_graph = nltk_nlp.generate_dependency_graph(current_span_node.content)
    current_span_node_tokens = current_span_node.tokens
    # print(current_span_node.content)
    # for _node in current_span_node_tokens:
    #     print('##@@@@@@@', _node.index, _node.value)
    node_index_to_dict_list_ranked = list(sorted(current_span_node_dependency_graph.nodes.items(), key=lambda d: d[0], reverse=False))
    # for node_index_to_dict in node_index_to_dict_list_ranked:
    #     print ('%%%%%%%%%%%%', node_index_to_dict) #%%%%%%%%%%%% (6, {'address': 6, 'word': ',', 'lemma': ',', 'ctag': ',', 'tag': ',', 'feats': '_', 'head': 2, 'deps': defaultdict(<class 'list'>, {}), 'rel': 'punct'})
    for (address, node_dict) in node_index_to_dict_list_ranked:
        # feats 暂时存放索引位置
        if address == 0:
            node_dict['feats'] = -1
        elif address <= len(current_span_node_tokens): #-1
            node_dict['feats'] = current_span_node_tokens[address - 1].index
        else:
            node_dict['feats'] = -1 #node_dict['address'] #
        # print ('####@@@', address, node_dict)

    # 判断 span 还有没有孩子
    if current_span_node.isTerminal:
        if len(current_span_node_tokens) == 1:
            # token's length == 1 针对这种情况，初始化一个dep node
            current_span_node_token_pos = nltk_nlp.get_pos(current_span_node_tokens[0].value)[0][1]
            current_span_node_info = {
                'address': -1,
                'word': current_span_node_tokens[0].value,
                'lemma': current_span_node_tokens[0].value,
                'ctag': current_span_node_token_pos,
                'tag': current_span_node_token_pos,
                'feats': current_span_node_tokens[0].index,
                'head': 0,
                'deps': defaultdict(list),
                'rel': None
            }
            return current_span_node_info
        else: # tokens' length > 1
            return current_span_node_dependency_graph

    # has children
    for child_span in span_tree.get_children_spans_by_fatherspan(current_span_node):
        # print('\t#child_span:\t', child_span)
        child_dependency_dict_or_graph = span_tree_to_dependency_graph_recursion(
            span_tree=span_tree, current_span_node=child_span)
        # headword_position = child_span.headword_position
        headword_node_in_dep = look_for_headword_in_dependencygraph(
            dependency_graph=current_span_node_dependency_graph,
            span_tree_tokens= current_span_node.tokens, #span_tree.tokens,
            headwords_position_in_span_tree_tokens=child_span.headword_position)
        # print('#headword_node_in_dep:\t', headword_node_in_dep['word'],
        #       '\t###father:', current_span_node.content,
        #       '\t###son:', child_span.content)
        # if child_span.headword_relation == 'cc':
        #     headword_node_in_dep = look_for_father_in_dependencygraph(
        #             current_span_node_dependency_graph, headword_node_in_dep)
        current_span_node_dependency_graph = merge(
                    merge_dependency_graph=current_span_node_dependency_graph,
                    child_dependency_dict_or_graph=child_dependency_dict_or_graph,
                    headword_node_in_dep=headword_node_in_dep,
                    modifier_relation=child_span.headword_relation)
    return current_span_node_dependency_graph

def merge(merge_dependency_graph=None, child_dependency_dict_or_graph=None,
          headword_node_in_dep=None, modifier_relation='other'):
    if isinstance(child_dependency_dict_or_graph, dict):
        '''add node in dependency graph'''
        node_info = child_dependency_dict_or_graph
        # add_index = len(merge_dependency_graph.nodes)
        node_info['address'] = len(merge_dependency_graph.nodes)
        node_info['head'] = headword_node_in_dep['address']
        node_info['rel'] = modifier_relation
        merge_dependency_graph.add_node(node_info)
        merge_dependency_graph.add_arc(headword_node_in_dep['address'], node_info['address'])
    elif isinstance(child_dependency_dict_or_graph, DependencyGraph):
        add_graph(skeleton_dependency_graph=merge_dependency_graph,
                  head_node_in_dependency_graph=headword_node_in_dep,
                  sub_dependency_graph=child_dependency_dict_or_graph,
                  dependency_rel=modifier_relation)

    return merge_dependency_graph

def add_graph(skeleton_dependency_graph=None, head_node_in_dependency_graph=None,
              sub_dependency_graph=None, dependency_rel=None):

    # 维护一个当前子树到新skeleton tree中的对应dict
    sub_dependency_graph_node_to_skeleton_node_dict = {}
    # 维护一个新地址id
    new_address = len(skeleton_dependency_graph.nodes) - 1

    # add nodes in sub_dependency_graph, add node, at the time record 'deps'
    node_index_to_dict_list_ranked = list(sorted(sub_dependency_graph.nodes.items(), key=lambda d: d[0], reverse=False))
    for (_, node_info_in_node) in node_index_to_dict_list_ranked:
        if node_info_in_node['head'] is None : continue # root of subgraph, 子树的根，则过滤
        new_address += 1
        # 记住new and old对应关系
        sub_dependency_graph_node_to_skeleton_node_dict[node_info_in_node['address']] = new_address
        node_info = copy.deepcopy(node_info_in_node)
        # 更新新地址
        node_info['address'] = sub_dependency_graph_node_to_skeleton_node_dict[node_info_in_node['address']]
        node_info['deps'] = defaultdict(list)
        # add skeleton
        skeleton_dependency_graph.add_node(node_info)

    # update arc in dependency graph 更新子树的结构信息
    for (_, node_info_in_node) in node_index_to_dict_list_ranked:
        if node_info_in_node['head'] is None: continue # root of subgraph, 子树的根，则过滤
        skeleton_node = skeleton_dependency_graph.nodes[
            sub_dependency_graph_node_to_skeleton_node_dict[node_info_in_node['address']]]
        if node_info_in_node['head'] != 0: # 非根，更新原先子树中的关系
            skeleton_node['head'] = sub_dependency_graph_node_to_skeleton_node_dict[node_info_in_node['head']]
        else: # 子树的根
            # skeleton_node = skeleton_dependency_graph.nodes[
            #     sub_dependency_graph_node_to_skeleton_node_dict[node_info_in_node['address']]
            # ]
            # print(head_node_in_dependency_graph, dependency_rel)
            skeleton_node['rel'] = dependency_rel
            skeleton_node['head'] = head_node_in_dependency_graph['address']
        skeleton_dependency_graph.add_arc(skeleton_node['head'], skeleton_node['address'])

def look_for_headword_in_dependencygraph(dependency_graph, span_tree_tokens, headwords_position_in_span_tree_tokens):
    headword_node_in_dep = None
    # look for node in skeleton span, 首先找到skeleton parsing中的token
    headword_token_in_skeleton = None
    for skeleton_token in span_tree_tokens:
        if skeleton_token.index == headwords_position_in_span_tree_tokens:
            headword_token_in_skeleton = skeleton_token
            break
    # print('#headword_token_in_skeleton:\t', headword_token_in_skeleton)
    # look for node in dep 通过字面比较，来判断在依存树上的头，可能会有bug
    for index, node_in_dep in dependency_graph.nodes.items():
        # print (headword_token_in_skeleton.value, node_in_dep['word'])
        if headword_token_in_skeleton.value == node_in_dep['word'] \
            or (headword_token_in_skeleton.value == ')' and node_in_dep['word'] == '-RRB-') \
            or (headword_token_in_skeleton.value == '(' and node_in_dep['word'] == '-LRB-') \
            or (headword_token_in_skeleton.value == '"' and node_in_dep['word'] == '\'\''):
            headword_node_in_dep = node_in_dep
    return headword_node_in_dep
