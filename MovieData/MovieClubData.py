import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import sqlite3

# Path to CSV file
Movies = 'Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Display the initial DataFrame
print("Initial DataFrame:")
print(df)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Normalize 'Picked By' column by stripping spaces and converting to lowercase
df['Picked By'] = df['Picked By'].str.strip().str.lower()

# Ensure 'Avg Rating' is numeric
df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')

# Drop rows with NaN values in 'Avg Rating' after conversion
df = df.dropna(subset=['Avg Rating'])

# Display the cleaned DataFrame
print("Cleaned DataFrame:")
print(df)

API_KEY = '0af5b4f32534825e575111d5029fb03e'

def get_movie_details(title, api_key):
    """Fetch movie details from TMDB API by title."""
    base_url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': title}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]
    return None

def get_genre_list(api_key):
    """Fetch the genre list from TMDB API."""
    base_url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {'api_key': api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {genre['id']: genre['name'] for genre in data['genres']}
    return None

# Get the genre list
genre_list = get_genre_list(API_KEY)

# Add columns to store additional data from TMDB
tmdb_columns = ['TMDB_ID', 'Overview', 'Genres', 'Release Date', 'Vote Average', 'Vote Count', 'TMDb Link', 'Running Time']
for col in tmdb_columns:
    df[col] = None

# Fetch data for each movie in the DataFrame
for idx, row in df.iterrows():
    title = row['Movie Name']
    movie_details = get_movie_details(title, API_KEY)
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

# Drop unused Columns
unused_columns = ['IMDB Link', '5 Star Rating', 'Unnamed: 10', 'Unnamed: 11', '1286', '1467', '1286']
df.drop(unused_columns, axis=1, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('Updated_Movies.csv', index=False)

# Create a SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Create a table to store movie data
c.execute('''CREATE TABLE IF NOT EXISTS movies
             (Movie_Name TEXT, Picked_By TEXT, Avg_Rating REAL, Date TEXT, TMDB_ID INTEGER, Overview TEXT, Genres TEXT, 
              Release_Date TEXT, Vote_Average REAL, Vote_Count INTEGER, TMDb_Link TEXT, Running_Time INTEGER)''')

# Insert data into the table
for _, row in df.iterrows():
    c.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (row['Movie Name'], row['Picked By'], row['Avg Rating'], row['Date'], row['TMDB_ID'], row['Overview'],
               row['Genres'], row['Release Date'], row['Vote Average'], row['Vote Count'], row['TMDb Link'], row['Running Time']))

# Commit changes and close the connection
conn.commit()
conn.close()

# Define the movie IDs to exclude
exclude_ids = [384717, 43074]

# Filter the DataFrame to include only the specified users and exclude specific TMDB IDs
df_filtered = df[(df['Picked By'].isin(['jon', 'jim', 'phill'])) & (~df['TMDB_ID'].isin(exclude_ids))]

# Display the filtered DataFrame
print("Filtered DataFrame:")
print(df_filtered)

# Plotting Functions
def plot_initial_charts(df_filtered):
    """Plot initial charts for rating frequency, heatmap, trend, and distribution."""
    rating_counts = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)
    rating_counts = rating_counts.T.reset_index().melt(id_vars='Avg Rating', var_name='User', value_name='Frequency')
    custom_palette = {'jon': '#4682B4', 'jim': '#228B22', 'phill': '#4B0082'}

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Avg Rating', y='Frequency', hue='User', data=rating_counts, palette=custom_palette)
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.title('Frequency of Avg Ratings (1-10) of films picked by Jon, Jim, and Phill')
    plt.show()

    rating_counts_heatmap = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(rating_counts_heatmap, annot=True, cmap="YlGnBu", fmt="d")
    plt.xlabel('Avg Rating')
    plt.ylabel('Picked By')
    plt.title('Heatmap of Ratings by Jon, Jim, and Phill')
    plt.show()

    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df_filtered, x='Date', y='Avg Rating', hue='Picked By', marker='o', palette=custom_palette)
    plt.xlabel('Date')
    plt.ylabel('Average Rating')
    plt.title('Trend of Average Ratings Over Time')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
    plt.show()

    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Picked By', y='Avg Rating', data=df_filtered, palette=custom_palette)
    plt.xlabel('Picked By')
    plt.ylabel('Average Rating')
    plt.title('Distribution of Average Ratings by User')
    plt.show()

# Plotting separate charts for each user
def plot_user_trends(df_filtered, users, custom_palette):
    """Plot trends of average ratings over time for each user."""
    for user in users:
        plt.figure(figsize=(12, 8))
        user_data = df_filtered[df_filtered['Picked By'] == user]
        sns.lineplot(data=user_data, x='Date', y='Avg Rating', marker='o', color=custom_palette[user])
        plt.xlabel('Date')
        plt.ylabel('Average Rating')
        plt.title(f'Trend of Average Ratings Over Time for {user.capitalize()}')
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
        plt.tight_layout()
        plt.show()

