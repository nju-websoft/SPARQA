import collections
from common_structs.grounded_graph import GroundedNode, GroundedEdge
from grounding import grounding_args

def parser_composition_q_cwq_(data_dict, s1=None,t1=None, constaint=False):
    candidate_graphquery_list = []
    for querytype in data_dict:
        if querytype == "1_0":
            candidate_graphquery_list.extend(_1_0_to_graphs(data_dict['1_0'],s1=s1, t1=t1))
        elif querytype == "1_1":
            candidate_graphquery_list.extend(_1_1_to_graphs(data_dict['1_1'],s1=s1, t1=t1))

        elif querytype == "1_2" and not constaint:
            candidate_graphquery_list.extend(_1_2_to_graphs(data_dict['1_2'],s1=s1, t1=t1))
        # elif querytype == "1_3":
        #     candidate_graphquery_list.extend(_1_3_to_graphs(data_dict['1_3'],s1))
        else:
            print ('Error structure')
    return candidate_graphquery_list

def parser_conjunction_q_cwq_(data_dict, s1=None, s2=None,t1=None,t2=None):
    candidate_graphquery_list = []
    for querytype in data_dict:
        if querytype == "2_0":
            candidate_graphquery_list.extend(_2_0_to_graphs(data_dict['2_0'], s1=s1, s2=s2,t1=t1,t2=t2))
        elif querytype == "2_1":
            candidate_graphquery_list.extend(_2_1_to_graphs(data_dict['2_1'], s1=s1, s2=s2,t1=t1,t2=t2))
        elif querytype == "2_2":
            candidate_graphquery_list.extend(_2_2_to_graphs(data_dict['2_2'], s1=s1, s2=s2,t1=t1,t2=t2))
        # elif querytype == "2_3":
        #     candidate_graphquery_list.extend(_2_3_to_graphs(data_dict['2_3'], s1=s1, s2=s2,t1=t1,t2=t2))
        else:
            print('Error structure')
    return candidate_graphquery_list

######################################

def parser_composition_q_graphq(data_dict, s1=None,t1=None, constaint=False):
    candidate_graphquery_list = []
    for querytype in data_dict:
        if querytype == "1_0":
            candidate_graphquery_list.extend(_1_0_to_graphs(data_dict['1_0'], s1=s1, t1=t1))
        elif querytype == "1_1":
            if constaint:
                candidate_graphquery_list.extend(_1_1_to_graphs(data_dict['1_1'],s1=s1, t1=t1, need_mediator=True))
            else:
                candidate_graphquery_list.extend(_1_1_to_graphs(data_dict['1_1'],s1=s1, t1=t1, need_mediator=False))
        # elif querytype == "1_2" and not constaint:
        #     candidate_graphquery_list.extend(_1_2_to_graphs(data_dict['1_2'],s1=s1, t1=t1))
        # elif querytype == "1_3":
        #     candidate_graphquery_list.extend(_1_3_to_graphs(data_dict['1_3'],s1))
        else:
            print ('Error structure')
    return candidate_graphquery_list

def parser_conjunction_q_graphq(data_dict, s1=None, s2=None,t1=None,t2=None):
    candidate_graphquery_list = []
    for querytype in data_dict:
        if querytype == "2_0":
            candidate_graphquery_list.extend(_2_0_to_graphs(data_dict['2_0'], s1=s1, s2=s2,t1=t1,t2=t2))
        elif querytype == "2_1":
            candidate_graphquery_list.extend(_2_1_to_graphs(data_dict['2_1'], s1=s1, s2=s2,t1=t1,t2=t2))
        elif querytype == "2_2":
            candidate_graphquery_list.extend(_2_2_to_graphs(data_dict['2_2'], s1=s1, s2=s2,t1=t1,t2=t2))
        # elif querytype == "2_3":
        #     candidate_graphquery_list.extend(_2_3_to_graphs(data_dict['2_3'], s1=s1, s2=s2,t1=t1,t2=t2))
        else:
            print('Error structure')
    return candidate_graphquery_list

######################################

