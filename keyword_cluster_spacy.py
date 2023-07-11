import pandas as pd
import spacy
import numpy as np
from collections import Counter
import sys

# This script generate clusters of keywords based on Spacy similarity.
# Running this script generate one file for clusters of words and 
# one file for output data with keywords replaced using above clusters.



threshold = 0.99
inp_data_path = 'output_data/20230626_proc_dataframe'
out_path_clusters = 'output_data/keywords_cluster_spacy.txt'
out_data_path = 'output_data/Spacy_processed_data.csv'

def keyword_cluster_spacy(words, threshold):
    nlp = spacy.load('en_core_web_lg')
    token = [nlp(w) for w in words]
    cluster = {}
    for i in range(len(token)):
        similarity = []
        for k in cluster:
            s = [token[i].similarity(token[j]) for j in cluster[k]]
            similarity.append(max(s))
            if max(s) == 1:
                break
        if len(similarity)==0 or max(similarity) < threshold:
            cluster[len(cluster)] = {i}
        else:
            k = np.array(similarity).argmax()
            cluster[k].add(i)
    cluster_out = {}
    for k in cluster:
        cluster_out[k] = set([words[j] for j in cluster[k]])
    return cluster_out

def clustering():
    df_read = pd.read_csv('output_data/20230626_proc_dataframe')
    df_read = df_read[df_read['keywords'].notna()]
    df_read['keywords_split'] = df_read['keywords_replace'].str.split(',')

    k_s = df_read['keywords_split'].dropna()
    all_keywords = [keyword for sublist in k_s for keyword in sublist]
    clusters = keyword_cluster_spacy(all_keywords,threshold) 
    f = open(out_path_clusters,'w')
    for k in clusters:
        if len(clusters[k])>1:
            _out = list(clusters[k])
            _out.sort(key = lambda x: len(x))
            out = ','.join(_out)
            print(out)
            f.write(out+'\n')
    f.close()   

def keywords_replace(inp, words):
    try:
        for i in range(len(inp)):
            for cluster in words:
                if inp[i] in cluster[1:]:
                    inp[i] = cluster[0]
    except:
        print(inp)

def replace():
    df_read = pd.read_csv(inp_data_path)
    df_read = df_read[df_read['keywords'].notna()]
    df_read['keywords_split'] = df_read['keywords_replace'].str.split(',')

    f = open(out_path_clusters,'r')
    read_words = []
    for line in f.readlines():
        if line[0] != '#':
            read_words.append(line.strip().split(','))
    f.close()

    df_read['keywords_split'].apply(lambda x: keywords_replace(x, read_words))

    df_save = df_read[['title','year','doi','keywords','keywords_split']]
    #df_save = df_save[df_save['keywords_split'].notna()]
    df_save['keywords_replace'] = df_save['keywords_split'].apply(lambda x: ','.join(x))
    df_save = df_save[['title','year','doi','keywords','keywords_replace']]
    df_save.to_csv(out_data_path)


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        clustering()
        replace()
    elif args[0] == 'cluster':
        clustering()
    elif args[0] == 'apply':
        replace()



if __name__ == '__main__':
    main()
    
