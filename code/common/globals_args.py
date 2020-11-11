from common.dataset_name import CWQFileName,GraphqFileName
from common.kb_name import KB_Freebase_Latest, KB_Freebase_en_2013
from argparse import ArgumentParser

root = 'C:/Users/ywsun/Desktop/github_test/SPARQA_dataset/dataset'
q_mode = 'graphq' #cwq graphq
parser_mode = 'head' #head, dep
kb_mode = 'kb_freebase_en_2013' #kb_freebase_latest, kb_freebase_en_2013

def get_args(root):
    parser = ArgumentParser(description="arguments")
    parser.add_argument('--glove_file', type=str, default=root+'/glove.6B.300d.txt')
    parser.add_argument('--ip_port', type=str, default='http://114.212.190.19:9003')
    parser.add_argument('--sutime_jar_files', type=str, default=root + '/resources_sutime/python-sutime-master/jars')
    parser.add_argument('--stopwords_dir', type=str, default=root+'/stopwords.txt')
    parser.add_argument('--ordinal_fengli', type=str, default=root + '/ordinal_fengli.tsv')
    parser.add_argument('--unimportantwords', type=str, default=root + "/unimportantwords")
    parser.add_argument('--unimportantphrases', type=str, default=root + "/unimportantphrases")
    # parser.add_argument('--freebase_pyodbc_info', type=str, default='DSN=freebaselatest;UID=dba;PWD=dba')
    parser.add_argument('--freebase_pyodbc_info', type=str, default='DSN=knowledgebase;UID=dba;PWD=dba')
    parser.add_argument('--freebase_sparql_html_info', type=str, default="http://114.212.86.194:8894/sparql")
    return parser.parse_args()


fn_graph_file = GraphqFileName(root)
fn_cwq_file = CWQFileName(root)
kb_freebase_latest_file = KB_Freebase_Latest(root=root)
kb_freebase_en_2013 = KB_Freebase_en_2013(root=root)
argument_parser = get_args(root)
