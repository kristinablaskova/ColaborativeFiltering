import pandas as pd
import numpy as np

books_url = 'BX-CSV-Dump/ratings_with_book_and_age.csv'
books = pd.read_csv(books_url, encoding='utf-8')

ratsim_url = 'BX-CSV-Dump/user_similarity.csv'
ratsim = pd.read_csv(ratsim_url, encoding='utf-8')
ratsim = ratsim.rename(columns={'User-ID_x': 'User-ID'})

# possible books to recommend - which books rated users similar to me?

rec_bookset = books.merge(ratsim, on='User-ID')
rec_bookset = rec_bookset[rec_bookset['Book-Rating'] != 0]
# rec_bookset.drop_duplicates(subset='ISBN', keep='first', inplace=True)
# rec_bookset.drop(rec_bookset.columns[4:], axis=1, inplace = True)
# print(rec_bookset.shape)
# print(rec_bookset.head())

# Define a lambda function to compute the weighted mean:
wm = lambda x: np.average(x, weights=rec_bookset.loc[x.index, "Similarity"])

# Define a dictionary with the functions to apply for a given column:
f = {'Book-Rating': wm, 'Readers-Count': 'count'}

rec_bookset['Readers-Count'] = 0
# Groupby and aggregate with your dictionary:
books_wm = rec_bookset.groupby(["ISBN"], as_index=False).agg(f)

books_wm['Score'] = books_wm['Readers-Count'].multiply(books_wm['Book-Rating'])

recommended_books = books_wm.sort_values(['Score'], ascending=False).merge(books, on='ISBN').drop_duplicates(subset='ISBN', keep='first')
print(recommended_books[:100])