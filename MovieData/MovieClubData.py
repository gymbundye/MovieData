import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
Movies = 'MovieData/Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Ensure 'Avg Rating' is numeric
df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')

# Drop rows with NaN values in 'Avg Rating' after conversion
df = df.dropna(subset=['Avg Rating'])

# Normalize 'Picked By' column by stripping spaces and converting to lowercase
df['Picked By'] = df['Picked By'].str.strip().str.lower()

# Check for variations in the spelling or formatting of "Phil"
print(df['Picked By'].unique())  # Check unique values to see variations

# Filter the DataFrame to include all variations of "Phil"
df_filtered = df[df['Picked By'].isin(['jon', 'jim', 'phil', 'phill'])]

# Count the frequency of each rating for these users
rating_counts = df_filtered.groupby(['Picked By', 'Avg Rating']).size().unstack(fill_value=0)

# Plot the bar chart
rating_counts.T.plot(kind='bar', figsize=(12, 8))

# Add labels and title
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Frequency of Ratings (1-10) by Jon, Jim, and Phill')
plt.legend(title='User')

# Display the plot
plt.show()
