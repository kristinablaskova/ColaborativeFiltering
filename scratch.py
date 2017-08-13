# Import the Pandas  and Numpy library
import pandas as pd
import numpy as np

# Load the datasets: users, lord of the rings books and dune books
users = pd.read_csv('BX-CSV-Dump/BX-Users.csv', sep=';', error_bad_lines=False, encoding='latin1')
lotr_books = pd.read_csv('BX-CSV-Dump/tolkien_lotr.csv', sep=';', error_bad_lines=False, encoding='latin1')
dune_books = pd.read_csv('BX-CSV-Dump/frank_herbert_dune.csv', sep=';', error_bad_lines=False, encoding='latin1')

#generates the reader and assigns him an User-ID and rating for the books he likes
def generate_reader(books, uid=12345678, rating=10):
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

#picks users that read at least one of the dune books AND at least one of the lotr books
# possibly drops the users that read the book, but didnt rate it
def calculate_similar(user, all_users: pd.DataFrame):
    dune_raters = all_users[all_users['ISBN'].isin(dune_reader['ISBN'])]
    lotr_raters = all_users[all_users['ISBN'].isin(lotr_reader['ISBN'])]
    # dune_raters = dune_raters.drop(dune_raters[dune_raters['Book-Rating'] == 0].index)
    # lotr_raters = lotr_raters.drop(lotr_raters[lotr_raters['Book-Rating'] == 0].index)
    lotr_raters = lotr_raters.drop(lotr_raters[~lotr_raters['User-ID'].isin(dune_raters['User-ID'])].index)
    dune_raters = dune_raters.drop(dune_raters[~dune_raters['User-ID'].isin(lotr_raters['User-ID'])].index)
    lotr_dune_raters = pd.concat([lotr_raters, dune_raters])

    # generates the set of ratings per book
    siml_rated = lotr_dune_raters.merge(user, on='ISBN')

    # computes the similarity between users with the help of distance function with euclidian metrics on ratings
    def sim_from_l2(grouped):
        new_user_ratings = grouped.as_matrix(columns=['Book-Rating_y'])
        user_rating = grouped.as_matrix(columns=['Book-Rating_x'])
        dst_vec = new_user_ratings - user_rating
        dst = np.sqrt(dst_vec.transpose().dot(dst_vec))[0][0]
        return 1./(1. + dst)

    siml = (siml_rated.groupby(['User-ID_x']).apply(sim_from_l2).reset_index(name='Similarity'))
    return siml

# Load the book ratings data set
ratings_url = 'BX-CSV-Dump/BX-Book-Ratings.csv'
ratings = pd.read_csv(ratings_url, sep=';', error_bad_lines=False, encoding='latin1')

#this is the user we would like to suggest books to
new_user = pd.concat([lotr_reader, dune_reader])

#here we calculate the similarity using the above functions
# we get columns: user-ID (user who read at least 1 dune AND 1 lotr book), Similarity (how much is the rating
# similar to ours)
sim = calculate_similar(new_user, ratings)
sim_url = 'BX-CSV-Dump/user_similarity.csv'
sim.to_csv(sim_url, sep=',', index=False)

books = pd.read_csv('BX-CSV-Dump/books-cleaned.csv', encoding='utf-8')





# # calculates how many people does not have filled location, this is not NaN value
# # 0 users without location; 848 users with nan value inside location string.
# # print(sum([1 for idx, user_data in users.iterrows() if user_data['Location'] == '' or 'nan' in user_data['Location'].lower()]))  # [1]['Location'])
# # lets see how many people didnt fill out 'age' column
# print('\nUSERS==============================')
# print(users.isnull().sum())
# print(users.shape)
# print('\nRATINGS============================')
# print(len(set(ratings['ISBN'].unique()) ^ set(books['ISBN'].unique())))
# print(books.shape)
#
# #merging ratings and users
# ratings_with_age = pd.merge(ratings, users, on='User-ID')
# cols = ['ISBN', 'User-ID', 'Book-Rating', 'Location','Age']
# ratings_with_age = ratings_with_age[cols]
#
# #dividing location to city state and country: creating new dataframe consisting only of location, splitting it according to comma, merging the dataframe with the rest of data, dropping location column
# ratings_tosplit = ratings_with_age[['Location']].copy()
# ratings_tosplit = pd.DataFrame(ratings_tosplit.Location.str.split(', ', 2).tolist(), columns=['City','State','Country'])
# ratings_final = pd.merge(ratings_with_age,ratings_tosplit, left_index=True, right_index=True)
# del ratings_final['Location']
# #the highest number of ratings - 766612 - is from the usa, that means it makes sense to keep the 'state' information
# #print(ratings_final.Country.value_counts())
# '''print(ratings_final.State.value_counts())
# print(ratings_final.City.value_counts())'''
#
# #loading the usa gps data
# usa_locations_url = 'BX-CSV-Dump/zip_codes_states.csv'
# usa_locations = pd.read_csv(usa_locations_url, sep=',', usecols=[1, 2, 3, 4])
#
# #lowercasing the column values so they are ready to be merged
# usa_locations['city']=usa_locations['city'].str.lower()
# usa_locations.rename(columns={'city': 'City'}, inplace=True)
# ratings_final['City']=ratings_final['City'].str.lower()
# # Load the datasets
# countries_loc_url = 'BX-CSV-Dump/countries_loc.csv'
# countries_loc = pd.read_csv(countries_loc_url)
#
# #lowering the case of countries
# countries_loc['Country']=countries_loc['name'].str.lower()
# del countries_loc['name']
# #print('LOCATION=================')
# #print(countries_loc)
# #print(ratings_final)
# ratings_final_loc = pd.merge(ratings_final, countries_loc, on='Country', how='left')
# ratings_final_loc_url = 'BX-CSV-Dump/ratings_final_loc.csv'
# ratings_final_loc.to_csv(ratings_final_loc_url, sep=',', index=False)
#
#
# cols = ['ISBN', 'User-ID', 'Book-Rating', 'Location','Age']
# ratings_with_age = ratings_with_age[cols]
# print(ratings_with_age.head())
#
# #print('\nUSER RATED BOOKS=======================')
# ratings_with_book_and_age = pd.merge(ratings_with_age, books, on='ISBN')
# rated_book_colls = [cols[0], 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher'] + cols[1:]
# ratings_with_book_and_age = ratings_with_book_and_age[rated_book_colls]
# ratings_with_book_and_age_url = 'BX-CSV-Dump/ratings_with_book_and_age.csv'
# ratings_with_book_and_age.to_csv(ratings_with_book_and_age_url, index=False)