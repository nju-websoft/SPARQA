from grounding import grounding_utils

class EntityLinker():
    '''entity linking by looking for lexicons'''
    def __init__(self, entity_vocabulary):
        self.entity_vocabulary = entity_vocabulary

    def get_indexrange_entity_pros_by_mention(self, mention_phrase, top_k):
        '''
        entity linking by one mention.
        function: return top_k entity, each mention_phrase
        '''
        entity_pros_friendlyname = self._friendlyname_entity_match_one(mention_phrase)
        entity_pros_alias = self._aliases_entity_match_one(mention_phrase)
        entity_pros_name = self._name_entity_match_one(mention_phrase)
        entity_pros_clueweb = self._clueweb_entity_match_one(mention_phrase)

        entity_pros_sum = self._entity_pros_sum_all(entity_pros_friendlyname, entity_pros_alias, entity_pros_name, entity_pros_clueweb)
        entity_pros_dict = dict()
        if len(entity_pros_sum) > 0:
            entity_pros_sort_list = list(sorted(entity_pros_sum.items(), key=lambda d: d[1], reverse=True))
            if len(entity_pros_sort_list) > top_k:
                entity_pros_dict = dict(entity_pros_sort_list[:top_k])
            else:
                entity_pros_dict = dict(entity_pros_sort_list)
        return entity_pros_dict

    def _entity_pros_sum_all(self, entity_pros_friendlyname, entity_pros_alias, entity_pros_name, entity_pros_clueweb):
        entity_pro_sum = dict()
        entity_pro_sum = grounding_utils.add_dict_number(entity_pro_sum, entity_pros_friendlyname)
        entity_pro_sum = grounding_utils.add_dict_number(entity_pro_sum, entity_pros_alias)
        entity_pro_sum = grounding_utils.add_dict_number(entity_pro_sum, entity_pros_name)
        entity_pro_sum = grounding_utils.add_dict_number(entity_pro_sum, entity_pros_clueweb)
        entity_pro_sum = dict(sorted(entity_pro_sum.items(), key=lambda d:d[1], reverse=True))
        return entity_pro_sum

    def _aliases_entity_match_one(self,phrase):
        '''add aliases'''
        entity_pros = dict()
        #  range=phrasen.split("\t")[1]
        if phrase in self.entity_vocabulary.freebase_graph_alias_entity:
            entities = self.entity_vocabulary.freebase_graph_alias_entity[phrase]
            for entity in entities:
                if "en." in entity:
                    entity_pros[entity] = float(0.9)
        return entity_pros

    def _name_entity_match_one(self,phrase):
        '''add freebase name'''
        entity_pros = dict()
        if phrase in self.entity_vocabulary.freebase_graph_name_entity:
            entities = self.entity_vocabulary.freebase_graph_name_entity[phrase]
            for entity in entities:
                # if ("m." in entity) | ("en." in entity):
                if "en." in entity:
                    entity_pros[entity] = float(1.0)
                    # entity_pros[entity] = float(0.6)
        return entity_pros

    def _clueweb_entity_match_one(self, phrase):
        '''linking by clueweb name'''
        entity_pros = dict()
        if phrase in self.entity_vocabulary.clueweb_mention_pro_entity:
            entity_pro = self.entity_vocabulary.clueweb_mention_pro_entity[phrase]
            for entity in entity_pro:
                # if ("m." in entity) | ("en." in entity):
                if "en." in entity:
                    entity_pros[entity] = entity_pro[entity]
        return entity_pros

    def _friendlyname_entity_match_one(self,phrase):
        '''linking entities by friendlyname'''
        entity_pros = dict()
        if phrase in self.entity_vocabulary.graphquestions_train_friendlyname_entity:
            entities = self.entity_vocabulary.graphquestions_train_friendlyname_entity[phrase]
            for entity in entities:
                if "en." in entity:
                    entity_pros[entity] = float(1.0)
        return entity_pros
