# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 19:40:37 2016

@author: alexis
"""

import urllib.request

url = 'https://www.data.gouv.fr/s/resources/classement-thematique-des-' + \
    'sujets-de-journaux-televises/20161012-124930/INA_barometre_JT-' + \
    'TV_donnees-mensuelles_2005-2015_durees.csv'

file_name = 'data/durees.csv'

with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    data = response.read() # a `bytes` object
    out_file.write(data)