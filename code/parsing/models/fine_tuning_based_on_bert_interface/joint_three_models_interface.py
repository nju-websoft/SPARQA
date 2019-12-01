import torch

from tqdm import tqdm
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from parsing.models.pytorch_pretrained_bert.tokenization import BertTokenizer
from parsing.models.pytorch_pretrained_bert.modeling import BertForSpanWithHeadwordWithLabel
from parsing.models import model_utils
from parsing.models.fine_tuning_based_on_bert.run_joint_three_models import read_one_example, \
    convert_examples_to_features, RawResult, write_span_headwords_with_nbest
from parsing.parsing_args import bert_args

labels_list = ["nmod", "conj", "acl:cl", "acl", "nmod:poss", "advcl", "xcomp"]
ids_label_map = {i: label for i, label in enumerate(labels_list)}
num_labels = len(labels_list)
args = model_utils.run_joint_three_models_get_local_args()
model_file = bert_args.fine_tuning_joint_threemodels_A_model

tokenizer = BertTokenizer.from_pretrained(args.bert_model)
model_state_dict = torch.load(model_file, map_location='cpu')
model = BertForSpanWithHeadwordWithLabel.from_pretrained(args.bert_model, state_dict=model_state_dict, num_labels=num_labels)
device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
model.to(device)

def simple_process(paragraph):
    '''process one sequence, such as question'''
    eval_examples = read_one_example(paragraph)
    eval_features = convert_examples_to_features(
        examples=eval_examples, label_list=labels_list,
        tokenizer=tokenizer, max_seq_length=args.max_seq_length,
        doc_stride=args.doc_stride, max_query_length=args.max_query_length,
        is_training=False)
    all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
    all_example_index = torch.arange(all_input_ids.size(0), dtype=torch.long)
    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_example_index)
    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.predict_batch_size)
    model.eval()
    all_results = []
    for input_ids, input_mask, segment_ids, example_indices in tqdm(eval_dataloader, desc="Evaluating"):
        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)
        with torch.no_grad():
            batch_start_logits, batch_end_logits, batch_headword_logits, batch_label_logits \
                = model(input_ids=input_ids, token_type_ids=segment_ids, attention_mask=input_mask)
        for i, example_index in enumerate(example_indices):
            start_logits = batch_start_logits[i].detach().cpu().tolist()
            end_logits = batch_end_logits[i].detach().cpu().tolist()
            headword_logits = batch_headword_logits[i].detach().cpu().tolist()
            label_logits = batch_label_logits[i].detach().cpu().tolist()
            eval_feature = eval_features[example_index.item()]
            unique_id = int(eval_feature.unique_id)
            # print('#token to orig map:\t', eval_feature.token_to_orig_map)
            # print('#tokens:\t', eval_feature.tokens)
            # print('#doc token:\t', eval_feature.doc_tokens)
            all_results.append(RawResult(
                unique_id=unique_id, start_logits=start_logits, end_logits=end_logits, headword_logits=headword_logits, label_logits=label_logits))
    span, headword, label_id, nbest_json = write_span_headwords_with_nbest(
        eval_examples, eval_features, all_results, args.n_best_size, args.max_answer_length, args.do_lower_case, args.verbose_logging)
    return span, headword, ids_label_map[int(label_id)], nbest_json

if __name__ == "__main__":
    question = 'In which city is the headquarter of Air China ?'
    question = 'What Greek Mythology movie does Logan Lerman play in ?'
    span, headword, label_id, nbest_json = simple_process(paragraph=question)
    print (question)
    print (span)    #of Air China
    print (headword)  #5
    print (label_id)  #nmod
