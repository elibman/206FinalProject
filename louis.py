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
    ids = []
    for x in d:
        ids.append(x["imdbid"])
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

        start = len(cur.execute("select * from imdb"))
        end = start + 25
        while start < end:
            row = info.items()
            cur.execute('INSERT INTO imdb (title, rating) VALUES (?, ?)',
        		(row[start[0]], row[start[1]]))
            conn.commit()
            start += 1
        cur.close()

Getratingfromimdb()




'''        
make to 25 each

use length of data base as index 

ask how to do 25 
how to clarify that we are all adding to the same data base so it is all one and how multiple people see it 

establish where you need to start counting

use count function
'''
"""
start = len(cur.execute("select * from imdb"))
end = start + 25
while start < end:
    row = info.items()
    cur.execute('INSERT INTO imdb (title, rating) VALUES (?, ?)',
        (row[start[0]], row[start[1]]))
    start += 1
    
"""
