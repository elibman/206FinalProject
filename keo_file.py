import sqlite3
import requests

# Set API key and URL for movies endpoint

url = f'https://api.themoviedb.org/3/movie/550?api_key=d0174faf259d4408d91f65a5c5bdf480'
response = requests.get(url)

if response.status_code == 200:
    movie_info = response.json()
else:
    print(f"Error: {response.status_code}")

dic = {}
dic[movie_info['title']] = movie_info['budget']





conn = sqlite3.connect('mydb.sqlite')
cur = conn.cursor()

conn.close()


