from common.bert_args import BertArgs
from sutime import SUTime
from parsing.nltk_nlp_utils import NLTK_NLP
from common import globals_args
from common import hand_files

parser_mode = globals_args.parser_mode
wh_words_set = {"what", "which", "whom", "who", "when", "where", "why", "how", "how many", "how large", "how big"}
bert_args = BertArgs(globals_args.root, globals_args.q_mode)
nltk_nlp = NLTK_NLP(globals_args.argument_parser.ip_port)
sutime = SUTime(jars=globals_args.argument_parser.sutime_jar_files, mark_time_ranges=True)
unimportantwords = hand_files.read_set(globals_args.argument_parser.unimportantwords)
unimportantphrases = hand_files.read_list(globals_args.argument_parser.unimportantphrases)
stopwords_dict = hand_files.read_set(globals_args.argument_parser.stopwords_dir)
ordinal_lines_dict = hand_files.read_ordinal_file(globals_args.argument_parser.ordinal_fengli)  #2 {'second', '2ndis_equal_wh_word'}

count_phrases = ['Count', 'How many', 'how many', 'the number of', 'the count of', 'the amount of', 'total number of', 'count']
count_ner_tags = ['count']
dayu_phrases = ['more', 'more than' ,'greater', 'higher', 'longer than', 'taller than'] #'over',
dayu_dengyu_phrases = ['at least', 'not less than', 'or more']
# dengyu_phrases = ['equal', 'same']
xiaoyu_phrases = ['earlier', 'less than', 'smaller', 'less', 'no higher than', 'fewer', 'fewer than']
xiaoyu_dengyu_phrases = ['at most', 'maximum', 'or less', 'no larger than']
comparative_ner_tags = ['>', '>=', '<', '<=']
argmin_phrases = ['smallest', 'least', 'weakest', 'minimum', 'minimal', 'youngest',
                  'closest', 'shortest', 'thinnest','tiniest','hollowest',
                  'narrowest','shallowest','simplest','latest','last','poorest','littlest']
argmax_phrases = ['largest', 'brightest', 'heaviest', 'most',
                  'most', 'maximum', 'maximal', 'ultimate', 'totally', 'hugest',
                  'longest', 'biggest', 'fattest', 'fastest',
                  'greatest', 'quickest', 'tallest', 'oldest',
                  'eldest', 'heaviest', 'farthest', 'furthest', 'richest', 'best']
arg_ner_tags = ['argmax', 'argmin']