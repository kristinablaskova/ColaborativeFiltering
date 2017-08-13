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

# Define a lambda function to compute the weighted mean:
weighted_mean = lambda x: np.average(x, weights=rec_bookset.loc[x.index, "Similarity"])

# Define a dictionary with the functions to apply for a given column:
f = {'Book-Rating': weighted_mean, 'Popularity': 'count'}

rec_bookset['Popularity'] = 0

books_wm = rec_bookset.groupby(["ISBN"], as_index=False).agg(f)

books_wm['Score'] = books_wm['Popularity'].multiply(books_wm['Book-Rating'])

recommended_books = books_wm.sort_values(['Score'], ascending=False).merge(books, on='ISBN')
recommended_books = recommended_books.drop_duplicates(subset='ISBN', keep='first')
print(recommended_books[:100])