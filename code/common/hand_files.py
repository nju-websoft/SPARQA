import json
import numpy as np
import mmap
import pickle

from common_structs.ungrounded_graph import UngroundedNode, UngroundedEdge, UngroundedGraph
from common_structs.grounded_graph import GrounedGraph, GroundedNode, GroundedEdge
from common_structs.structure import Structure
from collections import OrderedDict

########################################

def read_structure_file(structure_file):
    '''read structure file'''
    structure_list = read_structure_list_json(read_json(structure_file))
    return structure_list

def read_structure_list_json(structure_list_json):
    '''
    :param structure_list_json:
    :return: structure_list
    '''
    structure_list = []
    for structure_json in structure_list_json:
        structure_list.append(read_structure_json(structure_json))
    return structure_list

def read_structure_json(structure_json):
    '''read structure json file
    :param path_file:
	'''
    structure = Structure(qid=structure_json['qid'],
                              question=structure_json['question'],
                              words=structure_json['words'],
                              function=structure_json['function'],
                              compositionality_type=structure_json['compositionality_type'],
                              num_node=structure_json['num_node'], num_edge=structure_json['num_edge'],
                              span_tree=structure_json['span_tree'],
                              gold_graph_query = read_gold_graph_query(structure_json['gold_graph_query']), #structure_json['gold_graph_query'],
                              gold_answer=structure_json['gold_answer'],
                              gold_sparql_query=structure_json['gold_sparql_query'])
    # add  ungrounded_graph_forest
    for ungrounded_graph_json in structure_json['ungrounded_graph_forest']: #['query_graph_forest']:
        structure.add_ungrounded_graph(read_ungrounded_graph(ungrounded_graph_json))
        '''
        if 'grounded_graph_forest' not in ungrounded_graph_json.keys():
            continue
        # add grounded_graph_forest
        for grounded_graph_json in ungrounded_graph_json['grounded_graph_forest']:
            structure.add_grounded_graph(read_grounded_graph(grounded_graph_json))
        '''
    return structure

def structure_to_json(structure):
    '''write structure json file
    :param output_path_file:
    '''
    out = dict()
    # print(type(structure))
    out['question'] = structure.question  #question_annotation.question_normal
    out['qid'] = structure.qid  #question_annotation.qid
    out['function'] = structure.function  #question_annotation.function
    # out['multiple_relation'] = question_annotation.multiple_relation
    out['compositionality_type'] = structure.compositionality_type  #question_annotation.compositionality_type
    out['num_node'] = structure.num_node  #default
    out['num_edge'] = structure.num_edge  #default
    out['commonness'] = structure.commonness  #default
    out['span_tree'] = str(structure.span_tree)
    out['words'] = structure.words # [(question_annotation.word_list[i], question_annotation.pos_list[i]) for i in range(len(question_annotation.word_list))]
    # out['dependency_tree'] = str(question_annotation.question_dep_parser_tree)
    # out['constituency_tree'] = str(question_annotation.question_parser_tree)
    # out['query_graph_forest'] = []
    out['ungrounded_graph_forest'] = []
    for ungrounded_graph in structure.ungrounded_graph_forest:
        ungrounded_annotation = dict()
        ungrounded_annotation['ungrounded_query_id'] = ungrounded_graph.ungrounded_query_id
        ungrounded_annotation['blag'] = ungrounded_graph.blag
        ungrounded_annotation['nodes'] = ungrounded_graph.nodes
        ungrounded_annotation['edges'] = ungrounded_graph.edges
        ungrounded_annotation['important_words_list'] = ungrounded_graph.important_words_list
        ungrounded_annotation['abstract_question'] = ungrounded_graph.abstract_question
        ungrounded_annotation['sequence_ner_tag_dict'] = ungrounded_graph.sequence_ner_tag_dict
        ungrounded_annotation['grounded_linking'] = ungrounded_graph.grounded_linking
        ungrounded_annotation['grounded_graph_forest'] = ungrounded_graph.grounded_graph_forest
        out['ungrounded_graph_forest'].append(ungrounded_annotation)
    out['gold_graph_query'] = structure.gold_graph_query
    out['gold_answer'] = structure.gold_answer
    out['gold_sparql_query'] = structure.gold_sparql_query
    return out

