from parsing import parsing_utils
from parsing import parsing_args
from parsing import skeleton_to_dependency

from parsing import node_recognition
from parsing import relation_extraction_nff
from common_structs.question_annotation import QuestionAnnotation
from parsing import structure_transfers
from parsing import skeleton_parser
from parsing.aggregation import aggregation_interface

def run_ungrounded_graph_interface(qid=None, question_normal=None, gold_graph_query=None, gold_answer=None, gold_sparql_query=None):
    ''' 1. span tree;  2. node mention annotation;   3. dependency tree;  4. relation extraction '''
    # 1. span tree generate span tree
    tokens = parsing_utils.create_tokens(question_normal.split(" "))
    if parsing_args.parser_mode == 'head':
        span_tree = skeleton_parser.span_tree_generation_head(tokens=tokens)
    else:
        span_tree = skeleton_parser.span_tree_generation_only_dep(tokens=tokens)
    print('#span tree:', span_tree)
    # 3.generate dependency tree
    span_tree_hybrid_dependency_graph = skeleton_to_dependency.span_tree_to_hybrid_dependency_graph_interface(span_tree=span_tree)
    span_tree_hybrid_dependency_graph = parsing_utils.update_dependencygraph_indexs(old_dependency_graph=span_tree_hybrid_dependency_graph)
    # 2. node mention annotation sequence_bert_ner_tag_dict
    ungrounded_nodes = node_recognition.generate_nodes(question_normal=question_normal, qid=qid, tokens=tokens)
    # aggregation
    is_agg, serialization_list = aggregation_interface.aggregation_interface(question_normal=question_normal)
    if is_agg != 'none':
        for i, token in enumerate(tokens):
            if serialization_list[i] != 'O' and token.ner_tag is None:
                token.ner_tag = serialization_list[i]
        aggregation_interface.set_class_aggregation_function(ungrounded_nodes=ungrounded_nodes,
                                                             dependency_graph=span_tree_hybrid_dependency_graph,
                                                             surface_tokens=tokens)
    # bert's ungrounded graph
    # ungrounded_graph = ungrounded_graph_generator_bert.generate_ungrounded_graph(ungrounded_nodes=ungrounded_nodes,
    # --------------------------- transformation----------------------------------
    # relation -> relation  ==> {relation} -{class mention} -> {relation} 两个class之间插入空白节点
    # ungrounded_graph = transformations.update_merge_relation_to_relation(ungrounded_graph)
    # # merge aggregation node
    # ungrounded_graph = transformations.update_ungrounded_graph_count_aggregation(ungrounded_graph)
    # ungrounded_graph = transformations.update_ungrounded_graph_superlative_aggregation(ungrounded_graph)
    # ungrounded_graph = transformations.update_ungrounded_graph_comparative_aggregation(ungrounded_graph)
    # #relation -> class; relation -> entity;  转变为 class -{relation}->entity
    # ungrounded_graph = transformations.update_ungrounded_graph_contract_relation_node(ungrounded_graph=ungrounded_graph)
    # --------------------------------------------------------------------------------
    # nff's ungrounded graph
    super_ungrounded_graph = relation_extraction_nff.generate_ungrounded_graph(ungrounded_nodes=ungrounded_nodes, span_tree_hybrid_dependency_graph=span_tree_hybrid_dependency_graph)
    # --------------------------- transformation----------------------------------
    # relation -> relation  ==> {relation} -{class mention} -> {relation} 两个class之间插入空白节点
    # merge aggregation node
    # ungrounded_graph = transformations.update_ungrounded_graph_count_aggregation(ungrounded_graph)
    # ungrounded_graph = transformations.update_ungrounded_graph_superlative_aggregation(ungrounded_graph)
    # ungrounded_graph = transformations.update_ungrounded_graph_comparative_aggregation(ungrounded_graph)
    # -------------------------------transformation cwq------------------------------
    ungrounded_graphs_list = []
    super_ungrounded_graph.set_blag('super')
    ungrounded_graphs_list.append(super_ungrounded_graph)
    # class{value:wh-word; question_node:1} -> class  转变为class的question_node:1
    # 操作1：折叠合并 疑问词节点连接class的话, 折叠疑问词, 连接的class的question node设为1
    merge_question_ungrouned_graph = structure_transfers.update_ungrounded_graph_merge_question_node(ungrounded_graph=super_ungrounded_graph)
    if merge_question_ungrouned_graph is not None:
        merge_question_ungrouned_graph.set_blag('merge_qc')
        ungrounded_graphs_list.append(merge_question_ungrouned_graph)
    # 操作2: entity-class  entity-{class}-_blank_node  s,p,?   s, __,o
    # ec_ungrounded_graph = transformations.update_ungrounded_graph_ec(ungrounded_graph=super_ungrounded_graph)
    # if ec_ungrounded_graph is not None:
    #     ec_ungrounded_graph.set_blag('adjust_ec')
    #     ungrounded_graphs_list.append(ec_ungrounded_graph)
    # 操作3: 破圈操作:  包含e-e或e-l或l-l的圈，要把它们破开
    if merge_question_ungrouned_graph is not None:
        current_ungrounded_graph = merge_question_ungrouned_graph
    else:
        current_ungrounded_graph = super_ungrounded_graph
    del_cycle_ungrounded_graph = structure_transfers.undate_ungrounded_graph_del_cycle(ungrounded_graph=current_ungrounded_graph)
    if del_cycle_ungrounded_graph is not None:
        del_cycle_ungrounded_graph.set_blag('del_cycle')
        ungrounded_graphs_list.append(del_cycle_ungrounded_graph)
    # --------------------------------------------------------------------------------
    # abstract_question_word = parser_utils.abstract_question_word_generation(tokens=tokens, sequence_ner_tag_dict=sequence_bert_ner_tag_dict)
    abstract_question_word = parsing_utils.abstract_question_word_generation(tokens=tokens, ungrounded_nodes=ungrounded_nodes)
    sequence_bert_ner_tag_dict = parsing_utils.get_nertag_sequence(ungrounded_nodes=ungrounded_nodes)
    for ungrounded_graph in ungrounded_graphs_list:
        ungrounded_graph.sequence_ner_tag_dict = str(sequence_bert_ner_tag_dict)
        ungrounded_graph.abstract_question = str(abstract_question_word)
        ungrounded_graph.important_words_list = str(parsing_utils.importantwords_by_unimportant_abstractq(abstract_question_word))
    # --------------------------------------------------------------------------------
    # generate question annotation
    question_annotation = QuestionAnnotation(qid=qid,
                                             question=question_normal,
                                             question_normal=question_normal,
                                             span_tree=span_tree,
                                             span_tree_hybrid_dependency_graph=span_tree_hybrid_dependency_graph,
                                             super_ungrounded_graph=super_ungrounded_graph,
                                             sequence_ner_tag_dict=sequence_bert_ner_tag_dict,
                                             gold_graph_query=gold_graph_query,
                                             gold_answer=gold_answer,
                                             gold_sparql_query=gold_sparql_query)
    # --------------------------------------------------------------------------------
    # generate structure
    structure = question_annotation.convert_to_structure()
    structure.set_ungrounded_graph_forest(ungrounded_graph_forest=ungrounded_graphs_list)
    return structure

