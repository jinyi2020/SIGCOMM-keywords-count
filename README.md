# SIGCOMM keywords count
 
This project uses paper data from SIGCOMM conference proceedings. Scraped data is stored in output_data/20230617_full_dataframe.

The purpose of this project is to find what kind of paper is more likely to be accepted in SIGCOMM.

Method to solve this problem is to extract keyword part and count frequency of these words. Then get the most frequent keywords.

Before counting, there are steps for data cleaning. 

First run keyword_cluster_Levenshtein.py to cluster together similar words based on Levenshtein distance. output_data/20230626_proc_dataframe
is result from this step. It's generated with cluster files of output_data/L_keyword_cluster0.txt and output_data/L_keyword_cluster1.txt. 
These two cluster files are generated with keyword_cluster_Levenshtein.py script with threshold 0.1 and 0.2 and some manual editing.

Then run keyword_cluster_spacy.py to cluster based on spacy similarity. Result of this step is output_data/20230710_spacy_dataframe. Cluster of words 
in this step is output_data/S_keyword_cluster0.txt.

For above two scripts, can run with 'python keyword_cluster_Levenshtein.py' for generating both words cluster files and output data with replaced keywords.
Or run with 'python keyword_cluster_Levenshtein.py cluster', 'python keyword_cluster_Levenshtein.py apply' to generate one file each time.

count.py is used to print most frequent keywords in a given year range.

This project found 'datacenter networking', 'congestion control' are popular keywords in SIGCOMM papers.
