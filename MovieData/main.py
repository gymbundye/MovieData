import pandas as pd
import requests
from data_processing import read_and_clean_data
from api_functions import get_movie_details, get_genre_list
from database_functions import create_database, insert_movie_data, insert_error_messages, commit_and_close
from plotting import (
    plot_initial_charts, plot_user_trends, plot_comparison_chart, plot_genre_frequency,
    plot_genre_frequency_by_user, plot_total_running_time, plot_picks_by_user, display_genre_ratings_pivot
)

# Configuration
API_KEY = '0af5b4f32534825e575111d5029fb03e'
MOVIES_CSV = 'Movies.csv'
DB_NAME = 'movies.db'

# Read and clean data
df = read_and_clean_data(MOVIES_CSV)

# Get genre list
genre_list = get_genre_list(API_KEY)

# Add columns for TMDB data
tmdb_columns = ['TMDB_ID', 'Overview', 'Genres', 'Release Date', 'Vote Average', 'Vote Count', 'TMDb Link', 'Running Time']
for col in tmdb_columns:
    df[col] = None

# List to store error messages
error_messages = []

# Fetch data from TMDB
for idx, row in df.iterrows():
    title = row['Movie Name']
    movie_details, error_message = get_movie_details(title, API_KEY)
    if movie_details:
        movie_id = movie_details.get('id')
        if movie_id:
            movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
            movie_response = requests.get(movie_url, params={'api_key': API_KEY})
            if movie_response.status_code == 200:
                movie_full_details = movie_response.json()
                df.at[idx, 'TMDB_ID'] = movie_full_details.get('id')
                df.at[idx, 'Overview'] = movie_full_details.get('overview')
                df.at[idx, 'Genres'] = ', '.join([genre['name'] for genre in movie_full_details.get('genres', [])])
                df.at[idx, 'Release Date'] = movie_full_details.get('release_date')
                df.at[idx, 'Vote Average'] = movie_full_details.get('vote_average')
                df.at[idx, 'Vote Count'] = movie_full_details.get('vote_count')
                df.at[idx, 'Running Time'] = movie_full_details.get('runtime')
                tmdb_id = movie_full_details.get('id')
                if tmdb_id:
                    df.at[idx, 'TMDb Link'] = f'https://www.themoviedb.org/movie/{tmdb_id}'
    else:
        error_messages.append((title, error_message))

# Drop unused columns
unused_columns = ['IMDB Link', '5 Star Rating', 'Unnamed: 10', 'Unnamed: 11', '1286', '1467', '1286']
df.drop(unused_columns, axis=1, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('Updated_Movies.csv', index=False)

# Create and populate SQLite database
conn, c = create_database(DB_NAME)
insert_movie_data(c, df)
insert_error_messages(c, error_messages)
commit_and_close(conn)

# Define the movie IDs to exclude
exclude_ids = [384717, 43074]

# Filter the DataFrame
df_filtered = df[(df['Picked By'].isin(['jon', 'jim', 'phill'])) & (~df['TMDB_ID'].isin(exclude_ids))]

# Plotting
custom_palette = {'jon': '#4682B4', 'jim': '#228B22', 'phill': '#4B0082'}
users = ['jon', 'jim', 'phill']

plot_initial_charts(df_filtered)
plot_user_trends(df_filtered, users, custom_palette)
plot_comparison_chart(df_filtered, 'jon', '#4682B4')
plot_comparison_chart(df_filtered, 'jim', '#228B22')
plot_comparison_chart(df_filtered, 'phill', '#4B0082')
plot_genre_frequency(df_filtered)
plot_genre_frequency_by_user(df_filtered, custom_palette)
plot_total_running_time(df_filtered, custom_palette)
plot_picks_by_user(df_filtered)
display_genre_ratings_pivot(df_filtered)
