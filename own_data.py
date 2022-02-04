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

watchlist = pd.read_csv('madisonsmith126/watchlist.csv',sep=',')
watched  = pd.read_csv('madisonsmith126/watched.csv',sep=',')
ratings = pd.read_csv('madisonsmith126/ratings.csv',sep=',')


# director,country,genres = [],[],[]
# for k in ratings['Letterboxd URI']:
#     r = requests.get(k)
#     movie_page = r.text
#     soup = BeautifulSoup(movie_page,'lxml')
#     movie_header = soup.find('section', attrs={'id': 'featured-film-header'})
#     movie_title = movie_header.find('h1').text
#     movie_body = soup.find('section',attrs={'class': 'section col-10 col-main'})
#     movie_crew = soup.find('div',attrs={'id': 'tabbed-content'})
#     movie_director = movie_crew.select_one('a[href*=director]')['href'].split('/')[-2].replace('-',' ').title()
#     movie_country = movie_crew.select_one('a[href*=country]')['href'].split('/')[-2]
#     movie_genres = [i.text for i in movie_crew.select('a[href*="/films/genre"]')]
#     director.append(movie_director)
#     country.append(movie_country)
#     genres.append(movie_genres)
#     print(movie_title)

# ratings['director'] = director
# ratings['country'] = country
# ratings['genres'] = genres
ratings.to_csv('madisonsmith126/ratings.csv',sep=',',index=False)
by_year = ratings.groupby('Year')
for year,info in by_year:
    mean_rating = np.mean(info['Rating'])
    max_rating = np.max(info['Rating'])
    min_rating = np.min(info['Rating'])
    plt.errorbar(year,mean_rating,yerr=[[mean_rating-min_rating],[max_rating-mean_rating]],fmt='o')