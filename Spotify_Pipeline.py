import sqlite3 # Imported sqlite3 since it's a disk-based database that doesn't require a separate server process so I can load my data. 
import pandas as pd #Using pandas for data manipulation and analysis in Python.
import matplotlib.pyplot as plt #This is a library for creating  visualizations in Python.
import seaborn as sns #Using seaborn which is based on Matplotlib and offers a higher-level interface for creating attractive and informative statistical graphics.


# Extract
df = pd.read_csv("spotify_songs.csv")

# Transform

#Defining numeric_columns and doing a min-max normalization to make it easier to interpret and compare.
numeric_columns = ['track_popularity', 'loudness', 'tempo', 'duration_ms']
df[numeric_columns] = df[numeric_columns].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

#Categorizing track_popularity into three categories: Low (0-33), Medium (34-66), High (67-100) to simplify the analysis.
df['popularity_category'] = pd.cut(df['track_popularity'], bins=[0, 0.33, 0.66, 1], labels=['Low', 'Medium', 'High'])

#Converting the track_album_release_date column to a datetime format, for a more detailed analysis.
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce', format='mixed')

df['release_year'] = df['track_album_release_date'].dt.year
df['release_month'] = df['track_album_release_date'].dt.month
df['release_day'] = df['track_album_release_date'].dt.day

# Load

#Loading the new data into sqlite. 
conn = sqlite3.connect('Spotify_Database.db')

# Creating a new table to load the DataFrame into it
df.to_sql('Spotify_Songs', conn, if_exists='replace', index=False)

# Closing the connection
conn.close()