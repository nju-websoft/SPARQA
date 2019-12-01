from common import globals_args
from common import hand_files
from grounding import grounding_utils
import os

q_mode = globals_args.q_mode
kb_mode = globals_args.kb_mode
glove_file = globals_args.argument_parser.glove_file
wh_words_set = {"what", "which", "whom", "who", "when", "where", "why", "how", "how many", "how large", "how big"}
class_fuzz_weight = 0.5
class_glove_weight = 0.5

# 2.2 args
if q_mode == 'cwq':
    #2.2
    oracle_file_root = globals_args.fn_cwq_file.grounded_graph_file+'result/'
    oracle_all_files_path_names = os.listdir(oracle_file_root)
    # freebase_relations = hand_files.read_set(globals_args.fn_cwq_file.freebase_relations_file)
    # freebase_relation_finalwords = hand_files.read_dict(globals_args.fn_cwq_file.freebase_relation_finalword_file)
    # freebase_types = hand_files.read_set(globals_args.fn_cwq_file.freebase_types_file)
    # freebase_type_finalwords = hand_files.read_dict(globals_args.fn_cwq_file.freebase_type_finalword_file)
    # schema_lines_list = hand_files.read_list(globals_args.fn_cwq_file.schema_file)
    # property_reverse_dict = hand_files.read_dict(globals_args.fn_cwq_file.freebase_reverse_property)
    # class_popularity_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_latest_file.freebase_class_popularity)
    # mediators_instances_set = hand_files.read_set(globals_args.fn_cwq_file.mediators_instances_file)

    literal_to_id_map = grounding_utils.read_literal_to_id_map_cwq(file_root=globals_args.fn_cwq_file.grounded_graph_file)


# elif q_mode == 'webq':
    #2.2
    # oracle_file_root = globals_args.fn_webq_file.grounded_graph_file+'result/'
    # oracle_all_files_path_names = os.listdir(oracle_file_root)

# elif q_mode == 'graphq':
#     2.2
    # oracle_file_root = globals_args.fn_graph_file.grounded_graph_file+'result/'
    # oracle_all_files_path_names = os.listdir(oracle_file_root)

    # qid_to_position_grounding_result_dict = hand_files.read_ngram_el_grounding_result(globals_args.fn_graph_file.ngram_el)
    # freebase_relations = hand_files.read_set(globals_args.fn_graph_file.freebase_relations_file)
    # freebase_relation_finalwords = hand_files.read_dict(globals_args.fn_graph_file.freebase_relation_finalword_file)
    # freebase_types = hand_files.read_set(globals_args.fn_graph_file.freebase_types_file)
    # freebase_type_finalwords = hand_files.read_dict(globals_args.fn_graph_file.freebase_type_finalword_file)
    # schema_lines_list = hand_files.read_list(globals_args.fn_graph_file.schema_file)
    # mediatortypes = hand_files.read_set(globals_args.fn_graph_file.mediatortypes_file)
    # quotation_dict = dict()
    # property_reverse_dict = hand_files.read_dict(globals_args.fn_graph_file.freebase_reverse_property)
    # class_popularity_dict = hand_files.read_dict_dict_update(globals_args.fn_graph_file.freebase_class_popularity)
    # mediators_instances_set = hand_files.read_set(globals_args.fn_graph_file.mediators_instances_file)
    # test_qid_to_answers_mid_dict = hand_files.read_graphs_qid_to_answers_set(globals_args.fn_graph_file.graphquestions_testing_answers_dir)
    # train_qid_to_answers_mid_dict = hand_files.read_graphs_qid_to_answers_set(globals_args.fn_graph_file.graphquestions_training_answers_dir)

elif q_mode == 'lcquad':
    #2.2
    oracle_file_root = globals_args.fn_lcquad_file.grounded_graph_file+'result/'
    oracle_all_files_path_names = os.listdir(oracle_file_root)

