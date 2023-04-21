import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest 
import json

def get_genres_dct():


    imdb_url = "https://imdb-top-100-movies.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Key": "536c152bbemshbc7cbb92a43fe41p1ff4fbjsnba9018e95bd7",
        "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
    }

    imdb_response = requests.request("GET", imdb_url, headers=headers)

    
    # imdb_url = "https://imdb-top-100-movies.p.rapidapi.com/"

    # headers = {
	# "X-RapidAPI-Key": "d53ac055e7mshea37be8e69920fap17a024jsnc6076add2e01",
	# "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
    # }

    # imdb_response = requests.request("GET", imdb_url, headers=headers)
    imdb_data = imdb_response.text
    d = json.loads(imdb_data)

    #print(d)
    title_lst = []
    info = {}
    for x in d:
        #print(x)
        title = x['title']
        rating = x['rating']
        info[x['title']] = x['rating']
        #title_lst.append(title)

    movies = info.keys()
    #print(movies)
    for w in movies:
        title_lst.append(w)
    
    genres_dct = {}
    genres_lst = []
    title_dct = {}
    
    freshlst = []
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
            
        else:
            print(f"Error: {response.status_code}")
    #print(title_lst)
    for i in range(len(movies)):
        title_dct = {'title': title_lst[i], 'genre': genres_lst[i]}
        freshlst.append(title_dct)
    #print(title_dct)
    #print(freshlst)

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
    return (genres_dct, movies, freshlst)
    
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
                genre_id INTEGER
            );
        ''')

        
        start = len(cur.execute("select * from movie_genre").fetchall())
        end = start + 25
        for i in range(start, end):
            if i >= len(dct[1]):
                break
            row = dct[2][i]
            #print(row['title'])
            # try:
            #     for movie_title, movie_genres in dct[1].items():
            if row['genre'] == 'Drama':
                genre_id = 0
            elif row['genre'] == 'Western':
                genre_id = 1
            elif row['genre'] == 'Anime':
                genre_id = 2
            elif row['genre'] == 'Documentary':
                genre_id = 3
            elif row['genre'] == 'Thriller':
                genre_id = 4
            elif row['genre'] == 'Action & Adventure':
                genre_id = 5
            elif row['genre'] == 'Foreign':
                genre_id = 6
            elif row['genre'] == 'Music Feature Films':
                genre_id = 7
            elif row['genre'] == 'Comedy':
                genre_id = 8
            elif row['genre'] == 'Horror':
                genre_id = 9
            elif row['genre'] == 'Sci-Fi & Fantasy':
                genre_id = 10
            elif row['genre'] == 'Kids & Family':
                genre_id = 11
            elif row['genre'] == 'Musicals':
                genre_id = 12
            elif row['genre'] == 'Romance':
                genre_id = 13
            elif row['genre'] == 'Holiday':
                genre_id = 14
            elif row['genre'] == 'Bollywood':
                genre_id = 15
            elif row['genre'] == 'Independent':
                genre_id = 16
            elif row['genre'] == 'Concert Films':
                genre_id = 17
            elif row['genre'] == 'Sports':
                genre_id = 18
            elif row['genre'] == 'Classics':
                genre_id = 19
            elif row['genre'] == 'Special Interest':
                genre_id = 20
            elif row['genre'] == 'Short Films':
                genre_id = 21
            elif row['genre'] == 'Music Documentaries':
                genre_id = 22
            
            cur.execute('INSERT INTO movie_genre (title, genre_id) VALUES (?, ?)',
                        (row['title'], genre_id))
        conn.commit()

            # cur.execute('SELECT COUNT(*) FROM movie_genre WHERE title = ? AND genre_id = ?', (movie_title, genre_id))
            # count = cur.fetchone()[0]

            # # If a record doesn't already exist, insert a new one
            # if count == 0:
            #     cur.execute('INSERT INTO movie_genre (title, genre_id) VALUES (?, ?)', (movie_title, genre_id))
            #     conn.commit()

    cur.close()

create_tables(get_genres_dct())
