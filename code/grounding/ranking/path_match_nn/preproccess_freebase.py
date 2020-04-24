import os
import copy
import torch

from common.globals_args import fn_cwq_file, fn_graph_file, root, argument_parser, kb_freebase_latest_file, kb_freebase_en_2013
from common.hand_files import read_json, write_json, read_structure_file
import random
from grounding.ranking.path_match_nn.wordvec import WordEmbedding
from datasets_interface.question_interface.questions_utils import extract_grounded_graph_from_jena_freebase
from grounding.ranking.path_match_nn import path_match_word_utils
from grounding.ranking.path_match_nn import wordvec
from parsing import parsing_utils
from grounding.ranking.path_match_nn.parameters import get_parameters
model_parameters = get_parameters()

def conquer_cwq():
    '''1'''
    output_path = fn_cwq_file.dataset
    output_folder_name = '/2019.04.12_cwq/'
    output_file_folder = output_path + output_folder_name
    input_file_folders=['2.2_train_oracle_0_500','2.2_train_oracle_500_1000','2.2_train_oracle_1000_1500','2.2_train_oracle_1500_2000',
                       '2.2_train_oracle_2000_2500', '2.2_train_oracle_2500_3000', '2.2_train_oracle_3000_3500']
    all_files=list()
    for file in input_file_folders:
        infiles=os.listdir(output_file_folder + file)
        for infile in infiles:
            all_files.append(output_file_folder+file+'/'+infile)
    #
    # train_qid_to_grounded_graph_dict = complexwebquestion_interface.extract_grounded_graph_from_jena(globals_args.fn_cwq_file.complexwebquestion_train_bgp_dir)
    # property_level_words = read_json(fn_cwq_file.freebase + "property_level_words.json")
    # train_structure_with_2_1_grounded_graph_file = output_path + '/2019.05.01_cwq' + '/2.1/' + 'structures_with_2_1_ungrounded_graphs_train_0501_multi.json'
    # train_2_1 = read_structure_file(train_structure_with_2_1_grounded_graph_file)
    # train_qid_abstractquestions = get_qid_abstractquestion(train_2_1)
    # train_data_generation_samestructure(train_qid_to_grounded_graph_dict,list(property_level_words.keys()),all_files,train_qid_abstractquestions)

    '''2'''
    # trainorval_data=read_json(fn_cwq_file.path_match_dir + "data_for_trainorval_list_samestructure.json")
    # wem = WordEmbedding()
    # property_level_words = read_json(fn_cwq_file.freebase + "property_level_words.json")
    # create_data_for_trainorval(trainorval_data=trainorval_data,relortype_level_word=property_level_words,wem=wem,save_path=fn_cwq_file.path_match_dir+'trainorval_pathranking_samestructure.pt')

    '''3'''
    infile = fn_cwq_file.path_match_dir + "trainorval_pathranking_samestructure.pt"
    out_file1 = fn_cwq_file.path_match_dir + "train_pathranking_samestructure.pt"
    out_file2 = fn_cwq_file.path_match_dir + "valid_pathranking_samestructure.pt"
    divide_train_val(infile, out_file1, out_file2)

