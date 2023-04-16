import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest 
import json


url = "https://www.omdbapi.com/?apikey=f1b82c&"
omdb_api = requests.get(url)

