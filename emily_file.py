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

    dct = {}
    for movie_title in movies:
        #print(movie_title)
        url = f"https://itunes.apple.com/search?term={movie_title}&entity=movie"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # parse JSON data
        else:
            print(f"Error: {response.status_code}")

        #print(data)
        #iterate over the movie entries in the response and print the title and rating
        for entry in data['results']:
            #print(entry)
            genres = entry['primaryGenreName']
            print(genres)

GetGenre()
# url = 'https://itunes.apple.com/us/rss/topmovies/limit=100/json' # iTunes API URL to fetch top 100 movies

#  # send GET request to fetch data       

# data = response.json() # parse JSON data
# print(data)

# #print(data)
# #iterate over the movie entries in the response and print the title and rating
# for entry in data['feed']['entry']:
#     title = entry['title']['label']
#     genres = entry['category']['attributes']['term']
#     print(genres)
#     #print(title)

#import requests

# url = "https://mdblist.p.rapidapi.com/"

# headers = {
# 	"X-RapidAPI-Key": "536c152bbemshbc7cbb92a43fe41p1ff4fbjsnba9018e95bd7",
# 	"X-RapidAPI-Host": "mdblist.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

# import requests

# url = "https://ott-details.p.rapidapi.com/advancedsearch"

# querystring = {"max_imdb":"100","language":"english","type":"movie","sort":"highestrated","page":"1"}

# headers = {
# 	"X-RapidAPI-Key": "536c152bbemshbc7cbb92a43fe41p1ff4fbjsnba9018e95bd7",
# 	"X-RapidAPI-Host": "ott-details.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)