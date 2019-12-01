
class Structure():
    '''structure class , it contains: structure property and operation'''

    def __init__(self, qid=None, question=None, words=None, function=None, compositionality_type=None,
                 num_node=None, num_edge=None, span_tree=None,
                 gold_graph_query=None, gold_answer=None, gold_sparql_query=None):
        """Initialize structure"""
        self.qid = qid
        self.question = question
        self.words = words
        self.function = function
        self.compositionality_type = compositionality_type
        self.num_node = num_node
        self.num_edge = num_edge
        self.commonness = 0 # at time, do not use its metric
        self.span_tree = span_tree
        self.ungrounded_graph_forest = []
        # self.grounded_graph_forest = []
        self.gold_graph_query = gold_graph_query
        self.gold_answer = gold_answer
        self.gold_sparql_query = gold_sparql_query

    def get_ungrounded_graph_forest(self):
        return self.ungrounded_graph_forest

    def set_ungrounded_graph_forest(self, ungrounded_graph_forest):
        self.ungrounded_graph_forest.clear()
        self.ungrounded_graph_forest = ungrounded_graph_forest

    def add_ungrounded_graph(self, ungrounded_graph):
        if ungrounded_graph not in self.ungrounded_graph_forest:
            self.ungrounded_graph_forest.append(ungrounded_graph)

    def __str__(self):
        return '{}\t{}'.format(self.qid, self.question)
