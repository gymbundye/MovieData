import sqlite3

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (Movie_Name TEXT UNIQUE, Picked_By TEXT, Avg_Rating REAL, Date TEXT, TMDB_ID INTEGER, Overview TEXT, Genres TEXT, 
                  Release_Date TEXT, Vote_Average REAL, Vote_Count INTEGER, TMDb_Link TEXT, Running_Time INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS errors
                 (Movie_Name TEXT, Error_Message TEXT)''')
    return conn, c

def insert_movie_data(c, df):
    for _, row in df.iterrows():
        try:
            c.execute("INSERT INTO movies (Movie_Name, Picked_By, Avg_Rating, Date, TMDB_ID, Overview, Genres, Release_Date, Vote_Average, Vote_Count, TMDb_Link, Running_Time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (row['Movie Name'], row['Picked By'], row['Avg Rating'], row['Date'], row['TMDB_ID'], row['Overview'],
                       row['Genres'], row['Release Date'], row['Vote Average'], row['Vote Count'], row['TMDb Link'], row['Running Time']))
        except sqlite3.IntegrityError:
            print(f"Movie '{row['Movie Name']}' is already in the database.")

def insert_error_messages(c, error_messages):
    for movie_name, error_message in error_messages:
        c.execute("INSERT INTO errors VALUES (?, ?)", (movie_name, error_message))

def commit_and_close(conn):
    conn.commit()
    conn.close()
