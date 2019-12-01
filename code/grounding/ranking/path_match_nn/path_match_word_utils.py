import collections
import torch
from sklearn.metrics.pairwise import cosine_similarity

def get_qid_abstractquestion(any_2_1):
    print(len(any_2_1))
    qid_abstractquestions=collections.defaultdict(set)
    for one in any_2_1:
        qid=one.qid
        question=one.question
        for ungrounded_graph in one.ungrounded_graph_forest:
            question_=question
            for node in ungrounded_graph.nodes:
                if node.node_type == 'entity':
                    question_ = question_.replace(node.friendly_name, '<e>')
            qid_abstractquestions[str(qid)].add(question_)
    return qid_abstractquestions

def get_word_pair_sim_without_memory(word1, word2, wem):
    sim = max((judge_twowords_samelemma(word1, word2)),
              cosine_similarity([wem.get_word_embedding(word1).numpy(),
                                 wem.get_word_embedding(word2).numpy()])[0][1])
    return torch.tensor(float(sim))

def get_word_pair_sim(word1, word2, wem, word_pair_sim):
    if word1 + '###' + word2 in word_pair_sim:
        return word_pair_sim[word1 + '###' + word2]
    else:
        sim = max((judge_twowords_samelemma(word1, word2)),
                  cosine_similarity([wem.get_word_embedding(word1).numpy(),
                                     wem.get_word_embedding(word2).numpy()])[0][1])
        sim = torch.tensor(float(sim))
        word_pair_sim[word1 + '###' + word2] = sim
        return sim

def get_firstparts_by_path(path, relortype_level_word):
    first_part = list()
    for col in path.split("\t"):
        if col in relortype_level_word:
            if "0" in relortype_level_word[col]:
                if len(relortype_level_word[col]["0"])>3:
                    first_part.extend(relortype_level_word[col]["0"][:3])
                else:
                    first_part.extend(relortype_level_word[col]["0"])
            if "1" in relortype_level_word[col]:
                second_part=relortype_level_word[col]['1']
                sc_unique=set(second_part)-set(first_part)
                if len(sc_unique)>0:
                    first_part.append(list(sc_unique)[0])
                else:
                    first_part.append(second_part[0])
    return first_part

def judge_twowords_samelemma(word1,word2):
    '''判断两个word是否有相同的lemma'''
    word1_str=[w for w in word1]
    word2_str=[w for w in word2]
    len_min=min(len(word1_str),len(word2_str))
    len_max=max(len(word1_str),len(word2_str))
    if len_min<=1:
        return 0
    same=0
    for i in range(0,len_min):
        if word1_str[i]==word2_str[i]:
            same+=1
        else:
            break
    if float(same)/float(len_max)>=(float(3)/float(7)):
        return 1
    else:
        return 0

