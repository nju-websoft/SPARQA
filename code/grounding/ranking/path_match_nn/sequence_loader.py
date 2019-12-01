import torch
from torch.autograd import Variable

class SeqRankingLoader():

    def __init__(self, infile, model_parameters,device=-1):
        self.pos_ques_pathsimmax_list, self.pos_path_quessimmax_list, self.pos_path_len_list,\
        self.neg_ques_pathsimmax_list, self.neg_path_quessimmax_list, self.neg_path_len_list= torch.load(infile)
        # print(len(self.neg_path_quessimmax_list))
        self.model_parameters=model_parameters
        self.batch_size = model_parameters.batch_size
        self.batch_num = int(len(self.pos_ques_pathsimmax_list)/self.batch_size)+1
        print("batch_num",self.batch_num)
        self.device=device

    def next_batch(self, shuffle=True):
        device = self.device
        if shuffle:
            indices = torch.randperm(self.batch_num)
        else:
            indices = range(self.batch_num)
        indices = indices.numpy()
        for i in indices:
            if i * self.batch_size < len(self.pos_ques_pathsimmax_list):
                start = i * self.batch_size
                end = (i + 1) * self.batch_size
                if end > len(self.pos_ques_pathsimmax_list):
                    end = len(self.pos_ques_pathsimmax_list)
                # print(end)
                # print(start)
                # print(i)
                pos_ques_pathsimmax_list = torch.Tensor(end - start, self.model_parameters.max_question_word)
                pos_path_quessimmax_list = torch.Tensor(end - start, self.model_parameters.max_relortype_word)
                pos_path_len_list = torch.Tensor(end - start)
                neg_ques_pathsimmax_list = torch.Tensor(end - start, self.model_parameters.neg_size,self.model_parameters.max_question_word)
                neg_path_quessimmax_list = torch.Tensor(end - start,self.model_parameters.neg_size, self.model_parameters.max_relortype_word)
                neg_path_len_list = torch.Tensor(end - start, self.model_parameters.neg_size)

                # pos_ques_path_sim_list[0:end-start]=self.pos_ques_path_sim_list[start:end]
                for j in range(end - start):
                    pos_ques_pathsimmax_list[j] = self.pos_ques_pathsimmax_list[start + j]
                for j in range(end - start):
                    pos_path_quessimmax_list[j] = self.pos_path_quessimmax_list[start + j]
                for j in range(end - start):
                    pos_path_len_list[j] = self.pos_path_len_list[start + j]
                for j in range(end - start):
                    neg_ques_pathsimmax_list[j] = self.neg_ques_pathsimmax_list[start + j]
                for j in range(end - start):
                    neg_path_quessimmax_list[j] = self.neg_path_quessimmax_list[start + j]
                for j in range(end - start):
                    neg_path_len_list[j] = self.neg_path_len_list[start + j]

                if device >= 0:
                    pos_ques_pathsimmax_list = pos_ques_pathsimmax_list.cuda()
                    pos_path_quessimmax_list = pos_path_quessimmax_list.cuda()
                    pos_path_len_list = pos_path_len_list.cuda()
                    neg_ques_pathsimmax_list = neg_ques_pathsimmax_list.cuda()
                    neg_path_quessimmax_list = neg_path_quessimmax_list.cuda()
                    neg_path_len_list = neg_path_len_list.cuda()

                yield Variable(pos_ques_pathsimmax_list), Variable(pos_path_quessimmax_list),  Variable(pos_path_len_list)\
                    ,Variable(neg_ques_pathsimmax_list), Variable(neg_path_quessimmax_list), Variable(neg_path_len_list)

