from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.corenlp import CoreNLPParser
from nltk.parse import DependencyGraph

class NLTK_NLP():

    def __init__(self, ip_port):
        self.dep_parser = CoreNLPDependencyParser(url=ip_port)
        self.ner_parser = CoreNLPParser(url=ip_port, tagtype='ner')
        # self.parser = CoreNLPParser(url=ip_port)
        self.pos_tagger = CoreNLPParser(url=ip_port, tagtype='pos')

    def generate_dependency_tree(self, sentence):
        '''what is the name of the asteroid ?'''
        dependency_tree, = self.dep_parser.raw_parse(sentence=sentence)
        return dependency_tree

    def generate_dependency_graph(self, sentence):
        '''12 {'address': 12, 'word': '.', 'lemma': '.', 'ctag': '.', 'tag': '.', 'feats': '', 'head': 1, 'deps': defaultdict(<class 'list'>, {}), 'rel': 'punct'}
        7-tuple, where the values are ``word, lemma, ctag, tag, feats, head, rel``.'''
        dependency_tree, = self.dep_parser.raw_parse(sentence=sentence)
        return DependencyGraph(dependency_tree.to_conll(10))

    # def generate_constituency_tree(self, sentence):
    #     '''input: one question'''
        # tree_list = list(self.parser.raw_parse(sentence=sentence))
        # return tree_list[0]

    def get_pos(self, sentence):
        '''What is the airspeed of an unladen swallow ?
        [('What', 'WP'), ('is', 'VBZ'), ('the', 'DT'), 'airspeed', 'NN'), ('of', 'IN'), ('an', 'DT'), ('unladen', 'JJ'), ('swallow', 'VB'), ('?', '.')]
        '''
        pos_list = list(self.pos_tagger.tag(sentence.split()))
        # tokens = nltk.word_tokenize(sentence)
        # wordpos = nltk.pos_tag(tokens)
        return pos_list

    def get_pos_by_tokens(self, tokens):
        '''What is the airspeed of an unladen swallow ?'''
        pos_list = list(self.pos_tagger.tag(tokens))
        # tokens = nltk.word_tokenize(sentence)
        # wordpos = nltk.pos_tag(tokens)
        return pos_list

    def get_ner(self, sentence):
        # tokens = 'Rami Eid is studying at Stony Brook University in NY'.split()
        '''april the 26th, 1882 is the birth date of which athletes ?
        [('april', 'DATE'), ('the', 'DATE'), ('26th', 'DATE'), (',', 'DATE'), ('1882', 'DATE'),
        ('is', 'O'), ('the', 'O'), ('birth', 'O'), ('date', 'O'), ('of', 'O'), ('which', 'O'),
        ('athletes', 'O'), ('?', 'O')]'''
        sequence_ner_tuple_list = self.ner_parser.tag(sentence.split())
        sequence_ner_list = []
        for i, (word, ner_tag) in enumerate(sequence_ner_tuple_list):
            sequence_ner_list.append(ner_tag)
        return sequence_ner_list

    # def get_toknizer(self, sentence):
    #     return list(self.parser.tokenize(sentence))

    def find_phrases(self, tree, phrase_tag='NP'):
        return [subtree.leaves() for subtree in tree.subtrees(lambda t: t.label()==phrase_tag)]

# sequence = 'what is the name of the asteroid ?'
# sequence = ', ltd.'
# nltk_nlp = NLTK_NLP()
# dg = nltk_nlp.generate_dependency_graph(sequence)
# print(dg.tree())
# print(dg.tree().draw())
# dep_tree = nltk_nlp.generate_dependency_tree(sequence)
# for governor, dep, dependent in dep_tree.triples():
#     print(governor, dep, dependent)
#

# tokens = nltk_nlp.get_toknizer(sentence=sequence)
# print(tokens)
# pos = nltk_nlp.get_pos(sequence)
# print(pos)
# pos = nltk_nlp.get_pos_by_tokens(tokens=tokens)
# print(pos)

# sequence = 'april the 26th, 1882 is the birth date of which athletes ?'
# ner = nltk_nlp.get_ner(sequence)
# print(ner)
#
# tree = nltk_nlp.generate_constituency_tree(sentence=sequence)
# print(tree)
# tree.draw()
# for s in tree.subtrees(lambda t: t.height() == 2):
#     print(s)