import pandas as pd
import csv

books_url = 'BX-CSV-Dump/BX-Books.csv'

'''imports only first 5 relevant columns (others are just image urls), uses latin1 encoding while it otherwise reported error,
uses different separator while quotechar didnt work '''
books = pd.read_csv(books_url, sep='";"', skipinitialspace=True, error_bad_lines=False, encoding='latin1',
                    usecols=[0, 1, 2, 3, 4])

# getting rid of irrelevant quotes produced by chosen separator
books.rename(columns={'"ISBN': 'ISBN'}, inplace=True)
books['ISBN'] = books['ISBN'].str[1:]

# exporting new csv
cleaned_books_url = 'BX-CSV-Dump/books-cleaned.csv'
books.to_csv(cleaned_books_url, sep=',', index=False)
cleaned_books = pd.read_csv(cleaned_books_url, encoding='utf-8')
print(cleaned_books.head())
print(cleaned_books.shape)
