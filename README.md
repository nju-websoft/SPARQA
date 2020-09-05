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
        <td>skeleton</td><td>skeleton bank of complex questions</td>
    </tr>
    <tr>
        <td>slides</td><td>slides and poster</td>
    </tr>
</table>
 
## Requirements
* [requirements.txt](https://github.com/nju-websoft/SPARQA/blob/master/code/requirements.txt)

## Configuration
* Root of dataset: default D:/dataset. Note that you can edit it in common/globals_args.py. 

## Common Resources
* Eight Resources: GloVe (glove.6B.300d), Stanford CoreNLP server, SUTime Java library, BERT pre-trained Models, and four preprocessing files(stopwords.txt, ordinal_fengli.tsv, unimportantphrase, and unimportantwords). [pan](https://pan.baidu.com/s/1Wd3ghjpn3oB20uTodDFGHA). The extraction code is kbqa. unzip and save in the root.
* Two version Freebase: [latest version](https://developers.google.com/freebase) and 2013 version (email SPARQA author, if you can not find the version). Next, download a virtuoso server and load the KBs. The [file](http://ws.nju.edu.cn/blog/2017/03/virtuoso%E5%AE%89%E8%A3%85%E5%92%8C%E5%AF%BC%E5%85%A5%E6%95%B0%E6%8D%AE/) is helpful, if you meet questions.

## Specific CWQ 1.1 Resources
* CWQ 1.1 dataset, Skeleton Parsing models, Word-level scorer model, Sentence-level scorer model. [pan](https://pan.baidu.com/s/1gOPkTwXAS3dD9I3-ORQkSg). The extraction code is kbqa. unzip and save in the root.
* Entity-related Lexicons and schema-related lexicons. [pan](https://pan.baidu.com/s/1ToAesUe11RouLuQO_olorA). The extraction code is kbqa. unzip and save in the root.

## Specific GraphQuestions Resources
* GraphQuestions dataset, Skeleton Parsing models, Word-level scorer model. [pan](https://pan.baidu.com/s/1wiNczntTiWzE_k7hy9RuQw). The extraction code is kbqa. unzip and save in the root.
* Entity-related Lexicons and schema-related lexicons. [pan](https://pan.baidu.com/s/1Zs0ufmSAHYHqFgoD4Hig3w). The extraction code is kbqa. unzip and save in the default root/kb_freebase_en_2013.

## Run SPARQA Pipeline
The pipeline has two steps for answering questions: 

* (1) KB-indenpendent graph-structured ungrounded query generation.
* (2) KB-dependent graph-structure grounded query generation and ranking.

See running/freebase/pipeline_cwq.py if run CWQ 1.1.
See running/freebase/pipeline_grapqh.py if run GraphQuestions.
Below, an example on GraphQuestions.

### Specific-dataset Configuration

* Set datset in the common/globals_args.py: q_mode=graphq. (note that q_mode=cwq if CWQ 1.1)
* Set skeleton parsing in the common/globals_args.py: parser_mode=head, which means skeleton parsing. (note that parser_mode=dep, which means dependency parsing).
* Replace the freebase_pyodbc_info and freebase_sparql_html_info in the common/globals_args.py with your local address. (note that 2013 version is for GraphQuestions, and latest version is for CWQ 1.1).

### KB-indenpendent query generation
* Run KB-indenpendent query generation. Setup variable module=1.0. The input: graph_questions_filepath. The output: structure_with_1_ungrounded_graphq_file. We provided [one sample](https://github.com/nju-websoft/SPARQA/blob/master/slides/274000300.json) to help easily understand the complete structure. I can provide the structures of all questions if you need.

### KB-dependent query generation
* Generate variant generation. Set variable module=2.1. The input: structure_with_1_ungrounded_graphq_file. The output: structure_with_2_1_grounded_graph_file.
* Ground candidate queries. Set module=2.2. The input: structure_with_2_1_grounded_graph_file. The output: structure_with_2_2_grounded_graph_folder.
* Rank using word-level scorer. Set module=2.3_word_match. The input: structure_with_2_2_grounded_graph_folder.
* Combine sentence-level scorer and word-level scorer. Set module=2.3_add_question_match. The input: structure_with_2_2_grounded_graph_folder.
* Run evaluation. Set module=3_evaluation. The input: structure_with_2_2_grounded_graph_folder. The output: results. 

## Compare with Baselines
* GraphQuestions: PARA4QA, SCANNER, UDEPLAMBDA.
* CWQ 1.1: PullNet, SPLITQA, and MHQA-GRN. Note that PullNet used annotated topic entities of questions in its KB only setting. SPARQA, an end-to-end method, do not use annotated topic entities. Thus, it is not comparable.

## Skeleton Parsing
* SPARQA also provides a tool of parsing. The input is a question. The output is the skeleton of the question. (Now, it only supports English language. Later, it will support Chinese language)
* You can use SPARQA's skeleton parsing to train yourself language. (It need replace the pre-trained models and annotated data with your language)

## Multi-Strategy Scoring
* SPARQA has provided a trained word-level scorer model and sentence-level scorer above pan.

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
If you have any difficulty or questions in running codes, reproducing experimental results, and skeleton parsing, please email to him (ywsun at smail.nju.edu.cn). 
