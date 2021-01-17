# Written by: Nick Gerend, @dataoutsider
# Viz: "Big Screen", enjoy!

import gzip
import pandas as pd
import os

#region intial prep
# with gzip.open(os.path.dirname(__file__) + '/title.basics.tsv.gz') as f:
#     df = pd.read_csv(f, sep='\t')
# with gzip.open(os.path.dirname(__file__) + '/title.akas.tsv.gz') as f:
#     df = pd.read_csv(f, sep='\t')
#df.to_csv(os.path.dirname(__file__) + '/imdb_12_30_2020.csv', encoding='utf-8', index=False)
# print(df.head())
# print(df['region'].unique())
# print(df['language'].unique())
# df = df.loc[(df['language'] == 'en')]
# df.to_csv(os.path.dirname(__file__) + '/imdb_12_30_2020_en.csv', encoding='utf-8', index=False)
# df = pd.read_csv(os.path.dirname(__file__) + '/imdb_12_30_2020.csv')
# def label(s):
#     if ',' in s:
#         return 'Multiple'
#     elif '\\' in s:
#         return 'Undefined'
#     else:
#         return s
# df = df.loc[df['titleType'] == 'movie']
# df['label'] = [label(x) for x in df['genres']]
# df.to_csv(os.path.dirname(__file__) + '/imdb_12_30_2020_movie.csv', encoding='utf-8', index=False)
#endregion

df_m = pd.read_csv(os.path.dirname(__file__) + '/imdb_12_30_2020_movie.csv')
df_e = pd.read_csv(os.path.dirname(__file__) + '/imdb_12_30_2020_en.csv')
df = pd.merge(df_m, df_e, how='left', left_on=['tconst'], right_on = ['titleId'])
df.to_csv(os.path.dirname(__file__) + '/imdb_12_30_2020_movie.csv', encoding='utf-8', index=False)