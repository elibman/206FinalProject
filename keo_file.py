import sqlite3
import requests


id_lst = ['tt0068646', 'tt0468569', 'tt0071562', 'tt0050083', 'tt0108052', 'tt0167260', 'tt0110912', 'tt0120737', 
       'tt0060196', 'tt0109830', 'tt0137523', 'tt0167261', 'tt1375666', 'tt0080684', 'tt0133093',
       'tt0073486', 'tt0114369', 'tt0038650', 'tt0047478', 'tt0102926', 'tt0120815', 'tt0317248', 'tt0816692']

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



get_budget(id_lst)
add_db(get_budget(id_lst))