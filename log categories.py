#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:53:37 2023

@author: simon
"""
import pandas as pd
import numpy as np
import time

#df = pd.read_excel("deletiondump.xlsx", sheet_name=0)
df = pd.read_csv('quarry-24794-deletion-log-dump-run715873.csv')
df = df.rename(columns={'comment_text': 'log_comment'})

df['log_comment'] = df['log_comment'].fillna('no comment') 
df['log_comment'] = df['log_comment'].str.lower()
df['category'] = 'unclassified'
df['year'] = round(df['log_timestamp']/10000000000,0)

target = ['g1','g2','g3','g4',['mass deletion of pages','g5'],['g6','history merg'],'g7','g8','g9','g10','g11','g12','g13','g14','a1','a2','a3','a5','a7','a8','a9','a10','a11',['prod','proposed'],['wikipedia:articles for deletion','afd'],['redirect','r1','r2','r3','x1','neelix']]
category = ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','G13','G14','A1','A2','A3','A5','A7','A8','A9','A10','A11','PROD','AFD','redirect']
exclude = [['g14','g13','g12','g11','g10'],None,None,None,None,None,None,None,None,None,None,None,None,None,['a11','a10'],None,None,None,None,None,None,None,None,['wikipedia:articles for deletion','afd'],None,None]

print(len(target),len(category),len(exclude))


start_time = time.time()

for tg, c, e in zip(target,category,exclude):
    print(tg, c, e)
    if isinstance(tg, list) == False:
        if e == None:
            df.category = np.where(df['log_comment'].str.contains(tg), c, df.category)
        else:
            if len(e) == 2:
                df.category = np.where(df['log_comment'].str.contains(tg) & 
                                       ~df['log_comment'].str.contains(e[0]) & 
                                       ~df['log_comment'].str.contains(e[1]), c, df.category)     
    else:
        for t in tg:
            if e == None:
                df.category = np.where(df['log_comment'].str.contains(t), c, df.category)
            else:
                if len(e) == 2:
                    df.category = np.where(df['log_comment'].str.contains(t) & 
                                           ~df['log_comment'].str.contains(e[0]) & 
                                           ~df['log_comment'].str.contains(e[1]), c, df.category)     
                if len(e) == 5:
                    df.category = np.where(df['log_comment'].str.contains(t) & 
                                           ~df['log_comment'].str.contains(e[0]) & 
                                           ~df['log_comment'].str.contains(e[1]) &
                                           ~df['log_comment'].str.contains(e[2]) &
                                           ~df['log_comment'].str.contains(e[3]) &
                                           ~df['log_comment'].str.contains(e[4]), c, df.category)     
    
time_taken = time.time() - start_time
print(time_taken)

df = df[df['category'] != 'redirect']

summary = df.groupby(['year','category']).count()
summary.reset_index(inplace=True)
summary.head()

fig = px.area(summary, x="year", y="log_comment", color="category")
fig.show()
