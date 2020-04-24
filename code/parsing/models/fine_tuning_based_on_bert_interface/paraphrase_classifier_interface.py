import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from parsing.models import model_utils
from parsing.models.fine_tuning_based_on_bert.run_sequence_classifier import ParaphraseProcess, convert_examples_to_features
from parsing.models.pytorch_pretrained_bert import BertTokenizer
from parsing.models.pytorch_pretrained_bert.modeling import BertForSequenceClassification
from parsing.parsing_args import bert_args

num_labels_task = {"paraphrase":2}
processors = {"paraphrase": ParaphraseProcess}
task_name = "paraphrase"
args = model_utils.run_sequence_classifier_get_local_args()

processor = processors[task_name]()
label_list = processor.get_labels()
num_labels = num_labels_task[task_name]
tokenizer = BertTokenizer.from_pretrained(bert_args.bert_base_cased_tokenization, do_lower_case=args.do_lower_case)
# label_ids_map = {label: i for i, label in enumerate(label_list)}
ids_label_map = {i: label for i, label in enumerate(label_list)}

bert_fine_tuning_filepath = bert_args.fine_tuning_paraphrase_classifier_G_model
model_state_dict = torch.load(bert_fine_tuning_filepath, map_location='cpu')
model = BertForSequenceClassification.from_pretrained(args.bert_model, state_dict=model_state_dict, num_labels=num_labels)
device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
model.to(device)

def process(line_a, line_b=None):
    eval_examples = processor.get_simple_examples(line_a=line_a, line_b=line_b)
    eval_features = convert_examples_to_features(eval_examples, label_list, args.max_seq_length, tokenizer)
    all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
    all_label_ids = torch.tensor([f.label_id for f in eval_features], dtype=torch.long)
    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)
    model.eval()
    outputs = []
    logits = None
    for input_ids, input_mask, segment_ids, label_ids in eval_dataloader:
        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)
        with torch.no_grad():
            logits = model(input_ids, segment_ids, input_mask)
        logits = logits.detach().cpu().numpy()
        # print (logits) #[[ 0.6952358  -1.1702355  -1.8215117  -1.1374489   3.9811454  -0.49839512]]
        outputs = np.argmax(logits, axis=1)
    return logits, outputs[0] #paraphrase:logits[0][1]


if __name__ == "__main__":
    paraphrase_label = process(line_a='river end where originates Lake Itasca', line_b='outflow lake containedby partially location')
    print(paraphrase_label)

