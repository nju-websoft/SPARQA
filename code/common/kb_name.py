
class KB_Freebase_Latest():

    def __init__(self, root):
        self.dataset = root + '/kb_freebase_latest/'
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
        self.freebase_relations_file = self.dataset+"freebase_relations"


class KB_Freebase_en_2013():
    def __init__(self, root):
        self.dataset = root + '/kb_freebase_en_2013/'
        # entity linking resouces
        self.freebase_graph_name_entity = self.dataset + 'el_en_vocab/graphq201306_nameentity_handled'
        self.freebase_graph_alias_entity = self.dataset + 'el_en_vocab/graphq201306_aliasentity_handled'
        self.graphquestions_train_friendlyname_entity = self.dataset + 'el_en_vocab/graphquestions_train_friendlyname_entity_handled'
        self.clueweb_mention_pro_entity = self.dataset + 'el_en_vocab/clueweb_name_entity_pro_handled'
        self.mediatortypes_file = self.dataset + "mediatortypes"
        self.mediators_instances_file = self.dataset + "freebase_all_mediators_instances"
        self.freebase_class_pro = self.dataset + 'freebase_types_reverse'
        self.freebase_class_popularity = self.dataset + 'freebase_types_popularity'
