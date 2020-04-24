
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
        elif mode == 'webq':
            self.get_webq_args(root=root)
        elif mode == 'qald':
            self.get_qald_args(root=root)
        elif mode == 'lcquad':
            self.get_lcquad_args(root=root)
        else:
            pass

    def get_cwq_args(self, root):
        # root = root + '/dataset_cwq_1_1/fine_tuning_models_cwq_0825_v04/output_cwq_train_3e_5_epoch_20_0825/'
        root = root + '/dataset_cwq_1_1/fine_tuning_models_cwq_0831/'
        self.fine_tuning_headword_squad_F_model = root + 'debug_cwq_headwords_0831_squad_F/pytorch_model.bin'
        self.fine_tuning_joint_threemodels_A_model = root + 'debug_cwq_joint_threemodels_0831_A/pytorch_model.bin'
        self.fine_tuning_token_classifier_C_model = root + 'debug_cwq_node_classifier_0831_C/pytorch_model.bin'
        self.fine_tuning_redundancy_span_D_model = root + 'debug_cwq_redundancy_0831_D/pytorch_model.bin'
        self.fine_tuning_relation_classifier_E_model = root + 'debug_cwq_relation_classifier_0831_E/pytorch_model.bin'
        self.fine_tuning_sequence_classifier_B_model = root + 'debug_cwq_simplification_0831_B/pytorch_model.bin'

        self.fine_tuning_paraphrase_classifier_G_model = root + ''
        # self.fine_tuning_paraphrase_classifier_model = root + '/pytorch_pretrained_BERT/debug_complexwq_parahrase_0508/output/pytorch_model.bin'
        # /debug_cwq_ungrounded_to_grounded_0511/output/pytorch_model.bin'

    def get_webq_args(self, root):
        # root = root + '/dataset_webq/fine_tuning_models_webq_0812/output_webq_train_3e_5_epoch_200_0812'
        root = root + '/dataset_webq/fine_tuning_models_webq_0831/'
        self.fine_tuning_headword_squad_F_model = root + 'debug_webq_headwords_0831_squad_F/pytorch_model.bin'
        self.fine_tuning_joint_threemodels_A_model = root + 'debug_webq_joint_threemodels_0831_A/pytorch_model.bin'
        self.fine_tuning_token_classifier_C_model = root + 'debug_webq_node_classifier_0831_C/pytorch_model.bin'
        self.fine_tuning_redundancy_span_D_model = root + 'debug_webq_redundancy_0831_D/pytorch_model.bin'
        self.fine_tuning_relation_classifier_E_model = root + 'debug_webq_relation_classifier_0831_E/pytorch_model.bin'
        self.fine_tuning_sequence_classifier_B_model = root + 'debug_webq_simplification_0831_B/pytorch_model.bin'
        # self.fine_tuning_paraphrase_classifier_G_model = root + ''

    def get_qald_args(self, root):
        root = root + '/dataset_qald_9/fine_tuning_models_qald_0831/'
        # 'output_train_3e_5_epoch_200_0812/' \
        self.fine_tuning_headword_squad_F_model = root + 'debug_headwords_0831_squad_F/pytorch_model.bin'
        self.fine_tuning_joint_threemodels_A_model = root + 'debug_joint_threemodels_0831_A/pytorch_model.bin'
        self.fine_tuning_token_classifier_C_model = root + 'debug_node_3_0831_C/pytorch_model.bin'
        self.fine_tuning_redundancy_span_D_model = root + 'debug_redundancy_0831_D/pytorch_model.bin'
        self.fine_tuning_relation_classifier_E_model = root + 'debug_relation_classifier_0831_E/pytorch_model.bin'
        self.fine_tuning_sequence_classifier_B_model = root + 'debug_simplification_0831_B/pytorch_model.bin'
        # self.fine_tuning_paraphrase_classifier_G_model = root + ''

    def get_lcquad_args(self, root):
        root = root + '/dataset_lcquad_1_0/fine_tuning_models_lcquad_0831/'
        #output_lcquad_train_3e_5_epoch_200_0817
        self.fine_tuning_headword_squad_F_model = root + 'debug_lcquad_headwords_0831_squad_F/pytorch_model.bin'
        self.fine_tuning_joint_threemodels_A_model = root + 'debug_lcquad_joint_threemodels_0831_A/pytorch_model.bin'
        self.fine_tuning_token_classifier_C_model = root + 'debug_lcquad_node_classifier_0831_C/pytorch_model.bin'
        self.fine_tuning_redundancy_span_D_model = root + 'debug_lcquad_redundancy_0831_D/pytorch_model.bin'
        self.fine_tuning_relation_classifier_E_model = root + 'debug_lcquad_relation_classifier_0831_E/pytorch_model.bin'
        self.fine_tuning_sequence_classifier_B_model = root + 'debug_lcquad_simplification_0831_B/pytorch_model.bin'
        # self.fine_tuning_paraphrase_classifier_G_model = root + ''

    def get_graphq_args(self, root):
        root = root + '/dataset_graphquestions/fine_tuning_models_graphq_0905/'
        self.fine_tuning_headword_squad_F_model = root + 'debug_headwords_0905_squad_F/pytorch_model.bin'
        self.fine_tuning_token_classifier_C_model = root + 'debug_node_3_0905_C/pytorch_model.bin'
        self.fine_tuning_redundancy_span_D_model = root + 'debug_redundancy_0905_D/pytorch_model.bin'
        self.fine_tuning_relation_classifier_E_model = root + 'debug_relation_classifier_0905_E/pytorch_model.bin'
        self.fine_tuning_sequence_classifier_B_model = root + 'debug_simplification_0905_B/pytorch_model.bin'
        # self.fine_tuning_paraphrase_classifier_model = root + '/pytorch_pretrained_BERT/debug_cwq_parahrase_0508/output/pytorch_model.bin'
        # self.fine_tuning_joint_threemodels_A_model = root + '/pytorch_pretrained_BERT/fine_tuning_models_graphq/debug_graphq_joint_threemodels_0629_A/'

