# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 19:45:11 2016

@author: alexis
"""

import os
import pandas as pd

file_name = 'data/durees.csv'
if not os.path.exists(file_name):
    import download

data = pd.read_csv(file_name, encoding='cp1252', sep=';',
                   skiprows=1)

# une ligne en trop
data.drop(168, inplace=True)

# on transforme les durées en seconde
for col in data.columns[2:]:
    data[col] = pd.to_timedelta(data[col])/pd.Timedelta('1s')

# a finir mais peut-être de nouvelles données viendront...
date = data.iloc[:,0]
count_by_date = date.value_counts()
a_regarder = count_by_date[count_by_date == 13].index
categories = data[date == 'juin-10'].iloc[:,1]
for a_voir in a_regarder:
    print("probleme pour ", a_voir)
    extrait = data[date == a_voir].iloc[:,1]
    manquant = ~categories.isin(extrait)
    print(categories[manquant])


# change les dates
mois_to_num = dict(
    janv = '01',
    févr = '02',
    mars = '03',
    avr = '04',
    mai = '05',
    juin = '06',  
    juil = '07',
    août = '08',
    sept = '09',
    oct = '10',
    nov = '11',
    déc = '12',
    )

for mois, num in mois_to_num.items():
    date = date.str.replace(mois + '.-', num + '-')
    date = date.str.replace(mois + '.', num + '-')
data.iloc[:,0] = date


data.iloc[:,1][~data.iloc[:,1].isin(categories.values)].value_counts()

data.groupby(date)['Totaux'].sum()

data.columns = ['date', 'sujet'] + data.columns.tolist()[2:]
# on fait les brutes pour l'instant...
data.to_csv('data/durees2.csv', index=False)