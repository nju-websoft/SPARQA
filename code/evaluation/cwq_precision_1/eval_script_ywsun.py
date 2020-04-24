from evaluation.cwq_precision_1.eval_script import compare_span_to_answer, compute_P1, get_answers_names
import json
import pandas as pd

def evaluate(dataset_df, predictions):
    if len(dataset_df) != len(predictions):
        print('predictions file does not match dataset file number of examples!!!')
    P1 = 0
    for prediction in predictions:  #遍历prediction
        '''{
                "ID": "WebQTest-1311_a7365b8c3109f401f4cd077c706e4104",
                "answers": [
                {
                    "answer": "Belgium", 
                    "answer_id": "m.0154j", 
                    "aliases": [
                        "Belgique", 
                        "Belgi\u00eb", 
                        "Kingdom of Belgium"
                    ]
                }
               ] 
           },
        '''
        golden_answer_list = []  #把ID对应的所有的标准答案的label和aliases都标注出来
        for answer in dataset_df.loc[prediction['ID'], 'answers']:
            '''
            "answers": [
                {
                    "answer": "Belgium", 
                    "answer_id": "m.0154j", 
                    "aliases": [
                        "Belgique", 
                        "Belgi\u00eb", 
                        "Kingdom of Belgium"
                    ]
                }
            ] 
            '''
            golden_answer_list.append(answer['answer'])
            golden_answer_list += answer['aliases']

        if not None in golden_answer_list: #如果存在正确的答案, 则统计
            system_answer_names = get_answers_names(prediction['answers'])  #只取第一个实体的label和alias信息
            matched_answers = compare_span_to_answer(system_answer_names, golden_answer_list, dataset_df.loc[prediction['ID'], 'question'])
            curr_P1 = compute_P1(matched_answers, golden_answer_list, prediction['answers']) #如果matched_answers > 0, 则P1=100
            P1 += curr_P1
    print(P1, len(dataset_df))
    return P1/len(dataset_df)


if __name__ == '__main__':
    dataset_file_path = './ComplexWebQuestions_test.json'
    prediction_file_path = './prediction/sparqa_wo_wordlevel_prediction_test_wit_names.json'

    with open(dataset_file_path) as dataset_file:
        dataset_df = pd.DataFrame(json.load(dataset_file)).set_index('ID')
    with open(prediction_file_path) as prediction_file:
        predictions = json.load(prediction_file)
    print(json.dumps(evaluate(dataset_df, predictions)))
