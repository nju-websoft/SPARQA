# -*- coding: utf-8 -*-
# from common.globals_args import fn_graph_file, fn_cwq_file
# from grounding import grounding_args
from grounding._2_1_grounded_graph.entity_linking_en_vocab.entity_linker import EntityLinker
from common.hand_files import read_dict, read_dict_dict

class EntityVocabulary():
    '''four lexicons  entity_vocabulary'''
    def __init__(self, freebase_graph_name_entity_file, freebase_graph_alias_entity_file, graphquestions_train_friendlyname_entity_file, clueweb_mention_pro_entity_file):

        self.freebase_graph_name_entity = read_dict(freebase_graph_name_entity_file)
        self.freebase_graph_alias_entity = read_dict(freebase_graph_alias_entity_file)
        if graphquestions_train_friendlyname_entity_file != '':
            self.graphquestions_train_friendlyname_entity = read_dict(graphquestions_train_friendlyname_entity_file)
        else:
            self.graphquestions_train_friendlyname_entity = dict()
        self.clueweb_mention_pro_entity = read_dict_dict(clueweb_mention_pro_entity_file)

        # if mode == 'graphq':
            #read friendly name file
            #read clueweb mention

        # elif mode == 'cwq':
        #   self.graphquestions_train_friendlyname_entity = dict()
        #   self.clueweb_mention_pro_entity = dict()

class EntityLinkPipeline():
    '''entity linking'''
    def __init__(self, freebase_graph_name_entity_file, freebase_graph_alias_entity_file, graphquestions_train_friendlyname_entity_file, clueweb_mention_pro_entity_file):
        # if grounding_args.mode == 'graphq':
        #     self.freebase_graph_name_entity_file = fn_graph_file.freebase_graph_name_entity
        #     self.freebase_graph_alias_entity_file = fn_graph_file.freebase_graph_alias_entity
        #     self.graphquestions_train_friendlyname_entity_file = fn_graph_file.graphquestions_train_friendlyname_entity
        #     self.clueweb_mention_pro_entity_file = fn_graph_file.clueweb_mention_pro_entity

        # elif grounding_args.mode == 'cwq':
            # self.freebase_graph_name_entity_file = fn_cwq_file.freebase_graph_name_entity_file
            # self.freebase_graph_alias_entity_file = fn_cwq_file.freebase_graph_alias_entity_file
            # self.clueweb_mention_pro_entity_file = fn_cwq_file.clueweb_mention_pro_entity_file
            # self.graphquestions_train_friendlyname_entity_file = fn_graph_file.graphquestions_train_friendlyname_entity
        #initialize the vocabulary
        # mode = grounding_args.mode
        self.entity_vocabulary = EntityVocabulary(
            freebase_graph_name_entity_file, freebase_graph_alias_entity_file, graphquestions_train_friendlyname_entity_file, clueweb_mention_pro_entity_file)


    def get_indexrange_entity_el_pro_one_mention(self, phrase, top_k=10):
        '''
        :param indexrange_phrase: 3\t7 how many tennis tournament championships
        :return: 9	9 {'en.america': 1.4285881881259241,}
        '''
        el = EntityLinker(self.entity_vocabulary)
        return el.get_indexrange_entity_pros_by_mention(phrase, top_k)

# if __name__ == '__main__':
#     elp = EntityLinkPipeline()
#     print (elp.get_indexrange_entity_el_pro_one_mention('o', top_k=100))
