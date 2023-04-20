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

    genres_dct = {}
    genres_lst = []
    title_dct = {}
    title_lst = []
    for movie_title in movies:
        #print(movie_title)
        url = f"https://itunes.apple.com/search?term={movie_title}&entity=movie"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # parse JSON data
            #print(data)
            #print(data['results'])
            # while len(data['results']) < 100:
            for entry in data['results']:
                #print(entry)
                genres_lst.append(entry['primaryGenreName'])
                title_lst.append(entry['trackName'])
            
        else:
            print(f"Error: {response.status_code}")
    for i in range(len(movies)):
        title_dct[title_lst[i]] = genres_lst[i]
    #print(title_dct)
    
    unique_genres = []
    for x in genres_lst:
        if x not in unique_genres:
            unique_genres.append(x)
    #print(unique_genres)
    #print(unique_genres)
    #print(genres_lst)
    id = 0
    for genre in unique_genres:
        genres_dct[id] = genre
        id += 1

    #print(movies)
    #print(len(movies))
    return (genres_dct, title_dct, movies)
    
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
            DROP TABLE IF EXISTS movie_genre
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS movie_genre (
                title STRING,
                genre_id INTEGER
            );
        ''')

        
        start = len(cur.execute("select * from movie_genre").fetchall())
        #print(start)
        #print(dct[1].items())
        #print(len(dct[1].items()))
        #print(len(dct[1]))
        end = start + 25
        for i in range(start, end):
            if i >= len(dct[2]):
                break
            try:
                for movie_title, movie_genres in dct[1].items():
                    # Get the genre ID from the unique_genres table based on the genre name
                    cur.execute('SELECT id FROM itunes WHERE genre = ?', (movie_genres,))
                    genre_id = cur.fetchone()[0]

                    cur.execute('SELECT COUNT(*) FROM movie_genre WHERE title = ? AND genre_id = ?', (movie_title, genre_id))
                    count = cur.fetchone()[0]

                    # If a record doesn't already exist, insert a new one
                    if count == 0:
                        cur.execute('INSERT INTO movie_genre (title, genre_id) VALUES (?, ?)', (movie_title, genre_id))
                        conn.commit()

            except:
                return None
        cur.close()

create_tables(get_genres_dct())
