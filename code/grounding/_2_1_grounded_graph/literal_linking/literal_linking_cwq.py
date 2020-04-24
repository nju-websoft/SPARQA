from common.globals_args import fn_cwq_file
from datasets_interface import complexwebquestion_interface
from execute_freebase import kb_interface
from common.structure_utils import read_structure_file
from common.hand_files import write_set

qid_to_grounded_graph_dict = complexwebquestion_interface.extract_grounded_graph_from_jena(
    fn_cwq_file.complexwebquestion_test_bgp_dir)

types = ['composition', 'conjunction']
def test_complexwebq_ll_(structure_with_ungrounded_graphq_file, k=1):
    structure_list = read_structure_file(structure_with_ungrounded_graphq_file)
    test_node_type = 'literal'  # class
    recall=0
    question_count = 0

    for i, structure in enumerate(structure_list):
        grounded_graph=qid_to_grounded_graph_dict[structure.qid]
        gold_compositionality_type = complexwebquestion_interface.look_for_compositionality_type_by_id(structure.qid)
        if gold_compositionality_type not in types: continue
        grounded_literal=set()
        for node in grounded_graph.nodes:
            if node.node_type==test_node_type:
                grounded_literal.add(node.id)
        # if len(grounded_literal) == 0: continue
        for ungrounded_graph in structure.get_ungrounded_graph_forest():
            ungrounded_literals=[]
            kbcqa_grounded_linking = ungrounded_graph.grounded_linking
            for ungrounded_node in ungrounded_graph.nodes:
                if str(ungrounded_node.nid) in kbcqa_grounded_linking.keys() and test_node_type == ungrounded_node.node_type:
                    grounding_result = list(kbcqa_grounded_linking[str(ungrounded_node.nid)].keys())
                    mention=ungrounded_node.friendly_name
                    ungrounded_literals.append([mention,grounding_result])

            ungrounded_literals_all = set()
            for mention, grounding_result in ungrounded_literals:
                ungrounded_literals_all |= set(grounding_result[:k])
            if len(ungrounded_literals_all) == 0: continue
            print(structure.qid, structure.question)
            question_count+=1
            if len(grounded_literal)>0:
                recall+=len(ungrounded_literals_all&grounded_literal)/len(grounded_literal)
            else:
                recall+=1

            for ungrounded_literal in ungrounded_literals_all:
                literal_normal = literal_normalization(ungrounded_literal)
                if len(grounded_literal) > 0:
                    print(('%s\t%s\t%s') % (ungrounded_literal, literal_normal, grounded_literal.pop()))
                else:
                    print(('%s\t%s\t%s') % (ungrounded_literal, literal_normal, "wu"))

    print(question_count,recall,recall/question_count)

def gold_structure_literal():
    import utils
    for qid, grounded_graph in qid_to_grounded_graph_dict.items():
        gold_compositionality_type = complexwebquestion_interface.look_for_compositionality_type_by_id(qid)
        if gold_compositionality_type not in types: continue
        grounded_nodes = grounded_graph.nodes
        for edge in grounded_graph.edges:
            if utils.is_literal_node(grounded_nodes, edge.start) \
                or utils.is_literal_node(grounded_nodes, edge.end):
                range_ = kb_interface.get_range(edge.friendly_name)
                if len(range_) == 0: continue
                range_ = range_.pop()
                triple = edge.start+' '+edge.friendly_name +' '+ edge.end
                is_mediator = kb_interface.is_mediator_property_from_schema(edge.friendly_name)
                print (triple, is_mediator)

                # if range_ in literal_range_to_triples_set_dict:
                #     literal_range_to_triples_set_dict[range_].add(triple)
                # else:
                #     triples_set = set()
                #     triples_set.add(triple)
                #     literal_range_to_triples_set_dict[range_] = triples_set

file_literal=fn_cwq_file.grounded_graph_file+'oracle_grounded_graph_test_group_2/literals/'
filter_literal_mention = ['janaury 6  2003',
                          'december 252003', 'february 281991',
                          'july  2  2009', 'march 21954', 'january 201900']
def get_s_p_byliteral(i, literal_value):
    '''获取literal值的s_p'''
    if literal_value in filter_literal_mention: return set()
    s_p = kb_interface.get_s_p_literal_none(literal_value)
    write_set(s_p, file_literal + str(i))
    return s_p

def literal_normalization(literal_value):
    '''normalization
        # if 'http://www.w3.org/2001/XMLSchema#datetime' in literal_value:
        #     literal_normalization_result = literal_value.replace(
        #         'http://www.w3.org/2001/XMLSchema#datetime', 'xsd:dateTime')
        '''
    # rule 1: lower()
    literal_value = literal_value.lower()

    # rule 2: date time
    if 'http://www.w3.org/2001/xmlschema#datetime' in literal_value:
        literal_normalization_result = literal_value.replace(
            '^^http://www.w3.org/2001/xmlschema#datetime', "")
        literal_normalization_result = '"' + literal_normalization_result + '"^^xsd:dateTime'
    elif ',' in literal_value:  # rule 3: big int
        literal_normalization_result = literal_value.replace(',', '')
    else:  # rule 4: string
        literal_normalization_result = '"' + literal_value + '"'

    return literal_normalization_result

if __name__ == '__main__':

    print ('end')
