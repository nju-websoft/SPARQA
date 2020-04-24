# -*- coding: utf-8 -*-
import torch
import torch.optim as optim

from common.globals_args import root, fn_graph_file
from grounding.ranking.path_match_nn.sequence_loader import SeqRankingLoader
from grounding.ranking.path_match_nn.model import PathRanking
from grounding.ranking.path_match_nn.parameters import get_parameters

model_parameters = get_parameters()

model_parameters.cuda=False
torch.manual_seed(model_parameters.seed)
if not model_parameters.cuda:
    model_parameters.gpu = -1
if torch.cuda.is_available() and model_parameters.cuda:
    print("Note: You are using GPU for training")
    torch.cuda.set_device(model_parameters.gpu)
    torch.cuda.manual_seed(model_parameters.seed)
if torch.cuda.is_available() and not model_parameters.cuda:
    print("Warning: You have Cuda but do not use it. You are using CPU for training")

def train(train_file,val_file,model_file):
    model = PathRanking(model_parameters=model_parameters)
    train_loader = SeqRankingLoader(train_file,model_parameters, model_parameters.gpu)
    val_loader = SeqRankingLoader(val_file,model_parameters, model_parameters.gpu)
    if model_parameters.cuda:
        model.cuda()
        print("Shift model to GPU")
    for name, param in model.named_parameters():
        print(name, param.size())
    criterion = torch.nn.MarginRankingLoss(model_parameters.loss_margin)  # Max margin ranking loss function
    # print(model_parameters.lr)
    optimizer = optim.Adam(model.parameters(), lr=model_parameters.lr)
    iterations=0
    best_dev_acc=0.0
    iters_not_improved=0
    early_stop=False
    patience=1000000*train_loader.batch_num/model_parameters.dev_every
    for epoch in range(1, model_parameters.epochs + 1):
        if early_stop:
            print("Early stopping. Epoch: {}, Best Dev. Acc: {}".format(epoch, best_dev_acc))
            break
        n_correct, n_total = 0, 0
        for batch_idx, batch in enumerate(train_loader.next_batch()):
            iterations+=1
            model.train()
            optimizer.zero_grad()
            pos_score, neg_score = model(batch)
            n_correct += (torch.sum(torch.ge(pos_score, neg_score), 1).data == neg_score.size(1)).sum()
            n_total += pos_score.size(0)
            train_acc = 100. * n_correct / n_total
            ones = torch.autograd.Variable(torch.ones(pos_score.size(0) ,pos_score.size(1)))
            if model_parameters.cuda:
                ones = ones.cuda()
            loss = criterion(pos_score, neg_score, ones)
            print('epoch {} batch {}: loss per sentence: {}, accuracy:{}'.format(epoch,batch_idx, loss,train_acc))
            loss.backward()
            torch.nn.utils.clip_grad_norm(model.parameters(), model_parameters.clip_gradient)
            optimizer.step()
            if iterations % model_parameters.dev_every == 0:
                model.eval()
                total = 0
                correct = 0
                for data_batch in val_loader.next_batch():
                    pos_score, neg_score = model(data_batch)
                    correct += (torch.sum(torch.ge(pos_score, neg_score), 1).data == neg_score.size(1)).sum()
                    total += pos_score.size(0)
                dev_acc = 100. * correct / total
                print('validation accuracy:{}'.format(dev_acc))
                 # update model
                if dev_acc > best_dev_acc:
                    best_dev_acc = dev_acc
                    iters_not_improved = 0
                    snapshot_path = model_file+ '_iter_{}_devf1_{}_model.pt'.format(iterations, best_dev_acc)
                    torch.save(model, snapshot_path)
                else:
                    iters_not_improved += 1
                    if iters_not_improved > patience:
                        early_stop = True
                        break

if __name__=='__main__':

    # resources_webq = root + '/dataset_cwq_1_1/'
    # data_path_match = resources_webq + 'data_path_match/'
    # model_file = data_path_match+'models/'
    # train_file = data_path_match + "train_pathranking_samestructure.pt"
    # val_file = data_path_match + "valid_pathranking_samestructure.pt"
    # train(train_file, val_file, model_file)


    model_file = fn_graph_file.model_file
    train_file =fn_graph_file.path_match_dir + "train_pathranking_samestructure.pt"
    val_file = fn_graph_file.path_match_dir + "valid_pathranking_samestructure.pt"
    train(train_file, val_file, model_file)

    # model_file = fn_cwq_file.model_file
    # train_file =fn_cwq_file.path_match_dir + "train_pathranking_samestructure.pt"
    # val_file = fn_cwq_file.path_match_dir + "valid_pathranking_samestructure.pt"
    # train(train_file, val_file, model_file)
