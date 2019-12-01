
class GrounedGraph():
    '''grounded graph structure'''

    def __init__(self,
                 grounded_query_id=-1, type='2_0_1_1',
                 nodes=list(), edges=list(), key_path=None, sparql_query=None,
                 score=0.0, denotation=None, total_score=0.0, f1_score=0.0):
        self.grounded_query_id = grounded_query_id  #ungrounded_query_0001
        self.type = type
        self.nodes = nodes
        self.edges = edges
        self.key_path = key_path
        self.sparql_query = sparql_query
        self.score = score
        self.denotation = denotation
        self.total_score = total_score
        self.f1_score = f1_score

    # def add_score(self, score_):
    #     self.score += score_

    def set_grounded_query_id(self, id):
        self.grounded_query_id = id

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)

    # def del_node(self, node):
    #     if node in self.nodes:
    #         self.nodes.remove(node)

    # def del_node(self, node_nid):
    #     for node in self.nodes[:]:
    #         if node_nid == node.nid:
    #             self.nodes.remove(node)

    # def del_edge(self, edge):
    #     if edge in self.edges:
    #         self.edges.remove(edge)

    # def del_edge(self, start_id, end_id):
    #     for edge in self.edges[:]: # copy
    #         if edge.start == start_id and edge.end == end_id:
    #             self.edges.remove(edge)

    def get_node_degree(self, node):
        degree = 0
        for edge in self.edges:
            if node.nid == edge.start or node.nid == edge.end:
                degree += 1
        return degree

    def get_copy(self):
        new_grounded_graph = GrounedGraph()
        new_grounded_graph.grounded_query_id = self.grounded_query_id
        new_grounded_graph.nodes = [node.get_copy() for node in self.nodes]
        new_grounded_graph.edges = [edge.get_copy() for edge in self.edges]
        new_grounded_graph.type = self.type
        new_grounded_graph.key_path = self.key_path
        new_grounded_graph.sparql_query = self.sparql_query
        new_grounded_graph.denotation = self.denotation
        new_grounded_graph.score = self.score
        new_grounded_graph.total_score = self.total_score
        new_grounded_graph.f1_score = self.f1_score
        return new_grounded_graph

    def __str__(self):
        out = ''
        out += 'GrounedGraphID:'+str(self.grounded_query_id)
        for edge in self.edges:
            out += '\tEdge:\t'+str(edge)
        for node in self.nodes:
            out += '\tNode:\t'+str(node)
        return out

class GroundedNode:
    '''grounded node'''
    def __init__(self, nid=0, based_ungrounded_node_nid=-1, node_type="",
                 type_class="", friendly_name="", question_node=0, function="none", id="", score=0.0, ordinal='none'):
        self.nid = nid
        self.based_ungrounded_node_nid = based_ungrounded_node_nid
        #literal,entity,class
        self.node_type=node_type
        self.id = id
        #int,datetime,cvttype,float,entitytype
        self.type_class=type_class
        self.friendly_name = friendly_name
        self.question_node = question_node
        self.function = function
        self.score = score
        self.ordinal = ordinal

    def set_nid(self,nid):
        self.nid=nid

    def get_copy(self):
        new_grounded_node = GroundedNode()
        new_grounded_node.nid = self.nid
        new_grounded_node.based_ungrounded_node_nid = self.based_ungrounded_node_nid
        #literal,entity,class
        new_grounded_node.node_type= self.node_type
        new_grounded_node.id = self.id
        #int,datetime,cvttype,float,entitytype
        new_grounded_node.type_class= self.type_class
        new_grounded_node.friendly_name = self.friendly_name
        new_grounded_node.question_node = self.question_node
        new_grounded_node.function = self.function
        new_grounded_node.score = self.score
        new_grounded_node.ordinal = self.ordinal
        return new_grounded_node

    def __str__(self):
        print_str = '#grounded node: { nid:' + str(self.nid)
        print_str += ', id:' + str(self.id)
        print_str += ', node_type:' + self.node_type
        print_str += ', score:' + str(self.score)
        print_str += ', question_node:' + str(self.question_node)
        print_str += '}'
        return print_str

    def __eq__(self, other):
        if isinstance(other, GroundedNode):
            return self.id == other.id and self.nid == other.nid
        else:
            return False

class GroundedEdge:

    def __init__(self,start=-1,end=-1,relation='',friendly_name="",score=0.0):
        self.start=start
        self.end=end
        self.relation = relation
        self.friendly_name=friendly_name
        self.score=score

    def get_copy(self):
        new_grounded_edge = GroundedEdge()
        new_grounded_edge.start=self.start
        new_grounded_edge.end=self.end
        new_grounded_edge.relation = self.relation
        new_grounded_edge.friendly_name=self.friendly_name
        new_grounded_edge.score=self.score
        return new_grounded_edge

    def __str__(self):
        print_str = '#grounded edge: { start:' + str(self.start)
        print_str += ', end:' + str(self.end)
        print_str += ', relation:' + self.relation
        print_str += ', friendly_name:' + self.friendly_name
        print_str += ', score:' + str(self.score)
        print_str +=   '}'
        return print_str

    def __eq__(self, other):
        if isinstance(other, GroundedEdge):
            return self.start == other.start and self.end == other.end
        else:
            return False

