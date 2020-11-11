
def grounded_graph_to_key_path(grounded_graph):
    cvttype = ""
    answertype = ""

    for node in grounded_graph.nodes:
        if node.node_type == "class" and node.question_node == 0:
            cvttype = node.id
        elif node.node_type == "class" and node.question_node == 1:
            answertype = node.id

    ps = list()
    for edge in grounded_graph.edges:
        ps.append(edge.relation)

    if len(ps) == 2 and len(cvttype)>0 and len(answertype)>0:
        path = "\t".join([ps[0], cvttype, ps[1], answertype])
    else:
        if len(cvttype)>0:
            ps.append(cvttype)
        ps.append(answertype)
        path = "\t".join(ps)

    return path

def grounded_graph_to_sparql_LcQuAD(grounded_graph):
    nid_nodetype_id_questionnode_function_xid = dict()
    nodexid = 1
    sparql = ''
    for node in grounded_graph.nodes:
        if node.node_type == "class" and node.question_node==1:
            xid = "?x"
            select_sentence = """PREFIX : <http://dbpedia.org/resource/>  SELECT DISTINCT ?x WHERE { """
            sparql += select_sentence
        else:
            xid = "?x"+str(nodexid)
            nodexid += 1

        nodetype_id_questionnode_function_xid = dict()
        nodetype_id_questionnode_function_xid["node_type"] = node.node_type
        nodetype_id_questionnode_function_xid["type_class"] = node.type_class
        nodetype_id_questionnode_function_xid["id"] = node.id
        nodetype_id_questionnode_function_xid["question_node"] = node.question_node
        nodetype_id_questionnode_function_xid["function"] = node.function
        nodetype_id_questionnode_function_xid["xid"] = xid
        nid_nodetype_id_questionnode_function_xid[node.nid] = nodetype_id_questionnode_function_xid

    for nid in nid_nodetype_id_questionnode_function_xid:
        if nid_nodetype_id_questionnode_function_xid[nid]["node_type"]=="entity":
            sparql += "VALUES "+nid_nodetype_id_questionnode_function_xid[nid]["xid"]+" { :"+nid_nodetype_id_questionnode_function_xid[nid]["id"]+" } ."

    edge_sentence=""
    pid = 0
    for edge in grounded_graph.edges:
        if edge.relation is None or edge.relation == '':
            edge_sentence += (nid_nodetype_id_questionnode_function_xid[edge.start]["xid"] + " ?p"+str(pid) +" "+ nid_nodetype_id_questionnode_function_xid[edge.end]["xid"] + " .")
            pid += 1
        else:
            edge_sentence += (nid_nodetype_id_questionnode_function_xid[edge.start]["xid"] + " <" + edge.relation + "> " + nid_nodetype_id_questionnode_function_xid[edge.end]["xid"] + " .")
    sparql += edge_sentence
    sparql+=("}")
    return sparql

def grounded_graph_to_sparql_CWQ(grounded_graph):
    '''
    :param grounded_graph from complexwebquestions
    :return: sparql
    '''
    nid_nodetype_id_questionnode_function_xid = dict()
    nodexid = 1
    sparql = ''
    for node in grounded_graph.nodes:
        if node.node_type == "class" and node.question_node==1:
            xid = "?x"
            # select_sentence = """SELECT DISTINCT ?x WHERE {\nFILTER (!isLiteral(?x) OR lang(?x) = '' OR langMatches(lang(?x), 'en')) \n"""
            select_sentence = """SELECT DISTINCT ?x WHERE {\nFILTER (!isLiteral(?x)) \n"""
            sparql += select_sentence
        else:
            xid = "?x"+str(nodexid)
            nodexid += 1

        nodetype_id_questionnode_function_xid = dict()
        nodetype_id_questionnode_function_xid["node_type"] = node.node_type
        nodetype_id_questionnode_function_xid["type_class"] = node.type_class
        nodetype_id_questionnode_function_xid["id"] = node.id
        nodetype_id_questionnode_function_xid["question_node"] = node.question_node
        nodetype_id_questionnode_function_xid["function"] = node.function
        nodetype_id_questionnode_function_xid["xid"] = xid
        nid_nodetype_id_questionnode_function_xid[node.nid] = nodetype_id_questionnode_function_xid

    for nid in nid_nodetype_id_questionnode_function_xid:
        if nid_nodetype_id_questionnode_function_xid[nid]["node_type"]=="class":
            pass
            # if nid_nodetype_id_questionnode_function_xid[nid]["id"] in wh_words_set:
            #     continue
            # shot down: ?x1 :type.object.type :m.06mt91
            # sparql += nid_nodetype_id_questionnode_function_xid[nid]["xid"]+" :type.object.type :"+ nid_nodetype_id_questionnode_function_xid[nid]["id"]+" .\n"
        elif nid_nodetype_id_questionnode_function_xid[nid]["node_type"]=="entity":
            sparql += "VALUES "+nid_nodetype_id_questionnode_function_xid[nid]["xid"]+" { :"+nid_nodetype_id_questionnode_function_xid[nid]["id"]+" } .\n"

    edge_sentence = ""
    pid = 0
    for edge in grounded_graph.edges:
        if edge.relation is None or edge.relation == '':
            edge_sentence += (nid_nodetype_id_questionnode_function_xid[edge.start]["xid"] + " ?p"+str(pid) +" "+ nid_nodetype_id_questionnode_function_xid[edge.end]["xid"] + " .\n")
            pid += 1
        else:
            edge_sentence += (nid_nodetype_id_questionnode_function_xid[edge.start]["xid"] + " :" + edge.relation + " " + nid_nodetype_id_questionnode_function_xid[edge.end]["xid"] + " .\n")
    sparql += edge_sentence
    sparql+=("}")
    return sparql

