import torch
from torch.autograd import Variable

from common.globals_args import fn_graph_file, fn_cwq_file, kb_freebase_latest_file, kb_freebase_en_2013, q_mode as mode
from common.hand_files import read_json
from grounding.ranking.path_match_word_level.parameters import get_parameters
from grounding.ranking.path_match_word_level.wordvec import WordEmbedding
from grounding.ranking.path_match_word_level import path_match_word_utils


class PathMatchByLexicalNN():

    def __init__(self):
        self.model_parameters = get_parameters()
        self.define_cuda()
        self.set_model_data()

    def set_model_data(self):
        assert mode in ['cwq', 'graphq']
        if mode=='cwq':
            model_file=fn_cwq_file.model_file+"_iter_{}_devf1_{}_model.pt".format(2720, 52)
            self.relortype_level_word = read_json(kb_freebase_latest_file.dataset + "relortype_level_words.json")
        elif mode == 'graphq':
            model_file = fn_graph_file.model_file + "_iter_{}_devf1_{}_model.pt".format(570, 48)
            self.relortype_level_word = read_json(kb_freebase_en_2013.dataset + "relortype_level_words.json")

        if self.model_parameters.gpu >= 0:
            self.model = torch.load(model_file,map_location=lambda storage, location: storage.cuda(self.model_parameters.gpu))
        else:
            self.model = torch.load(model_file,map_location=lambda storage, location: storage)
        self.model.eval()
        self.wem = WordEmbedding()
        # self.pretrained_embedding = torch.load(self.model_parameters.vector_cache_file)
        # self.word_dict = torch.load(self.model_parameters.word_dict_file)
        # self.word_pair_sim = torch.load(fn_cwq_file.question_match_dir + 'word_pair_sim.pt')
        # self.pad_index = self.word_dict.lookup(self.word_dict.pad_token)
        self.word_pair_sim = dict()

    def define_cuda(self):
        self.model_parameters.cuda = False
        torch.manual_seed(self.model_parameters.seed)
        if not self.model_parameters.cuda:
            self.model_parameters.gpu = -1
        if torch.cuda.is_available() and self.model_parameters.cuda:
            print("Note: You are using GPU for training")
            torch.cuda.set_device(self.model_parameters.gpu)
            torch.cuda.manual_seed(self.model_parameters.seed)
        if torch.cuda.is_available() and not self.model_parameters.cuda:
            print("Warning: You have Cuda but do not use it. You are using CPU for training")

    # get the path pro given importantwords
    def get_path_pro(self, candidate, importantwords_list):
        # score=0.0
        # max_relortype_word = 3
        #11 dim
        pos_ques_pathsimmax = torch.Tensor(self.model_parameters.max_question_word).zero_()
        #16 dim
        pos_path_quessimmax = torch.Tensor(self.model_parameters.max_relortype_word).zero_()
        pos_path_len = torch.tensor(0)
        pos_ques_pathsimmax_list = torch.Tensor(1, self.model_parameters.max_question_word)
        pos_path_quessimmax_list = torch.Tensor(1, self.model_parameters.max_relortype_word)
        pos_path_len_list = torch.Tensor(1)
        # pos_ques_path_sim_list[0:end-start]=self.pos_ques_path_sim_list[start:end]
        for j in range(1):
            pos_ques_pathsimmax_list[j] = pos_ques_pathsimmax
        for j in range(1):
            pos_path_quessimmax_list[j] = pos_path_quessimmax
        for j in range(1):
            pos_path_len_list[j] = pos_path_len
        neg_size = 1
        neg_ques_path_sim = torch.Tensor(neg_size, self.model_parameters.max_question_word, self.model_parameters.max_relortype_word).zero_()
        neg_path_quessimmax = torch.Tensor(neg_size, self.model_parameters.max_relortype_word).zero_()
        neg_ques_pathsimmax = torch.Tensor(neg_size, self.model_parameters.max_question_word).zero_()
        neg_path_len = torch.Tensor(neg_size).zero_()
        neg_path_len[0] = torch.tensor(len(candidate.split("\t")))

        firstpart = path_match_word_utils.get_firstparts_by_path(candidate, self.relortype_level_word)
        if len(importantwords_list) > self.model_parameters.max_question_word:
            # importantwords_list = importantwords_by_unimportant(importantwords_list)
            importantwords_list = importantwords_list[:self.model_parameters.max_question_word]

        for i, word in enumerate(importantwords_list):
            if i < self.model_parameters.max_question_word:
                for j, pathword in enumerate(firstpart):
                    if j < self.model_parameters.max_relortype_word:
                        neg_ques_path_sim[0][i][j] = path_match_word_utils.get_word_pair_sim(
                            word1=word, word2=pathword, wem=self.wem, word_pair_sim=self.word_pair_sim)
        neg_ques_pathsimmax[0], index = torch.max(neg_ques_path_sim[0], 1)
        neg_path_quessimmax[0], index = torch.max(neg_ques_path_sim[0], 0)
        neg_ques_pathsimmax_list = torch.Tensor(1, neg_size, self.model_parameters.max_question_word)
        neg_path_quessimmax_list = torch.Tensor(1, neg_size, self.model_parameters.max_relortype_word)
        neg_path_len_list = torch.Tensor(1, neg_size)

        for j in range(1):
            neg_ques_pathsimmax_list[j] = neg_ques_pathsimmax
        for j in range(1):
            neg_path_quessimmax_list[j] = neg_path_quessimmax
        for j in range(1):
            neg_path_len_list[j] = neg_path_len

        if self.model_parameters.gpu >= 0:
            pos_ques_pathsimmax_list = pos_ques_pathsimmax_list.cuda()
            pos_path_quessimmax_list = pos_path_quessimmax_list.cuda()
            pos_path_len_list = pos_path_len_list.cuda()
            neg_ques_pathsimmax_list = neg_ques_pathsimmax_list.cuda()
            neg_path_quessimmax_list = neg_path_quessimmax_list.cuda()
            neg_path_len_list = neg_path_len_list.cuda()

        pos_score, neg_score = self.model(
            [Variable(pos_ques_pathsimmax_list), Variable(pos_path_quessimmax_list), Variable(pos_path_len_list),
            Variable(neg_ques_pathsimmax_list), Variable(neg_path_quessimmax_list), Variable(neg_path_len_list)])
        score = neg_score[0].detach().numpy().tolist()[0]
        return score


if __name__=="__main__":
    pmnn = PathMatchByLexicalNN()
    print(pmnn.get_path_pro("astronomy.celestial_object.magnitude\tastronomy.celestial_object",["celestial","object","largest","apparent","magnitude"]))

