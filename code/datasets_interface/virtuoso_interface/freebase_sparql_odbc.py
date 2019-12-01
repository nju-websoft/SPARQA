import pyodbc
import time

from grounding.grounding_args import freebase_relations
from common.globals_args import argument_parser

class SparqlQueryODBC():

    def __init__(self):
        # self.freebase_sparql = pyodbc.connect('DSN=knowledgebase;UID=dba;PWD=dba')
        # self.freebase_sparql = pyodbc.connect('DSN=freebaselatest;UID=dba;PWD=dba', ansi=True, autocommit=True)
        # self.freebase_sparql = pyodbc.connect('DSN=freebaselatest;UID=dba;PWD=dba', ansi=True, autocommit=True, timeout=500000)
        # self.freebase_sparql = pyodbc.connect('DSN=freebaselatest;UID=dba;PWD=dba', ansi=True, autocommit=True, timeout=500000)
        self.freebase_sparql = pyodbc.connect(argument_parser.freebase_pyodbc_info, ansi=True, autocommit=True, timeout=500000)
        # self.freebase_sparql = pyodbc.connect(pyodbc_info, ansi=True, autocommit=True, timeout=500000)
        self.freebase_sparql.setdecoding(pyodbc.SQL_CHAR, encoding='utf8')
        self.freebase_sparql.setdecoding(pyodbc.SQL_WCHAR, encoding='utf8')
        self.freebase_sparql.setencoding(encoding='utf8')
        # self.freebase_sparql.timeout = 1
        self.freebase_prefix = "http://rdf.freebase.com/ns/"
        self.prefix = "sparql PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> " \
                      "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> " \
                      "PREFIX : <http://rdf.freebase.com/ns/> "
        # self.freebase_sparql.close()
        # self.freebase_relations = read_set(fn.freebase_relations_file)
        # self.freebase_types = read_set(fn.freebase_types_file)

    def return_str_not_something(self,variable):
        '''filter'''
        return "FILTER ("+variable+"!= :type.object.type) .\n FILTER ("+variable+"!= :common.topic.notable_types) ."

    def filter_relation(self, relation):
        if self.freebase_prefix not in relation:
            return False
        a = relation.replace(self.freebase_prefix, "")
        if a.startswith("m.") or a.startswith("en.") \
                or a.startswith("type.") or a.startswith("common.") or a.startswith("freebase."):
            return False
        if a not in freebase_relations:
            return False
        return a

    def filter_entity(self, entity):
        if entity:
            if self.freebase_prefix not in entity:
                return False
            a = entity.replace(self.freebase_prefix, "")
            if a.startswith("m.") or a.startswith("en.") or a.startswith("g."):
                return a
            else:
                return False
        else:
            return False

    def get_p_o(self, s):
        '''获取s, 出边信息
        :return p_o_set, o_set, p_set
        '''
        p_o_set = set()
        o_set = set()
        p_set = set()
        results = self.freebase_sparql.execute(self.prefix + """
                       SELECT DISTINCT ?p ?o  WHERE { 
                       """ + self.return_str_not_something("?p")
                        + """{:""" + s + """ ?p ?o . }}""")
        for result in results:
            p = result[0]
            o = result[1]
            p = self.filter_relation(p)
            o = self.filter_entity(o)
            # if self.freebase_prefix in p: p = p.replace(self.freebase_prefix, "")
            # if self.freebase_prefix in o: o = o.replace(self.freebase_prefix, "")
            # if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in p: continue
            # if True:
            if p and o:
                # print(p)
                p_o_set.add("\t".join([p, o]))
                p_set.add(p)
                o_set.add(o)
        return p_o_set, o_set, p_set

    def get_s_p(self, o):
        '''获得o 的入边信息
        :return s_p_set, s_set, p_set'''
        s_p_set = set()
        s_set = set()
        p_set = set()
        results = self.freebase_sparql.execute(self.prefix + """
                       SELECT DISTINCT ?s ?p  WHERE { """
                                               + self.return_str_not_something("?p") + """
                                               {?s  ?p :""" + o + """ . }}""")
        for result in results:
            # print(result)
            s = result[0]
            p = result[1]
            s = self.filter_entity(s)
            p = self.filter_relation(p)
            # print (s, p)
            if s and p:
                # print(p)
                s_p_set.add("\t".join([s, p]))
                s_set.add(s)
                p_set.add(p)
        return s_p_set, s_set, p_set

    def get_s_p_literal_none(self, literal):
        '''读取literal的入边信息
        :return s_p_set
        '''
        # print('#literal:\t', literal)
        s_p_set = set()
        results = self.freebase_sparql.execute(self.prefix + """ 
                    SELECT DISTINCT ?s ?p  WHERE { 
                    VALUES ?x1 { """ + literal + """ } . ?s ?p ?x1 . } """) #limit 100000
        i = 0
        j = 0
        for result in results:
            if i < 10000:
                i += 1
            else:
                j += 1
                i = 0
                # print(j)
                # print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
            s = result[0]
            p = result[1]
            s = self.filter_entity(s)
            p = self.filter_relation(p)
            if s and p:
                s_p_set.add("\t".join([s, p]))
        return s_p_set

    def get_s_p_literal_function(self, literal, function, literaltype):
        ''':return s_p_set'''
        print('#literl:\t', literal, '#function:\t', function, '#literaltype:\t', literaltype)
        if function is None:
            function = ''
        s_p_set = set()
        if literaltype is None:
            results = self.freebase_sparql.execute(self.prefix + """
                                   SELECT DISTINCT ?s ?p  WHERE { 
                                   FILTER (?x1 """ + function + literal + """ ) .
                                   ?s ?p ?x1 .} limit 100000""")
        else:
            results = self.freebase_sparql.execute(self.prefix + """
                       SELECT DISTINCT ?s ?p  WHERE { 
                       FILTER (?x1 """ + function + literal + """ ) .
                       ?p :type.property.expected_type :""" + literaltype + """ . ?s ?p ?x1 .} limit 100000""")
        i = 0
        j = 0
        for result in results:
            if i < 10000:
                i += 1
            else:
                j += 1
                i = 0
                print(j)
                print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
            # print(result)
            s = result[0]
            p = result[1]
            s = self.filter_entity(s)
            p = self.filter_relation(p)
            if s and p:
                s_p_set.add("\t".join([s, p]))
        return s_p_set

    def get_entity_bytype(self,type):
        '''get entities of type'''
        print(type)
        results = self.freebase_sparql.execute(self.prefix + """
                                                      SELECT DISTINCT ?s  WHERE {
                                                       ?s :type.object.type :"""+type+""" .
                                                      }""")
        entitys = set()
        for result in results:
            entity = self.filter_entity(result[0])
            if entity:
                entitys.add(entity)
        return entitys

    def execute_sparql(self, sparqlquery):
        results = self.freebase_sparql.execute(self.prefix+sparqlquery)
        answers=set()
        for result in results:
            # print(type(result[0]))
            # if type(result[0])==type(2):
            if isinstance(result[0], str) and self.freebase_prefix in result[0]:
                answers.add(result[0].replace(self.freebase_prefix, ""))
            else:
                answers.add(result[0])
            # if isinstance(result[0], int):
            #     answers.add(result[0])
            # else:
            #     if self.freebase_prefix in result[0]:
            #         answers.add(result[0].replace(self.freebase_prefix, ""))
            #     else:
            #         answers.add(result[0])
                # entity=self.filter_entity(result[0])
                # answers.add(entity)
                # print(answers)
            # if isinstance(result[0], str):
            #     answers.add(result[0].replace(self.freebase_prefix, ""))
            # else:
            #     answers.add(result[0])
        return answers

    def execute_sparql_two_args(self, sparqlquery):
        '''return two args'''
        results = self.freebase_sparql.execute(self.prefix+sparqlquery)
        for result in results:
            instance = result[0]
            if isinstance(instance, str) and self.freebase_prefix in instance:
                instance = instance.replace(self.freebase_prefix, "")
        # print(('%s\t%s') % (instance_str, '\t'.join(answers)))
            class_str = result[1]
            if isinstance(class_str, str) and self.freebase_prefix in class_str:
                class_str = class_str.replace(self.freebase_prefix, "")
            print(('%s\t%s')%(instance, class_str))

    def execute_sparql_three_args(self, sparqlquery):
        '''return three args'''
        results = self.freebase_sparql.execute(self.prefix+sparqlquery)
        for result in results:
            instance = result[0]
            if isinstance(instance, str) and self.freebase_prefix in instance:
                instance = instance.replace(self.freebase_prefix, "")
        # print(('%s\t%s') % (instance_str, '\t'.join(answers)))
            p_str = result[1]
            if isinstance(p_str, str) and self.freebase_prefix in p_str:
                p_str = p_str.replace(self.freebase_prefix, "")
            o_str = result[2]
            if isinstance(o_str, str) and self.freebase_prefix in o_str:
                o_str = o_str.replace(self.freebase_prefix, "")
            print(('%s\t%s\t%s')%(instance, p_str, o_str))

    def execute_sparql_five_arg(self, sparqlquery):
        results = self.freebase_sparql.execute(self.prefix+sparqlquery)
        for result in results:
            s1 = result[0]
            if isinstance(s1, str) and self.freebase_prefix in s1:
                s1 = s1.replace(self.freebase_prefix, "")
            p1 = result[1]
            if isinstance(p1, str) and self.freebase_prefix in p1:
                p1 = p1.replace(self.freebase_prefix, "")
            o1 = result[2]
            if isinstance(o1, str) and self.freebase_prefix in o1:
                o1 = o1.replace(self.freebase_prefix, "")
            p2 = result[3]
            if isinstance(p2, str) and self.freebase_prefix in p2:
                p2 = p2.replace(self.freebase_prefix, "")
            o2 = result[4]
            if isinstance(o2, str) and self.freebase_prefix in o2:
                o2 = o2.replace(self.freebase_prefix, "")
            print (('%s\t%s\t%s\t%s\t%s')%(s1, p1, o1, p2, o2))

    def get_names(self, entity):
        # sparqlquery="""SELECT DISTINCT ?name  WHERE {
        #         VALUES ?x0 { :""" + entity + """ } .
        #          {?x0 :type.object.name ?name .}
        #          UNION
        #          {?x0 :common.topic.alias ?name}
        #     }"""
        sparqlquery="""SELECT DISTINCT ?name  WHERE {
                VALUES ?x0 { :""" + entity + """ } .
                ?x0 :type.object.name ?name .
                FILTER (langMatches(lang(?name), 'en')).
            }"""
        results = self.freebase_sparql.execute(self.prefix + sparqlquery)
        answers = set()
        for result in results:
            answers.add(result[0])
        return answers

    def get_alias_names(self, entity):
        sparqlquery="""SELECT DISTINCT ?name  WHERE {
                VALUES ?x0 { :""" + entity + """ } .
                ?x0 :common.topic.alias ?name .
                FILTER (langMatches(lang(?name), 'en')).
            }"""
        results = self.freebase_sparql.execute(self.prefix + sparqlquery)
        answers = set()
        for result in results:
            answers.add(result[0])
        return answers