def read_ungrounded_graph(ungrounded_graph_json):
    '''
        function: read ungrounded_graph data
        :param ungrounded_graph_json: ungrounded_graph json file
        :return: ungrounded_graph structure list
    '''
    ungrounded_query_id = ungrounded_graph_json['ungrounded_query_id']
    blag = ''
    if 'blag' in ungrounded_graph_json.keys():
        blag = ungrounded_graph_json['blag']
    nodes = []
    edges = []
    for node_json in ungrounded_graph_json['nodes']:
        if 'score' in node_json.keys():
            score = node_json['score']
        else:
            score = 0.0
        if 'ordinal' in node_json.keys():
            ordinal = node_json['ordinal']
        else:
            ordinal = "none"
        nodes.append(UngroundedNode(
                          nid=node_json["nid"],
                          node_type=node_json["node_type"],
                          friendly_name=node_json["friendly_name"],
                          question_node=node_json["question_node"],
                          function_str=node_json["function"],
                          score=score,
                          normalization_value=node_json["normalization_value"],
                          type_class=node_json['type_class'],
                          ordinal=ordinal))
    for edge_json in ungrounded_graph_json['edges']:
        if 'score' in edge_json.keys():
            score = edge_json['score']
        else:
            score = 0.0
        edges.append(UngroundedEdge(start=edge_json["start"],
                                    end=edge_json["end"],
                                    friendly_name=edge_json["friendly_name"],
                                    score=score))
    important_words_list = ungrounded_graph_json['important_words_list']
    abstract_question = ungrounded_graph_json['abstract_question']
    sequence_ner_tag_dict = ungrounded_graph_json['sequence_ner_tag_dict']
    grounded_linking = None
    if 'grounded_linking' in ungrounded_graph_json.keys():
        grounded_linking = ungrounded_graph_json['grounded_linking']
    grounded_graph_list = []
    if 'grounded_graph_forest' in ungrounded_graph_json.keys():
        # add grounded_graph_forest
        for grounded_graph_json in ungrounded_graph_json['grounded_graph_forest']:
            grounded_graph_list.append(read_grounded_graph(grounded_graph_json))
    return UngroundedGraph(
        ungrounded_query_id=ungrounded_query_id,
        blag=blag,
        nodes=nodes, edges=edges, important_words_list=important_words_list,
        abstract_question=abstract_question,
        sequence_ner_tag_dict=sequence_ner_tag_dict,
        grounded_linking=grounded_linking,
        grounded_graph_forest=grounded_graph_list)

def read_grounded_graph(grounded_graph_json):
    '''
        function: read grounded_graph data
        :param grounded_graph_json: grounded_graph_json
        :return: grounded_graph structure
        '''
    grounded_query_id = grounded_graph_json['grounded_query_id']
    nodes = []
    edges = []
    if 'nodes' in grounded_graph_json:
        for node_json in grounded_graph_json["nodes"]:
            nodes.append(GroundedNode(
                            nid=node_json["nid"],
                            node_type=node_json["node_type"],
                            id=node_json["id"], type_class=node_json['type_class'],
                            friendly_name=node_json["friendly_name"], question_node=node_json["question_node"], function=node_json["function"],
                            score=node_json['score'],
                            ordinal=node_json['ordinal']))
    if 'edges' in grounded_graph_json:
        for edge_json in grounded_graph_json["edges"]:
            edges.append(GroundedEdge(start=edge_json["start"],
                                        end=edge_json["end"],
                                        relation=edge_json["relation"], friendly_name=edge_json["friendly_name"],
                                        score=edge_json["score"]))

    type = grounded_graph_json['type']
    key_path = grounded_graph_json['key_path']
    sparql_query = grounded_graph_json["sparql_query"]
    score = grounded_graph_json["score"]
    denotation = grounded_graph_json["denotation"]
    total_score = 0.0
    f1_score = 0.0
    if 'total_score' in grounded_graph_json.keys():
        total_score = grounded_graph_json['total_score']
    if 'f1_score' in grounded_graph_json.keys():
        f1_score = grounded_graph_json['f1_score']
    return GrounedGraph(grounded_query_id, type, nodes, edges,
                        key_path=key_path, sparql_query=sparql_query,
                        score=score, denotation=denotation,
                        total_score=total_score, f1_score=f1_score)

