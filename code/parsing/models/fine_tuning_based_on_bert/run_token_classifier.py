"""BERT finetuning runner."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
import mmap
import csv
import os
import random
from tqdm import tqdm, trange
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.distributed import DistributedSampler
#-----------------------------------
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
os.environ['CUDA_VISIBLE_DEVICES']='2'
#------------------------------------------------
from parsing.models.pytorch_pretrained_bert.tokenization import BertTokenizer
from parsing.models.pytorch_pretrained_bert.modeling import BertForTokenClassification
from parsing.models.pytorch_pretrained_bert.optimization import BertAdam
from parsing.models.pytorch_pretrained_bert.file_utils import PYTORCH_PRETRAINED_BERT_CACHE
from parsing.models import model_utils
###############################################

class InputExample(object):
    """A single training/test example for simple sequence classification."""
    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.
        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label

class InputFeatures(object):
    """A single set of features of data."""
    def __init__(self, input_ids, input_mask, segment_ids, label_ids):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_ids = label_ids

###############################################

class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""
    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()
    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()
    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()
    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with open(input_file, "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                lines.append(line)
            return lines
    @classmethod
    def _read_line_data(cls, input_file):
        '''read 'what amenities are provided in the lanna thai restaurant ?\tO I O O O O I I I O' '''
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = []
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            line = mm.readline()
            while line:
                tmp_list = line.decode().replace('\r\n', '').replace('\n', '').split('\t')
                if len(tmp_list) >= 2:
                    lines.append([tmp_list[1], tmp_list[0]])
                line = mm.readline()
        mm.close()
        f.close()
        return lines
    # @classmethod
    # def _read_data(cls, input_file):
    #     """Reads a BIO data."""
    #     with open(input_file) as f:
    #         lines = []
    #         words = []
    #         labels = []
    #         for line in f:
    #             contends = line.strip()
    #             word = line.strip().split(' ')[0]
    #             label = line.strip().split(' ')[-1]
    #             if contends.startswith("-DOCSTART-"):
    #                 words.append('')
    #                 continue
    #             if len(contends) == 0 and words[-1] == '.':
    #                 l = ' '.join([label for label in labels if len(label) > 0])
    #                 w = ' '.join([word for word in words if len(word) > 0])
    #                 lines.append([l, w])
    #                 words = []
    #                 labels = []
    #                 continue
    #             words.append(word)
    #             labels.append(label)
    #         return lines

class NodeRecogniationProcessor(DataProcessor):

    def get_sequence_example(self,sequence):
        guid = "%s-%s" % ('test', 0)
        # text = tokenizer.convert_to_unicode(line[1])
        # label = tokenization.convert_to_unicode(line[0])
        text_a = sequence
        return InputExample(guid=guid, text_a=text_a, text_b=None, label=None)

    def get_train_examples(self, data_dir):
        return self._create_example(
            self._read_line_data(os.path.join(data_dir, "train.txt")), "train")

    def get_dev_examples(self, data_dir):
        return self._create_example(
            self._read_line_data(os.path.join(data_dir, "dev.txt")), "dev")

    def get_test_examples(self,data_dir):
        return self._create_example(
            self._read_line_data(os.path.join(data_dir, "test.txt")), "test")

    def get_labels(self):
        # return ["0", "I", "X", "[CLS]", "[SEP]", "comparative", "class", "entity",
        # "count", "literal", "relation", "target", "superlative", "neg"]
        #"0", "I", "X", "[CLS]", "[SEP]", "comparative", "class", "entity",
        # "count", "literal", "relation", "target", "superlative", "neg"
        return ["O", "X", "[CLS]", "[SEP]", "class", "entity", "literal"]

    def _create_example(self, lines, set_type):
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            # text = tokenizer.convert_to_unicode(line[1])
            # label = tokenization.convert_to_unicode(line[0])
            text_a = line[1]
            label = line[0]
            examples.append(InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
        return examples

###############################################

def convert_example_to_features_for_test(example, max_seq_length, tokenizer):
    """Loads a data file into a list of `InputBatch`s."""
    features = []
    tokens = []
    labels_temp = []
    for i, word in enumerate(example.text_a.split(' ')):
        token_wordpiece = tokenizer.tokenize(word)  #04/26/1882 ['04', '/', '26', '/', '1882']
        tokens.extend(token_wordpiece)
        for m in range(len(token_wordpiece)):
            if m == 0:
                labels_temp.append(0)
            else:
                labels_temp.append('X')
    # max_seq_length-1
    if len(tokens) >= max_seq_length - 1:
        tokens = tokens[0:(max_seq_length - 2)]
        labels_temp = labels_temp[0:(max_seq_length - 2)]

    ntokens = []
    new_labels_temp = []
    segment_ids = []

    ntokens.append('[CLS]')
    new_labels_temp.append('[CLS]')
    segment_ids.append(0)
    for i, token in enumerate(tokens):
        ntokens.append(token)
        new_labels_temp.append(labels_temp[i])
        segment_ids.append(0)
    ntokens.append('[SEP]')
    new_labels_temp.append('[SEP]')
    segment_ids.append(0)
    input_ids = tokenizer.convert_tokens_to_ids(ntokens)
    input_mask = [1] * len(input_ids)

    #if the length is short, tianbu 0
    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)
        #we do not concerned about it
        ntokens.append('NULL')

    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length

    features.append(InputFeatures(input_ids=input_ids, input_mask=input_mask, segment_ids=segment_ids, label_ids=None))
    return features, new_labels_temp

def convert_examples_to_features_for_train(examples, label_list, max_seq_length, tokenizer):
    """Loads a data file into a list of `InputBatch`s."""
    label_map = {label : i for i, label in enumerate(label_list)} #label -> i  index dictionary
    features = []
    for (ex_index, example) in enumerate(examples):
        label_list = example.label.split(' ')

        tokens = []
        labels = []
        for i, word in enumerate(example.text_a.split(' ')): #textlist
            token_wordpiece = tokenizer.tokenize(word)
            tokens.extend(token_wordpiece)
            label_current = label_list[i]
            for m in range(len(token_wordpiece)):
                if m == 0:
                    labels.append(label_current)
                else:
                    labels.append('X')

        # max_seq_length-1
        if len(tokens) >= max_seq_length - 1:
            tokens = tokens[0:(max_seq_length - 2)]
            labels = labels[0:(max_seq_length - 2)]

        ntokens = []
        segment_ids = []
        label_ids = []

        ntokens.append('[CLS]')
        segment_ids.append(0)
        label_ids.append(label_map['[CLS]'])
        # print(tokens, labels)
        for i, token in enumerate(tokens):
            ntokens.append(token)
            segment_ids.append(0)
            label_ids.append(label_map[labels[i]])

        ntokens.append('[SEP]')
        segment_ids.append(0)
        label_ids.append(label_map['[SEP]'])

        input_ids = tokenizer.convert_tokens_to_ids(ntokens)
        input_mask = [1] * len(input_ids)

        #if the length is short, tianbu 0
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)
            #we do not concerned about it
            label_ids.append(0)
            ntokens.append('NULL')

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length

        features.append(InputFeatures(input_ids=input_ids, input_mask=input_mask, segment_ids=segment_ids, label_ids=label_ids))
    return features

###############################################

def main(args=None):
    if args is None:
        args = model_utils.run_token_classifier_get_local_args()
    # task_name = 'ner'
    # task_name = 'importantwords'
    # task_name = 'headword'
    task_name = 'node_recognition'
    processors = {
        # "ner": NerProcessor,
        # "importantwords": ImportantwordRecogniationProcessor,
        # "headword": HeadwordProcessor
        "node_recognition": NodeRecogniationProcessor,
    }
    num_labels_task = {
        # "ner" : len(processor.get_labels()),
        # "importantwords": len(processor.get_labels()),
        # "headword": len(processor.get_labels())
        "node_recognition": 7,
    }

    if args.local_rank == -1 or args.no_cuda:
        device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
        n_gpu = torch.cuda.device_count()
    else:
        torch.cuda.set_device(args.local_rank)
        device = torch.device("cuda", args.local_rank)
        n_gpu = 1
        # Initializes the distributed backend which will take care of sychronizing nodes/GPUs
        torch.distributed.init_process_group(backend='nccl')
    # logger.info("device: {} n_gpu: {}, distributed training: {}, 16-bits training: {}".format(
    #     device, n_gpu, bool(args.local_rank != -1), args.fp16))
    if args.gradient_accumulation_steps < 1:
        raise ValueError("Invalid gradient_accumulation_steps parameter: {}, should be >= 1".format(args.gradient_accumulation_steps))

    args.train_batch_size = int(args.train_batch_size / args.gradient_accumulation_steps)
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

    if not args.do_train and not args.do_eval:
        raise ValueError("At least one of `do_train` or `do_eval` must be True.")
    if os.path.exists(args.output_dir) and os.listdir(args.output_dir):
        raise ValueError("Output directory ({}) already exists and is not empty.".format(args.output_dir))
    os.makedirs(args.output_dir, exist_ok=True)

    # task_name = args.task_name.lower()
    if task_name not in processors:
        raise ValueError("Task not found: %s" % (task_name))
    processor = processors[task_name]()
    num_labels = num_labels_task[task_name]
    label_list = processor.get_labels()

    tokenizer = BertTokenizer.from_pretrained(args.bert_model, do_lower_case=args.do_lower_case)

    train_examples = None
    num_train_steps = None
    if args.do_train:
        train_examples = processor.get_train_examples(args.data_dir)
        num_train_steps = int(len(train_examples) / args.train_batch_size / args.gradient_accumulation_steps * args.num_train_epochs)

    # Prepare model
    model = BertForTokenClassification.from_pretrained(
              args.bert_model,
              cache_dir=PYTORCH_PRETRAINED_BERT_CACHE / 'distributed_{}'.format(args.local_rank),
              num_labels=num_labels)
    if args.fp16:
        model.half()
    model.to(device)
    if args.local_rank != -1:
        try:
            from apex.parallel import DistributedDataParallel as DDP
        except ImportError:
            raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use distributed and fp16 training.")
        model = DDP(model)
    elif n_gpu > 1:
        model = torch.nn.DataParallel(model)

    # Prepare optimizer
    param_optimizer = list(model.named_parameters())
    no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]
    t_total = num_train_steps
    if args.local_rank != -1:
        t_total = t_total // torch.distributed.get_world_size()
    if args.fp16:
        try:
            from apex.optimizers import FP16_Optimizer
            from apex.optimizers import FusedAdam
        except ImportError:
            raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use distributed and fp16 training.")
        optimizer = FusedAdam(optimizer_grouped_parameters,
                              lr=args.learning_rate,
                              bias_correction=False,
                              max_grad_norm=1.0)
        if args.loss_scale == 0:
            optimizer = FP16_Optimizer(optimizer, dynamic_loss_scale=True)
        else:
            optimizer = FP16_Optimizer(optimizer, static_loss_scale=args.loss_scale)

    else:
        optimizer = BertAdam(optimizer_grouped_parameters,
                             lr=args.learning_rate,
                             warmup=args.warmup_proportion,
                             t_total=t_total)
    global_step = 0
    if args.do_train:
        train_features = convert_examples_to_features_for_train(train_examples, label_list, args.max_seq_length, tokenizer)
        all_input_ids = torch.tensor([f.input_ids for f in train_features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in train_features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in train_features], dtype=torch.long)
        all_label_ids = torch.tensor([f.label_ids for f in train_features], dtype=torch.long)
        train_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
        if args.local_rank == -1:
            train_sampler = RandomSampler(train_data)
        else:
            train_sampler = DistributedSampler(train_data)
        train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=args.train_batch_size)

        model.train()
        for _ in trange(int(args.num_train_epochs), desc="Epoch"):
            tr_loss = 0
            nb_tr_examples, nb_tr_steps = 0, 0
            for step, batch in enumerate(tqdm(train_dataloader, desc="Iteration")):
                batch = tuple(t.to(device) for t in batch)
                input_ids, input_mask, segment_ids, label_ids = batch
                loss = model(input_ids=input_ids, token_type_ids=segment_ids, attention_mask=input_mask, labels=label_ids)
                if n_gpu > 1:
                    loss = loss.mean() # mean() to average on multi-gpu.
                if args.gradient_accumulation_steps > 1:
                    loss = loss / args.gradient_accumulation_steps

                if args.fp16:
                    optimizer.backward(loss)
                else:
                    loss.backward()

                tr_loss += loss.item()
                nb_tr_examples += input_ids.size(0)
                nb_tr_steps += 1
                if (step + 1) % args.gradient_accumulation_steps == 0:
                    # modify learning rate with special warm up BERT uses
                    lr_this_step = args.learning_rate * model_utils.warmup_linear(global_step/t_total, args.warmup_proportion)
                    for param_group in optimizer.param_groups:
                        param_group['lr'] = lr_this_step
                    optimizer.step()
                    optimizer.zero_grad()
                    global_step += 1

    # Save a trained model
    model_to_save = model.module if hasattr(model, 'module') else model  # Only save the model it-self
    output_model_file = os.path.join(args.output_dir, "pytorch_model.bin")
    torch.save(model_to_save.state_dict(), output_model_file)

    # Load a trained model that you have fine-tuned
    model_state_dict = torch.load(output_model_file)
    model = BertForTokenClassification.from_pretrained(args.bert_model, state_dict=model_state_dict, num_labels=num_labels)
    model.to(device)

    if args.do_eval and (args.local_rank == -1 or torch.distributed.get_rank() == 0):
        eval_examples = processor.get_dev_examples(args.data_dir)
        eval_features = convert_examples_to_features_for_train(eval_examples, label_list, args.max_seq_length, tokenizer)
        all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
        all_label_ids = torch.tensor([f.label_ids for f in eval_features], dtype=torch.long)
        eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
        # Run prediction for full data
        eval_sampler = SequentialSampler(eval_data)
        eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)

        model.eval()
        eval_loss, eval_accuracy = 0, 0
        nb_eval_steps, nb_eval_examples = 0, 0
        for input_ids, input_mask, segment_ids, label_ids in eval_dataloader:  #8*128
            input_ids = input_ids.to(device)
            input_mask = input_mask.to(device)
            segment_ids = segment_ids.to(device)
            label_ids = label_ids.to(device)

            with torch.no_grad():
                # tmp_eval_loss = model(input_ids=input_ids, token_type_ids=segment_ids, attention_mask=input_mask, labels=label_ids)
                logits = model(input_ids=input_ids, token_type_ids=segment_ids, attention_mask=input_mask)

            logits = logits.detach().cpu().numpy()  #[batch_size, sequence_length, num_labels].  #2*128*label_num_size
            label_ids = label_ids.to('cpu').numpy()
            #---------------------------------------------
            # outputs = np.argmax(logits, axis=2)
            # print('#outputs:\t', outputs.shape)
            # print('#label_ids:\t', label_ids.shape)
            # [rows, cols] = outputs.shape
            # print(rows, cols)
            # for x_axis in range(rows):
            #     sequence_output = outputs[x_axis]
            #     labels = label_ids[x_axis]
                # print(sequence_output, labels)
            #---------------------------------------------
            tmp_eval_accuracy = model_utils.token_classifier_accuracy(logits, label_ids)
            # eval_loss += tmp_eval_loss.mean().item()
            eval_accuracy += tmp_eval_accuracy
            nb_eval_examples += input_ids.size(0) * input_ids.size(1)
            nb_eval_steps += 1
        eval_loss = eval_loss / nb_eval_steps
        eval_accuracy = eval_accuracy / nb_eval_examples
        result = {'eval_loss': eval_loss,
                  'eval_accuracy': eval_accuracy,
                  'global_step': global_step,
                  'loss': tr_loss/nb_tr_steps}
        output_eval_file = os.path.join(args.output_dir, "eval_results.txt")
        with open(output_eval_file, "w") as writer:
            for key in sorted(result.keys()):
                writer.write("%s = %s\n" % (key, str(result[key])))

if __name__ == "__main__":
    main()
