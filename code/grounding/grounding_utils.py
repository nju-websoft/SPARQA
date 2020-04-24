from common_structs.graph import Graph
from common_structs.grounded_graph import GrounedGraph
from common_structs.depth_first_paths import DepthFirstPaths
from common_structs.graph import Digragh
from common_structs.cycle import DirectedCycle
import mmap
import torch

def posword_wordlist(posword_list):
    '''get word list of posword'''
    word_list = list()
    for pos_word in posword_list:
        word = pos_word.split("\t")[1].lower()
        word_list.append(word)
    return word_list

def posword_poslist(posword_list):
    '''get pos list of posword'''
    pos_list = list()
    for pos_word in posword_list:
        pos = pos_word.split("\t")[0]
        pos_list.append(pos)
    return pos_list

# >=3
def generate_n_gram_indexrange(wordlist):
    '''get >=3 gram'''
    indexranges = set()
    size = len(wordlist)
    for i in range(0, size):
        for j in range(i + 2, size):
            indexranges.add(str(i) + "\t" + str(j))
    return indexranges

# <=2
def generate_biunigram_indexrange(wordlist):
    '''get <=2 gram'''
    indexranges = set()
    size = len(wordlist)
    for i in range(0, size-1):
        indexranges.add(str(i) + '\t' + str(i))
        indexranges.add(str(i) + "\t" + str(i + 1))
    return indexranges

def merge_dict(dict1, dict2):
    ''''''
    diction =dict()
    for indexrange in dict1:
        if "\t" not in indexrange:
            indexrange_new="\t".join([indexrange,indexrange])
            diction[indexrange_new]=dict1[indexrange]
        else:
            diction[indexrange] = dict1[indexrange]
    for indexrange in dict2:
        if indexrange not in diction:
            if "\t" not in indexrange:
                indexrange_new = "\t".join([indexrange, indexrange])
                diction[indexrange_new] = dict2[indexrange]
            else:
                diction[indexrange] = dict2[indexrange]
    return diction

def get_old_mention(new_mention):
    '''
    old_mention = get_old_mention('Yes we can !')
    All honor 's wounds are self-inflicted		The devil is God 's ape !	's 前者合并
    if ?后缀, 则删除
    El Gouna Beverage Co. Sakara Gold beer is produced	El Gouna Beverage Co . Sakara Gold	与前者合并
    Forgive your enemies, but never forget their names		Forgive your enemies , but never forget their names .	有标点符号的话，都与前者合并
    King : A Filmed Record ... Montgomery to Memphis	King: A Film Record...Montgomery to Memphis
    Columbia Lions men 's basketball team
    Saami , Lule Language
    The future is ... black .		The future is... black.
    The Climb?	?结尾的, 就删掉
    Canzone , S. 162 no. 2		"How did the composer of \"Canzone, S. 162 no. 2\" earn a living?",
    William DeWitt , Jr.	William DeWitt, Jr. is
    Christmas ( 2011 )		Christmas (2011)
    Yes we can !	Yes we can!
    :param new_mention:
    :return: old mention
    '''
    tokens = new_mention.replace('?', '').split(' ')
    old_mention_list = []
    for i, token in enumerate(tokens):
        if token in ['\'s', '.', ',', '...', '!'] and i > 0:
            old_mention_list.pop()
            old_mention_list.append(tokens[i-1]+token)
        else:
            old_mention_list.append(token)
    old_mention = ' '.join(old_mention_list)
    return old_mention

'''sum all four lexicons'''
def add_dict_number(entity_pro_sum, entity_pro_partial):
    '''
    :param entity_pro_sum:
    :param entity_pro_partial:
    :return: entity_pro_sum, sum dict
    '''
    for entity in entity_pro_partial:
        if entity in entity_pro_sum:
            entity_pro_sum[entity] = entity_pro_sum[entity] + entity_pro_partial[entity]
        else:
            entity_pro_sum[entity] = entity_pro_partial[entity]
    return entity_pro_sum

def get_question_node(nodes):
    result = None
    for node in nodes:
        if is_question_node(node):
            result = node
            break
    return result

def is_question_node(node):
    '''check if node is class node'''
    class_list = ["class"]
    if node.node_type in class_list and node.question_node == 1:
        return True
    else:
        return False

