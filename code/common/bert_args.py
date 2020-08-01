
class BertArgs():

    def __init__(self, root, mode):
        # uncased model
        self.bert_base_uncased_model = root + '/pre_train_models/bert-base-uncased.tar.gz'
        self.bert_base_uncased_tokenization = root + '/pre_train_models/bert-base-uncased-vocab.txt'
        # cased model
        self.bert_base_cased_model = root + '/pre_train_models/bert-base-cased.tar.gz'
        self.bert_base_cased_tokenization = root + '/pre_train_models/bert-base-cased-vocab.txt'
        if mode == 'cwq':
            self.get_cwq_args(root=root)
        elif mode == 'graphq':
            self.get_graphq_args(root=root)
        else:
            pass

    def get_cwq_args(self, root):
        root = root + '/dataset_cwq_1_1/fine_tuning_models_cwq_0831/'
        self.fine_tuning_headword_squad_F_model = root + 'debug_cwq_headwords_0831_squad_F/pytorch_model.bin'
        self.fine_tuning_token_classifier_C_model = root + 'debug_cwq_node_classifier_0831_C/pytorch_model.bin'
        self.fine_tuning_redundancy_span_D_model = root + 'debug_cwq_redundancy_0831_D/pytorch_model.bin'
        self.fine_tuning_relation_classifier_E_model = root + 'debug_cwq_relation_classifier_0831_E/pytorch_model.bin'
        self.fine_tuning_sequence_classifier_B_model = root + 'debug_cwq_simplification_0831_B/pytorch_model.bin'

    def get_graphq_args(self, root):
        root = root + '/dataset_graphquestions/fine_tuning_models_graphq_0905/'
        self.fine_tuning_headword_squad_F_model = root + 'debug_headwords_0905_squad_F/pytorch_model.bin'
        self.fine_tuning_token_classifier_C_model = root + 'debug_node_3_0905_C/pytorch_model.bin'
        self.fine_tuning_redundancy_span_D_model = root + 'debug_redundancy_0905_D/pytorch_model.bin'
        self.fine_tuning_relation_classifier_E_model = root + 'debug_relation_classifier_0905_E/pytorch_model.bin'
        self.fine_tuning_sequence_classifier_B_model = root + 'debug_simplification_0905_B/pytorch_model.bin'
