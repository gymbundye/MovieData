import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Normalize 'Picked By' column by stripping spaces and converting to lowercase
df['Picked By'] = df['Picked By'].str.strip().str.lower()

# Ensure 'Avg Rating' is numeric
df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')

# Drop rows with NaN values in 'Avg Rating' after conversion
df = df.dropna(subset=['Avg Rating'])

# Display the cleaned DataFrame
print(df)

# Filter the DataFrame to include only the specified users
df_filtered = df[df['Picked By'].isin(['jon', 'jim', 'phill'])]

# Count the frequency of each rating for these users
rating_counts = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)

# Reset index for seaborn
rating_counts = rating_counts.T.reset_index().melt(id_vars='Avg Rating', var_name='User', value_name='Frequency')

# Plot the grouped bar chart
plt.figure(figsize=(12, 8))
sns.barplot(x='Avg Rating', y='Frequency', hue='User', data=rating_counts, palette={'jon': 'blue', 'jim': 'green', 'phill': 'purple'})

# Add labels and title
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Frequency of Ratings (1-10) by Jon, Jim, and Phill')

# Display the plot
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Normalize 'Picked By' column by stripping spaces and converting to lowercase
df['Picked By'] = df['Picked By'].str.strip().str.lower()

# Ensure 'Avg Rating' is numeric
df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')

# Drop rows with NaN values in 'Avg Rating' after conversion
df = df.dropna(subset=['Avg Rating'])

# Filter the DataFrame to include only the specified users
df_filtered = df[df['Picked By'].isin(['jon', 'jim', 'phill'])]

# Count the frequency of each rating for these users
rating_counts = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(rating_counts, annot=True, cmap="YlGnBu", fmt="d")

# Add labels and title
plt.xlabel('Avg Rating')
plt.ylabel('Picked By')
plt.title('Heatmap of Ratings by Jon, Jim, and Phill')

# Display the plot
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Normalize 'Picked By' column by stripping spaces and converting to lowercase
df['Picked By'] = df['Picked By'].str.strip().str.lower()

# Ensure 'Avg Rating' is numeric
df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')

# Drop rows with NaN values in 'Avg Rating' after conversion
df = df.dropna(subset=['Avg Rating'])

# Filter the DataFrame to include only the specified users
df_filtered = df[df['Picked By'].isin(['jon', 'jim', 'phill'])]

# Plot the line chart
plt.figure(figsize=(12, 8))
sns.lineplot(data=df_filtered, x='Date', y='Avg Rating', hue='Picked By', marker='o')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Average Rating')
plt.title('Trend of Average Ratings Over Time')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Normalize 'Picked By' column by stripping spaces and converting to lowercase
df['Picked By'] = df['Picked By'].str.strip().str.lower()

# Ensure 'Avg Rating' is numeric
df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')

# Drop rows with NaN values in 'Avg Rating' after conversion
df = df.dropna(subset=['Avg Rating'])

# Filter the DataFrame to include only the specified users
df_filtered = df[df['Picked By'].isin(['jon', 'jim', 'phill'])]

# Plot the box plot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Picked By', y='Avg Rating', data=df_filtered, palette={'jon': 'blue', 'jim': 'green', 'phill': 'purple'})

# Add labels and title
plt.xlabel('Picked By')
plt.ylabel('Average Rating')
plt.title('Distribution of Average Ratings by User')

# Display the plot
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Normalize 'Picked By' column by stripping spaces and converting to lowercase
df['Picked By'] = df['Picked By'].str.strip().str.lower()

# Ensure 'Avg Rating' is numeric
df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')

# Drop rows with NaN values in 'Avg Rating' after conversion
df = df.dropna(subset=['Avg Rating'])

# Filter the DataFrame to include only the specified users
df_filtered = df[df['Picked By'].isin(['jon', 'jim', 'phill'])]

# Count the frequency of each rating for these users
rating_counts = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)

# Define a function to create pie charts for each user
def create_pie_chart(data, user, colors):
    labels = data.index
    sizes = data.values
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.title(f'Distribution of Ratings for {user.capitalize()}')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# Define colors for each user
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#c4e17f','#76d7c4','#ff6f61','#6a5acd']

# Create pie charts for each user
for user in ['jon', 'jim', 'phill']:
    if user in rating_counts.index:
        create_pie_chart(rating_counts.loc[user], user, colors)


import requests
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual TMDB API key
API_KEY = '0af5b4f32534825e575111d5029fb03e'

# Function to get movie details by title
def get_movie_details(title, api_key):
    base_url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': api_key,
        'query': title
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]  # Return the first search result
    return None

# Function to fetch the genre list from TMDB API
def get_genre_list(api_key):
    base_url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {genre['id']: genre['name'] for genre in data['genres']}
    return None

# Get the genre list
genre_list = get_genre_list(API_KEY)

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Add columns to store additional data from TMDB
df['TMDB_ID'] = None
df['Overview'] = None
df['Genres'] = None
df['Release Date'] = None
df['Vote Average'] = None
df['Vote Count'] = None
df['TMDb Link'] = None

#Change year to date
df.rename(columns={'Release Year': 'Release Date'}, inplace=True)

# Fetch data for each movie in the DataFrame
for idx, row in df.iterrows():
    title = row['Movie Name']
    movie_details = get_movie_details(title, API_KEY)
    if movie_details:
        df.at[idx, 'TMDB_ID'] = movie_details.get('id')
        df.at[idx, 'Overview'] = movie_details.get('overview')
        df.at[idx, 'Genres'] = ', '.join(
            [genre_list.get(genre_id) for genre_id in movie_details.get('genre_ids', [])]
        )
        df.at[idx, 'Release Date'] = movie_details.get('release_date')
        df.at[idx, 'Vote Average'] = movie_details.get('vote_average')
        df.at[idx, 'Vote Count'] = movie_details.get('vote_count')

        tmdb_id = movie_details.get('id')
        if tmdb_id:
            df.at[idx, 'TMDB Link'] = f'https://www.themoviedb.org/movie/{tmdb_id}' 

# Drop the 'IMDb Link' column
df.drop('IMDB Link', axis=1, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('MovieData/Updated_Movies.csv', index=False)

# Display the updated DataFrame
print(df.head())

