
class KB_Freebase_Latest():

    def __init__(self, root):
        self.dataset = root + '/kb_freebase_latest/'
        # lexicon
        # self.clueweb_mention_pro_entity_file=self.dataset+'clueweb_mention_proconmen_entitylist'
        # self.freebase_graph_name_entity_file = self.dataset + 'freebase_instance_names_handle'
        # self.freebase_graph_alias_entity_file = self.dataset + 'freebase_instance_alias_handle'
        # self.classmention_embedding_file=self.dataset+'classmention_embedding'
        #entity linking
        self.entity_list_file = self.dataset + "el_aqqu_mid_vocab/entity-list"
        self.surface_map_file = self.dataset + "el_aqqu_mid_vocab/entity-surface-map"
        self.entity_index_prefix = self.dataset + "el_aqqu_mid_vocab/entity-index"

        self.mediatortypes_file = self.dataset + "mediators.tsv"
        self.mediators_instances_file = self.dataset + "freebase_all_mediators_instances"
        self.quotation_file = self.dataset + 'freebase_all_quotations_name'
        #class linking
        self.freebase_class_pro = self.dataset + 'freebase_types_reverse'
        self.freebase_class_popularity = self.dataset + 'freebase_types_popularity'

        # self.relortype_level_words = self.dataset + 'relortype_level_words.json'
        self.freebase_relations_file = self.dataset+"freebase_relations"
        # self.freebase_relation_finalword_file = self.dataset + "freebase_relations_finalwords"
        # self.freebase_types_file = self.dataset+"freebase_types"
        # self.freebase_type_finalword_file = self.dataset+"freebase_types_finalwords"
        # self.entity_types_file_dat = self.dataset + "freebase_instance_types_1.pickle"
        # self.schema_file = self.dataset + "freebase_schema"
        # self.freebase_reverse_property = self.dataset + "freebase_reverse_property"
        # self.entity_names_path = self.dataset+"freebase_instance_names"

        # self.vocabulary_file = self.llzhang_file + "vocabulary/"
        # self.freebase_class_index = self.dataset + '/dataset_freebase_latest/mysql_indexs/freebase_types_with_index_reverse'
        # self.freebase_os_topic_id_type_nid_file = self.dataset + '/dataset_freebase_latest/mysql_indexs/os_topic_id_type_nid.txt'
        # self.freebase_so_topic_id_type_nid_file = self.dataset + '/dataset_freebase_latest/mysql_indexs/so_topic_id_type_nid.txt'
        # self.freebase_os_types_id_type_nid_file = self.dataset + '/dataset_freebase_latest/mysql_indexs/os_types_id_type_nid.txt'
        # self.freebase_so_types_id_type_nid_file = self.dataset + '/dataset_freebase_latest/mysql_indexs/so_types_id_type_nid.txt'
        # self.aqqu_entity_contained = self.dataset + "/el_aqqu_mid_vocab/aqqu_entity_contained"
        # parser.add_argument('--freebase_class_pro', type=str, default= root + "/resources_class_linking/2019.03.13_freebase_class_pro_150g.txt")

class KB_Freebase_en_2013():

    def __init__(self, root):
        self.dataset = root + '/kb_freebase_en_2013/'
        # entity linking resouces
        self.freebase_graph_name_entity = self.dataset + 'el_en_vocab/graphq201306_nameentity_handled'
        self.freebase_graph_alias_entity = self.dataset + 'el_en_vocab/graphq201306_aliasentity_handled'
        self.graphquestions_train_friendlyname_entity = self.dataset + 'el_en_vocab/graphquestions_train_friendlyname_entity_handled'
        self.clueweb_mention_pro_entity = self.dataset + 'el_en_vocab/clueweb_name_entity_pro_handled'

        # self.personname = self.dataset + 'el_en_vocab/personname'
        # self.train_friendlyname = self.dataset + 'el_en_vocab/train_friendlyname'
        # self.suoxie = self.dataset + 'el_en_vocab/suoxie'

        self.mediatortypes_file = self.dataset + "mediatortypes"
        self.mediators_instances_file = self.dataset + "freebase_all_mediators_instances"

        self.freebase_class_pro = self.dataset + 'freebase_types_reverse'
        self.freebase_class_popularity = self.dataset + 'freebase_types_popularity'

        # vocabularys
        # self.freebase_relations_file = self.dataset + "freebase_relations"
        # self.freebase_types_file = self.dataset + "freebase_types"
        # self.freebase_type_finalword_file = self.dataset + "freebase_type_finalword"
        # self.freebase_relation_finalword_file = self.dataset + "freebase_relation_finalword"
        # self.schema_file = self.dataset + "2019.05.13_freebase_schema.txt"
        # self.entity_types_file_dat = self.dataset + "entity_types.dat"
        # self.entity_types_file = self.dataset + "entity_types"
        # self.mediatortypes_file = self.dataset + "mediatortypes"
        # self.mediators_instances_file = self.dataset + "freebase_all_mediators_instances"
        # self.entity_iscvt_file = self.dataset + "entity_iscvt"
        # self.entity_iscvt_structure1_file = self.dataset + "entity_iscvt_structure1"
        # self.entity_relation_intorfloat_file = self.dataset + "entity_relation_intorfloat"
        # self.freebase_reverse_property = self.dataset + "freebase_reverse_property"
        # self.vocabulary_file = self.llzhang_file + "vocabulary/"
        # self.candidates_generation_backup_file = self.candidates_generation_file + "backup/"
        # self.ngram_el = self.dataset + 'el_en_vocab/2018.02.25_graphq_test_ngram_el.txt'
        # self.entityPopularity = self.dataset + 'el_en_vocab/entityPopularity'
