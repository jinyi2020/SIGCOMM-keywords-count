import pandas as pd
import numpy as np
from collections import Counter
import sys

# This script counts keyword appearing times in input dataset.


# input datapath.
inp_data_path = 'output_data/20230626_proc_dataframe' 
# year range for counting
year_start = 1993
year_end = 2022
# top n words to print 
top_n = 15


def count_keywords(df_proc_tmp):

    all_keywords = [keyword for sublist in df_proc_tmp['keywords_split'] for keyword in sublist]
    keyword_counts = Counter(all_keywords)
    keyword_counts_df = pd.DataFrame.from_dict(keyword_counts, orient='index', columns=['count'])
    out = keyword_counts_df.sort_values(by = ['count'], ascending = False)
    return out

def count():
    df_read = pd.read_csv(inp_data_path)
    df_read = df_read[df_read['keywords'].notna()]
    df_read['keywords_split'] = df_read['keywords_replace'].str.split(',')

    df_check = df_read[(df_read['year'] >= year_start) & (df_read['year'] <= year_end)]
    out = count_keywords(df_check)
    #out[out['count']>1]
    if top_n > 0:
        print(out.head(top_n))
    else:
        print(out)

def main():
    count()

if __name__ == '__main__':
    main()