def conquer_graphq():
    '''1'''
    # output_path = fn_graph_file.dataset
    # # output_path = globals_args.argument_parser.output
    # output_folder_name = '/output_graphq/'
    # output_file_folder = output_path + output_folder_name
    # input_file_folders=['2.2_train']
    # all_files = list()
    # for file in input_file_folders:
    #     infiles = os.listdir(output_file_folder + file)
    #     for infile in infiles:
    #         all_files.append(output_file_folder+file+'/'+infile)
    # property_level_words = read_json(kb_freebase_en_2013.dataset + "/relortype_level_words.json")
    # # property_level_words = read_json(fn_graph_file.dataset + "/dataset_freebase_graphq/relortype_level_words.json")
    # qid_abstractquestions = read_json(fn_graph_file.question_match_dir+'qid_abstractquestion.json')
    # train_data_generation_samestructure_graphq(list(property_level_words.keys()),all_files, qid_abstractquestions)

    '''2'''
    # trainorval_data=read_json(fn_graph_file.path_match_dir + "data_for_trainorval_list_samestructure.json")
    # wem = WordEmbedding()
    # property_level_words = read_json(kb_freebase_en_2013.dataset + "/relortype_level_words.json")
    # # property_level_words = read_json(fn_graph_file.dataset + "/dataset_freebase_graphq/relortype_level_words.json")
    # create_data_for_trainorval(trainorval_data=trainorval_data, relortype_level_word=property_level_words,
    #                            wem=wem, save_path=fn_graph_file.path_match_dir+'trainorval_pathranking_samestructure.pt')

    '''3'''
    infile = fn_graph_file.path_match_dir + "trainorval_pathranking_samestructure.pt"
    out_file1 = fn_graph_file.path_match_dir + "train_pathranking_samestructure.pt"
    out_file2 = fn_graph_file.path_match_dir + "valid_pathranking_samestructure.pt"
    divide_train_val(infile, out_file1, out_file2)

def conquer_cwq_0904():
    resources_cwq = root + '/dataset_cwq_1_1/'
    data_path_match = resources_cwq + 'data_path_match/'
    train_cwq_bgp_filepath = resources_cwq + '/ComplexWebQuestions_train_bgp.txt'

    # output_path = argument_parser.output
    # output_file_folder = output_path + '/2019.06.03_webq'
    output_path = resources_cwq + 'output_cwq'
    train_structure_with_2_1_grounded_graph_file = output_path + '/2.1/' + 'structures_with_2_1_grounded_graph_all_train_head_0901_0_15000.json'

    '''1'''
    # input_file_folder = output_path + '/2.2_train/'
    # all_files = list()
    # infiles = os.listdir(input_file_folder)
    # for infile in infiles:
    #     all_files.append(input_file_folder+'/'+infile)
    # train_qid_to_grounded_graph_dict = extract_grounded_graph_from_jena_freebase(train_cwq_bgp_filepath)
    # # property_level_words = read_json(fn_cwq_file.freebase + "property_level_words.json")
    # property_level_words = read_json(kb_freebase_latest_file.dataset + "property_level_words.json")
    # train_2_1 = read_structure_file(train_structure_with_2_1_grounded_graph_file)
    # train_qid_abstractquestions = path_match_word_utils.get_qid_abstractquestion(train_2_1)
    # train_data_generation_samestructure_wq(
    #     train_qid_to_grounded_graph_dict, list(property_level_words.keys()),
    #     all_files, train_qid_abstractquestions, mode='wq')

    '''2'''
    # trainorval_data = read_json(data_path_match + "data_for_trainorval_list_samestructure.json")
    # wem = wordvec.WordEmbedding()
    # # property_level_words = read_json(fn_cwq_file.freebase + "property_level_words.json")
    # property_level_words = read_json(kb_freebase_latest_file.dataset + "property_level_words.json")
    # create_data_for_trainorval(
    #     trainorval_data=trainorval_data, relortype_level_word=property_level_words,
    #     wem=wem, save_path=data_path_match+'trainorval_pathranking_samestructure.pt')

    '''3'''
    infile =data_path_match+ "trainorval_pathranking_samestructure.pt"
    out_file1 = data_path_match + "train_pathranking_samestructure.pt"
    out_file2 = data_path_match + "valid_pathranking_samestructure.pt"
    divide_train_val(infile, out_file1, out_file2)

