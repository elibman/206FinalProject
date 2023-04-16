import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest 
import json

url = "https://imdb-top-100-movies.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "536c152bbemshbc7cbb92a43fe41p1ff4fbjsnba9018e95bd7",
	"X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)