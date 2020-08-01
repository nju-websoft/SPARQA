# SPARQA: a question answering system over knowledge bases

Code and dataset for paper: "SPARQA: Skeleton-based Semantic Parsing for Complex Questions over Knowledge Bases" (AAAI-2020).

If you meet any question, please email to him (ywsun@smail.nju.edu.cn).

## Paper Abstract:
> Semantic parsing transforms a natural language question into a formal query over a knowledge base. Many existing methods rely on syntactic parsing like dependencies. However, the accuracy of producing such expressive formalisms is not satisfying on long complex questions. In this paper, we propose a novel skeleton grammar to represent the high-level structure of a complex question. This dedicated coarse-grained formalism with a BERT-based parsing algorithm helps to improve the accuracy of the downstream fine-grained semantic parsing. Besides, to align the structure of a question with the structure of a knowledge base, our multi-strategy method combines sentence-level and word-level semantics. Our approach shows promising performance on several datasets.

Please, refer to the paper for more the model description and training details.[the paper](https://www.aaai.org/Papers/AAAI/2020GB/AAAI-SunY.3419.pdf)

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

## Resources Preparation (occur error if not prepare the resources and lexicons)
* Root datasets: default value D:/dataset. You can edit it in the configution globals_args.py. 
* GloVe embedding (glove.6B.300d) [download here](https://nlp.stanford.edu/projects/glove/)
* Stanford CoreNLP server. The sever version we use is stanford-corenlp-full-2018-10-05. download [here](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html), get started, and replace ip_port address in globals_args.py with URL of your CoreNLP.
* Python wrapper for Stanford CoreNLP's SUTime Java library. download [here](https://github.com/FraBle/python-sutime)). SPARQA need to use the Java library. default save in the folder: root/resource_sutime/. if you save other place, remember to replace the address sutime_jar_files in configution with your folder path.
* Four files (stopwords.txt, ordinal_fengli.tsv, unimportantphrase, and unimportantwords) [download here](https://drive.google.com/open?id=1AW5rT5MaZrDkc2rNz0TZhDJaQVQwJgT4). download the file, and saves in the root (default. you can edit these addresses).
* To access interface virtuoso server, you need configure odbc address (freebase_pyodbc_info) in globals_args.py.
* To access interface virtuoso html service, you need configure html address (freebase_sparql_html_info) in globals_args.py.
* BERT pre-trained Models [download here](https://drive.google.com/drive/folders/1tlUF7ALLLXiHu280gPdlVyQlGvJFklGC) and save the seven files in the default root/pre_train_models address in the configuration bert.args.py (you can edit these addresses).
* CWQ 1.1 five BERT pre-trained Models for Skeleton Parsing. [download here](https://drive.google.com/drive/folders/1t4Rb2feVOSGF_5lRBHwrB_GfxyL2rqby) and save the five files in the default root/dataset_cwq_1_1 address in the configuration bert.args.py (you can edit these addresses).
* GraphQuestions five BERT pre-trained Models for Skeleton Parsing. [download here](https://drive.google.com/drive/folders/1Mjpan599INCVRgRQTsirgVdyt29iKblO) and save the five files in the default root/dataset_graphquestions address in the configuration bert.args.py (you can edit these addresses).
* Entity-related Lexicons and schema-related lexicons of Freebase latest version. [download here](https://drive.google.com/drive/folders/1t4Rb2feVOSGF_5lRBHwrB_GfxyL2rqby). Specificaly, the files variables in KB_Freebase_Latest class in the configuration kb_name.py.
* Entity-related Lexicons and schema-related lexicons of Freebase 2013 version. [download here](https://drive.google.com/drive/folders/1Mjpan599INCVRgRQTsirgVdyt29iKblO). Specificaly, the files variables in KB_Freebase_en_2013 class in the configuration kb_name.py.



## How to run SPARQA pipeline
SPARQA pipeline has two steps for answering questions: (1) KB-indenpendent graph-structured ungrounded query generation. (2) KB-dependent graph-structure grounded query generation and ranking. (also, retrieve knowledge base). Below, **I will describe how to run our SPARQA by step-to-step**.

### step 1 KB-indenpendent query generation
* step 1.1 Skeleton Parsing
** Configuration: is_span_tree = True, which means skeleton parsing. is_span_tree = False, which means dependency parsing.
* step 1.2 Node Recognition
* step 1.3 Relation Extraction

### step 2 KB-dependent query generation
* step 2.1 Variant Generation
* step 2.2 Grounding
* step 2.3 Multi-Strategy Scoring
  
## Citation

    Sun Y, Zhang L, Cheng G, et al. SPARQA: Skeleton-Based Semantic Parsing for Complex Questions over Knowledge Bases[C]//AAAI. 2020: 8952-8959.

## Contacts
If you have any difficulty or questions in running codes, reproducing experimental results, and skeleton parsing, please email to him (ywsun@smail.nju.edu.cn).
