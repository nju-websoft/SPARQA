import torch
from torch import nn

class PathRanking(nn.Module):

    def __init__(self,model_parameters):
        super(PathRanking, self).__init__()
        self.model_parameters=model_parameters
        self.fc1 = nn.Sequential(nn.Linear(self.model_parameters.max_question_word, 1))
        self.fc2 = nn.Sequential(nn.Linear(self.model_parameters.max_relortype_word,  1))
        self.fc3 = nn.Sequential(nn.Linear(2, 1))
        # only first part of path

    def forward(self, batch):
        # pos_pos_ques_path_sim_list:batchsize*max_question_word*max_relortype_word
        # neg_ques_path_sim_list:batchsize*neg_size*max_question_word*max_relortype_word
        # pos_path_len_list:batchsize     (len(positive_path.split("\t")))
        # neg_path_len_list:batchsize*neg_size  (len(positive_path.split("\t")))
        # ques_index_list:batchsize*max_question_word
        pos_ques_pathsimmax_list, pos_path_quessimmax_list, pos_path_len_list,\
        neg_ques_pathsimmax_list, neg_path_quessimmax_list, neg_path_len_list = batch
        batch_size = len(pos_ques_pathsimmax_list)
        neg_size = len(neg_path_len_list[0])
        # print(pos_ques_pathsimmax_list.shape)
        pos_ques_z1=self.fc1(pos_ques_pathsimmax_list).squeeze(1)
        pos_path_z2=self.fc2(pos_path_quessimmax_list).squeeze(1)
        # print(pos_ques_z1.shape)
        pos_z1_z2 = torch.Tensor(2,len(pos_ques_z1))
        pos_z1_z2[0]=pos_ques_z1
        pos_z1_z2[1]=pos_path_z2
        pos_z1_z2=pos_z1_z2.transpose(0,1)
        if self.model_parameters.cuda:
            pos_z1_z2 = pos_z1_z2.cuda()
        pos_score=self.fc3(pos_z1_z2).squeeze(1)
        # print(pos_score.shape)
        # print(pos_path_len_list.shape)
        # pos_score=pos_score/pos_path_len_list
        # print(pos_score.shape)
        pos_score = pos_score.view(batch_size,1).expand(batch_size, neg_size)

        neg_ques_z1 = self.fc1(neg_ques_pathsimmax_list).squeeze(2)
        neg_path_z2 = self.fc2(neg_path_quessimmax_list).squeeze(2)
        # neg_z1_z2 = torch.Tensor(len(neg_ques_z1),len(neg_ques_z1[0]), 2)
        neg_z1_z2 = torch.Tensor(2, len(pos_ques_z1),len(neg_ques_z1[0]),)
        neg_z1_z2[0] = neg_ques_z1
        neg_z1_z2[1] = neg_path_z2
        neg_z1_z2 = neg_z1_z2.transpose(0, 1)
        neg_z1_z2 = neg_z1_z2.transpose(1, 2)
        if self.model_parameters.cuda:
            neg_z1_z2 = neg_z1_z2.cuda()
        neg_score = self.fc3(neg_z1_z2).squeeze(2)
        # print(neg_score.shape)
        # neg_score = neg_score / neg_path_len_list
        return pos_score, neg_score
