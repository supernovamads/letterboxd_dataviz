#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 14:30:21 2021

@author: madisonsmith
"""
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import numpy as np
import json

watchlist = pd.read_csv('user/watchlist.csv',sep=',')
watched  = pd.read_csv('user/watched.csv',sep=',')
ratings = pd.read_csv('user/ratings.csv',sep=',')

director,country,genres,themes = [],[],[],[]
for k in ratings['Letterboxd URI']:
    r = requests.get(k)
    movie_page = r.text
    soup = BeautifulSoup(movie_page,'lxml')
    movie_header = soup.find('section', attrs={'id': 'featured-film-header'})
    movie_title = movie_header.find('h1').text
    movie_body = soup.find('section',attrs={'class': 'section col-10 col-main'})
    movie_crew = soup.find('div',attrs={'id': 'tabbed-content'})
    movie_director = movie_crew.select_one('a[href*=director]')['href'].split('/')[-2].replace('-',' ').title()
    try:
        movie_country = movie_crew.select_one('a[href*=country]')['href'].split('/')[-2]
    except:
        movie_country= np.nan
    movie_genres = [i.text for i in movie_crew.select('a[href*="/films/genre"]')]
    
    try:
        movie_themes = [i.text for i in movie_crew.select('a[href*="/films/theme"]')]
    except:
        movie_themes = []
    director.append(movie_director)
    country.append(movie_country)
    genres.append(movie_genres)
    themes.append(movie_themes)
    print(movie_title)

ratings['director'] = director
ratings['country'] = country
ratings['genres'] = genres
ratings['themes'] = themes

def my_hottest_takes(movie):
    movie_req = requests.get(movie['Letterboxd URI'])
    print(movie['Name'])
    movie_page = movie_req.text
    movie_soup = BeautifulSoup(movie_page,'lxml')
    rating = movie_soup.find("span", attrs={"class": "rating"})
    rating_class = rating['class'][-1]
    rating_val = int(rating_class.split('-')[-1])
    smaller_soup = movie_soup.find('script',attrs={'type':'application/ld+json'})
    json_metadata = json.loads(smaller_soup.contents[0].strip('\n/* <![CDATA[ */\n').strip('\n/* ]]>'))
    ratingcount = json_metadata['aggregateRating']['ratingCount']
    movie['ratingCount'] = ratingcount
    movie['communityScoreRaw'] = rating_val
    movie['communityScoreWeighted'] = json_metadata['aggregateRating']['ratingValue']
    return movie

# def film_populatiry(movie):
#     movie_req = requests.get(movie['Letterboxd URI'])
#     print(movie['Name'])
#     movie_page = movie_req.text
#     movie_soup = BeautifulSoup(movie_page,'lxml')

if 'communityScoreRaw' in ratings.columns.values :
    df = ratings.copy()
else:
    df = ratings.apply(my_hottest_takes,axis=1)
    df.to_csv('user/ratings.csv',sep=',',index=False)

plt.scatter(df['Rating'],df['Rating']-df['communityScoreWeighted'],s=5,c='k')
plt.ylabel('My Rating - Letterboxd Users Rating')
plt.xlabel('My Rating')
plt.show()


df.to_csv('user/ratings.csv',sep=',',index=False)


# by_year = ratings.groupby('Year')
# for year,info in by_year:
#     mean_rating = np.mean(info['Rating'])
#     max_rating = np.max(info['Rating'])
#     min_rating = np.min(info['Rating'])
#     plt.errorbar(year,mean_rating,yerr=[[mean_rating-min_rating],[max_rating-mean_rating]],fmt='o')