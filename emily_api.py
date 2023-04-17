import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest 
import json

# url = 'https://itunes.apple.com/us/rss/topmovies/limit=100/json' # iTunes API URL to fetch top 100 movies

# response = requests.get(url) # send GET request to fetch data
# data = response.json() # parse JSON data

# dct ={}
# #print(data)
# #iterate over the movie entries in the response and print the title and rating
# for entry in data['feed']['entry']:
#     #print(entry)
#     title = entry['title']['label']
#     rating = entry['im:rating']['label']
#     #rating = entry['attributes']['im:id']
#     print(rating)
#     #print(title)

import requests

url = "https://mdblist.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "536c152bbemshbc7cbb92a43fe41p1ff4fbjsnba9018e95bd7",
	"X-RapidAPI-Host": "mdblist.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