def plot_comparison_chart(df_filtered, user, color):
    """Plot comparison of user ratings and TMDB ratings for a specific user."""
    comparison_df = df_filtered[df_filtered['Picked By'] == user][['Movie Name', 'Avg Rating', 'Vote Average']]
    comparison_df.set_index('Movie Name', inplace=True)

    plt.figure(figsize=(14, 7))
    comparison_df.plot(kind='bar', color=[color, 'gray'], edgecolor='black')
    plt.xlabel('Movie Name')
    plt.ylabel('Rating')
    plt.title(f'Comparison of {user.capitalize()}\'s Picks Ratings and TMDB Ratings')
    plt.legend([f'{user.capitalize()}\'s Rating', 'TMDB Rating'])
    plt.xticks(rotation=90)
    plt.show()

# Get the frequency of each genre
def plot_genre_frequency(df_filtered):
    """Plot the frequency of each genre."""
    genre_counts = df_filtered['Genres'].str.split(', ').explode().value_counts()
    plt.figure(figsize=(12, 8))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
    plt.xlabel('Frequency')
    plt.ylabel('Genre')
    plt.title('Frequency of Genres')
    plt.show()

def plot_genre_frequency_by_user(df_filtered, custom_palette):
    """Plot the frequency of each genre picked by each user."""
    df_exploded = df_filtered.copy()
    df_exploded['Genres'] = df_exploded['Genres'].str.split(', ')
    df_exploded = df_exploded.explode('Genres')

    genre_user_counts = df_exploded.groupby(['Picked By', 'Genres']).size().unstack(fill_value=0)
    genre_user_counts = genre_user_counts.reset_index().melt(id_vars='Picked By', var_name='Genre', value_name='Frequency')

    plt.figure(figsize=(14, 10))
    sns.barplot(x='Genre', y='Frequency', hue='Picked By', data=genre_user_counts, palette=custom_palette)
    plt.xlabel('Genre')
    plt.ylabel('Frequency')
    plt.title('Frequency of Each Genre Picked by Jon, Jim, and Phill')
    plt.xticks(rotation=45)
    plt.legend(title='User')
    plt.show()

def plot_total_running_time(df_filtered, custom_palette):
    """Plot the total running time of movies picked by each user."""
    total_running_time = df_filtered.groupby('Picked By')['Running Time'].sum().sort_values(ascending=False)
    total_running_time_days = total_running_time / (24 * 60)

    fig, ax1 = plt.subplots(figsize=(14, 8))

    barplot = sns.barplot(x=total_running_time.index, y=total_running_time.values, 
                          palette=[custom_palette[user] for user in total_running_time.index], ax=ax1)

    for index, value in enumerate(total_running_time.values):
        barplot.text(index, value + 5, f'      {round(value, 2)} Minutes or ', color='black', ha="right")

    ax1.set_xlabel('User')
    ax1.set_ylabel('Total Running Time (minutes)')
    ax1.set_title('Total Running Time of Movies Picked by Each User')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Total Running Time (days)')
    ax2.set_ylim(ax1.get_ylim()[0] / (24 * 60), ax1.get_ylim()[1] / (24 * 60))

    for index, value in enumerate(total_running_time_days.values):
        ax2.text(index, value + (5 / (24 * 60)), f'{round(value, 2)} Days', color='blue', ha="left")

    plt.show()

def plot_picks_by_user(df_filtered):
    """Plot the number of picks by each user."""
    pivot_table_picks = pd.pivot_table(df_filtered, values='Movie Name', index='Picked By', aggfunc='count')

    plt.figure(figsize=(10, 6))
    plt.bar(pivot_table_picks.index, pivot_table_picks['Movie Name'], color=['#4682B4', '#228B22', '#4B0082'])
    plt.xlabel('User')
    plt.ylabel('Number of Picks')
    plt.title('Number of Picks by Each User')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    print("Pivot Table (Number of Picks by Each User):")
    print(pivot_table_picks)

def display_genre_ratings_pivot(df_filtered):
    """Display a pivot table summarizing the average rating given by each user for each genre."""
    df_exploded = df_filtered.copy()
    df_exploded['Genres'] = df_exploded['Genres'].str.split(', ')
    df_exploded = df_exploded.explode('Genres')

    pivot_table = pd.pivot_table(df_exploded, values='Avg Rating', index='Genres', columns='Picked By', aggfunc='mean', fill_value=0)
    print("Pivot Table (Average Rating by Genre and User):")
    print(pivot_table)

# Plotting all charts
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
