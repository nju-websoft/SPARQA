# SPARQA

Code and dataset for paper: "SPARQA: Skeleton-based Semantic Parsing for Complex Questions over Knowledge Bases" [preprint](https://arxiv.org/pdf/2003.13956.pdf) (AAAI-2020).

## Dataset
It contains two public datasets involving complex questions: GraphQuestions and ComplexWebQuestions.
Also, it contains resources for entity linking or candidate grounded query ranking.

## Skeleton
It is a complex questions skeleton bank by manually annotation. It contains about 10K questions (5,166 questions and 5000 questions from ComplexWebQuestions). We make this resource public to supporch future research (question understanding or semanatic parsing research).

## Dependencies

sklearn
corenlp
pytorch
SPARQLWrapper
pyodbc
nltk
fuzzywuzzy
SUTime
virtuoso

## Run
SPARQA pipeline has two steps for answering questions: (1) KB-indenpendent graph-structured ungrounded query generation. (2) KB-dependent graph-structure grounded query generation and ranking. (also, retrieve knowledge base). Below, I will describe how to run our SPARQA by step-to-step.

### step 1

### step 2

#### step 2.1

#### step 2.2

#### step 2.3


## Citation

    SPARQA: Skeleton-based Semantic Parsing for Complex Questions over Knowledge Bases, AAAI-2020

If you have any difficulty or questions in running code, reproducing experimental results, and skeleton parsing, please email to me (ywsun@smail.nju.edu.cn).
