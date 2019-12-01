from parsing.parsing_args import bert_args
from parsing.models.fine_tuning_based_on_bert.run_token_classifier import NodeRecogniationProcessor, convert_example_to_features_for_test
from parsing.models import model_utils
import sys
import os
import random
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from parsing.models.pytorch_pretrained_bert.tokenization import BertTokenizer
from parsing.models.pytorch_pretrained_bert.modeling import BertForTokenClassification
#------------------------------------------------
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
# print (sys.path)
os.environ['CUDA_VISIBLE_DEVICES']='2'
#------------------------------------------------

task_name = 'node_recognition'
args = model_utils.run_token_classifier_get_local_args()
processors = {
    "node_recognition": NodeRecogniationProcessor,
}
num_labels_task = {
    "node_recognition": 7 ,#len(processor.get_labels()),
}

processor = processors[task_name]()
device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
random.seed(args.seed)
np.random.seed(args.seed)
torch.manual_seed(args.seed)

num_labels = num_labels_task[task_name]
label_list = processor.get_labels()
label_ids_map = {label: i for i, label in enumerate(label_list)}
ids_label_map = {i: label for i, label in enumerate(label_list)}

tokenizer = BertTokenizer.from_pretrained(bert_args.bert_base_cased_tokenization, do_lower_case=args.do_lower_case)

model_state_dict = torch.load(bert_args.fine_tuning_token_classifier_C_model, map_location='cpu')
model = BertForTokenClassification.from_pretrained(bert_args.bert_base_cased_model, state_dict=model_state_dict, num_labels=num_labels)
model.to(device)

def process(sequence):
    eval_example = processor.get_sequence_example(sequence)
    eval_features, new_labels_temp = convert_example_to_features_for_test(eval_example, args.max_seq_length, tokenizer)
    all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)
    model.eval()
    result_sequence = None
    for input_ids, input_mask, segment_ids in eval_dataloader:  #8*128
        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)
        with torch.no_grad():
            logits = model(input_ids=input_ids, token_type_ids=segment_ids, attention_mask=input_mask)
        logits = logits.detach().cpu().numpy()  #[batch_size, sequence_length, num_labels].  #2*128*label_num_size
        #---------------------------------------------
        outputs = np.argmax(logits, axis=2)
        [rows, _] = outputs.shape
        for x_axis in range(rows):
            sequence_output = outputs[x_axis]
            result_sequence = model_utils.ner_prediction_sequence(ids_label_map=ids_label_map, outputs=sequence_output)
    return model_utils.ner_postprocess(result_sequence, new_labels_temp)

if __name__ == "__main__":
    print(process('Where was the main artist featured in the Rihanna : Live in Concert Tour raised ?'))

####################################
# "headword": 5 # task_name = 'headword'     # "headword": HeadwordProcessor
