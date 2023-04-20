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
            for entry in data['results']:
                #print(entry)
                genres_lst.append(entry['primaryGenreName'])
                title_lst.append(entry['trackName'])
            
        else:
            print(f"Error: {response.status_code}")
    for i in range(len(movies)):
        title_dct[title_lst[i]] = genres_lst[i]

    for b in title_dct:
        genres = b[1]
    print(genres)
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
        end = start + 25
        for i in range(start, end):
            if i >= len(dct[2]):
                break
            try:
                for movie_title, movie_genres in dct[1].items():
                    if movie_genres == 'Drama':
                        genre_id = 0
                    elif movie_genres == 'Western':
                        genre_id = 1
                    elif movie_genres == 'Anime':
                        genre_id = 2
                    elif movie_genres == 'Documentary':
                        genre_id = 3
                    elif movie_genres == 'Thriller':
                        genre_id = 4
                    elif movie_genres == 'Action & Adventure':
                        genre_id = 5
                    elif movie_genres == 'Foreign':
                        genre_id = 6
                    elif movie_genres == 'Music Feature Films':
                        genre_id = 7
                    elif movie_genres == 'Comedy':
                        genre_id = 8
                    elif movie_genres == 'Horror':
                        genre_id = 9
                    elif movie_genres == 'Sci-Fi & Fantasy':
                        genre_id = 10
                    elif movie_genres == 'Kids & Family':
                        genre_id = 11
                    elif movie_genres == 'Musicals':
                        genre_id = 12
                    elif movie_genres == 'Romance':
                        genre_id = 13
                    elif movie_genres == 'Holiday':
                        genre_id = 14
                    elif movie_genres == 'Bollywood':
                        genre_id = 15
                    elif movie_genres == 'Independent':
                        genre_id = 16
                    elif movie_genres == 'Concert Films':
                        genre_id = 17
                    elif movie_genres == 'Sports':
                        genre_id = 18
                    elif movie_genres == 'Classics':
                        genre_id = 19
                    elif movie_genres == 'Special Interest':
                        genre_id = 20
                    elif movie_genres == 'Short Films':
                        genre_id = 21
                    elif movie_genres == 'Music Documentaries':
                        genre_id = 22

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
