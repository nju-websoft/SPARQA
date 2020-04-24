
class UngroundedGraph():
    '''ungrounded graph structure'''
    def __init__(self,
                 ungrounded_query_id=1,
                 blag=None,
                 nodes=list(),
                 edges=list(),
                 important_words_list=list(),
                 abstract_question=None,
                 grounded_linking=None,
                 grounded_graph_forest=None,
                 sequence_ner_tag_dict=None):
        self.ungrounded_query_id = ungrounded_query_id
        self.blag = blag  # str: super; merge_qc , adjust_ec; del_cycle
        self.nodes = nodes
        self.edges = edges
        self.important_words_list = important_words_list
        self.abstract_question=abstract_question
        self.sequence_ner_tag_dict = sequence_ner_tag_dict
        self.grounded_linking = grounded_linking
        self.grounded_graph_forest = grounded_graph_forest

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges = edge

    def get_node_degree(self, node):
        degree = 0
        for edge in self.edges:
            if node.nid == edge.start or node.nid == edge.end:
                degree += 1
        return degree

    def set_grounded_graph_forest(self, grounded_graph_forest):
        # self.grounded_graph_forest.clear()
        self.grounded_graph_forest = grounded_graph_forest

    def get_grounded_graph_forest(self):
        return self.grounded_graph_forest

    def set_grounded_linking(self, grounding_result_list):
        '''
        grounding_result_list:{
        "nid": 4,
        "node_type": "class",
        "friendly_name": "which block",
        "question_node": 1,
        "function": "none",
        "score": 1.0,
        "normalization_value": null
        }, { "base.mtgbase.magic_block": 1.0}
        '''
        nid_to_grounding_result = dict()
        for index, (node, grounding_result) in enumerate(grounding_result_list):
            nid_to_grounding_result[node.nid] = grounding_result
        self.grounded_linking = nid_to_grounding_result

    def get_grounded_linking(self):
        return self.grounded_linking

    def set_blag(self, blag):
        self.blag = blag

class UngroundedNode:
    '''node of graphquestions graph query'''
    def __init__(self, nid='0', node_type='entity', friendly_name='', question_node=0,
                 function_str='none', score=0.0, start_position=-1,
                 end_position=-1, normalization_value=None, type_class=None, ordinal='none'):
        self.nid = nid
        self.node_type = node_type
        self.friendly_name = friendly_name
        self.question_node = question_node
        self.function = function_str
        self.score = score
        self.start_position = start_position
        self.end_position = end_position
        self.normalization_value = normalization_value
        self.type_class = type_class
        self.ordinal = ordinal

    def __str__(self):
        print_str = '#ungrounded node: { nid:' + str(self.nid)
        print_str += ', node_type:' + str(self.node_type)
        print_str += ', friendly_name:' + str(self.friendly_name)
        print_str += ', question_node:' + str(self.question_node)
        print_str += ', function:' + str(self.function)
        print_str += ', ordinal:' + str(self.ordinal)
        print_str += ', score:' + str(self.score)
        print_str += ', start:' + str(self.start_position)
        print_str += ', end:' + str(self.end_position)
        print_str += ', normalization_value:' + str(self.normalization_value)
        print_str += ', type_class:' + str(self.type_class)
        print_str += '}'
        return print_str

    def __eq__(self, other):
        return self.nid == other.nid \
               and self.node_type == other.node_type \
               and self.friendly_name == other.friendly_name \
               and self.question_node == other.question_node \
               and self.function == other.function \
               and self.score == other.score \
               and self.start_position == other.start_position \
               and self.end_position == other.end_position \
               and self.normalization_value == other.normalization_value \
               and self.type_class == other.type_class \
               and self.ordinal == other.ordinal

class UngroundedEdge:
    '''edge of graphquestion graph query '''
    def __init__(self, start=-1, end=-1, friendly_name='ungrounded_edge', score=0.0):
        self.start = start
        self.end = end
        self.friendly_name = friendly_name
        self.score = score

    def __str__(self):
        print_str = '#ungrounded edge: { start:' + str(self.start)
        print_str += ', end:' + str(self.end)
        print_str += ', friendly_name:' + self.friendly_name
        print_str += ', score:' + str(self.score)
        print_str +=   '}'
        return print_str

