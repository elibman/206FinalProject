import sqlite3
import requests
import json


def getmovieid():
   url = "https://imdb-top-100-movies.p.rapidapi.com/"


   headers = {
   "X-RapidAPI-Key": "d53ac055e7mshea37be8e69920fap17a024jsnc6076add2e01",
   "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
   }
  
   response = requests.request("GET", url, headers=headers)
   data = response.text
   d = json.loads(data)


   ids = []
   for x in d:
       ids.append(x["imdbid"])
   return ids



def get_budget(id_lst):
    budget_list = []
    for movie_id in id_lst:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d0174faf259d4408d91f65a5c5bdf480'
        response = requests.get(url)

        if response.status_code == 200:
            movie_info = response.json()
            budget_dict = {
                'title': movie_info['title'],
                'budget': movie_info['budget']
            }
            budget_list.append(budget_dict)
        else:
            print(f"Error: {response.status_code}")

    return budget_list

def add_db(movie_info):
    with sqlite3.connect('imdb.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                title TEXT NOT NULL,
                budget INTEGER NOT NULL
            );
        ''')
        


        start = len(cursor.execute('SELECT * FROM budget').fetchall())
        end = start + 25
        for i in range(start, end):
            if i >= len(movie_info):
                break
            row = movie_info[i]
            cursor.execute('INSERT INTO budget (title, budget) VALUES (?, ?)',
                        (row['title'], row['budget']))
        conn.commit()
    conn.close()



get_budget(getmovieid())
add_db(get_budget(getmovieid()))