def grounded_graph_to_sparql_GraphQ(grounded_graph):
    '''
    :param grounded_graph: from graphquestions
    :return: sparql
    '''
    sparql = ""
    nodexid = 1
    argmax_nid = ""
    argmin_nid = ""
    nid_nodetype_id_questionnode_function_xid = dict()

    for node in grounded_graph.nodes:
        if node.node_type == "class" and node.question_node==1:
            answertype=node.id
            xid= "?x0"
            select_sentence = """SELECT (?x0 AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \n"""
            # print(node.function)
            if node.function=="count":
                select_sentence="""SELECT (COUNT(?x0) AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \n"""
            elif node.function=="none" or node.function is None:
                select_sentence="""SELECT (?x0 AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \n"""
            sparql += select_sentence
        else:
            xid = "?x"+str(nodexid)
            nodexid += 1
        nodetype_id_questionnode_function_xid = dict()
        nodetype_id_questionnode_function_xid["node_type"] = node.node_type
        nodetype_id_questionnode_function_xid["type_class"] = node.type_class
        nodetype_id_questionnode_function_xid["id"] = node.id
        nodetype_id_questionnode_function_xid["question_node"] = node.question_node
        nodetype_id_questionnode_function_xid["function"] = node.function
        nodetype_id_questionnode_function_xid["xid"] = xid
        nid_nodetype_id_questionnode_function_xid[node.nid] = nodetype_id_questionnode_function_xid

    node_sentence = ""
    for nid in nid_nodetype_id_questionnode_function_xid:
        if nid_nodetype_id_questionnode_function_xid[nid]["node_type"]=="class":
            sparql+=nid_nodetype_id_questionnode_function_xid[nid]["xid"]+":type.object.type :"+ nid_nodetype_id_questionnode_function_xid[nid]["id"]+" .\n"
            node_sentence+=nid_nodetype_id_questionnode_function_xid[nid]["xid"]+":type.object.type :"+ nid_nodetype_id_questionnode_function_xid[nid]["id"]+" .\n"

        elif nid_nodetype_id_questionnode_function_xid[nid]["node_type"]=="entity":
            sparql += "VALUES "+nid_nodetype_id_questionnode_function_xid[nid]["xid"]+" { :"+nid_nodetype_id_questionnode_function_xid[nid]["id"]+" } .\n"
            node_sentence += "VALUES "+nid_nodetype_id_questionnode_function_xid[nid]["xid"]+" { :"+nid_nodetype_id_questionnode_function_xid[nid]["id"]+" } .\n"

        elif nid_nodetype_id_questionnode_function_xid[nid]["node_type"] == "literal":
            if nid_nodetype_id_questionnode_function_xid[nid]["type_class"]=="type.datetime":
                id = "'"+nid_nodetype_id_questionnode_function_xid[nid]["id"].split("^^")[0]+"'"+"^^<http://www.w3.org/2001/XMLSchema#datetime>"
            else:
                id=nid_nodetype_id_questionnode_function_xid[nid]["id"].split("^^")[0]
            if nid_nodetype_id_questionnode_function_xid[nid]["function"]=="none":
                sparql += "VALUES " + nid_nodetype_id_questionnode_function_xid[nid]["xid"] + " { " + id + " } .\n"
                node_sentence+="VALUES " + nid_nodetype_id_questionnode_function_xid[nid]["xid"] + " { " + id + " } .\n"

            elif nid_nodetype_id_questionnode_function_xid[nid]["function"]==">=" or \
             nid_nodetype_id_questionnode_function_xid[nid]["function"]=="<=" or \
             nid_nodetype_id_questionnode_function_xid[nid]["function"]=="<" or \
                nid_nodetype_id_questionnode_function_xid[nid]["function"] == ">":
                sparql+="FILTER ( "+nid_nodetype_id_questionnode_function_xid[nid]["xid"]+" "+nid_nodetype_id_questionnode_function_xid[nid]["function"]+" "+id+" ) .\n"
                node_sentence+="FILTER ( "+nid_nodetype_id_questionnode_function_xid[nid]["xid"]+" "+nid_nodetype_id_questionnode_function_xid[nid]["function"]+" "+id+" ) .\n"

            elif nid_nodetype_id_questionnode_function_xid[nid]["function"]=="argmax":
                argmax_nid = nid
            elif nid_nodetype_id_questionnode_function_xid[nid]["function"]=="argmin":
                argmin_nid = nid

    filter_sentences=[]
    nids=list(nid_nodetype_id_questionnode_function_xid.keys())
    for i in range(len(nid_nodetype_id_questionnode_function_xid)):
        for j in range(i+1,len(nid_nodetype_id_questionnode_function_xid)):
            filter_sentences.append(nid_nodetype_id_questionnode_function_xid[nids[i]]["xid"]+" != "+nid_nodetype_id_questionnode_function_xid[nids[j]]["xid"])
    filter_sentence="FILTER ( "+" && ".join(filter_sentences)+ " ) .\n"
    edge_sentence=""
    for edge in grounded_graph.edges:
        edge_sentence += (nid_nodetype_id_questionnode_function_xid[edge.start]["xid"] + " :" + edge.relation + " " +
                          nid_nodetype_id_questionnode_function_xid[edge.end]["xid"] + " .\n")

    if argmax_nid=="" and (argmin_nid)=="":
        sparql+=edge_sentence
    elif (argmax_nid)!="":
        sparql+=("{\n")
        sparql+=("SELECT (MAX("+nid_nodetype_id_questionnode_function_xid[argmax_nid]["xid"].replace("?x","?y")+") AS "+nid_nodetype_id_questionnode_function_xid[argmax_nid]["xid"]+" ) WHERE{\n")
        sparql+=(node_sentence.replace("?x","?y")+edge_sentence.replace("?x","?y"))
        sparql+=(filter_sentence.replace("?x","?y"))
        sparql += ("}\n}\n")
        sparql+=edge_sentence

    elif (argmin_nid)!="":
        sparql += ("{\n")
        sparql += (
        "SELECT (MIN(" + nid_nodetype_id_questionnode_function_xid[argmin_nid]["xid"].replace("?x", "?y") + ") AS " +
        nid_nodetype_id_questionnode_function_xid[argmin_nid]["xid"] + " ) WHERE{\n")
        sparql += (node_sentence.replace("?x", "?y") + edge_sentence.replace("?x", "?y"))
        sparql += (filter_sentence.replace("?x", "?y"))
        sparql += ("}\n}\n")
        sparql += edge_sentence
    sparql+=filter_sentence

    sparql+=("}\n}\n")

    return sparql

def grounded_graph_to_denotation(grounded_graph):
    denotation_set = set()
    if grounded_graph is None: return denotation_set
    for node in grounded_graph.nodes:
        if node.node_type == "class" and node.question_node==1:
            denotation_set.add(node.id)
    return list(denotation_set)

def sparql_to_denotation_freebase(sparqlquery):
    '''sparql_result = list(sparql_to_denotation(gold_sparql))'''
    # from execute_freebase.sparql_query_html import SparqlQueryHTML
    # sparql_query_execute = SparqlQueryHTML()
    # sparql="SELECT (?x0 AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \nVALUES ?x1 { :en.lascaux } .\n?x0:type.object.type :base.biblioness.bibs_location .\n?x1 :base.caveart.cave.region ?x0 .\nFILTER ( ?x1 != ?x0 ) .\n}\n}"
    # denotation_set = sparql_query_execute.execute_sparql(sparqlquery)
    from datasets_interface.virtuoso_interface import freebase_kb_interface
    denotation_set = freebase_kb_interface.execute_sparql(sparqlquery)
    return denotation_set

