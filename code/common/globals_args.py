from common.dataset_name import CWQFileName,GraphqFileName
from common.kb_name import KB_Freebase_Latest, KB_Freebase_en_2013
from argparse import ArgumentParser

root = 'D:/dataset'
q_mode = 'graphq' #cwq graphq
parser_mode = 'head' #joint, head, dep
kb_mode = 'kb_freebase_latest' #kb_freebase_latest, kb_freebase_en_2013

def get_args(root):
    parser = ArgumentParser(description="arguments")
    parser.add_argument('--is_span_tree', type=bool, default=True) #is_span_tree = True #True False
    parser.add_argument('--sutime_jar_files', type=str, default=root + '/resources_sutime/python-sutime-master/jars')
    parser.add_argument('--stopwords_dir', type=str, default=root+'/stopwords.txt') # self.stopwords_file = self.root + "stopwords.txt"
    # parser.add_argument('--output', type=str, default=root + '/output/')
    parser.add_argument('--ordinal_fengli', type=str, default=root + '/ordinal_fengli.tsv')
    parser.add_argument('--unimportantwords', type=str, default=root + "/unimportantwords")
    parser.add_argument('--unimportantphrases', type=str, default=root + "/unimportantphrases")
    parser.add_argument('--glove_file', type=str, default=root+'/glove.6B.300d.txt')

    # parser.add_argument('--ip_port', type=str, default='http://114.212.84.164:9000')
    parser.add_argument('--ip_port', type=str, default='http://114.212.86.243:9000')
    # parser.add_argument('--ip_port', type=str, default='http://114.212.86.243:9003')

    parser.add_argument('--freebase_pyodbc_info', type=str, default='DSN=freebaselatest;UID=dba;PWD=dba') #'DSN=knowledgebase;' 'DSN=Local Virtuoso;'
    parser.add_argument('--freebase_sparql_html_info', type=str, default="http://114.212.86.194:8894/sparql") #http://114.212.86.243:8894/sparql

    parser.add_argument('--dbpedia_pyodbc_info', type=str, default='DSN=llzhang;UID=dba;PWD=dba') #'DSN=knowledgebase;' 'DSN=Local Virtuoso;'
    parser.add_argument('--dbpedia_sparql_html_info', type=str, default="http://114.212.81.113:8890/sparql") #http://114.212.86.243:8894/sparql
    # parser.add_argument('--dbpedia_pyodbc_info', type=str, default='DSN=knowledgebase;UID=dba;PWD=dba') #'DSN=knowledgebase;' 'DSN=Local Virtuoso;'
    # parser.add_argument('--dbpedia_sparql_html_info', type=str, default="http://114.212.84.164:8890/sparql") #http://114.212.86.243:8894/sparql

    # parser.add_argument('--mode', type=str, default='lcquad')
    # parser.add_argument('--nl_num', type=int, default=10)
    # parser.add_argument('--superlative_fengli', type=str, default=root + '/superlative_fengli.tsv')
    # parser.add_argument('--cl_threshold', type=float, default=0.1)
    # parser.add_argument('--operation', help='select which modules runs, candidates:"1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "3.0"', type=str, default='2.3')
    return parser.parse_args()

fn_graph_file = GraphqFileName(root)
fn_cwq_file = CWQFileName(root)

kb_freebase_latest_file = KB_Freebase_Latest(root=root)
kb_freebase_en_2013 = KB_Freebase_en_2013(root=root)

argument_parser = get_args(root)

