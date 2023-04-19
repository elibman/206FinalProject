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
    
    return genres_dct
    
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
        start = len(cur.execute('SELECT * FROM itunes').fetchall())
        end = start + 25
        for i in range(start, end):
            if i >= len(dct.keys()):
                break
            for id, genre in dct.items():
                cur.execute('INSERT INTO itunes (id, genre) VALUES (?, ?)',
                (id, genre))
                conn.commit()

        # cur.execute('''
        #     CREATE TABLE IF NOT EXISTS movie_info (
        #         title STRING ,
        #         rating INTEGER ,
        #         genre STRING,
        #         genre_id INTEGER
        #     );
        # ''')
        conn.commit()

create_tables(get_genres_dct())