def read_gold_graph_query(gold_grounded_graph_json):
    '''
            function: read grounded_graph data
            :param grounded_graph_json: grounded_graph_json
            :return: grounded_graph structure
            '''
    if gold_grounded_graph_json is None: return None
    grounded_query_id = -1
    nodes = []
    edges = []
    for node_json in gold_grounded_graph_json['nodes']:
        type_class = None
        if 'type_class' in node_json.keys():
            type_class = node_json['type_class']
        elif 'class' in node_json.keys():
            type_class = node_json['class']
        nodes.append(GroundedNode(
            nid=node_json["nid"],
            node_type=node_json["node_type"],
            id=node_json["id"], type_class=type_class, #class
            friendly_name=node_json["friendly_name"], question_node=node_json["question_node"],
            function=node_json["function"]))
    for edge_json in gold_grounded_graph_json["edges"]:
        edges.append(GroundedEdge(start=edge_json["start"],
                                  end=edge_json["end"],
                                  relation=edge_json["relation"], friendly_name=edge_json["friendly_name"]))
    type = 'gold'
    # key_path = grounded_graph_json['key_path']
    # sparql_query = grounded_graph_json["sparql_query"]
    # score = grounded_graph_json["score"]
    # denotation = grounded_graph_json["denotation"]
    # total_score = 0.0
    # if 'total_score' in grounded_graph_json.keys():
    #     total_score = grounded_graph_json['total_score']
    return GrounedGraph(grounded_query_id, type, nodes, edges)