def parser_composition_q_lcquad(data_dict, s1=None,t1=None, constaint=False):
    candidate_graphquery_list = []
    for querytype in data_dict:
        #1_0
        if querytype == "1_0":
            candidate_graphquery_list.extend(_1_0_to_graphs(data_dict['1_0'],s1=s1,t1=t1))
        elif querytype == "1_0_b":
            candidate_graphquery_list.extend(_1_0_b_to_graphs(data_dict['1_0_b'],s1=s1,t1=t1))

        #1_1
        elif querytype == "1_1":
            candidate_graphquery_list.extend(_1_1_to_graphs(data_dict['1_1'],s1=s1,t1=t1))
        elif querytype == "1_1_b":
            candidate_graphquery_list.extend(_1_1_b_to_graphs(data_dict['1_1_b'],s1=s1,t1=t1))
        elif querytype == "1_1_c":
            candidate_graphquery_list.extend(_1_1_c_to_graphs(data_dict['1_1_c'],s1=s1,t1=t1))
        elif querytype == "1_1_d":
            candidate_graphquery_list.extend(_1_1_d_to_graphs(data_dict['1_1_d'],s1=s1,t1=t1))

        #1_2
        elif querytype == "1_2" and not constaint:
            candidate_graphquery_list.extend(_1_2_to_graphs(data_dict['1_1'],s1=s1,t1=t1))
        elif querytype == "1_2_b" and not constaint:
            candidate_graphquery_list.extend(_1_2_b_to_graphs(data_dict['1_2_b'],s1=s1,t1=t1))
        elif querytype == "1_2_c" and not constaint:
            candidate_graphquery_list.extend(_1_2_c_to_graphs(data_dict['1_2_c'],s1=s1,t1=t1))
        elif querytype == "1_2_d" and not constaint:
            candidate_graphquery_list.extend(_1_2_d_to_graphs(data_dict['1_2_d'],s1=s1,t1=t1))
        elif querytype == "1_2_e" and not constaint:
            candidate_graphquery_list.extend(_1_2_e_to_graphs(data_dict['1_2_e'],s1=s1,t1=t1))
        elif querytype == "1_2_f" and not constaint:
            candidate_graphquery_list.extend(_1_2_f_to_graphs(data_dict['1_2_f'],s1=s1,t1=t1))
        elif querytype == "1_2_g" and not constaint:
            candidate_graphquery_list.extend(_1_2_g_to_graphs(data_dict['1_2_g'],s1=s1,t1=t1))
        elif querytype == "1_2_h" and not constaint:
            candidate_graphquery_list.extend(_1_2_h_to_graphs(data_dict['1_2_h'],s1=s1,t1=t1))
        else:
            print ('Error structure')
    return candidate_graphquery_list

