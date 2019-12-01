from argparse import ArgumentParser

def get_parameters():
    parser = ArgumentParser(description='kbcqa-pathmatchnn model')
    parser.add_argument('--neg_size', type=int, default=300, help='negtive sampling number')
    # parser.add_argument('--word_dict_file', type=str, default=fn.path_match_file+'word_dict.pt', help='word-index')
    # parser.add_argument('--word_vectors_file', type=str, default=fn.ranker_path + "glove.6B.300d.txt")
    # parser.add_argument('--vector_cache_file', type=str, default=fn.path_match_file + 'input_vectors.pt')
    parser.add_argument('--max_question_word', type=int, default=11, help='max len of question word')
    # parser.add_argument('--max_question_word', type=int, default=22, help='max len of question word')
    parser.add_argument('--max_relortype_word', type=int, default=16, help='max len of relation or type word')
    # parser.add_argument('--max_relortype_word', type=int, default=8*5, help='max len of relation or type word')
    parser.add_argument('--dropout_prob', type=float, default=0.3)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--dev_every', type=int, default=10)

    parser.add_argument('--word_normalize', action='store_true')
    parser.add_argument('--d_word_embed', type=int, default=300)
    parser.add_argument('--loss_margin', type=float, default=1)
    parser.add_argument('--lr', type=float, default=1e-3)
    # parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--seed', type=int, default=1111, help='random seed for reproducing results')
    parser.add_argument('--clip_gradient', type=float, default=0.6, help='gradient clipping')
    parser.add_argument('--gpu', type=int, default=0, help='GPU device to use')  # use -1 for CPU
    parser.add_argument('--cuda', type=bool, default=True, help='GPU device to use')  # use -1 for CPU
    parser.add_argument('--epochs', type=int, default=1000)
    args = parser.parse_args()
    return args
