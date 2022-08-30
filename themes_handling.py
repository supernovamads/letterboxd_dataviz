#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:17:30 2022

@author: madisonsmith
"""
import numpy as np
import pandas as pd
import re
from ast import literal_eval
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from textwrap import wrap


ratingsdf = pd.read_csv('user/ratings.csv',sep=',',converters={'themes':literal_eval})
    


possible_themes = list(set([a for b in ratingsdf['themes'].values.tolist() for a in b]))

themes_dict = {key : [] for key in possible_themes}
for (idx, k) in ratingsdf.iterrows():
    for theme in k['themes']:
        if k['Name'] not in themes_dict[theme]:
            themes_dict[theme].append(k['Name'])


themes_df = pd.DataFrame({'theme': themes_dict.keys(),
                          'Name' :themes_dict.values()})
themesdf = themes_df.explode('Name')

themesdf = themesdf.merge(ratingsdf[['Name','Rating','communityScoreWeighted']],how='left')

groupedbythemedf_mean = themesdf.groupby('theme').mean()
groupedbythemedf_mean.columns = ['myaverage','communityaverage']
groupedbythemedf_std = themesdf.groupby('theme').std()
groupedbythemedf_std.columns = ['mystd','communitystd']
grouped_stats = groupedbythemedf_mean.merge(groupedbythemedf_std,on='theme',how='left')
grouped_stats = grouped_stats.reset_index()
grouped_stats.to_csv('user/grouped_theme_averages.csv',sep=',')



fig, ax = plt.subplots(6,3,sharey=True,sharex=True)
df_count = 0
myheight = 1.5
communityheight = 4
labels = [ '\n'.join(wrap(l, 20)) for l in grouped_stats['theme'].values ]

for l in range(6):
    for k in range(3):
        mycurrentaverage = grouped_stats['myaverage'].iloc[df_count]
        mycurrentstd = grouped_stats['mystd'].iloc[df_count]
        communitycurrentaverage = grouped_stats['communityaverage'].iloc[df_count]
        communitycurrentstd = grouped_stats['communitystd'].iloc[df_count]
        ax[l][k].errorbar(mycurrentaverage,myheight,xerr=mycurrentstd,
                          color='royalblue',ecolor='royalblue',capsize=5,ms=6,marker='o')
        ax[l][k].errorbar(communitycurrentaverage,communityheight,xerr=communitycurrentstd,
                          color='firebrick',ecolor='firebrick',capsize=5,ms=6,marker='o')
        ax[l][k].set_ylim(0,6)
        ax[l][k].set_xlim(0.1,5)
        ax[l][k].tick_params(axis='y',which='both',length=0,labelsize=0)
        ax[l][k].xaxis.set_major_locator(MultipleLocator(1))
        ax[l][k].xaxis.set_minor_locator(MultipleLocator(0.5))
        ax[l][k].text(0.2,2.2,labels[df_count])
        ax[5][0].set_xlabel('Movie Rating')
        ax[5][1].set_xlabel('Movie Rating')
        ax[5][2].set_xlabel('Movie Rating')
        df_count += 1

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
fig.set_size_inches(10,8)


