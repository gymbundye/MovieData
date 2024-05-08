import pandas as pd
import matplotlib.pyplot as plt
# Path to your CSV file
Movies = 'MovieData\Movies.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(Movies)

# Display the DataFrame
#print(df)



# Select the first 10 rows and plot
df.head(20).plot(kind='bar', x='Picked By', y='Avg Rating')

# Add labels and title
plt.xlabel('Rating')
plt.ylabel('Picked By')
plt.title('Bar Graph of First 20 Rows')

# Display the plot
plt.show()
