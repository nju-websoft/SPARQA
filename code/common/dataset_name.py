from common.hand_files import read_ngram_el_grounding_result


class CWQFileName():
    def __init__(self, root):
        self.dataset = root + '/dataset_cwq_1_1/'
        self.path_match_dir=self.dataset+'data_path_match/'
        self.model_file = self.path_match_dir + "models/"
        self.question_match_dir = self.dataset + 'data_question_match/'
        self.question_model_file = self.question_match_dir + "models/"
        self.complexwebquestion_test_dir = self.dataset + 'ComplexWebQuestions_test.json'
        self.complexwebquestion_train_dir = self.dataset + 'ComplexWebQuestions_train.json'
        self.complexwebquestion_dev_dir = self.dataset + 'ComplexWebQuestions_dev.json'
        self.complexwebquestion_all_questions_dir = self.dataset + 'ComplexWebQuestions_1_0_all_question.json'
        self.complexwebquestion_test_bgp_dir = self.dataset +'ComplexWebQuestions_test_bgp.txt'
        self.complexwebquestion_train_bgp_dir = self.dataset +'ComplexWebQuestions_train_bgp.txt'
        self.complexwebquestion_dev_bgp_dir = self.dataset +'ComplexWebQuestions_dev_bgp.txt'
        self.grounded_graph_file = self.dataset + "oracle_grounded_graph_cwq/"


class GraphqFileName():
    def __init__(self, root):
        self.dataset = root + '/dataset_graphquestions/'
        # self.graphquestions_testing_dir = self.dataset + 'graphquestions.testing.json'
        self.graphquestions_testing_dir = self.dataset + 'graphquestions.testing_nju_1209.json'
        # self.graphquestions_training_dir = self.dataset + 'graphquestions.training.json'
        self.graphquestions_training_dir = self.dataset + 'graphquestions.training_nju_1209.json'
        self.question_qid_normal_dict = self.dataset + 'graph_testing_question_normal.txt'
        #path match
        self.path_match_dir = self.dataset + 'data_path_match/'
        self.model_file = self.path_match_dir + "models/"
        self.question_match_dir = self.dataset + 'data_question_match/'
        self.question_model_file = self.question_match_dir + "models/"
        #oracle
        self.grounded_graph_file = self.dataset + "/oracle_grounded_graph_graphq/"
        self.ngram_el = self.dataset + '2018.02.25_graphq_test_ngram_el.txt'
        self.ngram_el_qid_to_position_grounding_result_dict = read_ngram_el_grounding_result(self.ngram_el)
