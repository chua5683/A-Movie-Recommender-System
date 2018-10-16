import requests
import bs4
import time
import json

base_url = "https://api.themoviedb.org/3/movie/"
# API_KEY can be obtained from TMDB https://www.themoviedb.org/documentation/api
API_KEY = 'XX'
json_file = open('data/credits_metadata.json', 'a')

json_file.write('[')

firstRow = True
with open('data/links.csv', 'r') as f:
    for count, line in enumerate(f):
        if count > 0:
            line = line.split(',')
            tmdbId = line[2]
            if len(tmdbId) == 0:
                print("Movie doesn't exist in TMDB Database.")
                continue
            url = base_url + tmdbId + "/credits" + "?api_key=" + API_KEY
            
            print("Requesting Movie Number: " + str(count))
            res = requests.get(url)
            
            if res.status_code == 404:
                print("Movie doesn't exist in TMDB Database.")
                continue
            elif res.status_code == 429:
                print("Time out. Waiting for 10 seconds.")
                time.sleep(10)
                res = requests.get(url)
            else:
                res.raise_for_status()
                
            if firstRow:
                json_file.write(str(res.text))
                firstRow = False
            else:
                json_file.write(", " + str(res.text))
                
json_file.write(']')
json_file.close()