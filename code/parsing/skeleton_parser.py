from common_structs.skeleton import SpanTree
from parsing.models.fine_tuning_based_on_bert_interface import redundancy_span_interface
from parsing.models.fine_tuning_based_on_bert_interface import sequences_classifier_interface
from parsing.models.fine_tuning_based_on_bert_interface import headword_span_interface
from parsing.models.fine_tuning_based_on_bert_interface import simplif_classifier_interface
from parsing import parsing_utils

def span_tree_generation_only_dep(tokens):
    span_tree = SpanTree(tokens=tokens)
    span_tree.add_span_node(id=0, head_tail_position=[0, len(tokens)], isRoot=True, tokens=tokens)
    return span_tree

def span_tree_generation_head(tokens):
    '''
    产生叶子顶点
    产生非叶子顶点
    每个树的顶点, 视为tokens列表
    边: 视为顶点与另一顶点内的某个token之间关系.
    '''
    epoch = 0
    span_tree = SpanTree(tokens=tokens)
    root_span_node = span_tree.add_span_node(id=0, head_tail_position=[0, len(tokens)], isRoot=True, tokens=tokens)
    while simplif_classifier_interface.process(root_span_node.content) == 1:
        epoch = epoch + 1
        if epoch > 10:
            break
        # --------------------------------------
        redundancy_span, redundancy_nbest_json = redundancy_span_interface.simple_process(root_span_node.content)
        if redundancy_span is None or redundancy_span == 'empty' or redundancy_nbest_json is None or len(root_span_node.tokens) - len(redundancy_span.split(' ')) <= 3:
            #heuristic rule, 如果删除以后, tokens数量小于4 超过10轮的迭代, 就退出
            break
        # -----------------head---------------------
        headword_index, _ = headword_span_interface.simple_process(question=root_span_node.content, span=redundancy_span)
        #update headword index, based on complete sequence
        headword_index = parsing_utils.update_headword_index(tokens=root_span_node.tokens, headword_index=headword_index)
        # ---------------span position--------------# look for position in utterance
        start_index, end_index = parsing_utils.look_for_position(redundancy_span, root_span_node)
        if start_index > end_index:
            break
        sub_tokens = parsing_utils.get_sub_tokens(root_span_node.tokens, start_index=start_index, end_index=end_index)
        sub_span_node = span_tree.add_span_node(id=epoch, head_tail_position=[start_index, end_index], tokens=sub_tokens, isRoot=False)
        # --------------------------------------
        #增长树结构: 判断是叶子顶点还是非叶子顶点.
        #span node部分是不是有其他node的根, 如果有, 则为非叶子顶点; 否则, 则为叶子顶点.
        if not parsing_utils.is_leaf(span_tree=span_tree, span_node=sub_span_node):
            #非叶子顶点, 等价于插入顶点
            parsing_utils.update_span_tree_structure(span_tree=span_tree, sub_span_node=sub_span_node)
        # -------------------relation classifier 检测修饰关系-------------------
        relation = sequences_classifier_interface.process(line_a=root_span_node.content, line_b=redundancy_span)
        # --------------------------------------
        # print('###:\t', root_span_node.content)
        # print('####:\tspan:', redundancy_span, 'headword_index:', headword_index, 'rel_index:', relation)
        span_tree.add_child_rel_with_headword(father_id=root_span_node.id, son_id=sub_span_node.id, headword_position=headword_index, headword_relation=relation)
        # --------------------------------------
        parsing_utils.update_span_tree_nodes(span_tree=root_span_node, start_index=start_index, end_index=end_index)
        # --------------------------------------
    return span_tree

def span_tree_generation_joint__(tokens):
    '''
    产生叶子顶点
    产生非叶子顶点
    每个树的顶点, 视为tokens列表
    边: 视为顶点与另一顶点内的某个token之间关系.
    '''
    from parsing.models.fine_tuning_based_on_bert_interface import joint_three_models_interface
    epoch = 0
    span_tree = SpanTree(tokens=tokens)
    root_span_node = span_tree.add_span_node(id=0, head_tail_position=[0, len(tokens)], isRoot=True, tokens=tokens)
    while simplif_classifier_interface.process(root_span_node.content) == 1:
        epoch = epoch + 1
        if epoch > 10:
            break
        # --------------------------------------
        redundancy_span, headword_index, relation, redundancy_nbest_json = joint_three_models_interface.simple_process(root_span_node.content)
        if redundancy_span is None or redundancy_span == 'empty' or redundancy_nbest_json is None or len(root_span_node.tokens)-len(redundancy_span.split(' '))<=3:
            #heuristic rule, 如果删除以后, tokens数量小于4 超过10轮的迭代, 就退出
            break
        # -----------------head---------------------
        #update headword index, based on complete sequence
        headword_index = parsing_utils.update_headword_index(tokens=root_span_node.tokens, headword_index=headword_index)
        # ---------------span position--------------
        # look for position in utterance
        start_index, end_index = parsing_utils.look_for_position(redundancy_span, root_span_node)
        if start_index > end_index: break
        # --------------------------------------
        # reg nodes
        sub_tokens = parsing_utils.get_sub_tokens(root_span_node.tokens, start_index=start_index, end_index=end_index)
        sub_span_node = span_tree.add_span_node(id=epoch, head_tail_position=[start_index, end_index], tokens=sub_tokens, isRoot=False)
        #增长树结构: 判断是叶子顶点还是非叶子顶点.
        #span node部分是不是有其他node的根, 如果有, 则为非叶子顶点; 否则, 则为叶子顶点.
        if not parsing_utils.is_leaf(span_tree=span_tree, span_node=sub_span_node): #非叶子顶点, 等价于插入顶点
            parsing_utils.update_span_tree_structure(span_tree=span_tree, sub_span_node=sub_span_node)
        # print('###:\t', root_span_node.content)
        # print('####:\tspan:', redundancy_span, 'headword_index:', headword_index, 'rel_index:', relation)
        span_tree.add_child_rel_with_headword(father_id=root_span_node.id, son_id=sub_span_node.id,
                                              headword_position=headword_index, headword_relation=relation)
        # ---update root span node
        parsing_utils.update_span_tree_nodes(span_tree=root_span_node, start_index=start_index, end_index=end_index)
        # --------------------------------------
    return span_tree