def parser_conjunction_q_lcquad(data_dict, s1=None, s2=None,t1=None,t2=None):
    candidate_graphquery_list = []
    for querytype in data_dict:
        if querytype == "2_0":
            candidate_graphquery_list.extend(_2_0_to_graphs(data_dict['2_0'], s1=s1, s2=s2,t1=t1,t2=t2))
        elif querytype == "2_0_b":
            candidate_graphquery_list.extend(_2_0_b_to_graphs(data_dict['2_0_b'], s1=s1, s2=s2,t1=t1,t2=t2))
        elif querytype == "2_0_c":
            candidate_graphquery_list.extend(_2_0_c_to_graphs(data_dict['2_0_c'], s1=s1, s2=s2,t1=t1,t2=t2))
        elif querytype == "2_0_d":
            candidate_graphquery_list.extend(_2_0_d_to_graphs(data_dict['2_0_d'], s1=s1, s2=s2,t1=t1,t2=t2))

        elif querytype == "2_1":
            candidate_graphquery_list.extend(_2_1_to_graphs(data_dict['2_1'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_1_b":
            candidate_graphquery_list.extend(_2_1_b_to_graphs(data_dict['2_1_b'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_1_c":
            candidate_graphquery_list.extend(_2_1_c_to_graphs(data_dict['2_1_c'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_1_d":
            candidate_graphquery_list.extend(_2_1_d_to_graphs(data_dict['2_1_d'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_1_e":
            candidate_graphquery_list.extend(_2_1_e_to_graphs(data_dict['2_1_e'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_1_f":
            candidate_graphquery_list.extend(_2_1_f_to_graphs(data_dict['2_1_f'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_1_g":
            candidate_graphquery_list.extend(_2_1_g_to_graphs(data_dict['2_1_g'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_1_h":
            candidate_graphquery_list.extend(_2_1_h_to_graphs(data_dict['2_1_h'], s1=s1, s2=s2, t1=t1, t2=t2))

        elif querytype == "2_2":
            candidate_graphquery_list.extend(_2_2_to_graphs(data_dict['2_2'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_2_b":
            candidate_graphquery_list.extend(_2_2_b_to_graphs(data_dict['2_2_b'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_2_c":
            candidate_graphquery_list.extend(_2_2_c_to_graphs(data_dict['2_2_c'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_2_d":
            candidate_graphquery_list.extend(_2_2_d_to_graphs(data_dict['2_2_d'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_2_e":
            candidate_graphquery_list.extend(_2_2_e_to_graphs(data_dict['2_2_e'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_2_f":
            candidate_graphquery_list.extend(_2_2_f_to_graphs(data_dict['2_2_f'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_2_g":
            candidate_graphquery_list.extend(_2_2_g_to_graphs(data_dict['2_2_g'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "2_2_h":
            candidate_graphquery_list.extend(_2_2_h_to_graphs(data_dict['2_2_h'], s1=s1, s2=s2, t1=t1, t2=t2))

        elif querytype == "3_0":
            candidate_graphquery_list.extend(_3_0_to_graphs(data_dict['3_0'], s1=s1, s2=s2, t1=t1, t2=t2))
        elif querytype == "3_0_b":
            candidate_graphquery_list.extend(_3_0_b_to_graphs(data_dict['3_0_b'], s1=s1, s2=s2, t1=t1, t2=t2))

        else:
            print('Error structure')
    return candidate_graphquery_list

######################################

def _1_0_to_graphs(candidate_pathes, s1, t1):
    '''1_0 	entity-{p}->o	对应, 第1位对应到路径是p, 第二位对应到路径是o
    ns:m.0dhqrm "organization.organization.headquarters\tm.08cshk7'''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid+=1
    node_answer_entity= GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p_answers=collections.defaultdict(set)
    for candidate in candidate_pathes:
        cols = candidate.split("\t")
        if len(cols) != 2:
            continue
        relation, answer_entity = cols
        p_answers[relation].add(answer_entity)

    for p in p_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_0'
        candidate_graphquery["nodes"] = [node_topic_entity, node_answer_entity]

        if t1=='literal': #如果是literal就翻一番
            edge=GroundedEdge(start=node_answer_entity.nid,end=node_topic_entity.nid,relation=p)
        else:
            edge = GroundedEdge(start=node_topic_entity.nid, end=node_answer_entity.nid, relation=p)

        candidate_graphquery["edges"] = [edge]
        candidate_graphquery["path"] = p
        candidate_graphquery["denotation"] = list(p_answers[p])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_0_b_to_graphs(candidate_pathes, s1, t1):
    '''
    s-{p}->entity
     "http://dbpedia.org/resource/Vivian_Kubrick\thttp://dbpedia.org/ontology/parent"  entity	//两个对应,  第1位对应到路径是s, 第二位对应到路径是p.
    :param candidate_pathes:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p_answers = collections.defaultdict(set)
    for candidate in candidate_pathes:
        cols = candidate.split("\t")
        if len(cols) != 2:
            continue
        answer_entity, relation = cols
        p_answers[relation].add(answer_entity)
    for p in p_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_0_b'
        candidate_graphquery["nodes"] = [node_topic_entity, node_answer_entity]
        edge = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity.nid, relation=p)
        candidate_graphquery["edges"] = [edge]
        candidate_graphquery["path"] = p
        candidate_graphquery["denotation"] = list(p_answers[p])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_1_to_graphs(paths, s1, t1, need_mediator=False):
    '''
    e-{p1}->c*-{p2}->a
    "organization.organization.headquarters\tm.08cshk7\tlocation.mailing_address.state_province_region\tm.015jr
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 4: continue
        p1, c_entity, p2, answer_entity = cols
        # filter c entity
        # --------------------------------------
        # webq, graphquestions
        if need_mediator:
            if c_entity in grounding_args.mediators_instances_set: #仅仅考虑mediator
                p1_p2_answers['\t'.join([p1,p2])].add(answer_entity)
        else: # 不考虑need mediator, 所有的都考虑
            p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)
        # --------------------------------------
        # lcquad
        # p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)
    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_1'
        candidate_graphquery["nodes"] = [node_topic_entity, node_c_entity, node_answer_entity]
        p1,p2 = p1_p2.split('\t')
        if t1=='literal':
            edge1 = GroundedEdge(start=node_c_entity.nid, end=node_topic_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity.nid, end=node_c_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_c_entity.nid, end=node_answer_entity.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1, edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_1_b_to_graphs(paths, s1,t1):
    '''
    e->c*<-a 完全对应
    Saraban "http://dbpedia.org/property/distributor\thttp://dbpedia.org/resource/Sony_Pictures_Classics\thttp://dbpedia.org/ontology/distributor\thttp://dbpedia.org/resource/Lambert_&_Stamp"
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)

    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 4:
            continue
        p1, c_entity, p2, answer_entity = cols #完全对应
        p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)
    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_1_b'
        candidate_graphquery["nodes"] = [node_topic_entity, node_c_entity, node_answer_entity]
        p1,p2 = p1_p2.split('\t')
        edge1 = GroundedEdge(start=node_topic_entity.nid, end=node_c_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_c_entity.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1, edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_1_c_to_graphs(paths, s1,t1):
    '''
    e<-{p1}-c*<-{p2}-a
    entity(Stanley_Kubrick) <- "http://dbpedia.org/property/influences\thttp://dbpedia.org/resource/Daniel_Knauf\thttp://dbpedia.org/property/writer\thttp://dbpedia.org/resource/The_Kenyon_Family",
    两个对应, 第1位对应到路径的p1,  第2位对应到路径的c, 第3位对应到路径的p2, 第4位对应路径的a,
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 4:
            continue
        p1, c_entity, p2, answer_entity = cols
        p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)

    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_1_c'
        candidate_graphquery["nodes"] = [node_topic_entity, node_c_entity, node_answer_entity]
        p1, p2 = p1_p2.split('\t')
        edge1 = GroundedEdge(start=node_c_entity.nid, end=node_topic_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_c_entity.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1, edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_1_d_to_graphs(paths, s1,t1):
    '''
    e<-{p1}-c*-{p2}->a
    entity(Stanley_Kubrick) <- "http://dbpedia.org/ontology/director \t http://dbpedia.org/resource/Fear_and_Desire \t http://dbpedia.org/ontology/producer \t http://dbpedia.org/resource/ Stanley_Kubrick"
    两个对应,
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 4:
            continue
        p1, c_entity, p2, answer_entity = cols
        p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)

    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_1_d'
        candidate_graphquery["nodes"] = [node_topic_entity, node_c_entity, node_answer_entity]
        p1,p2 = p1_p2.split('\t')
        edge1 = GroundedEdge(start=node_c_entity.nid, end=node_topic_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_c_entity.nid, end=node_answer_entity.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1,edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

#################################################

def _1_2_to_graphs(paths, s1,t1):
    '''
    #e-{p1}->*1-{p2}->*2-{p3}->a 对应
    Saraband -> "http://dbpedia.org/property/starring\thttp://dbpedia.org/resource/Erland_Josephson\thttp://dbpedia.org/property/spouse\thttp://dbpedia.org/resource/Kristina_Adolphson\thttp://dbpedia.org/property/birthDate\t1937-09-02",
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split('\t')
        if len(cols) != 6:
            continue
        p1, m_entity, p2, c_entity, p3, answer_entity = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)

    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2'
        candidate_graphquery["nodes"] = [node_topic_entity,node_m_entity, node_c_entity, node_answer_entity]
        p1, p2,p3 = p1_p2_p3.split('\t')
        if t1=='literal':
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity.nid, end=node_m_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_c_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_c_entity.nid, end=node_answer_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_2_b_to_graphs(paths, s1, t1):
    '''
    e<-{p1}-*1-{p2}->*2-{p3}->a
    entity(Stanley_Kubrick)    http://dbpedia.org/ontology/influenced\thttp://dbpedia.org/resource/Vladimir_Nabokov    \thttp://dbpedia.org/ontology/spouse    \thttp://dbpedia.org/resource/V\u00e9ra_Nabokov\thttp://purl.org/dc/elements/1.1/description\tEditor, translator
    两个对应.
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)

    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, m_entity, p2, c_entity, p3, answer_entity = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)

    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2_b'
        candidate_graphquery["nodes"] = [node_topic_entity, node_m_entity, node_c_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_c_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_c_entity.nid, end=node_answer_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_2_c_to_graphs(paths, s1, t1):
    '''
    #e<-{p1}-*1m<-{p2}-*2c-{p3}->a
    Massachusetts_Department_of_Transportation http://dbpedia.org/property/owner\thttp://dbpedia.org/resource/Connecticut_River_Line\thttp://dbpedia.org/property/line\thttp://dbpedia.org/resource/Holyoke_station\thttp://dbpedia.org/ontology/numberOfTracks\t1",
    对应
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)

    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, m_entity, p2, c_entity, p3, answer_entity = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)

    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2_c'
        candidate_graphquery["nodes"] = [node_topic_entity, node_m_entity, node_c_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_c_entity.nid, end=node_m_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_c_entity.nid, end=node_answer_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_2_d_to_graphs(paths, s1, t1):
    '''
    #e-{p1}->*1<-{p2}-*2-{p3}->a
    对应
    Massachusetts_Department_of_Transportation http://dbpedia.org/ontology/headquarter\thttp://dbpedia.org/resource/Boston  \t  http://dbpedia.org/ontology/hometown\thttp://dbpedia.org/resource/Hey_Mama_(band)\thttp://dbpedia.org/property/website\thttp://www.heymamamusic.com/",
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 6: continue
        p1, m_entity, p2, c_entity, p3, answer_entity = cols
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2_d'
        candidate_graphquery["nodes"] = [node_topic_entity, node_m_entity, node_c_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        edge1 = GroundedEdge(start=node_topic_entity.nid, end=node_m_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_c_entity.nid, end=node_m_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_c_entity.nid, end=node_answer_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_2_e_to_graphs(paths, s1, t1):
    '''#e-{p1}->*1-{p2}->*2<-{p3}-a
    最后一个triple异常
    Massachusetts_Department_of_Transportation    "http://dbpedia.org/ontology/location\t   ?m http://dbpedia.org/resource/Boston   ?p2\thttp://dbpedia.org/ontology/isPartOf\t
            http://dbpedia.org/resource/Massachusetts\thttp://dbpedia.org/resource/Aaron_Turner\thttp://dbpedia.org/ontology/birthPlace",   //o s p
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, m_entity, p2, c_entity, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2_e'
        candidate_graphquery["nodes"] = [node_topic_entity, node_m_entity, node_c_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        edge1 = GroundedEdge(start=node_topic_entity.nid, end=node_m_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_c_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_c_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_2_f_to_graphs(paths, s1, t1):
    '''
    #e<-{p1}-*1-{p1}->*2<-{p3}-a
    bug
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, m_entity, p2, c_entity, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)

    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2_f'
        candidate_graphquery["nodes"] = [node_topic_entity, node_m_entity, node_c_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_c_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_c_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_2_g_to_graphs(paths, s1, t1):
    '''#e<-{p1}-*1<-{p1}-*2<-{p3}-a
    entity(Stanley_Kubrick) <-http://dbpedia.org/ontology/influenced\thttp://dbpedia.org/resource/Vladimir_Nabokov\thttp://dbpedia.org/ontology/influencedBy\thttp://dbpedia.org/resource/Christopher_Hitchens\thttp://dbpedia.org/resource/Vladimir_Nabokov\thttp://dbpedia.org/property/influenced"
    //最右侧的triple不对应, 倒数第二个是a实体, 倒数第一个是p3
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, m_entity, p2, c_entity, answer_entity, p3  = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2_g'
        candidate_graphquery["nodes"] = [node_topic_entity, node_m_entity, node_c_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_c_entity.nid, end=node_m_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_c_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _1_2_h_to_graphs(paths, s1, t1):
    '''
    #e-{p1}->*1<-{p2}-*2<-{p3}-a
    Massachusetts_Department_of_Transportation        "http://dbpedia.org/property/jurisdiction\thttp://dbpedia.org/resource/Massachusetts
                                    \thttp://dbpedia.org/property/subdivisionName\thttp://dbpedia.org/resource/Woods_Hole,_Massachusetts
                                                        \thttp://dbpedia.org/resource/Selman_Waksman\thttp://dbpedia.org/ontology/residence",
    最右侧的triple不对应, 倒数第二个是a实体, 倒数第一个是p3
    :param paths:
    :param s1:
    :param t1:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_c_entity = GroundedNode(nid=current_nid, node_type="class", id='?c', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, m_entity, p2, c_entity, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)

    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '1_2_h'
        candidate_graphquery["nodes"] = [node_topic_entity, node_m_entity, node_c_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        edge1 = GroundedEdge(start=node_topic_entity.nid, end=node_m_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_c_entity.nid, end=node_m_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_c_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

#################################################

def _2_0_to_graphs(paths, s1, s2,t1,t2):
    '''
    	e1->a<-e2
    	【对应】	比如:	Google_Videos	"http://dbpedia.org/ontology/owner\thttp://dbpedia.org/resource/Google\thttp://dbpedia.org/ontology/author"		Google_Web_Toolkit
    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)
    for candidate in paths:  #merge answers
        p1, answer_entity, p2  = candidate.split("\t")
        p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)
    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_0'
        candidate_graphquery["nodes"] = [node_topic_entity1,node_topic_entity2, node_answer_entity]
        p1, p2 = p1_p2.split('\t')

        if t1=='literal':
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)

        if t2=='literal':
            edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p2)
        else:
            edge2 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1, edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_0_b_to_graphs(paths, s1, s2, t1, t2):
    '''e1<-a->e2
    【对应】	Neil_Brown_(Australian_politician)	 "http://dbpedia.org/property/deputy\thttp://dbpedia.org/resource/John_Howard\thttp://dbpedia.org/property/successor"	Andrew_Peacock'''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 3:
            continue
        p1, answer_entity, p2 = cols
        p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)

    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_0_b'
        candidate_graphquery["nodes"] = [node_topic_entity1,node_topic_entity2, node_answer_entity]
        p1, p2 = p1_p2.split('\t')
        if t1=='literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        if t2=='literal':
            edge2 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p2)
        else:
            edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1, edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_0_c_to_graphs(paths, s1, s2, t1, t2):
    '''e1->a->e2'''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 3:
            continue
        p1, answer_entity, p2 = cols
        p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)

    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_0_c'
        candidate_graphquery["nodes"] = [node_topic_entity1,node_topic_entity2, node_answer_entity]
        p1, p2 = p1_p2.split('\t')
        if t1=='literal':
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        if t2=='literal':
            edge2 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p2)
        else:
            edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1, edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_0_d_to_graphs(paths, s1, s2, t1, t2):
    '''
    	e1<-a<-e2
    	【对应】	Joe_Pass	http://dbpedia.org/ontology/associatedMusicalArtist\thttp://dbpedia.org/resource/Norman_Granz\thttp://dbpedia.org/ontology/producer",	Dream_Dancing_(album)'''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 3:
            continue
        p1, answer_entity, p2 = cols
        p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)

    for p1_p2 in p1_p2_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_0_d'
        candidate_graphquery["nodes"] = [node_topic_entity1,node_topic_entity2, node_answer_entity]
        p1, p2 = p1_p2.split('\t')
        if t1=='literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        if t2=='literal':
            edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p2)
        else:
            edge2 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p2)
        candidate_graphquery["edges"] = [edge1, edge2]
        candidate_graphquery["path"] = p1_p2
        candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

#################################################

def _2_1_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0-{p1}->*1-{p2}->a<-{p3}-e1
    对应】

    比如: e0{Marine_Corps_Air_Station_Kaneohe_Bay} 	http://dbpedia.org/ontology/city\thttp://dbpedia.org/resource/Marine_Corps_Base_Hawaii\thttp://dbpedia.org/ontology/builder\thttp://dbpedia.org/resource/United_States_Navy\thttp://dbpedia.org/property/operator	e1{New_Sanno_Hotel}'''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid +=1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:   #merge answers
        p1, m_entity, p2, answer_entity, p3  = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)

    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')

        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)

        edge2=GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)

        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p3)

        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_1_b_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0<-{p1}-*1-{p2}->a<-{p3}-e1
    对应
    conjunction_entity_Greg_Daniels_entity_The_Office_(U.S._TV_series)
    http://dbpedia.org/property/creator\thttp://dbpedia.org/resource/Parks_and_Recreation\thttp://dbpedia.org/ontology/runtime\t1320.0\thttp://dbpedia.org/property/runtime",
    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="",  question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:  # merge answers
        p1, m_entity, p2, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1_b'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_1_c_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0-{p1}->*1<-{p2}-a<-{p3}-e1
    对应
    conjunction_entity_Greg_Daniels_entity_The_Office_(U.S._TV_series)
    "http://dbpedia.org/ontology/occupation\thttp://dbpedia.org/resource/Screenwriter\t  http://dbpedia.org/ontology/occupation\thttp://dbpedia.org/resource/B._J._Novak\thttp://dbpedia.org/ontology/starring"
    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:  # merge answers
        p1, m_entity, p2, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1_c'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_1_d_to_graphs(paths, s1, s2,t1,t2):
    '''
2_1_d		e0<-{p1}-*1<-{p2}-a<-{p3}-e1
           :param paths:
            :param s1:
            :param s2:
            :param t1:
            :param t2:
            :return:
            '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:  # merge answers
        p1, m_entity, p2, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1_d'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_1_e_to_graphs(paths, s1, s2,t1,t2):
    '''
            e0-{p1}->*1-{p2}->a-{p3}->e1
            【对应】	 conjunction_entity_Neil_Brown_(Australian_politician) http://dbpedia.org/property/successor\thttp://dbpedia.org/resource/Kevin_Andrews_(politician)\thttp://dbpedia.org/property/primeminister\thttp://dbpedia.org/resource/John_Howard\thttp://dbpedia.org/property/successor", _entity_Andrew_Peacock
        '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:  # merge answers
        p1, m_entity, p2, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1_e'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_1_f_to_graphs(paths, s1, s2,t1,t2):
    '''
    对应
    e0<-{p1}-*1-{p2}->?a-{p3}->e1
            "http://dbpedia.org/ontology/influenced\thttp://dbpedia.org/resource/Ralph_Waldo_Emerson\t  http://dbpedia.org/property/influenced\t
                                                    http://dbpedia.org/resource/Henry_David_Thoreau     \thttp://dbpedia.org/ontology/mainInterest",

    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:  # merge answers
        p1, m_entity, p2, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1_f'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_1_g_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0-{p1}->*1<-{p2}-a-{p3}->e1
            【对应】	Google_Videos  http://dbpedia.org/ontology/owner\thttp://dbpedia.org/resource/Google
                \thttp://dbpedia.org/ontology/author\thttp://dbpedia.org/resource/Gerrit_(software)\thttp://dbpedia.org/ontology/programmingLanguage"	Google_Web_Toolkit

    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:  # merge answers
        p1, m_entity, p2, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1_g'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_1_h_to_graphs(paths, s1, s2,t1,t2):
    '''
        e0<-{p1}-*1<-{p2}-a-{p3}->e1
       :param paths:
        :param s1:
        :param s2:
        :param t1:
        :param t2:
        :return:
        '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:  # merge answers
        p1, m_entity, p2, answer_entity, p3 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_1_g'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

#################################################

def _2_2_to_graphs(paths, s1, s2,t1, t2):
    '''e0-{p1}->a<-{p2}-*1<-{p3}-e1
     e0{Sam_Loyd} http://dbpedia.org/property/birthPlace\thttp://dbpedia.org/resource/United_States\t
        http://dbpedia.org/ontology/birthPlace      \thttp://dbpedia.org/resource/New_York_City         \thttp://dbpedia.org/ontology/country",	e1{Eric_Schiller}
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)

        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)

        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_m_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_2_b_to_graphs(paths, s1, s2,t1,t2):
    '''e0-{p1}->a<-{p2}-*1-{p3}->e1

    conjunction_entity_Tommy_Tucker's_Tooth_entity_Walt_Disney
    "http://dbpedia.org/property/producer\thttp://dbpedia.org/resource/Walt_Disney
                    \thttp://dbpedia.org/ontology/child\thttp://dbpedia.org/resource/Flora_Call_Disney\thttp://dbpedia.org/property/children",
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="" , question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2_b'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_2_c_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0-{p1}->a-{p2}->*1<-{p3}-e1
    conjunction_entity_United_States_entity_John_Adams
     "http://dbpedia.org/property/leaderName\thttp://dbpedia.org/resource/Joe_Biden
                \thttp://dbpedia.org/ontology/deathPlace\thttp://dbpedia.org/resource/United_States\thttp://dbpedia.org/ontology/birthPlace",
      :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2_c'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_m_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_2_d_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0-{p1}->a-{p2}->*1-{p3}->e1
    "http://dbpedia.org/ontology/producer\thttp://dbpedia.org/resource/Walt_Disney
        \thttp://dbpedia.org/property/children\thttp://dbpedia.org/resource/Flora_Call_Disney\thttp://dbpedia.org/property/parents",'''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2_d'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_2_e_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0<-{p1}-a<-{p2}-*1<-{p3}-e1
    conjunction_entity_Greg_Daniels_entity_The_Office_(U.S._TV_series)
   "http://dbpedia.org/ontology/developer\thttp://dbpedia.org/resource/The_Office_(U.S._TV_series)\thttp://dbpedia.org/property/starring\thttp://dbpedia.org/resource/Creed_Bratton\thttp://dbpedia.org/ontology/award"

    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2_e'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_m_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_2_f_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0<-{p1}-a<-{p2}-*1-{p3}->e1
    conjunction_entity_Greg_Daniels_entity_The_Office_(U.S._TV_series)
            "http://dbpedia.org/ontology/relative\thttp://dbpedia.org/resource/Paul_Lieberstein
                    \thttp://dbpedia.org/ontology/notableWork\thttp://dbpedia.org/resource/Greg_Daniels\thttp://dbpedia.org/property/relatives",
    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2_f'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m_entity.nid, end=node_answer_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_2_g_to_graphs(paths, s1, s2,t1,t2):
    '''e0<-{p1}-a-{p2}->*1<-{p3}-e1
    	【不对应】	e0{Marine_Corps_Air_Station_Kaneohe_Bay}  	http://dbpedia.org/ontology/garrison\thttp://dbpedia.org/resource/VP-47
    	        \thttp://dbpedia.org/ontology/tenant\thttp://dbpedia.org/resource/United_States_Navy\thttp://dbpedia.org/ontology/militaryBranch", e1{New_Sanno_Hotel}
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="",question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="",  question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2_g'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_topic_entity2.nid, end=node_m_entity.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _2_2_h_to_graphs(paths, s1, s2,t1,t2):
    '''
    e0<-{p1}-a-{p2}->*1-{p3}->e1
        conjunction_entity_Greg_Daniels_entity_The_Office_(U.S._TV_series)

            "http://dbpedia.org/property/creator\thttp://dbpedia.org/resource/Creed_Bratton_(character)\thttp://dbpedia.org/ontology/award\thttp://dbpedia.org/resource/Creed_Bratton\thttp://dbpedia.org/ontology/portrayer",

    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="",  question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="",  question_node=0)
    current_nid += 1
    node_m_entity = GroundedNode(nid=current_nid, node_type="class", id='?m', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_answers = collections.defaultdict(set)
    for candidate in paths:
        p1, answer_entity, p3, m_entity, p2 = candidate.split("\t")
        p1_p2_p3_answers['\t'.join([p1, p2, p3])].add(answer_entity)
    for p1_p2_p3 in p1_p2_p3_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_2_h'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m_entity, node_answer_entity]
        p1, p2, p3 = p1_p2_p3.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
        edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_m_entity.nid, relation=p2)
        if t2 == 'literal':
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        else:
            edge3 = GroundedEdge(start=node_m_entity.nid, end=node_topic_entity2.nid, relation=p3)
        candidate_graphquery["edges"] = [edge1, edge2, edge3]
        candidate_graphquery["path"] = p1_p2_p3
        candidate_graphquery["denotation"] = list(p1_p2_p3_answers[p1_p2_p3])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

#################################################

def _2_3_to_graphs(paths, s1, s2,t1,t2):
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m1_entity = GroundedNode(nid=current_nid, node_type="class", id='?m1', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_m2_entity = GroundedNode(nid=current_nid, node_type="class", id='?m2', type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p1_p2_p3_p4_answers = collections.defaultdict(set)
    for candidate in paths:  #merge answers
        p1, m1_entity, p2, answer_entity, p4, m2_entity, p3 = candidate.split("\t")
        p1_p2_p3_p4_answers['\t'.join([p1, p2, p3, p4])].add(answer_entity)

    for p1_p2_p3_p4 in p1_p2_p3_p4_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '2_3'
        candidate_graphquery["nodes"] = [node_topic_entity1, node_topic_entity2, node_m1_entity,node_m2_entity, node_answer_entity]
        p1, p2, p3,p4 = p1_p2_p3_p4.split('\t')
        if t1 == 'literal':
            edge1 = GroundedEdge(start=node_m1_entity.nid, end=node_topic_entity1.nid, relation=p1)
        else:
            edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_m1_entity.nid, relation=p1)
        edge2 = GroundedEdge(start=node_m1_entity.nid, end=node_answer_entity.nid, relation=p2)
        edge3 = GroundedEdge(start=node_m2_entity.nid, end=node_answer_entity.nid, relation=p3)
        if t2 == 'literal':
            edge4 = GroundedEdge(start=node_m2_entity.nid, end=node_topic_entity2.nid, relation=p4)
        else:
            edge4 = GroundedEdge(start=node_topic_entity2.nid, end=node_m2_entity.nid, relation=p4)
        candidate_graphquery["edges"] = [edge1, edge2, edge3,edge4]
        candidate_graphquery["path"] = p1_p2_p3_p4
        candidate_graphquery["denotation"] = list(p1_p2_p3_p4_answers[p1_p2_p3_p4])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

#################################################

def _3_0_to_graphs(paths, s1, s2,t1,t2):
    '''1_0 	entity-{p}->o	对应, 第1位对应到路径是p, 第二位对应到路径是o
        ns:m.0dhqrm "organization.organization.headquarters\tm.08cshk7'''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 2:
            continue
        relation, answer_entity = cols
        p_answers[relation].add(answer_entity)

    for p in p_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '3_0'
        candidate_graphquery["nodes"] = [node_topic_entity, node_answer_entity]

        if t1 == 'literal':  # 如果是literal就翻一番
            edge = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity.nid, relation=p)
        else:
            edge = GroundedEdge(start=node_topic_entity.nid, end=node_answer_entity.nid, relation=p)

        candidate_graphquery["edges"] = [edge]
        candidate_graphquery["path"] = p
        candidate_graphquery["denotation"] = list(p_answers[p])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

def _3_0_b_to_graphs(paths, s1, s2,t1,t2):
    '''
         s p   "http://dbpedia.org/resource/The_Office_(U.S._TV_series)\thttp://dbpedia.org/ontology/executiveProducer",
    :param paths:
    :param s1:
    :param s2:
    :param t1:
    :param t2:
    :return:
    '''
    candidate_graphquery_list = []
    current_nid = 1
    node_topic_entity = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
    current_nid += 1
    node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
    p_answers = collections.defaultdict(set)
    for candidate in paths:
        cols = candidate.split("\t")
        if len(cols) != 2:
            continue
        answer_entity, relation = cols
        p_answers[relation].add(answer_entity)
    for p in p_answers:
        candidate_graphquery = dict()
        candidate_graphquery["querytype"] = '3_0_b'
        candidate_graphquery["nodes"] = [node_topic_entity, node_answer_entity]
        edge = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity.nid, relation=p)
        candidate_graphquery["edges"] = [edge]
        candidate_graphquery["path"] = p
        candidate_graphquery["denotation"] = list(p_answers[p])
        candidate_graphquery_list.append(candidate_graphquery)
    return candidate_graphquery_list

#################################################

# def _2_0_a_to_graphs(paths, s1, s2, t1, t2):
#     candidate_graphquery_list = []
#     current_nid = 1
#     node_topic_entity1 = GroundedNode(nid=current_nid, node_type=t1, id=s1, type_class='', friendly_name="", question_node=0)
#     current_nid += 1
#     node_topic_entity2 = GroundedNode(nid=current_nid, node_type=t2, id=s2, type_class='', friendly_name="", question_node=0)
#     current_nid += 1
#     node_answer_entity = GroundedNode(nid=current_nid, node_type="class", id='?a', type_class='', friendly_name="", question_node=1)
#     p1_p2_answers = collections.defaultdict(set)
#     for candidate in paths:
#         cols = candidate.split("\t")
#         if len(cols) != 3: continue
#         p1, answer_entity, p2 = cols
#         p1_p2_answers['\t'.join([p1, p2])].add(answer_entity)
#
#     for p1_p2 in p1_p2_answers:
#         candidate_graphquery = dict()
#         candidate_graphquery["querytype"] = '2_0_a'
#         candidate_graphquery["nodes"] = [node_topic_entity1,node_topic_entity2, node_answer_entity]
#         p1, p2 = p1_p2.split('\t')
#         if t1=='literal':
#             edge1 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity1.nid, relation=p1)
#         else:
#             edge1 = GroundedEdge(start=node_topic_entity1.nid, end=node_answer_entity.nid, relation=p1)
#         if t2=='literal':
#             edge2 = GroundedEdge(start=node_answer_entity.nid, end=node_topic_entity2.nid, relation=p2)
#         else:
#             edge2 = GroundedEdge(start=node_topic_entity2.nid, end=node_answer_entity.nid, relation=p2)
#         candidate_graphquery["edges"] = [edge1, edge2]
#         candidate_graphquery["path"] = p1_p2
#         candidate_graphquery["denotation"] = list(p1_p2_answers[p1_p2])
#         candidate_graphquery_list.append(candidate_graphquery)
#     return candidate_graphquery_list
