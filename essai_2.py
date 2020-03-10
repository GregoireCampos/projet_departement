# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:59:03 2020

@author: campo
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import xlrd

workbook = xlrd.open_workbook('C:/Users/campo/Desktop/lucas_excel.xlsx')
SheetNameList = workbook.sheet_names()
#SheetNameList = excel_percentage
worksheet = workbook.sheet_by_name(SheetNameList[0])
#j'ai directement modifié les chiffres sur le fichier xlsx en les pondérant
num_rows = worksheet.nrows 
num_cells = worksheet.ncols 
#print( 'num_rows, num_cells', num_rows, num_cells )

# Comment lire l'excel
curr_row = 0
while curr_row < num_rows:
    row = worksheet.row(curr_row)
    """
    print row, len(row), row[0], row[1]
    print( 'Row: ', curr_row )
    print('regarde')
    print(row)
    print( row, len(row), row[0] )
    """
    curr_cell = 0
    while curr_cell < num_cells:
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        cell_type = worksheet.cell_type(curr_row, curr_cell)
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        # print( ' ', cell_type, ':', cell_value )
        curr_cell += 1
    curr_row += 1
    
# On veut créer une matrice avec les lignes : les différents critères et les colonnes : les différentes années
M=[]
criteria = []
i = 0
while i < 13 :
    # on ajoute la ligne en cours dans la liste
    ligne = []
    curr_row = i
    row = worksheet.row(curr_row)
    curr_cell = 0
    while curr_cell < num_cells:
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        if type(cell_value) == float :
            ligne.append(round(cell_value,4))
        else :
            ligne.append(cell_value)
        curr_cell += 1
    if i>0:
        criteria.append(str(ligne[0]))
    M.append(ligne[1:])
    i += 1

#print(M)
#print(dates)
# M est bien la matrice voulue

date = M[0]

data = pd.DataFrame(columns=[date], index = criteria)
for i in range (12):
    data.loc[criteria[i], date] = M[i+1][0:]
    
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

loading_scores = pd.Series(pca.components_[0], index=criteria)
# ensuite on trie les loading scores selon leur magnitude (= valeur absolue)
sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)
# ensuite on récupère le top 5 des gènes
top_10_genes = sorted_loading_scores[0:10].index.values

print(loading_scores[top_10_genes])

# on constate que les valeurs sont très proches donc beaucoup de gènes sont importants pour départager les deux 
# pools (et pas simplement un ou deux)
