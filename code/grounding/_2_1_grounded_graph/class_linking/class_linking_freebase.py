from sklearn.metrics.pairwise import cosine_similarity
from common.hand_files import loadGloveModel
from fuzzywuzzy import fuzz
import collections
import numpy as np
from grounding import grounding_args

glove_model = loadGloveModel(grounding_args.glove_file)

def generate_clmention_embedding():
    clmention_embedding = dict()
    for cl_mention in grounding_args.cl_dict_dict:
        phrase_b=cl_mention.lower()
        word_b_list = []
        if ' ' in phrase_b:
            word_b_list.extend(phrase_b.split(' '))
        else:
            word_b_list.append(phrase_b)
        word_b_to_vect_list = []
        for word_b in word_b_list:
            if word_b in glove_model:
                word_b_to_vect_list.append(glove_model[word_b])
        phrase_b_vect = np.zeros(300)
        if len(word_b_to_vect_list) >= 1:
            phrase_b_vect = np.mean(np.array(word_b_to_vect_list), axis=0)
        clmention_embedding[cl_mention]=phrase_b_vect
    return clmention_embedding

clmention_embedding = generate_clmention_embedding()
questionmention_embedding = dict()

def class_linking_interface(mention, top_k=50):
    fuzz_class_grounding_dict = class_mention_linking_fuzz(mention)
    glove_class_grounding_dict = class_mention_linking_glove(mention)
    # combine
    class_grounding_dict = dict()
    for class_ in fuzz_class_grounding_dict:
        combine_pro = grounding_args.class_fuzz_weight * fuzz_class_grounding_dict[class_] \
                      + grounding_args.class_glove_weight * glove_class_grounding_dict[class_]
        class_grounding_dict[class_] = combine_pro
    # rank
    rank_class_grounding_dict = dict(sorted(class_grounding_dict.items(), key=lambda d: d[1], reverse=True))
    top_k_class_popularity_dict = collections.OrderedDict()
    # top_k
    num = 0
    for class_ in rank_class_grounding_dict:
        num += 1
        top_k_class_popularity_dict[class_] = grounding_args.class_popularity_dict[class_]
        if num > top_k:
            break

    # reranker by popularity
    top_k_class_popularity_dict = dict(sorted(top_k_class_popularity_dict.items(), key=lambda d: d[1], reverse=True))
    top_k_rank_class_grounding_dict = collections.OrderedDict()
    for class_ in top_k_class_popularity_dict:
        top_k_rank_class_grounding_dict[class_] = rank_class_grounding_dict[class_]
    return top_k_rank_class_grounding_dict

def class_mention_linking_fuzz(phrase):
    ''''user.leobard.my_test_domain.dfki_person': 0.6443441706691506'''
    grounding_to_score_dict = dict()
    for cl_mention in grounding_args.cl_dict_dict:
        score = fuzz.ratio(cl_mention, phrase) / 100
        for class_ in grounding_args.cl_dict_dict[cl_mention]:
            grounding_to_score_dict[class_] = score
    return grounding_to_score_dict

def class_mention_linking_glove(phrase):
    ''''user.leobard.my_test_domain.dfki_person': 0.6443441706691506'''
    grounding_to_score_dict = dict()
    for cl_mention in grounding_args.cl_dict_dict:
        score = similarity_interface(cl_mention, phrase)
        for class_ in grounding_args.cl_dict_dict[cl_mention]:
            grounding_to_score_dict[class_] = score
    return grounding_to_score_dict

def similarity_interface(phrase_a, phrase_b):
    phrase_b_= phrase_b
    if phrase_b in questionmention_embedding:
        phrase_b_vect = questionmention_embedding[phrase_b]
    else:
        phrase_b = phrase_b.lower()
        word_b_list = []
        if ' ' in phrase_b:
            word_b_list.extend(phrase_b.split(' '))
        else:
            word_b_list.append(phrase_b)

        word_b_to_vect_list = []
        for word_b in word_b_list:
            if word_b in glove_model:
                word_b_to_vect_list.append(glove_model[word_b])
        phrase_b_vect = np.zeros(300)
        if len(word_b_to_vect_list) >= 1:
            phrase_b_vect = np.mean(np.array(word_b_to_vect_list), axis=0)
        questionmention_embedding[phrase_b_]=phrase_b_vect
    phrase_a_vect = clmention_embedding[phrase_a]
    return cosine_similarity([phrase_a_vect, phrase_b_vect])[0][1]

if __name__ == '__main__':
    pass
    # generate_clmention_embedding()
    # similarity_interface('hello world','hello nancy')
    # class_grounding_dict = class_linking_interface('university')