def read_lexicon_path(file_path):
    label_to_iris_dict_dict = dict()
    with open(file_path, 'r',encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            cols = line.decode().strip().split('\t')
            if len(cols) == 2:
                label_to_iris_dict_dict[cols[0]] = eval(cols[1])
            line = mm.readline()
    mm.close()
    f.close()
    return label_to_iris_dict_dict

def read_graphs_qid_to_answers_set(filepath):
    '''read answers file'''
    qid_to_answers_dict = dict()
    with open(filepath, 'r', encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            line = line.decode().strip().lower()
            cols = line.split('\t')
            qid = int(cols[0])
            qid_to_answers_dict[qid] = eval(cols[3])  #mid_answers
            line = mm.readline()
    mm.close()
    f.close()
    return qid_to_answers_dict

def read_ordinal_file(filepath):
    ordinal_lines_dict = OrderedDict()
    lines_list = read_list(filepath)
    for line in lines_list:
        terms = line.split(' ')
        index = terms[0]
        ordinal_lines_dict[index] = set(terms[1].split(','))
    # for index, _set in lines_dict.items():
    #     print(index, _set)
    return ordinal_lines_dict

def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r', encoding='utf-8')
    model = {}
    i = 0
    for line in f:
        print (i)
        i += 1
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    return model

def read_ngram_el_grounding_result(filename):
    qid_to_position_grounding_result_dict = {}
    if filename is None or filename == '':
        return qid_to_position_grounding_result_dict

    lines = read_list(filename)
    position_grounding_result_dict = {}
    qid = None
    for line in lines:
        if line[0:5].isdigit():
            terms = line.split(' ')
            qid = int(terms[0])
        elif line.startswith('#ngram'):
            terms = line.split('\t')
            start_position = terms[1]
            end_position = terms[2]
            # grounding_dict = json.loads(terms[3])
            grounding_dict = eval(terms[3])
            # for grounding_entity, pro in grounding_dict.items():
            #     print (grounding_entity, pro)
            position_grounding_result_dict[start_position+'\t'+end_position] = grounding_dict
        elif line == '-----':
            qid_to_position_grounding_result_dict[qid] = position_grounding_result_dict
            position_grounding_result_dict = {}
    # for qid, position_grounding_result_dict in qid_to_position_grounding_result_dict.items():
    #     print (qid, position_grounding_result_dict)
    return qid_to_position_grounding_result_dict

def read_pickle(file_path):
    # 使用load()将数据从文件中序列化读出
    '''
    :param file_path:
    :return: data
    # dataDic = { 0: [1, 2, 3, 4], 2: {'c' :'yes' ,'d' :'no'}}
    # label_to_iris_dict_dict = read_lexicon_path(fn_lcquad_file.pageRedirects_lexicon_path)
    # write_pickle(label_to_iris_dict_dict, './2019.07.20_dbpedia201604_wikiPageRedirects_lexicon.pt')

    dataDic = read_pickle(fn_lcquad_file.pageRedirects_lexicon_path)
    print(type(dataDic))
    for key, value in dataDic.items():
    print(key, value)
    print ('end')
    '''
    fr = open(file_path, 'rb')
    data = pickle.load(fr)
    fr.close()
    return data

def read_json(pathfile):
    with open(pathfile, 'r',encoding="utf-8") as f:
        data = json.load(f)
    f.close()
    return data

def read_set(read_path):
    seta=set()
    with open(read_path, 'r',encoding='utf-8') as f:
        f.fileno()
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            seta.add(line.decode().strip().lower())
            line = mm.readline()
    mm.close()
    f.close()
    return seta

def read_list(read_path):
    seta=list()
    with open(read_path, 'r',encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            seta.append(line.decode().strip().lower())
            line = mm.readline()
    mm.close()
    f.close()
    return seta

def read_list_yuanshi(read_path):
    seta = list()
    with open(read_path, 'r', encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            # seta.append(line.decode().strip())
            # there is a bug.  'utf-8' codec can't decode byte 0xa1 in position 71: invalid start byte
            seta.append(line.decode(errors='ignore').strip())
            # seta.append(line.decode().strip())
            # seta.append(line.decode().strip().lower())
            line = mm.readline()
    mm.close()
    f.close()
    return seta

def read_dict(pathfile):
    diction=dict()
    with open(pathfile, 'r',encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            cols = line.decode().strip().split('\t')
            entity = cols[0].strip()
            del cols[0]
            diction[entity] = cols
            line = mm.readline()
    mm.close()
    f.close()
    return diction

def read_dict_dict(pathfile):
    '''
    poompuhar	en.poombuhar: 0.6887141237907649	en.puhar: 0.8015519227586992	en.puhar: 0.8015519227586992
    '''
    diction = dict()
    with open(pathfile, 'r') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            cols = line.decode().strip().split('\t')
            entity = cols[0]
            del cols[0]
            valdict = dict()
            for col in cols:
                entity_aqqu = col.split(": ")[0]
                prob_aqqu = float(col.split(": ")[1])
                valdict[entity_aqqu] = prob_aqqu
            diction[entity] = valdict
            line = mm.readline()
    mm.close()
    f.close()
    return diction

def read_dict_dict_update(pathfile):
    '''
    auditorium	{'user.yellowbkpk.default_domain.auditorium': 1.0, 'm.03z8j58': 1.0}
    '''
    diction = dict()
    with open(pathfile, 'r') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        line = mm.readline()
        while line:
            cols = line.decode().strip().split('\t')
            entity = cols[0]
            diction[entity] = eval(cols[1])
            line = mm.readline()
    mm.close()
    f.close()
    return diction

################################

def write_set(seta,write_file):
    fi = open(write_file, "w", encoding="utf-8")
    for key in seta:
        fi.write(key)
        fi.write("\n")
    fi.close()

def write_dict(dict,write_file):
    fi = open(write_file, "w", encoding="utf-8")
    # fi.write(str(len(dict)))
    # fi.write("\n")
    for key in dict:
        fi.write(str(key))
        fi.write("\n")
        value = dict[key]
        # fi.write(str(len(value)))
        # fi.write("\n")
        for val in value:
            fi.write(str(val))
            fi.write("\n")
    #    fi.write("\n")
      #  fi.write("\n")
        fi.write("\n")
    fi.close()

def write_dict_dict_str(dict,write_file):
    fi = open(write_file, "w", encoding="utf-8")
    # fi.write(str(len(dict)))
    # fi.write("\n")
    for key in dict:
        fi.write(str(key))
        fi.write("\n")
        value = dict[key]
        #    fi.write(str(len(value)))
        for val in value:
            fi.write( str(val))
            fi.write(":")
            fi.write(str(dict[key][val]))
            fi.write("\t")
        fi.write("\n")
    fi.close()

def write_dict_str(dict,write_file):
    fi = open(write_file, "w", encoding="utf-8")
    for key in dict:
        fi.write(str(key))
        fi.write("\t")
        value = dict[key]
        fi.write(str(value))
        fi.write("\n")
    fi.close()

def write_json(result, pathfile):
    with open(pathfile, 'w', encoding="utf-8") as f:
        json.dump(result, f,indent=4,cls=OtherClassEncoder)
        #print(json.dumps(structure_json, indent=4) + ",")
    f.close()

def write_pickle(object, file_path):
    # 使用dump()将数据序列化到文件中
    '''write object into file'''
    fw = open(file_path, 'wb')
    pickle.dump(object, fw, -1)
    fw.close()

def write_structure_file(structure_list, write_json_pathfile):
    '''write structure file'''
    out_list = []
    for structure in structure_list:
        out = structure_to_json(structure)
        out_list.append(out)
    write_json(out_list, write_json_pathfile)

################################

class OtherClassEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, GrounedGraph):
            node_dict = dict()
            node_dict['grounded_query_id'] = obj.grounded_query_id
            node_dict['type'] = obj.type
            node_dict['nodes'] = obj.nodes #in order to jianshao space, shut down
            node_dict['edges'] = obj.edges #in order to jianshao space, shut down
            node_dict['key_path'] = obj.key_path
            node_dict['sparql_query'] = obj.sparql_query
            node_dict['score'] = obj.score
            node_dict['denotation'] = obj.denotation
            node_dict['total_score'] = obj.total_score
            node_dict['f1_score'] = obj.f1_score
            return node_dict
        elif isinstance(obj,GroundedNode):
            node_dict = dict()
            node_dict["nid"] = obj.nid
            node_dict["node_type"] = obj.node_type
            node_dict["id"] = obj.id
            node_dict["type_class"] = obj.type_class
            node_dict["friendly_name"] = obj.friendly_name
            node_dict["question_node"] = obj.question_node
            node_dict["function"] = obj.function
            node_dict["score"] = obj.score
            node_dict["ordinal"] = obj.ordinal
            return node_dict
        elif isinstance(obj, GroundedEdge):
            edge_dict = dict()
            edge_dict["start"] = obj.start
            edge_dict["end"] = obj.end
            edge_dict["relation"] = obj.relation
            edge_dict["friendly_name"] = obj.friendly_name
            edge_dict["score"] = obj.score
            return edge_dict
        elif isinstance(obj, Structure):
            structure_dict = dict()
            structure_dict["qid"] = obj.qid
            structure_dict["question"] = obj.question
            structure_dict["function"] = obj.function
            structure_dict["compositionality_type"] = obj.compositionality_type
            structure_dict["commonness"] = obj.commonness
            structure_dict["num_node"] = obj.num_node
            structure_dict["num_edge"] = obj.num_edge
            structure_dict["span_tree"] = obj.span_tree
            structure_dict["words"] = obj.words
            # structure_dict["query_graph_forest"] = []
            structure_dict["ungrounded_graph_forest"] = obj.ungrounded_graph_forest
            # structure_dict["grounded_graph_forest"] = obj.grounded_graph_forest
            structure_dict["gold_graph_query"] = obj.gold_graph_query
            structure_dict["gold_answer"] = obj.gold_answer
            structure_dict["gold_sparql_query"] = obj.gold_sparql_query
            return structure_dict
        elif isinstance(obj, UngroundedGraph):
            ungrounded_graph = dict()
            ungrounded_graph["ungrounded_query_id"] = obj.ungrounded_query_id
            ungrounded_graph["blag"] = obj.blag
            ungrounded_graph["nodes"] = obj.nodes
            ungrounded_graph["edges"] = obj.edges
            ungrounded_graph["important_words_list"] = obj.important_words_list
            ungrounded_graph["abstract_question"] = obj.abstract_question
            ungrounded_graph["sequence_ner_tag_dict"] = obj.sequence_ner_tag_dict
            ungrounded_graph["grounded_linking"] = obj.grounded_linking
            ungrounded_graph["grounded_graph_forest"] = obj.grounded_graph_forest
            return ungrounded_graph
        elif isinstance(obj, UngroundedNode):
            ungrounded_node = dict()
            ungrounded_node["nid"] = obj.nid
            ungrounded_node["node_type"] = obj.node_type
            ungrounded_node["friendly_name"] = obj.friendly_name
            ungrounded_node["question_node"] = obj.question_node
            ungrounded_node["function"] = obj.function
            ungrounded_node["score"] = obj.score
            ungrounded_node["normalization_value"] = obj.normalization_value
            ungrounded_node["type_class"] = obj.type_class
            ungrounded_node["ordinal"] = obj.ordinal
            return ungrounded_node
        elif isinstance(obj, UngroundedEdge):
            ungrounded_edge = dict()
            ungrounded_edge["start"] = obj.start
            ungrounded_edge["end"] = obj.end
            ungrounded_edge["friendly_name"] = obj.friendly_name
            ungrounded_edge["score"] = obj.score
            return ungrounded_edge
        else:
            return json.JSONEncoder.default(self, obj)
