from common_structs.grounded_graph import GrounedGraph, GroundedNode, GroundedEdge
from common.hand_files import read_list_yuanshi
from common import utils

def extract_grounded_graph_from_jena_dbpedia(file_path='./2019.07.17_qald_test_bgp.txt'):
    '''
    :argument: file path
    :return qid_to_graphs_dict
    for qid, grounded_graph in qid_to_grounded_graph_dict.items():
        print (qid, grounded_graph)
    '''

    qid_to_graphs_dict = dict()
    lines = read_list_yuanshi(file_path)
    triples_list = []
    nodes_set = []
    qid = None
    question = None
    for line in lines:
        if line.startswith('#Qid'):
            qid = 'train_'+line.split('\t')[2]
            # qid = line.split('\t')[2]
            triples_list = []
            nodes_set = []
        elif line.startswith('#Question'):
            if len(line.split('\t')) == 2:
                question = line.split('\t')[1]
            else:
                question=''
        elif line.startswith('#2.2_triple'):
            triples_list.append(line.split('\t')[1:])
        elif line.startswith('#2.2_node'):
            nodes_set.append(line)
        if line.startswith('-------------------'):
            grounded_nodes = []
            grounded_edges = []
            for node_line in nodes_set:
                cols = node_line.split('\t')
                # node_id = cols[1].replace('http://dbpedia.org/resource/','')
                node_id = cols[1]
                node = GroundedNode(id=node_id, nid=node_id)

                if node.id == '?uri':
                    node.question_node = 1

                if node_id.startswith('http://dbpedia.org/resource/'):
                    node.node_type = 'entity'
                else:
                    node.node_type = 'class'
                # if node_id.startswith('?'):
                #     node.node_type = 'class'
                # elif node_id.startswith('http://dbpedia.org/resource/'):
                #     node.node_type = 'entity'
                # else:
                #     node.node_type = 'class'
                grounded_nodes.append(node)
            for triple in triples_list:
                start_node = utils.get_node_by_id(grounded_nodes, triple[0])
                end_node = utils.get_node_by_id(grounded_nodes, triple[2])
                grounded_edges.append(GroundedEdge(start=start_node.nid, end=end_node.nid, relation=triple[1], friendly_name=triple[1]))
            # qid_to_graphs_dict[qid] = [question,GrounedGraph(nodes=grounded_nodes, edges=grounded_edges)]
            qid_to_graphs_dict[qid] = GrounedGraph(nodes=grounded_nodes, edges=grounded_edges)
    return qid_to_graphs_dict

def extract_grounded_graph_from_jena_freebase(file_path='./2019.04_15_complexwebq_test_bgp.txt'):
    '''
    :argument: file path
    :return qid_to_graphs_dict
    qid_to_grounded_graph_dict = complexwebquestion_interface.extract_grounded_graph_from_jena(globals_args.fn_cwq_file.complexwebquestion_test_bgp_dir)
    for qid, grounded_graph in qid_to_grounded_graph_dict.items():
        print (qid, grounded_graph)
    '''
    qid_to_graphs_dict = dict()
    lines = read_list_yuanshi(file_path)
    triples_list = []
    nodes_set = []
    qid = None
    question = None
    for line in lines:
        if line.startswith('#QID'):
            # qid = line.split('\t')[2]
            qid = 'train_' + line.split('\t')[2]
            triples_list = []
            nodes_set = []
        elif line.startswith('#question'):
            if len(line.split('\t'))==2:
                question = line.split('\t')[1]
            else:
                question=''
        elif line.startswith('#2.2_triple'):
            triples_list.append(line.split('\t')[1:])
        elif line.startswith('#2.2_node'):
            nodes_set.append(line)
        if line.startswith('-------------------'):
            grounded_nodes = []
            grounded_edges = []
            # id = 20
            for node_line in nodes_set:
                # id += 1
                cols = node_line.split('\t')
                node_id = cols[1]
                node = GroundedNode(id=node_id, nid=node_id)
                if node.id == '?x':
                    node.question_node = 1
                if node_id.startswith('?'):
                    node.node_type = 'class'
                elif node_id.startswith('m.') or node_id.startswith('g.') or node_id.startswith('en.'):
                    node.node_type = 'entity'
                else:
                    node.node_type = 'literal'
                if len(cols) == 3:
                    node.friendly_name = eval(cols[2]) #set #2.2_node:	m.03_dwn	{'Lou Seal'}
                elif len(cols) == 4:
                    node.friendly_name = eval(cols[3]) ##2.2_node:	?x	False	{'m.0117q3yz': {'base.type_ontology.abstract', 'common.topic', 'base.type_ontology.inanimate', 'base.type_ontology.non_agent', 'time.event', 'sports.sports_championship_event'}}
                grounded_nodes.append(node)
            for triple in triples_list:
                start_node = utils.get_node_by_id(grounded_nodes, triple[0]) #.replace('http://rdf.freebase.com/ns/','')
                end_node = utils.get_node_by_id(grounded_nodes, triple[2]) #.replace('http://rdf.freebase.com/ns/','')
                if triple[1] == 'common.topic.notable_types':
                    end_node.node_type = 'class'
                    continue
                grounded_edges.append(GroundedEdge(start=start_node.nid, end=end_node.nid, relation=triple[1], friendly_name=triple[1]))
            if len(grounded_nodes)>0:
                qid_to_graphs_dict[qid] = GrounedGraph(nodes=grounded_nodes, edges=grounded_edges)
    return qid_to_graphs_dict
