import torch
from tqdm import tqdm
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from parsing.models.pytorch_pretrained_bert.tokenization import BertTokenizer
from parsing.models.pytorch_pretrained_bert.modeling import BertForQuestionAnswering
from parsing.models.fine_tuning_based_on_bert.run_headword_span \
    import read_one_example, convert_examples_to_features, RawResult, write_span_headwords_with_nbest
from parsing.models import model_utils
from parsing.parsing_args import bert_args

args = model_utils.run_redundancy_span_get_local_args()
model_file = bert_args.fine_tuning_headword_squad_F_model
tokenizer = BertTokenizer.from_pretrained(args.bert_model)
model_state_dict = torch.load(model_file, map_location='cpu')
model = BertForQuestionAnswering.from_pretrained(args.bert_model, state_dict=model_state_dict)
device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
model.to(device)

def simple_process(question, span):
    '''process one sequence, such as question'''
    eval_examples = read_one_example(paragraph=question, question=span)
    eval_features = convert_examples_to_features(examples=eval_examples, tokenizer=tokenizer,
            max_seq_length=args.max_seq_length, doc_stride=args.doc_stride,
            max_query_length=args.max_query_length, is_training=False)
    all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
    all_example_index = torch.arange(all_input_ids.size(0), dtype=torch.long)
    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_example_index)
    # Run prediction for full data
    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.predict_batch_size)
    model.eval()
    all_results = []
    # logger.info("Start evaluating")
    for input_ids, input_mask, segment_ids, example_indices in tqdm(eval_dataloader, desc="Evaluating"):
        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)
        with torch.no_grad():
            batch_start_logits, batch_end_logits = model(input_ids=input_ids, token_type_ids=segment_ids, attention_mask=input_mask)
        for i, example_index in enumerate(example_indices):
            start_logits = batch_start_logits[i].detach().cpu().tolist()
            end_logits = batch_end_logits[i].detach().cpu().tolist()
            eval_feature = eval_features[example_index.item()]
            unique_id = int(eval_feature.unique_id)
            all_results.append(RawResult(unique_id=unique_id, start_logits=start_logits, end_logits=end_logits))
    span, nbest_json = write_span_headwords_with_nbest(eval_examples, eval_features, all_results,
                          args.n_best_size, args.max_answer_length, args.do_lower_case, args.verbose_logging)
    return span, nbest_json


if __name__ == "__main__":
    span, nbest_json = simple_process(question='What is the language spoken in Switzerland that is mostly spoken in Italy ?', span='in Italy')
    print (span)
    # print (nbest_json) [OrderedDict([('text', 'owner'), ('text_index', 3), ('probability', 0.7110507253704911),
    # ('start_logit', -7.255896091461182), ('end_logit', -6.328417778015137)]),
    # OrderedDict([('text', 'station'), ('text_index', 6), ('probability', 0.22272930211485184),
