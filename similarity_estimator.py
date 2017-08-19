# Import the Pandas  and Numpy library
import pandas as pd
import numpy as np

# Load the datasets: users, lord of the rings books and dune books
users = pd.read_csv('BX-CSV-Dump/BX-Users.csv', sep=';', error_bad_lines=False, encoding='latin1')
lotr_books = pd.read_csv('BX-CSV-Dump/tolkien_lotr.csv', sep=';', error_bad_lines=False, encoding='latin1')
dune_books = pd.read_csv('BX-CSV-Dump/frank_herbert_dune.csv', sep=';', error_bad_lines=False, encoding='latin1')


# generates the reader and assigns him a User-ID and rating for the books he likes
def generate_reader(books, uid=12345678, rating=10):
    """Generates reader DataFrame by books he should like and assigns his rating.

    :rtype: pd.DataFrame
    :return: DataFrame of user and his ratings for books.
    :argument books: DataFrame of books.
    :type books: pd.DataFrame
    """
    reader = pd.DataFrame(columns=['ISBN', 'User-ID', 'Book-Rating'])
    reader['ISBN'] = books['ISBN'].copy()
    reader['Book-Rating'] = rating
    reader['User-ID'] = uid
    return reader


lotr_reader = generate_reader(lotr_books)
dune_reader = generate_reader(dune_books)
del lotr_books
del dune_books

print(lotr_reader)
print(dune_reader)


# picks users that read at least one of the dune books AND at least one of the lotr books
def calculate_similar(user, others: pd.DataFrame):
    """Calculates similarity between user and other users ratings. Picks users that read at least on of Dune and one
    of Lotr books.

    :argument user: User ratings data frame which similarity to others will be calculated.
    :type user: pd.DataFrame
    :argument others: DataFrame of ratings of other users.
    :type others: pd.DataFrame
    :return: User similarity data frame.
    :rtype: pd.DataFrame"""

    dune_raters = others[others['ISBN'].isin(dune_reader['ISBN'])]
    lotr_raters = others[others['ISBN'].isin(lotr_reader['ISBN'])]
    # After small experiments I decided to let users who don't rate books in set of all users.
    # Because their similarity was low, but it yielded much larger collection of possibly interesting books.
    # That other much more similar to NEW (UNKNOWN) user might like.
    # Most importantly it boosted popularity (Readers-Count) that is used to compute final score.
    # dune_raters = dune_raters.drop(dune_raters[dune_raters['Book-Rating'] == 0].index)
    # lotr_raters = lotr_raters.drop(lotr_raters[lotr_raters['Book-Rating'] == 0].index)
    lotr_raters = lotr_raters.drop(lotr_raters[~lotr_raters['User-ID'].isin(dune_raters['User-ID'])].index)
    dune_raters = dune_raters.drop(dune_raters[~dune_raters['User-ID'].isin(lotr_raters['User-ID'])].index)
    lotr_dune_raters = pd.concat([lotr_raters, dune_raters])

    # generates the set of ratings per book
    siml_rated = lotr_dune_raters.merge(user, on='ISBN')

    # computes the similarity between users with the help of distance function with euclidian metrics on ratings
    def euclidean_similarity(grouped):
        """Calculates similarity between two users (aggregated data frame by User-ID_x) using Euclidean distance as
        siml = 1/ (1 + d(u, v)) for u \in U; v \in U\{u}.
        :argument grouped: Data frame of ratings of both users.
        :type grouped: pd.DataFrame
        :return: Similarity calculated from euclidean distance, (0, 1].
        :rtype: float"""
        new_user_ratings = grouped.as_matrix(columns=['Book-Rating_y'])
        user_rating = grouped.as_matrix(columns=['Book-Rating_x'])
        dst_vec = new_user_ratings - user_rating
        dst = np.sqrt(dst_vec.transpose().dot(dst_vec))[0][0]
        return 1./(1. + dst)

    siml = (siml_rated.groupby(['User-ID_x']).apply(euclidean_similarity).reset_index(name='Similarity'))
    return siml

# Load the book ratings data set
ratings_url = 'BX-CSV-Dump/BX-Book-Ratings.csv'
ratings = pd.read_csv(ratings_url, sep=';', error_bad_lines=False, encoding='latin1')

# this is the user we would like to suggest books to
new_user = pd.concat([lotr_reader, dune_reader])

# here we calculate the similarity using the above functions
# we get columns: user-ID (user who read at least 1 dune AND 1 lotr book), Similarity (how much is the rating
# similar to ours)
sim = calculate_similar(new_user, ratings)
sim_url = 'BX-CSV-Dump/user_similarity.csv'
sim.to_csv(sim_url, sep=',', index=False)


books = pd.read_csv('BX-CSV-Dump/books-cleaned.csv', encoding='utf-8')

# merging ratings and users
ratings_with_age = pd.merge(ratings, users, on='User-ID')
cols = ['ISBN', 'User-ID', 'Book-Rating', 'Location','Age']
ratings_with_age = ratings_with_age[cols]


ratings_with_book_and_age = pd.merge(ratings_with_age, books, on='ISBN')
rated_book_colls = [cols[0], 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher'] + cols[1:]
ratings_with_book_and_age = ratings_with_book_and_age[rated_book_colls]
ratings_with_book_and_age_url = 'BX-CSV-Dump/ratings_with_book_and_age.csv'
ratings_with_book_and_age.to_csv(ratings_with_book_and_age_url, index=False)
