# SPARQA: a question answering system over knowledge bases

Code and dataset for paper: "SPARQA: Skeleton-based Semantic Parsing for Complex Questions over Knowledge Bases" (AAAI-2020). 

## Paper Abstract:
> Semantic parsing transforms a natural language question into a formal query over a knowledge base. Many existing methods rely on syntactic parsing like dependencies. However, the accuracy of producing such expressive formalisms is not satisfying on long complex questions. In this paper, we propose a novel skeleton grammar to represent the high-level structure of a complex question. This dedicated coarse-grained formalism with a BERT-based parsing algorithm helps to improve the accuracy of the downstream fine-grained semantic parsing. Besides, to align the structure of a question with the structure of a knowledge base, our multi-strategy method combines sentence-level and word-level semantics. Our approach shows promising performance on several datasets.

Please, refer to the paper for more the model description and training details. Preprint: [https://arxiv.org/pdf/2003.13956.pdf](https://arxiv.org/pdf/2003.13956.pdf) 

## Project Structure:

<table>
    <tr>
        <th>File</th><th>Description</th>
    </tr>
    <tr>
        <td>code</td><td>SPARQA codes</td>
    </tr>
    <tr>
        <td>dataset</td><td>QA datasets and resouces for entity linking</td>
    </tr>
    <tr>
        <td>skeleton</td><td>Skeleton bank of 10K complex questions</td>
    </tr>
    <tr>
        <td>slides</td><td>SPARQA slides and poster</td>
    </tr>
</table>
 
## Dataset
It contains two public datasets involving complex questions: GraphQuestions and ComplexWebQuestions.
Also, it contains resources for entity linking or candidate grounded query ranking.

## Skeleton
It is a complex questions skeleton bank by manually annotation. It contains about 10K questions (5,166 questions and 5000 questions from ComplexWebQuestions). We make this resource public to supporch future research (question understanding or semanatic parsing research).

## Requirements
* Python 3.6
* PyTorch 1.3.0+ - [read here about installation](http://pytorch.org/)
* See `requirements.txt` for the full list of packages
* A running instance of the Stanford CoreNLP server (https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) for dependency parsing and NE recognition. Do not forget to download English model. Replace the address in configution with URL of your CoreNLP instance.
* A running instance of the python wrapper for Stanford CoreNLP's SUTime Java library. [read here about installation](https://github.com/FraBle/python-sutime)
* To set up a virtuoso graph database to store and query Freebase latest version for ComplexWebQuestions [read here about installation](https://developers.google.com/freebase)
* To set up a virtuoso graph database to store and query Freebase 2013 version for ComplexQuestion [read here about installation](https://github.com/percyliang/sempre)

## Resources
* Lexicons for Entity Linking and Disambigution of Freebase latest version and Freebase 2013 version. We will provide Google dive URI to get the lexicons. [read here](https://drive.google.com/open?id=1AW5rT5MaZrDkc2rNz0TZhDJaQVQwJgT4).
** Entity lexicons from ClubWeb and Freebase entity literal or alias.
** Freebase schema
* GloVe embedding (glove.6B.300d) [read here about download](https://nlp.stanford.edu/projects/glove/)

## How to run SPARQA pipeline
SPARQA pipeline has two steps for answering questions: (1) KB-indenpendent graph-structured ungrounded query generation. (2) KB-dependent graph-structure grounded query generation and ranking. (also, retrieve knowledge base). Below, I will describe how to run our SPARQA by step-to-step.

### step 1 KB-indenpendent query generation
* step 1.1 Skeleton Parsing
* step 1.2 Node Recognition
* step 1.3 Relation Extraction

### step 2 KB-dependent query generation
* step 2.1 Variant Generation
* step 2.2 Grounding
* step 2.3 Multi-Strategy Scoring
  
## Citation

    SPARQA: Skeleton-based Semantic Parsing for Complex Questions over Knowledge Bases, AAAI-2020

## Contacts
If you have any difficulty or questions in running codes, reproducing experimental results, and skeleton parsing, please email to me (ywsun@smail.nju.edu.cn).