def train_data_generation_samestructure_graphq(propertys,files,qid_abstractquestions):
    data_for_train_list = list()
    for i,file in enumerate(files):
        print(i,file)
        data=read_structure_file(file)
        qid=file.split('/')[-1].split('.')[0]

        if len(qid_abstractquestions[qid])==0:
            continue

        negatives=list()
        j=0
        # join=True
        for structure in data:
            gold_path = []
            predicates = []
            # for edge in structure.gold_graph_query.edges:
            #     gold_path.append(edge.relation)
            #     predicates.append(edge.relation)
            for edge in structure.gold_sparql_query['edges']:
                gold_path.append(edge['relation'])
                predicates.append(edge['relation'])

            gold_path.sort()
            gold_path = '\t'.join(gold_path)
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.grounded_graph_forest:
                    path=grounded_graph.key_path
                    ps=path.split('\t')
                    ps.sort()
                    path='\t'.join(ps)
                    if j < model_parameters.neg_size and len(ps) == len(predicates) and path!=gold_path:
                        negatives.append(path)
                        j += 1
        if j>0:
            if j < model_parameters.neg_size:
                while j < model_parameters.neg_size:
                    candidate = list()
                    for i in range(len(predicates)):
                        candidate.append(propertys[random.randint(0, len(propertys) - 1)])
                    candidate.sort()
                    candidate = "\t".join(candidate)
                    if candidate != gold_path and candidate not in negatives:
                        negatives.append(candidate)
                        j += 1
            one=dict()
            one["qid"] = qid
            one["abstractquestion"] = (qid_abstractquestions[qid])
            one["gold_path"] = gold_path
            one["negatives"] = negatives
            data_for_train_list.append(one)
        else:
            print('not join',qid)
    write_json(data_for_train_list, fn_graph_file.path_match_dir + "data_for_trainorval_list_samestructure.json")

def train_data_generation_samestructure(train_qid_to_grounded_graph_dict,propertys,files,train_qid_abstractquestions,mode='cwq'):
    data_for_train_list = list()
    for i,file in enumerate(files):
        print(i,file)
        data=read_structure_file(file)
        qid=file.split('/')[-1].split('.')[0]

        if len(train_qid_abstractquestions[qid])==0:
            continue
        elif len(list(train_qid_abstractquestions[qid])[0])==0:
            continue

        gold_graph=train_qid_to_grounded_graph_dict[qid]
        predicates = []
        for edge in gold_graph.edges:
            predicates.append(edge.friendly_name)
        predicates.sort()
        gold_path = '\t'.join(predicates)
        negatives=list()
        j=0
        # join=True
        for structure in data:
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.grounded_graph_forest:
                    path=grounded_graph.key_path
                    ps=path.split('\t')
                    ps.sort()
                    path='\t'.join(ps)
                    if j < model_parameters.neg_size and len(ps) == len(predicates) and path!=gold_path:
                        negatives.append(path)
                        j += 1
        if j>0:
            if j < model_parameters.neg_size:
                while j < model_parameters.neg_size:
                    candidate = list()
                    for i in range(len(predicates)):
                        candidate.append(propertys[random.randint(0, len(propertys) - 1)])
                    candidate.sort()
                    candidate = "\t".join(candidate)
                    if candidate != gold_path and candidate not in negatives:
                        negatives.append(candidate)
                        j += 1
            one=dict()
            one["qid"] = qid
            one["abstractquestion"] = list(train_qid_abstractquestions[qid])[0]
            one["gold_path"] = gold_path
            one["negatives"] = negatives
            data_for_train_list.append(one)
        else:

            print('not join',qid)
    if mode=='cwq':
        write_json(data_for_train_list,
               fn_cwq_file.path_match_dir + "data_for_trainorval_list_samestructure.json")

