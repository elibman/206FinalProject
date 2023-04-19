import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest 
import json

def get_genres_dct():

    imdb_url = "https://imdb-top-100-movies.p.rapidapi.com/"

    headers = {
	"X-RapidAPI-Key": "d53ac055e7mshea37be8e69920fap17a024jsnc6076add2e01",
	"X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
    }

    imdb_response = requests.request("GET", imdb_url, headers=headers)
    imdb_data = imdb_response.text
    d = json.loads(imdb_data)

    info = {}
    for x in d:
        title = x['title']
        rating = x['rating']
        info[x["title"]] = x["rating"]

    movies = info.keys()
    #print(movies)

    genres_dct = {}
    genres_lst = []
    newdct = {}
    newlst = []
    for movie_title in movies:
        #print(movie_title)
        url = f"https://itunes.apple.com/search?term={movie_title}&entity=movie"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # parse JSON data
            for entry in data['results']:
                #print(entry)
                genres_lst.append(entry['primaryGenreName'])
                itunes_titles = entry['trackName']
                #print(itunes_title)
                newlst.append(itunes_titles)
                for x in range(len(newlst)):
                    newdct[newlst[x]] = genres_lst[x]
        else:
            print(f"Error: {response.status_code}")
    unique_genres = list(set(genres_lst))
    #print(unique_genres)
    #print(genres_lst)
    #print(newdct)
    id = 0
    for genre in unique_genres:
        genres_dct[id] = genre
        id += 1
    #print(genres_dct)
    #print(newdct)
    return (genres_dct, newdct)
    
get_genres_dct()
            
def create_tables(dct):    

    with sqlite3.connect('imdb.db') as conn:
        cur = conn.cursor()

        cur.execute('''
            DROP TABLE IF EXISTS itunes
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS itunes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre STRING
            );
        ''')
        conn.commit()

        for id, genre in dct[0].items():
            cur.execute('INSERT INTO itunes (id, genre) VALUES (?, ?)',
                (id, genre))
            conn.commit()



        cur.execute('''
            CREATE TABLE IF NOT EXISTS movie_genre (
                title STRING,
                genre STRING,
                genre_id INTEGER
            );
        ''')

        conn.commit()

        start = len(cur.execute("select * from movie_genre").fetchall())
        #print(start)
        #print(dct[1].items())
        end = start + 25
        while start < end:
            try:
                for movie_title, movie_genres in dct[1].items():
                    # Get the genre ID from the unique_genres table based on the genre name
                    cur.execute('SELECT id FROM itunes WHERE genre = ?', (genre,))
                    genre_id = cur.fetchone()[0]
    
                    # Insert a new row into the movie_genre table with the movie title, genre, and genre ID
                    cur.execute('INSERT INTO movie_genre (movie_title, genre, genre_id) VALUES (?, ?, ?)', (movie_title, movie_genres, genre_id))
                    conn.commit()
                start += 1
            except:
                return None
        cur.close()

create_tables(get_genres_dct())
