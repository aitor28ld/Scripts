#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create new virtual environment
# py -3 -m venv .venv
# Enable the virtual environment
# .venv/Scripts/activate
# Disable it when you have finished
# deactivate

# pip install requests
import requests
# pip install urllib3
import urllib3
# pip install bs4
from bs4 import BeautifulSoup

dictseries = {'0': {
            'nombre':'superman-y-lois',
            'temporadas':[],
            'capitulos':[],
            },
        '1':{
            'nombre':'brooklyn-nine-nine',
            'temporadas':[],
            'capitulos':[],
        },
        '2':{
            'nombre':'falcon-y-el-soldado-de-invierno',
            'temporadas':[],
            'capitulos':[],
        },
        '3':{
            'nombre':'invincible',
            'temporadas':[],
            'capitulos':[],
        }
}

# Checking gnula page status
def connectivity():
    response = requests.get('https://gnula.se')
    if response.status_code == 200:
        print("done")

# Parsing url into readable objects
def parsing(identificador, serie):
    http = urllib3.PoolManager()
    url = 'https://gnula.se/capitulos/'+serie+'/'
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'html.parser')

    for content in soup.find_all('strong'):
        content = str(content).split('>')[1].split('<')[0]
        if 'Temporada' in content:
            #print(content)
            dictseries[identificador]['temporadas'].append(content)
        else:
            dictseries[identificador]['capitulos'].append(content)

for id in dictseries.keys():
    parsing(id,dictseries[id]['nombre'])

print(dictseries)