def train_data_generation_samestructure_wq(train_qid_to_grounded_graph_dict, propertys, files, train_qid_abstractquestions, mode='cwq'):
    data_for_train_list = list()
    for i, file in enumerate(files):
        print(i, file)
        data = read_structure_file(file)
        qid = file.split('/')[-1].split('.')[0]
        if len(train_qid_abstractquestions[qid]) == 0:
            continue
        elif len(list(train_qid_abstractquestions[qid])[0]) == 0:
            continue

        # if 'WebQTrn-'+str(qid) not in train_qid_to_grounded_graph_dict:
        #     print('do not exist: WebQTrn-'+str(qid))
        #     continue
        # gold_graph = train_qid_to_grounded_graph_dict['WebQTrn-'+str(qid)]

        if qid not in train_qid_to_grounded_graph_dict:
            print('do not exist: '+ qid)
            continue
        gold_graph = train_qid_to_grounded_graph_dict[qid]
        predicates = []
        for edge in gold_graph.edges:
            predicates.append(edge.friendly_name)
        predicates.sort()
        gold_path = '\t'.join(predicates)

        negatives=list()
        j=0
        for structure in data:
            for ungrounded_graph in structure.ungrounded_graph_forest:
                for grounded_graph in ungrounded_graph.grounded_graph_forest:
                    #path
                    path = grounded_graph.key_path
                    ps = path.split('\t')
                    ps.sort()
                    path = '\t'.join(ps)
                    if j < model_parameters.neg_size and len(ps) == len(predicates) and path != gold_path:
                        negatives.append(path)
                        j += 1

        if j>0:
            if j < model_parameters.neg_size:
                while j < model_parameters.neg_size:
                    candidate = list()
                    for i in range(len(predicates)):
                        candidate.append(propertys[random.randint(0, len(propertys) - 1)])
                    candidate.sort()
                    candidate = "\t".join(candidate)
                    if candidate != gold_path \
                            and candidate not in negatives:
                        negatives.append(candidate)
                        j += 1
            one = dict()
            one["qid"] = qid
            one["abstractquestion"] = list(train_qid_abstractquestions[qid])[0]
            one["gold_path"] = gold_path
            one["negatives"] = negatives
            data_for_train_list.append(one)
        else:
            print('not join', qid)
    write_json(data_for_train_list, root + '/dataset_cwq_1_1/data_path_match/data_for_trainorval_list_samestructure.json')

def create_data_for_trainorval(trainorval_data,relortype_level_word,wem,save_path):
    qid_list=[]
    pos_ques_pathsimmax_list=[]
    pos_path_quessimmax_list=[]
    neg_ques_pathsimmax_list = []
    neg_path_quessimmax_list = []
    pos_path_len_list=[]
    neg_path_len_list=[]
    for index, one in enumerate(trainorval_data):
        print(one["qid"])
        positive_ques_path_sim=torch.Tensor(
            model_parameters.max_question_word, model_parameters.max_relortype_word).zero_()
        pos_ques_pathsimmax=torch.Tensor(
            model_parameters.max_question_word).zero_()
        pos_path_quessimmax=torch.Tensor(
            model_parameters.max_relortype_word).zero_()
        abstractquestion = one["abstractquestion"]
        importantwords_list = parsing_utils.get_importantwords_byabstractquestion(abstractquestion)
        if len(importantwords_list)==0:
            continue
        positive_path = one["gold_path"]
        candidates = one["negatives"]

        positive_path_firstpart = path_match_word_utils.get_firstparts_by_path(positive_path, relortype_level_word)
        for i, word in enumerate(importantwords_list):
            if i < model_parameters.max_question_word:
                for j, pathword in enumerate(positive_path_firstpart):
                    if j < model_parameters.max_relortype_word:
                        positive_ques_path_sim[i][j] = path_match_word_utils.get_word_pair_sim_without_memory(word, pathword, wem)
                    else:
                        print("goldpath>max_relortype_word", one["qid"])

        pos_ques_pathsimmax,index=torch.max(positive_ques_path_sim,1)
        pos_path_quessimmax,index=torch.max(positive_ques_path_sim,0)
        pos_path_len = torch.tensor(len(positive_path.split("\t")))
        pos_ques_pathsimmax_list.append(pos_ques_pathsimmax)
        pos_path_quessimmax_list.append(pos_path_quessimmax)
        pos_path_len_list.append(pos_path_len)

        neg_ques_path_sim = torch.Tensor(model_parameters.neg_size,model_parameters.max_question_word,model_parameters.max_relortype_word).zero_()
        neg_path_quessimmax = torch.Tensor(model_parameters.neg_size,model_parameters.max_relortype_word).zero_()
        neg_ques_pathsimmax = torch.Tensor(model_parameters.neg_size,model_parameters.max_question_word).zero_()
        neg_path_len=torch.Tensor(model_parameters.neg_size).zero_()
        for k,candidate in enumerate(candidates):
            neg_path_len[k]=torch.tensor(len(candidate.split("\t")))
            firstpart = path_match_word_utils.get_firstparts_by_path(candidate, relortype_level_word)
            for i, word in enumerate(importantwords_list):
                if i < model_parameters.max_question_word:
                    for j,pathword in enumerate(firstpart):
                        if j < model_parameters.max_relortype_word:
                            sim = path_match_word_utils.get_word_pair_sim_without_memory(word,pathword, wem)
                            neg_ques_path_sim[k][i][j]=sim
            neg_ques_pathsimmax[k],index = torch.max(neg_ques_path_sim[k],1)
            neg_path_quessimmax[k],index = torch.max(neg_ques_path_sim[k],0)

        neg_ques_pathsimmax_list.append(neg_ques_pathsimmax)
        neg_path_quessimmax_list.append(neg_path_quessimmax)
        neg_path_len_list.append(neg_path_len)
        qid_list.append(str(one["qid"]))
    torch.save((pos_ques_pathsimmax_list, pos_path_quessimmax_list, pos_path_len_list,
                neg_ques_pathsimmax_list, neg_path_quessimmax_list,
                neg_path_len_list, qid_list),  save_path)