def analysis_structure_category(_2_1_graph):
    '''2.1 query graph structure'''
    g = Graph()
    for edge in _2_1_graph.edges:
        g.add_edge(edge.start, edge.end)
    question_node = get_question_node(_2_1_graph.nodes)
    if question_node is None:
        return None, None
    dfp = DepthFirstPaths(g, question_node.nid)
    path_list = []
    for node in _2_1_graph.nodes:
        if node.nid == question_node.nid:
            continue
        if _2_1_graph.get_node_degree(node) > 1:
            continue
        if dfp.has_path_to(node.nid):
            path_to_list = [i for i in dfp.path_to(node.nid)]
            path_list.append(path_to_list)

    category = 'other'  # composition, conjunction
    if len(path_list) == 1:
        if len(path_list[0]) == 2:
            category = "composition-0" #[[1, 2]]
        else:
            category = "composition-1" #[[1, 2, 3, 4]]
    elif len(path_list) == 2:
        category = "conjunction"
    print('#category:\t', category, path_list)  ## composition-1 [[1, 2, 3]]
    return category, path_list


def is_undate_ungrounded_graph_cycle(ungrounded_graph):
    '''破圈操作:  包含e-e或e-l或l-l的圈，要把它们破开。有圈情况:  event型问句,
    比如what were the compositions made by bach in 1749; O并列;  VP 并列; 修饰疑问短语，挂到了动词身上'''
    has_cycle = False
    ungrounded_graph_edges = ungrounded_graph.edges
    di_graph = Digragh()
    for edge in ungrounded_graph_edges:
        di_graph.add_edge(edge.start, edge.end)
        di_graph.add_edge(edge.end, edge.start)
    directed_cycle = DirectedCycle(di_graph)
    if len(directed_cycle.all_cycles) > 0:
        has_cycle = True
    return has_cycle

def read_literal_to_id_map(mode, file_root):
    literal_to_id_dict = dict()
    lines = list()
    with open(file_root+'test_group_2_literal.txt', 'r', encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            lines.append(line.decode().strip())
            line = mm.readline()
    mm.close()
    f.close()
    if mode == 'cwq':
        for i, line in enumerate(lines):
            cols = line.split('\t')
            if cols[1] == 'cuowu': continue
            literal_to_id_dict[cols[0]] = i
            # s_p = get_s_p_byliteral(i, cols[1])
    elif mode == 'graphq':
        #11	1.88	6258
        for i, line in enumerate(lines):
            cols = line.split('\t')
            literal_to_id_dict[cols[1]] = cols[0]
    return literal_to_id_dict

def candidate_query_to_grounded_graph(candidate_graphquerys):
    result = []
    for candidate_graphquery in candidate_graphquerys:
        result.append(
            GrounedGraph(type=candidate_graphquery["querytype"],
                         nodes=candidate_graphquery["nodes"],
                         edges=candidate_graphquery["edges"],
                         key_path=candidate_graphquery["path"],
                         denotation=candidate_graphquery['denotation']))
    return result

def convert_2_1_graph_to_qid_entities(_2_1_graph):
    entities_list = []
    for node in _2_1_graph.nodes:
        if node.node_type == 'entity':
            entities_list.append([node.id, node.node_type])
    return entities_list

def load_word2vec_format(file):
    '''
    print(time.time())
    ab=load_word2vec_format(root+'/glove.6B.300d.txt')
    print(time.time())'''
    matrix=dict()
    with open(file, errors='ignore',encoding='utf8') as f:
        for line in f:
            line = line.rstrip().split(' ')
            word = line[0]
            vector = line[1:]
            col=[]
            for v in vector:
                col.append(float(v))
            matrix[word]=torch.Tensor(col)
    return matrix

def extract_class_mention(node_mention, wh_words_set):
    # 去掉疑问词, 再linking, such as, delete wh-words What type of government -> type of governmet
    node_mention_word_list = node_mention.split(' ')
    node_mention_new_word_list = []
    for node_mention_word in node_mention_word_list:
        if node_mention_word not in wh_words_set:
            node_mention_new_word_list.append(node_mention_word)
    # if len(node_mention_new_word_list) == 0: return dict()
    node_mention = ' '.join(node_mention_new_word_list)
    node_mention = node_mention.replace('type of', '').strip()
    return node_mention

def read_literal_to_id_map_cwq(file_root):
    literal_to_id_dict = dict()
    lines = list()
    with open(file_root + 'test_group_2_literal.txt', 'r', encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            lines.append(line.decode().strip())
            line = mm.readline()
    mm.close()
    f.close()
    for i, line in enumerate(lines):
        cols = line.split('\t')
        if cols[1] == 'cuowu':
            continue
        literal_to_id_dict[cols[0]] = i
        # s_p = get_s_p_byliteral(i, cols[1])
    return literal_to_id_dict


def read_literal_to_id_map_graphq(file_root):
    literal_to_id_dict = dict()
    lines = list()
    with open(file_root+'test_group_2_literal.txt', 'r', encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            lines.append(line.decode().strip())
            line = mm.readline()
    mm.close()
    f.close()
    #11	1.88	6258
    for i, line in enumerate(lines):
        cols = line.split('\t')
        literal_to_id_dict[cols[1]] = cols[0]
    return literal_to_id_dict

