from grounding.grounding_args import freebase_relation_finalwords, \
    freebase_type_finalwords

def judge_twowords_samelemma(word1, word2):
    word1_str = [w for w in word1]
    word2_str = [w for w in word2]
    len_min = min(len(word1_str), len(word2_str))
    len_max = max(len(word1_str), len(word2_str))
    if len_min <= 1:
        return False
    same = 0
    for i in range(0, len_min):
        if word1_str[i] == word2_str[i]:
            same += 1
        else:
            break
    if float(same) / float(len_max) >= (float(3) / float(7)):
        return True
    else:
        return False

def path_same_preffix(path):
    ports = path.split("\t")
    options = set()
    options.add("base")
    options.add("people")
    for port in ports:
        if port.split(".")[0] != "base" and port.split(".")[0] != "people":
            options.add(port.split(".")[0])
            break
    # 不应当同时有people,base,其他的；可以people+其他或者base+其他
    all_preffix = set()
    for port in ports:
        all_preffix.add(port.split(".")[0])
    if len(all_preffix) >= 3:
        return 0
    for port in ports:
        if port.split(".")[0] not in options:
            return 0
    return 1

# def compute_cosinesimilarity():
    # questions = read_list(fn.path_match_file+"abstractquestions")
    # lineindex_word_embedding=read_lineindex_word_bertembedding(fn.path_match_file+"abstractquestions_embedding.json")

class RelationTypeMatchByVocabulary():

    def __init__(self):
        self.freebase_relation_finalwords = freebase_relation_finalwords
        self.freebase_type_finalwords = freebase_type_finalwords

    # get the path pro given importantwords
    def get_path_pro(self, grounded_graph_path, importantwords):
        freebase_relation_or_type_list = grounded_graph_path.split("\t")
        importantwords_hitted = set()
        pathwords_hitted = set()

        for importantword in importantwords:
            for freebase_relation_or_type in freebase_relation_or_type_list:
                freebase_relation_or_type_words = self.freebase_relation_or_type_to_words(
                    freebase_relation_or_type)
                for freebase_relation_or_type_word in freebase_relation_or_type_words:
                    if judge_twowords_samelemma(importantword, freebase_relation_or_type_word):
                        importantwords_hitted.add(importantword)
                        pathwords_hitted.add(freebase_relation_or_type_word)

        num_cols_hit = 0
        for freebase_relation_or_type_word_samelemma in pathwords_hitted:
            for freebase_relation_or_type in freebase_relation_or_type_list:
                freebase_relation_or_type_words = self.freebase_relation_or_type_to_words(
                    freebase_relation_or_type)
                if freebase_relation_or_type_word_samelemma in freebase_relation_or_type_words:
                    num_cols_hit += 1

        same = path_same_preffix(grounded_graph_path)
        if len(importantwords) == 0:
            pro = same
        else:
            #第一个括号内的为一个col映射上几个importantwords，
            #第二个括号内为importantwords映射率
            pro=(num_cols_hit/len(freebase_relation_or_type_list)) \
                * (len(importantwords_hitted)/len(importantwords)) + same
        return pro

    def freebase_relation_or_type_to_words(self, freebase_relation_or_type):
        words = set()
        if freebase_relation_or_type in self.freebase_relation_finalwords:
            words = self.freebase_relation_finalwords[freebase_relation_or_type]
        elif freebase_relation_or_type in self.freebase_type_finalwords:
            words = self.freebase_type_finalwords[freebase_relation_or_type]
        return words

