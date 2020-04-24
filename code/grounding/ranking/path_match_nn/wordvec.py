import time
import torch
from grounding.grounding_args import glove_file
from grounding.grounding_utils import load_word2vec_format

class WordEmbedding():

    def __init__(self):
        # self.pretrained = dict()
        self.pretrained = load_word2vec_format(glove_file)
        self.train_generation_embedding = dict()
        self.ten = torch.Tensor(len(self.pretrained), len(list(self.pretrained.values())[0]))
        for i, val in enumerate(list(self.pretrained.values())):
            self.ten[i] = val
        self.scale = torch.std(self.ten)
        # self.scale =1

    def get_word_embedding(self,word):
        random_range = (-self.scale, self.scale)
        if word in self.pretrained:
            return self.pretrained[word]
        elif word in self.train_generation_embedding:
            return self.train_generation_embedding[word]
        else:
            self.train_generation_embedding[word]=torch.Tensor(300)
            torch.nn.init.uniform(self.train_generation_embedding[word],random_range[0], random_range[1])
            return self.train_generation_embedding[word]
