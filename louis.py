import requests
import json
import unittest
import os
import sqlite3



def Getratingfromimdb():

    url = "https://imdb-top-100-movies.p.rapidapi.com/"

    headers = {
	"X-RapidAPI-Key": "d53ac055e7mshea37be8e69920fap17a024jsnc6076add2e01",
	"X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.text
    d = json.loads(data)

    info = {}
    for x in d:
        info[x["title"]] = x["rating"]
    
    with sqlite3.connect('imdb.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS imdb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                rating INTEGER NOT NULL
            );
        ''')
        conn.commit()

        for title, rating in info.items():
            cur.execute('INSERT INTO imdb (title, rating) VALUES (?, ?)',
            (title, rating))
            conn.commit()
        cur.close()

Getratingfromimdb()