def divide_train_val(infile, out_file1, out_file2):
    pos_ques_pathsimmax_list, pos_path_quessimmax_list, pos_path_len_list,\
    neg_ques_pathsimmax_list, neg_path_quessimmax_list, neg_path_len_list,\
    qid_list = torch.load(infile)
    qid_shuffle_list=copy.deepcopy(qid_list)
    print(qid_shuffle_list)
    random.shuffle(qid_shuffle_list)
    print(qid_shuffle_list)
    train_size = int(len(qid_shuffle_list) / 5 * 4)
    train_qidupper=qid_shuffle_list[0:train_size]

    train_pos_ques_pathsimmax_list=list()
    train_pos_path_quessimmax_list=list()
    train_pos_path_len_list=list()
    train_neg_ques_pathsimmax_list = list()
    train_neg_path_quessimmax_list = list()
    train_neg_path_len_list=list()

    val_pos_ques_pathsimmax_list = list()
    val_pos_path_quessimmax_list = list()
    val_pos_path_len_list = list()
    val_neg_ques_pathsimmax_list = list()
    val_neg_path_quessimmax_list = list()
    val_neg_path_len_list = list()

    for i in range(len(qid_list)):
        qidupper=(qid_list[i])
        if qidupper in train_qidupper:
            print(qidupper,"train")
            train_pos_ques_pathsimmax_list.append(pos_ques_pathsimmax_list[i])
            train_pos_path_quessimmax_list.append(pos_path_quessimmax_list[i])
            train_neg_ques_pathsimmax_list.append(neg_ques_pathsimmax_list[i])
            train_neg_path_quessimmax_list.append(neg_path_quessimmax_list[i])
            train_pos_path_len_list.append(pos_path_len_list[i])
            train_neg_path_len_list.append(neg_path_len_list[i])
        else:
            print(qidupper, "val")
            val_pos_ques_pathsimmax_list.append(pos_ques_pathsimmax_list[i])
            val_pos_path_quessimmax_list.append(pos_path_quessimmax_list[i])
            val_neg_ques_pathsimmax_list.append(neg_ques_pathsimmax_list[i])
            val_neg_path_quessimmax_list.append(neg_path_quessimmax_list[i])
            val_pos_path_len_list.append(pos_path_len_list[i])
            val_neg_path_len_list.append(neg_path_len_list[i])
    torch.save((train_pos_ques_pathsimmax_list, train_pos_path_quessimmax_list, train_pos_path_len_list,train_neg_ques_pathsimmax_list, train_neg_path_quessimmax_list,train_neg_path_len_list),out_file1)
    torch.save((val_pos_ques_pathsimmax_list, val_pos_path_quessimmax_list, val_pos_path_len_list,val_neg_ques_pathsimmax_list, val_neg_path_quessimmax_list,val_neg_path_len_list),out_file2)

if __name__=='__main__':

    conquer_graphq()
    # pass
    # conquer()
    # random.shuffle(['a','bc'])
