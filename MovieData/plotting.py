import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_initial_charts(df_filtered):
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
    sns.boxplot(x='Picked By', y='Avg Rating', data=df_filtered, palette=custom_palette)
    plt.xlabel('Picked By')
    plt.ylabel('Average Rating')
    plt.title('Distribution of Average Ratings by User')
    plt.show()

def plot_user_trends(df_filtered, users, custom_palette):
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
    comparison_df = df_filtered[df_filtered['Picked By'] == user][['Movie Name', 'Avg Rating', 'Vote Average']]
    comparison_df.set_index('Movie Name', inplace=True)

    plt.figure(figsize=(14, 7))
    comparison_df.plot(kind='bar', color=[color, 'gray'])
    plt.xlabel('Movie Name')
    plt.ylabel('Rating')
    plt.title(f'Comparison of {user.capitalize()}\'s Rating vs TMDB Rating')
    plt.legend(['User Rating', 'TMDB Rating'])
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def plot_genre_frequency(df_filtered):
    genre_counts = df_filtered['Genres'].str.split(', ').explode().value_counts()
    plt.figure(figsize=(12, 8))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
    plt.xlabel('Frequency')
    plt.ylabel('Genre')
    plt.title('Frequency of Genres')
    plt.tight_layout()
    plt.show()

def plot_genre_frequency_by_user(df_filtered, custom_palette):
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
    plt.tight_layout()
    plt.show()

def plot_total_running_time(df_filtered, custom_palette):
    total_running_time = df_filtered.groupby('Picked By')['Running Time'].sum().sort_values(ascending=False)
    total_running_time_days = total_running_time / (24 * 60)

    fig, ax1 = plt.subplots(figsize=(14, 8))

    barplot = sns.barplot(x=total_running_time.index, y=total_running_time.values, 
                          palette=[custom_palette[user] for user in total_running_time.index], ax=ax1)

    for index, value in enumerate(total_running_time.values):
        barplot.text(index, value + 5, f'{round(value, 2)} Minutes or {round(value / (24 * 60), 2)} Days', color='black', ha="center")

    ax1.set_xlabel('User')
    ax1.set_ylabel('Total Running Time (minutes)')
    ax1.set_title('Total Running Time of Movies Picked by Each User')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    plt.tight_layout()
    plt.show()

def plot_picks_by_user(df_filtered):
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
    df_exploded = df_filtered.copy()
    df_exploded['Genres'] = df_exploded['Genres'].str.split(', ')
    df_exploded = df_exploded.explode('Genres')

    pivot_table = pd.pivot_table(df_exploded, values='Avg Rating', index='Genres', columns='Picked By', aggfunc='mean', fill_value=0)
    print("Pivot Table (Average Rating by Genre and User):")
    print(pivot_table)