def test_span_tree(question):
    tokens = parsing_utils.create_tokens(question.split(" "))
    span_tree = skeleton_parser.span_tree_generation_head(tokens=tokens)
    # span_tree = skeleton_parser.span_tree_generation_joint(tokens=tokens)
    # span_tree_hybrid_dependency_graph = skeleton_to_dependency.span_tree_to_hybrid_dependency_graph_interface(span_tree=span_tree)
    print('#question:\t', question)
    print('#span tree:\t', span_tree)
    return span_tree

def test_hybrid_dependency_tree(question):
    tokens = parsing_utils.create_tokens(question.split(" "))
    span_tree = skeleton_parser.span_tree_generation_head(tokens=tokens)
    # span_tree = skeleton_parser.span_tree_generation_joint(tokens=tokens)
    # span_tree_hybrid_dependency_graph = skeleton_to_dependency.span_tree_to_hybrid_dependency_graph_interface(span_tree=span_tree)
    print('#question:\t', question)
    print('#span tree:\t', span_tree)
    span_tree_hybrid_dependency_graph = skeleton_to_dependency.span_tree_to_hybrid_dependency_graph_interface(span_tree=span_tree)
    return parsing_utils.update_dependencygraph_indexs(old_dependency_graph=span_tree_hybrid_dependency_graph)

def test_ungrounded_graph(question_normal=None):
    ''' 1. span tree;  2. node mention annotation;   3. dependency tree;  4. relation extraction '''
    tokens = parsing_utils.create_tokens(question_normal.split(" "))
    span_tree = skeleton_parser.span_tree_generation_head(tokens=tokens)
    print('#span tree:', span_tree)
    span_tree_hybrid_dependency_graph = skeleton_to_dependency.span_tree_to_hybrid_dependency_graph_interface(span_tree=span_tree)
    span_tree_hybrid_dependency_graph = parsing_utils.update_dependencygraph_indexs(old_dependency_graph=span_tree_hybrid_dependency_graph)
    ungrounded_nodes = node_recognition.generate_nodes(question_normal=question_normal, qid=None, tokens=tokens)
    super_ungrounded_graph = relation_extraction_nff.generate_ungrounded_graph(
        ungrounded_nodes=ungrounded_nodes, span_tree_hybrid_dependency_graph=span_tree_hybrid_dependency_graph)
    return super_ungrounded_graph

