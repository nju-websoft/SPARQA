# SPARQA: question answering over knowledge bases

Codes for paper: "SPARQA: Skeleton-based Semantic Parsing for Complex Questions over Knowledge Bases" (AAAI-2020) [detail](https://www.aaai.org/Papers/AAAI/2020GB/AAAI-SunY.3419.pdf).

If you meet any questions, please email to him (ywsun at smail.nju.edu.cn).

## Project Structure:

<table>
    <tr>
        <th>File</th><th>Description</th>
    </tr>
    <tr>
        <td>code</td><td>codes</td>
    </tr>
    <tr>
        <td>dataset</td><td>datasets and files for preprocessing </td>
    </tr>
    <tr>
        <td>skeleton</td><td>skeleton bank of complex questions</td>
    </tr>
    <tr>
        <td>slides</td><td>slides and poster</td>
    </tr>
</table>
 
## Requirements
* See [requirements.txt](https://github.com/nju-websoft/SPARQA/blob/master/code/requirements.txt) for the full list of packages

## Common Resources
* GloVe (glove.6B.300d) [download](https://nlp.stanford.edu/projects/glove/)
* Stanford CoreNLP server. download [here](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html), get started, and replace ip_port address in globals_args.py with URL of your CoreNLP.
* Python wrapper for Stanford CoreNLP's SUTime Java library. download [here](https://github.com/FraBle/python-sutime). Default save in root/resource_sutime/. If you save other place, replace the address sutime_jar_files in configution with your path.
* BERT pre-trained Models download [here](https://drive.google.com/drive/folders/1tlUF7ALLLXiHu280gPdlVyQlGvJFklGC) and save the seven files in the default root/pre_train_models address in the configuration bert.args.py.
* Download two version freebases: latest version for ComplexWebQuestions [here](https://developers.google.com/freebase) and 2013 version for GraphQuestions [here](https://github.com/ysu1989/GraphQuestions)
* Download a virtuoso server and load the KBs. The [file](http://ws.nju.edu.cn/blog/2017/03/virtuoso%E5%AE%89%E8%A3%85%E5%92%8C%E5%AF%BC%E5%85%A5%E6%95%B0%E6%8D%AE/) is helpful, if you meet questions.

## Configuration
* Root datasets: default value D:/dataset. You can edit it in the configution globals_args.py. 
* Four files (stopwords.txt, ordinal_fengli.tsv, unimportantphrase, and unimportantwords) download [here](https://drive.google.com/open?id=1AW5rT5MaZrDkc2rNz0TZhDJaQVQwJgT4). download the file, and saves in the root (default, you can edit these addresses).

## Specific CWQ 1.1 Resources
* To access interface virtuoso server, you need configure odbc address (freebase_pyodbc_info) in globals_args.py. 
* To access interface virtuoso html service, you need configure html address (freebase_sparql_html_info) in globals_args.py. 
* CWQ 1.1 five BERT pre-trained Models for Skeleton Parsing. download [here](https://drive.google.com/drive/folders/1t4Rb2feVOSGF_5lRBHwrB_GfxyL2rqby) and save the five files in the default root/dataset_cwq_1_1 address in the configuration bert.args.py (you can edit these addresses).
* Entity-related Lexicons and schema-related lexicons of Freebase latest version. download [here](https://drive.google.com/drive/folders/1t4Rb2feVOSGF_5lRBHwrB_GfxyL2rqby). Specificaly, the files variables in KB_Freebase_Latest class in the configuration kb_name.py.
* ComplexWebQuestions 1.1 dataset. download all files from [here](https://github.com/nju-websoft/SPARQA/tree/master/dataset/dataset_cwq_1_1). It consists of train/dev/test data and pre-processed sparql query bgp files. Note that the data_path_match file is used to save the word-level scoring model and the data_question_match file is used to save the sentence-level scoring model. The oracle_grounded_graph_cwq file used to save the pre-processed query structures to improve the query generation efficiency.

## Specific GraphQuestions Resources
* To access interface virtuoso server, you need configure odbc address (freebase_pyodbc_info) in globals_args.py. 
* To access interface virtuoso html service, you need configure html address (freebase_sparql_html_info) in globals_args.py.
* GraphQuestions five BERT pre-trained Models for Skeleton Parsing. download [here](https://drive.google.com/drive/folders/1Mjpan599INCVRgRQTsirgVdyt29iKblO) and save the five files in the default root/dataset_graphquestions address in the configuration bert.args.py (you can edit these addresses).
* Entity-related Lexicons and schema-related lexicons of Freebase 2013 version. download [here](https://drive.google.com/drive/folders/1Mjpan599INCVRgRQTsirgVdyt29iKblO). Specificaly, the files variables in KB_Freebase_en_2013 class in the configuration kb_name.py.
* GraphQuestions dataset. download all files from [here](https://github.com/nju-websoft/SPARQA/tree/master/dataset/dataset_graphquestions). It consists of train/test data and pre-processed sparql files. Note that the data_path_match file is used to save the word-level scoring model and the data_question_match file is used to save the sentence-level scoring model. The oracle_grounded_graph_graphq file used to save the pre-processed query structures to improve the query generation efficiency. The three files (graph_testing_question_normal.txt, 2019.05.13_test_answers, and 2019.05.13_train_answers) are combined in graphquestions.testing_nju_1209.json and graphquestions.training_nju_1209.json. It should modify the dataset interface of code. Once meet error when runing, please email to ywsun.

## Run SPARQA Pipeline
The pipeline has two steps for answering questions: 

* (1) KB-indenpendent graph-structured ungrounded query generation.
* (2) KB-dependent graph-structure grounded query generation and ranking.

Specifically, see running/freebase/pipeline_cwq.py if you want to run ComplexWebQuestions 1.1. or see running/freebase/pipeline_grapqh.py if you want to run GraphQuestions.
Below, I describe how to run our SPARQA by step-to-steps on GraphQuestions.

### Specific-dataset Configuration

* Datset Selection in the configuration globals_args.py: q_mode = graphq, which means GraphQuestions. q_mode = cwq, which means ComplexWebQuestions 1.1.
* Skeleton Parsing in the configuration globals_args.py: parser_mode = head, which means skeleton parsing. (note that parser_mode=dep, which means dependency parsing).
* Replace the address freebase_pyodbc_info and freebase_sparql_html_info in the globals_args.py with your local information.

### KB-indenpendent query generation
* Variable module = 1.0, which means run KB-indenpendent query generation. The input: graph_questions_filepath. The output: structure_with_1_ungrounded_graphq_file.

### KB-dependent query generation
* Variable module = 2.1, which means to run variant generation. The input: structure_with_1_ungrounded_graphq_file. The output: structure_with_2_1_grounded_graph_file.
* Variable module = 2.2, which means to grounding. The input: structure_with_2_1_grounded_graph_file. The output: structure_with_2_2_grounded_graph_folder.
* Variable module = 2.3_word_match, which means to ranking using word-level scorer. The input: structure_with_2_2_grounded_graph_folder.
* Variable module = 2.3_add_question_match, which means to combine sentence-level scorer and word-level scorer. The input: structure_with_2_2_grounded_graph_folder.
* Variable module = 3_evaluation, which means to run evaluation. The input: structure_with_2_2_grounded_graph_folder. The output: results.

## Instruction of Output File
* It consists of list. The output of every question is dict. Specifically, keys (question, qid, function, compositionality_type, num_node, num_edge, words, gold_graph_query, gold_answer, and gold_sparql_query) is question information.
* Key span_tree represents question skeleton. 
* Key ungrounded_graph_forest represents KB-indenpendent query. It consists of ungrounded_query_id, blag, nodes, edges, important_words_list, abstract_question, sequence_ner_tag_dict, grounded_linking, and grounded_graph_forest.
* Key grounded_graph_forest represents candidate KB-dependent queries. It consists of grounded_query_id, type, nodes, edges, key_path, sparql_query, score, and denotation.

## Train Skeleton Models
* Five models (continue...)

## Train Multi-strategy Scoring Models
* Word-level scorer (continue...)
* Sentence-level scorer (continue...)

## Compare with Baselines
* GraphQuestions: PARA4QA, SCANNER, UDEPLAMBDA
* ComplexWebQuestions: PullNet, SPLITQA, and MHQA-GRN. Note that PullNet used annotated topic entities of questions in its kB only setting. SPARQA, an end-to-end method, do not use annotated topic entities. It is thus not comparable.

## Citation

	@inproceedings{SunZ0Q20,
	  author    = {Yawei Sun and Lingling Zhang and Gong Cheng and Yuzhong Qu},
	  title     = {{SPARQA:} Skeleton-Based Semantic Parsing for Complex Questions over Knowledge Bases},
	  booktitle = {The Thirty-Fourth {AAAI} Conference on Artificial Intelligence, {AAAI} 2020, The Thirty-Second Innovative Applications of Artificial Intelligence Conference, {IAAI} 2020, The Tenth {AAAI} Symposium on Educational Advances in Artificial Intelligence, {EAAI} 2020, New York, NY, USA, February 7-12, 2020},
	  pages     = {8952--8959},
	  publisher = {{AAAI} Press},
	  year      = {2020},
	  url       = {https://aaai.org/ojs/index.php/AAAI/article/view/6426},
	}

## Contacts
If you have any difficulty or questions in running codes, reproducing experimental results, and skeleton parsing, please email to him (ywsun@smail.nju.edu.cn).
