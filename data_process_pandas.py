# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:04:48 2020

@author: campo
"""

import pandas as pd
import data_process as dp
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/campo/projet_dep/excel_percentage_ponderes.csv', sep = " ; ", index_col = 0)
scaled_data = preprocessing.scale (df)   
# création de l'objet PCA
pca = PCA()
# maths de la pca (calcul des loading scores et des variations)
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)
# on calcule le pourcentage de variation de chaque composante principale
per_var = np.round(pca.explained_variance_ratio_*100, decimals = 1)
# on crée les labels pour plotter
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
# on utilise matplotlib pour faire le bazar
criteria = dp.M[0]

plt.bar(x = range(1, len(per_var)+1), height = per_var, tick_label = labels)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal component')
plt.title('Scree plot')
plt.show()

# on finit en regardant l'habileté de PC1 à déterminer quel gène a la plus grande influence
# pour séparer les deux clusters le long de l'axe des abscisses
# On commence par créer des Series pandas avec les loading scores de PC1. Elles sont indexées
# par 0 donc PC1 = 0
loading_scores = pd.Series(pca.components_[0], index=criteria)
# ensuite on trie les loading scores selon leur magnitude (= valeur absolue)
sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)
# ensuite on récupère le top 10 des gènes
top_10_genes = sorted_loading_scores[0:10].index.values

print(loading_scores[top_10_genes])