elif q_mode == 'graphq':
    #2.2
    oracle_file_root = globals_args.fn_graph_file.grounded_graph_file+'result/'
    oracle_all_files_path_names = os.listdir(oracle_file_root)
    literal_to_id_map = grounding_utils.read_literal_to_id_map_graphq(file_root=globals_args.fn_graph_file.grounded_graph_file)

    test_qid_to_answers_mid_dict = hand_files.read_graphs_qid_to_answers_set(globals_args.fn_graph_file.graphquestions_testing_answers_dir)
    train_qid_to_answers_mid_dict = hand_files.read_graphs_qid_to_answers_set(globals_args.fn_graph_file.graphquestions_training_answers_dir)


# elif q_mode == 'qald':
    #2.2
    # oracle_file_root = globals_args.fn_qald_file.grounded_graph_file+'result/'
    # oracle_all_files_path_names = os.listdir(oracle_file_root)

#-------------------------------------------------

# 2.1 args

if kb_mode == 'kb_dbpedia_201604':
    label_to_iris_dict_dict = hand_files.read_pickle(globals_args.kb_dbpedia_201604_file.label_lexicon_path)
    wikipage_to_iris_dict_dict = hand_files.read_pickle(globals_args.kb_dbpedia_201604_file.pageRedirects_lexicon_path)
    wikilinkText_to_iris_dict_dict = hand_files.read_pickle(globals_args.kb_dbpedia_201604_file.wikiLinkText_lexicon_path)
    cl_dict_dict = hand_files.read_dict_dict_update(globals_args.kb_dbpedia_201604_file.dbpedia_class_pro)

elif kb_mode == 'kb_dbpedia_201610':
    label_to_iris_dict_dict = hand_files.read_pickle(globals_args.kb_dbpedia_201610_file.label_lexicon_path)
    wikipage_to_iris_dict_dict = hand_files.read_pickle(globals_args.kb_dbpedia_201610_file.pageRedirects_lexicon_path)
    wikilinkText_to_iris_dict_dict = hand_files.read_pickle(globals_args.kb_dbpedia_201610_file.wikiLinkText_lexicon_path)
    cl_dict_dict = hand_files.read_dict_dict_update(globals_args.kb_dbpedia_201610_file.dbpedia_class_pro)

elif kb_mode == 'kb_freebase_latest':
    # entity linking
    entity_list_file = globals_args.kb_freebase_latest_file.entity_list_file
    surface_map_file = globals_args.kb_freebase_latest_file.surface_map_file
    entity_index_prefix = globals_args.kb_freebase_latest_file.entity_index_prefix
    # freebase_graph_name_entity_file = globals_args.kb_freebase_latest_file.freebase_graph_name_entity_file
    # freebase_graph_alias_entity_file = globals_args.kb_freebase_latest_file.freebase_graph_alias_entity_file
    # clueweb_mention_pro_entity_file = globals_args.kb_freebase_latest_file.clueweb_mention_pro_entity_file
    # graphquestions_train_friendlyname_entity_file = ''
    freebase_relations = globals_args.kb_freebase_latest_file.freebase_relations_file


    quotation_dict = hand_files.read_dict(globals_args.kb_freebase_latest_file.quotation_file)
    cl_dict_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_latest_file.freebase_class_pro)
    class_popularity_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_latest_file.freebase_class_popularity)

    # mediator
    mediatortypes = hand_files.read_set(globals_args.kb_freebase_latest_file.mediatortypes_file)

elif kb_mode == 'kb_freebase_en_2013':
    freebase_graph_name_entity_file = globals_args.kb_freebase_en_2013.freebase_graph_name_entity
    freebase_graph_alias_entity_file = globals_args.kb_freebase_en_2013.freebase_graph_alias_entity
    clueweb_mention_pro_entity_file = globals_args.kb_freebase_en_2013.clueweb_mention_pro_entity
    graphquestions_train_friendlyname_entity_file = globals_args.kb_freebase_en_2013.graphquestions_train_friendlyname_entity

    cl_dict_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_en_2013.freebase_class_pro)
    class_popularity_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_en_2013.freebase_class_popularity)
    # mediator
    mediatortypes = hand_files.read_set(globals_args.kb_freebase_en_2013.mediatortypes_file)
    mediators_instances_set = hand_files.read_set(globals_args.kb_freebase_en_2013.mediators_instances_file)
    quotation_dict = dict()

else:
    pass



