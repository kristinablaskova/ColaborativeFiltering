"""This module is another attempt. We will first estimate readers location and age. And we will extend set of books by
books that are most suited for his/hers location and/or age."""


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