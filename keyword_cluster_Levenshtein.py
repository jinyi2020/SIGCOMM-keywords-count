import json
import pandas as pd
import numpy as np
from collections import Counter
import sys
import Levenshtein


# This script generate clusters of keywords based on Levenshtein distance.
# Running this script generate one file for clusters of words and 
# one file for output data with keywords replaced using above clusters.



threshold = 0.1
inp_data_path = 'output_data/20230617_full_dataframe'
out_path_clusters = 'output_data/keywords_cluster_Levenshtein.txt'
out_data_path = 'output_data/Levenshtein_processed_data.csv'

def keyword_cluster(words, threshold):
    cluster = {}
    while len(words)>0:
        w = words[0]
        words.pop(0)
        distance = []
        for k in cluster:
            d = [Levenshtein.distance(w, t) for t in cluster[k]]           
            distance.append(min(d))
            if min(d) == 0:
                break
        if len(distance)==0 or min(distance) > len(w)*threshold:
            cluster[len(cluster)] = {w}
        else:
            k = np.array(distance).argmin()
            cluster[k].add(w)
        #print(distance)
        #print(cluster)
    return cluster

def clustering():
    df = pd.read_csv(inp_data_path)
    df_proc = df[df['at']=='inproceedings']
    df_proc['keywords_split'] = df_proc['keywords'].apply(lambda x: x.lower().split(', ') if isinstance(x, str) else '')
    k_s = df_proc['keywords_split'].dropna()
    #print(k_s)
    all_keywords = [keyword for sublist in k_s for keyword in sublist]
    #word_list = ["datacenter", "data center", "information", "datacentre", "network", "data center"]
    clusters = keyword_cluster(all_keywords,threshold)

    f = open(out_path_clusters,'w')
    for k in clusters:
        if len(clusters[k])>1:
            out = ','.join(clusters[k])
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
    df = pd.read_csv(inp_data_path)
    df_proc = df[df['at']=='inproceedings']
    df_proc['keywords_split'] = df_proc['keywords'].apply(lambda x: x.lower().split(', ') if isinstance(x, str) else '')

    f = open(out_path_clusters,'r')
    read_words = []
    for line in f.readlines():
        if line[0] != '#':
            read_words.append(line.strip().split(','))
    f.close()

    df_proc['keywords_split'].apply(lambda x: keywords_replace(x, read_words))

    df_save = df_proc[['title','year','doi','keywords','keywords_split']]
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
