# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:38:07 2020

@author: campo
"""
import xlrd
import numpy as np
workbook = xlrd.open_workbook('C:/Users/campo/projet_dep/excel_percentage_ponderes.xlsx')
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
dates = []
i = 0
while i < 62 :
    # on ajoute la ligne en cours dans la liste
    ligne = []
    curr_row = i
    row = worksheet.row(curr_row)
    curr_cell = 0
    while curr_cell < num_cells:
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        if type(cell_value) == float :
            ligne.append(round(cell_value,2))
        else :
            ligne.append(cell_value)
        curr_cell += 1
    if i>0:
        dates.append(str(ligne[0]))
    M.append(ligne[1:])
    i += 1
#print(M)
#print(dates)
# M est bien la matrice voulue
    


