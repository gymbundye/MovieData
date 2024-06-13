import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import sqlite3

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

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

# Define the movie IDs to exclude
exclude_ids = [384717, 43074]

# Filter the DataFrame to include only the specified users and exclude specific TMDB IDs
df_filtered = df[(df['Picked By'].isin(['jon', 'jim', 'phill'])) & (~df['TMDB_ID'].isin(exclude_ids))]

# Display the filtered DataFrame
print("Filtered DataFrame:")
print(df_filtered)

# Replace 'YOUR_API_KEY' with your actual TMDB API key
API_KEY = '0af5b4f32534825e575111d5029fb03e'

# Add columns for Vote Average, Vote Count, and TMDb Link
df['Vote Average'] = None
df['Vote Count'] = None
df['TMDb Link'] = None

# Change 'Release Year' to 'Release Date'
df.rename(columns={'Release Year': 'Release Date'}, inplace=True)

# Fetch data for each movie in the DataFrame and populate TMDb Link
for idx, row in df.iterrows():
    tmdb_id = row['TMDB_ID']
    df.at[idx, 'TMDb Link'] = f'https://www.themoviedb.org/movie/{tmdb_id}'

# Drop unused columns
columns_to_drop = ['IMDB Link', '5 Star Rating', 'Unnamed: 10', 'Unnamed: 11', '1242', '1418', '1286']
df.drop(columns=columns_to_drop, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('MovieData/Updated_Movies.csv', index=False)

# Create a SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Create a table to store movie data
c.execute('''CREATE TABLE IF NOT EXISTS movies
             (Movie_Name TEXT, Picked_By TEXT, Avg_Rating REAL, Date TEXT, TMDB_ID INTEGER, Overview TEXT, Genres TEXT, Release_Date TEXT, Vote_Average REAL, Vote_Count INTEGER, TMDb_Link TEXT)''')

# Insert data into the table
for _, row in df.iterrows():
    c.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (row['Movie Name'], row['Picked By'], row['Avg Rating'], row['Date'], row['TMDB_ID'], row['Overview'],
               row['Genres'], row['Release Date'], row['Vote Average'], row['Vote Count'], row['TMDb Link']))

# Commit changes and close the connection
conn.commit()
conn.close()

# Display the updated DataFrame
print("Updated DataFrame:")
print(df)

# Filter the DataFrame again to ensure correct filtering after saving
df_filtered = df[(df['Picked By'].isin(['jon', 'jim', 'phill'])) & (~df['TMDB_ID'].isin(exclude_ids))]

# Display the filtered DataFrame
print("Filtered DataFrame:")
print(df_filtered)

# Plotting Functions
def plot_initial_charts(df_filtered):
    # Count the frequency of each rating for these users
    rating_counts = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)

    # Reset index for seaborn
    rating_counts = rating_counts.T.reset_index().melt(id_vars='Avg Rating', var_name='User', value_name='Frequency')

    # Plot the grouped bar chart
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Avg Rating', y='Frequency', hue='User', data=rating_counts, palette={'jon': 'blue', 'jim': 'green', 'phill': 'purple'})
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.title('Frequency of Ratings (1-10) by Jon, Jim, and Phill')
    plt.show()

    # Plot the heatmap
    rating_counts_heatmap = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 8))
    sns.heatmap(rating_counts_heatmap, annot=True, cmap="YlGnBu", fmt="d")
    plt.xlabel('Avg Rating')
    plt.ylabel('Picked By')
    plt.title('Heatmap of Ratings by Jon, Jim, and Phill')
    plt.show()

    # Plot the line chart
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df_filtered, x='Date', y='Avg Rating', hue='Picked By', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Average Rating')
    plt.title('Trend of Average Ratings Over Time')
    plt.xticks(rotation=45)
    plt.show()

    # Plot the box plot
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Picked By', y='Avg Rating', data=df_filtered, palette={'jon': 'blue', 'jim': 'green', 'phill': 'purple'})
    plt.xlabel('Picked By')
    plt.ylabel('Average Rating')
    plt.title('Distribution of Average Ratings by User')
    plt.show()

plot_initial_charts(df_filtered)

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

# Count the frequency of each rating for these users
rating_counts_pie = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)

# Create pie charts for each user
for user in ['jon', 'jim', 'phill']:
    if user in rating_counts_pie.index:
        create_pie_chart(rating_counts_pie.loc[user], user, colors)

# Extract genres from the DataFrame
genres = df_filtered['Genres'].str.split(', ')

# Flatten the list of genres
genres = [genre for sublist in genres.dropna() for genre in sublist]

# Count the occurrences of each genre for each user
genre_counts_by_user = pd.DataFrame()
for user in ['jon', 'jim', 'phill']:
    user_genre_counts = pd.Series([genre for sublist in genres[df_filtered['Picked By'] == user].dropna() for genre in sublist]).value_counts()
    genre_counts_by_user[user] = user_genre_counts

# Plot the bar chart for genre counts by user
genre_counts_by_user = genre_counts_by_user.fillna(0).T  # Ensure no NaN values and transpose for plotting
plt.figure(figsize=(12, 8))
genre_counts_by_user.plot(kind='bar', stacked=True, colormap='viridis')
plt.xlabel('Genre')
plt.ylabel('Frequency')
plt.title('Most Picked Genres by User')
plt.legend(title='User')
plt.xticks(rotation=45)
plt.show()
