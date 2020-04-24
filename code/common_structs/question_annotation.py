from common_structs.structure import Structure

class QuestionAnnotation():

    def __init__(self,
                 qid=None,
                 question=None,
                 question_normal=None,
                 span_tree=None,
                 span_tree_hybrid_dependency_graph=None,
                 surface_tokens_to_dep_node_dict=None,
                 super_ungrounded_graph=None,
                 sequence_ner_tag_dict=None,
                 gold_graph_query=None,
                 gold_answer=None,
                 gold_sparql_query=None):
        self.qid = qid
        self.question = question
        self.question_normal = question_normal
        self.tokens = span_tree.tokens
        self.compositionality_type = "simple"  # nest, conj, simple
        self.function = None
        self.commonness = 0
        self.num_node = -1
        self.num_edge = -1
        self.span_tree = span_tree
        self.span_tree_hybrid_dependency_graph = span_tree_hybrid_dependency_graph
        self.super_ungrounded_graph = super_ungrounded_graph
        self.surface_tokens_to_dep_node_dict = surface_tokens_to_dep_node_dict
        self.sequence_ner_tag_dict = sequence_ner_tag_dict

        self.abstract_question_word = []
        self.important_words_list = []
        self.gold_graph_query = gold_graph_query
        self.gold_answer = gold_answer
        self.gold_sparql_query = gold_sparql_query
        self.question_classification()

    def question_classification(self):
        # complex or simple  and  > , >=, <, <=, count, argmax, argmin
        self.compositionality_type = "simple"  # nest, conj, simple
        if self.num_edge > 1:
            self.compositionality_type = "complex"
        self.function = None
        for node in self.super_ungrounded_graph.nodes:
            if node.function != 'none':
                self.function = node.function

    def convert_to_structure(self):
        '''
        structure = Structure(question_annotation.qid,
                      question_annotation.question_normal,
                      words=str([question_annotation.tokens[i].value for i in range(len(question_annotation.tokens))]),
                      function=question_annotation.function,
                      compositionality_type=question_annotation.compositionality_type,
                      num_node=len(super_ungrounded_graph.nodes),
                      num_edge=len(super_ungrounded_graph.edges),
                      span_tree=str(question_annotation.span_tree),
                      gold_graph_query=question_annotation.gold_graph_query,
                      gold_answer=question_annotation.gold_answer,
                      gold_sparql_query=question_annotation.gold_sparql_query)
        '''
        return Structure(self.qid,
                              self.question_normal,
                              words=str([self.tokens[i].value for i in range(len(self.tokens))]),
                              function=self.function,
                              compositionality_type=self.compositionality_type,
                              num_node=len(self.super_ungrounded_graph.nodes),
                              num_edge=len(self.super_ungrounded_graph.edges),
                              span_tree=str(self.span_tree),
                              gold_graph_query=self.gold_graph_query,
                              gold_answer=self.gold_answer,
                              gold_sparql_query=self.gold_sparql_query)

    # def abstract_question_word_generation(self):
    #     i = 0
    #     while i < len(self.tokens):
    #         is_contained = False
    #         for sequence_start_end, ner_tag in self.sequence_ner_tag_dict.items():
    #             if ner_tag not in ['entity', 'literal', 'class']: continue
    #             sequence_start = int(sequence_start_end.split('\t')[0])
    #             sequence_end = int(sequence_start_end.split('\t')[1])
    #             if sequence_start <= i <= sequence_end:
    #                 # self.abstract_question_word.append('NP')
    #                 # self.abstract_question_pos.append('NP')
    #                 self.abstract_question_word.append(ner_tag)
    #                 # self.abstract_question_pos.append(node_type)
    #                 is_contained = True
    #                 i += (sequence_end - sequence_start + 1)
    #                 break
    #         if not is_contained:
    #             self.abstract_question_word.append(self.tokens[i].value)
    #             # self.abstract_question_pos.append(self.pos_list[i])
    #             i += 1

