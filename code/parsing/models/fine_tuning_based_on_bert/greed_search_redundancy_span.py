import os
import sys

#------------------------------------------------
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
os.environ['CUDA_VISIBLE_DEVICES']='2'
#------------------------------------------------

import model_utils
from fine_tuning_based_on_bert import run_redundancy_span

def grid_search(dataset, learning_rate_list, train_batch_size_list, train_epochs_list):
    args = model_utils.run_redundancy_span_get_local_args()

    for learning_rate in learning_rate_list:
        for train_batch_size in train_batch_size_list:
            for train_epochs in train_epochs_list:
                args.learning_rate = learning_rate
                args.train_batch_size = train_batch_size
                args.num_train_epochs = train_epochs

                args.bert_model = 'bert-base-cased'
                args.do_train = True
                args.do_predict = True
                args.train_file = '../tasks/'+dataset+'/train-data-new-redundancy.txt'
                args.predict_file = '../tasks/'+dataset+'/dev-data-new-redundancy.txt'
                args.predict_batch_size = 16
                args.max_seq_length = 64
                args.doc_stride = 128
                args.output_dir = '../tasks/'+dataset+'/debug_redundancy_0831_D/' \
                                  'output_train_rate_'+str(learning_rate)+'_batch_'+str(train_batch_size)+'_epochs_'+str(train_epochs)+'_0831/'
                print (args.output_dir)
                run_redundancy_span.main(args=args)

if __name__ == '__main__':

    learning_rate_list = [3e-5, 4e-5, 5e-5]
    train_batch_size_list = [16, 32]
    train_epochs_list = [40, 60, 80, 100]

    dataset = 'fine_tuning_models_qald_0831'
    # fine_tuning_models_qald_0831
    # fine_tuning_models_lcquad_0831
    # fine_tuning_models_webq_0831
    # fine_tuning_models_cwq_0831
    grid_search(dataset=dataset, learning_rate_list=learning_rate_list,
                train_batch_size_list=train_batch_size_list, train_epochs_list=train_epochs_list)

