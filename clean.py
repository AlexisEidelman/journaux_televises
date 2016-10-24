# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 19:45:11 2016

@author: alexis
"""

import os
import pandas as pd

file_name = 'data/new_durees.csv'
if not os.path.exists(file_name):
    import download

data = pd.read_csv(file_name, encoding='cp1252', sep=';',
                   skiprows=1)

data.columns = ['date', 'sujet'] + data.columns.tolist()[2:]
# une ligne en trop dans la premiere version
# data.drop(168, inplace=True)

# on transforme les durées en seconde
for col in data.columns[2:]:
    data[col] = pd.to_timedelta(data[col])/pd.Timedelta('1s')

for icol in range(2, data.shape[1]):
    assert data.iloc[:,icol].dtype == 'float64'

assert all(data.notnull())
# a finir mais peut-être de nouvelles données viendront...
date = data.date
categories = data.sujet.unique()
assert all(data.date.value_counts() == len(categories))
# en cas de soucis
#count_by_date = date.value_counts()
#a_regarder = count_by_date[count_by_date == 13].index
#for a_voir in a_regarder:
#    print("probleme pour ", a_voir)
#    extrait = data[date == a_voir].iloc[:,1]
#    manquant = ~categories.isin(extrait)
#    print(categories[manquant])

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

date.replace('09-mbre-10', '09-10', inplace=True)
assert all(date.str.len() == 5)
date = pd.to_datetime(date, format='%m-%y')
data.index = pd.DatetimeIndex(date).normalize()
del data['date']

Total = data['Totaux']
del data['Totaux']
assert all(data.sum(axis=1) == Total)

# pourcentage par sujet 
pourcent_by_sujet = data.copy()
pourcent_by_sujet.iloc[:,1:] = pourcent_by_sujet.iloc[:,1:].divide(Total, axis=0)


# on fait les brutes pour l'instant...

# Tidy data operation
tidy_data = data.reset_index()
data = pd.melt(tidy_data, id_vars=['index','sujet'])
data.columns = ['date', 'sujet', 'chaine', 'temps']

data.to_csv('data/durees2.csv')