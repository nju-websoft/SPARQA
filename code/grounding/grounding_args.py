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
    literal_to_id_map = grounding_utils.read_literal_to_id_map_cwq(file_root=globals_args.fn_cwq_file.grounded_graph_file)
elif q_mode == 'graphq':
    #2.2
    oracle_file_root = globals_args.fn_graph_file.grounded_graph_file+'result/'
    oracle_all_files_path_names = os.listdir(oracle_file_root)
    literal_to_id_map = grounding_utils.read_literal_to_id_map_graphq(file_root=globals_args.fn_graph_file.grounded_graph_file)

# 2.1 args
if kb_mode == 'kb_freebase_latest':
    # entity linking
    entity_list_file = globals_args.kb_freebase_latest_file.entity_list_file
    surface_map_file = globals_args.kb_freebase_latest_file.surface_map_file
    entity_index_prefix = globals_args.kb_freebase_latest_file.entity_index_prefix
    # mediator
    mediatortypes = hand_files.read_set(globals_args.kb_freebase_latest_file.mediatortypes_file)
    mediators_instances_set = hand_files.read_set(globals_args.kb_freebase_latest_file.mediators_instances_file)
    # quotations
    quotation_dict = hand_files.read_dict(globals_args.kb_freebase_latest_file.quotation_file)
    # class linking
    cl_dict_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_latest_file.freebase_class_pro)
    class_popularity_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_latest_file.freebase_class_popularity)
    # relation
    freebase_relations = globals_args.kb_freebase_latest_file.freebase_relations_file
elif kb_mode == 'kb_freebase_en_2013':
    # entity linking
    freebase_graph_name_entity_file = globals_args.kb_freebase_en_2013.freebase_graph_name_entity
    freebase_graph_alias_entity_file = globals_args.kb_freebase_en_2013.freebase_graph_alias_entity
    clueweb_mention_pro_entity_file = globals_args.kb_freebase_en_2013.clueweb_mention_pro_entity
    graphquestions_train_friendlyname_entity_file = globals_args.kb_freebase_en_2013.graphquestions_train_friendlyname_entity
    # mediator
    mediatortypes = hand_files.read_set(globals_args.kb_freebase_en_2013.mediatortypes_file)
    mediators_instances_set = hand_files.read_set(globals_args.kb_freebase_en_2013.mediators_instances_file)
    # quotations
    quotation_dict = dict()
    # class linking
    cl_dict_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_en_2013.freebase_class_pro)
    class_popularity_dict = hand_files.read_dict_dict_update(globals_args.kb_freebase_en_2013.freebase_class_popularity)
    # relation
    freebase_relations = globals_args.kb_freebase_en_2013.freebase_relations_file
else:
    print('kb mode is error!')
