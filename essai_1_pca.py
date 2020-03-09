# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import data_process as dp
import pandas as pd
import numpy as np
import random as rd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
"""
genes = [dp.M[0][1:]]
col = dp.dates
data = pd.DataFrame(columns=col, index = genes)
for gene in data.index:
    for j in range(61):
        data.loc[gene, col[j]] = dp.M[j]

genes = ['gene' + str(i) for i in range(1,101)]

wt = ['wt'+str(i) for i in range (1,6)]
ko = ['ko'+str(i) for i in range (1,6)]

data = pd.DataFrame(columns=[*wt, *ko], index = genes)

for gene in data.index:
    data.loc[gene, 'wt1':'wt5'] = np.random.poisson(lam=rd.randrange(10,1000), size=5)
    data.loc[gene, 'ko1':'ko5'] = np.random.poisson(lam=rd.randrange(10,1000), size=5)

"""

criteria = dp.M[0]

date = dp.dates

data = pd.DataFrame(columns=[date], index = criteria)
dp.M = list(map(list, zip(*dp.M)))
for i in range (12):
    data.loc[criteria[i], dp.dates] = dp.M[i][1:]
    
print(data.head())
print(data.shape) 
# la on centre et scale les data, pour que la moyenne soit 0 et que la standard deviation soit 1. 
# Il faut qu'on transpose parce qu'il faut des lignes plutôt que des colonnes pour les scaler
scaled_data = preprocessing.scale (data.T)   

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

plt.bar(x = range(1, len(per_var)+1), height = per_var, tick_label = labels)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal component')
plt.title('Scree plot')
plt.show()
"""
pca_df = pd.DataFrame(pca_data, index=[date], columns = labels)
plt.scatter(pca_df.PC1, pca_df.PC2)
plt.title('My PCA Graph')
plt.xlabel('PC1 - {0}%'.format(per_var[0]))
plt.ylabel('PC2 - {0}%'.format(per_var[1]))
for sample in pca_df.index :
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))
plt.show()
"""
# les ko forment une colonne d'un côté, suggérant qu'ils forment un premier pool.
# les wt forment une colonne de l'autre côté, suggérant qu'ils forment un deuxième pool.
# la grande séparation entre les deux suggèrent que les deux groupes sont très différents

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

# on constate que les valeurs sont très proches donc beaucoup de gènes sont importants pour départager les deux 
# pools (et pas simplement un ou deux)