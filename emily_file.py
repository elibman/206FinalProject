import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest 
import json

def GetGenre():

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
        info[x["title"]] = x["rating"]

    movies = info.keys()
    #print(movies)

    genres_dct = {}
    genres_lst = []
    for movie_title in movies:
        #print(movie_title)
        url = f"https://itunes.apple.com/search?term={movie_title}&entity=movie"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # parse JSON data
            for entry in data['results']:
                genres_lst.append(entry['primaryGenreName'])
        else:
            print(f"Error: {response.status_code}")
    unique_genres = list(set(genres_lst))
    #print(unique_genres)
        
    id = 0
    for genre in unique_genres:
        genres_dct[id] = genre
        id += 1
    #print(genres_dct)
    
    with sqlite3.connect('itunes.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS itunes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre STRING
            );
        ''')
        conn.commit()

        for id, genre in genres_dct.items():
            cur.execute('INSERT INTO itunes (id, genre) VALUES (?, ?)',
            (id, genre))
            conn.commit()
        cur.close()

GetGenre()