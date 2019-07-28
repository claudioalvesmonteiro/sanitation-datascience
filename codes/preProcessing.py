'''
OSAR
@observatoriosar
observatoriosar.wordpress.com

@ Claudio Alves Monteiro 2019
'''

# import modules
import numpy as np
import pandas as pd
import os
import re


#========================================
#           IMPORTING DATA
#========================================

#------------- loop for reading and concatenate data

# path and list  of files
path = 'data/SNIS/'
fl = os.listdir(path)

# function to take first 4 characters in a string
def take4(string):
    cont = 0
    str_out = ''
    while cont <= 3:
        str_out =  str_out + string[cont]
        cont = cont + 1
    return str_out

''' Loop to read and concatenate files. Verify if is Excel file,
    Reads first dataset and concat subsequentials,
    Includes year of data based on file name.
'''
key = True
for f in fl:
    if f.endswith(".xls"):
        year = take4(f)
        if key == True:
            df = pd.ExcelFile(path + f)
            df = df.parse(0)
            df['Ano'] = year
            key = False
        else:
            x = pd.ExcelFile(path + f)
            x = x.parse(0)
            x['Ano'] = year
            df = pd.concat([df, x])

'''
# CSV Version
key = True
for f in fl:
    if f.endswith(".csv"):
        year = take4(f)
        if key == True:
            df = pd.read_csv(path + f, sep = ';', header = 0, encoding = 'UTF-16', error_bad_lines=False)
            df['Ano'] = year
            key = False
        else:
            x = pd.read_csv(path + f, sep = ';', header = 0, encoding = 'UTF-16', error_bad_lines=False)
            x['Ano'] = year
            df = pd.concat([df, x])
'''

#====================================
# CLEAN DATA
#====================================

# select columns
colnames = ['Código do Município', 'Município', 'Estado', 'Região',
           'Ano', 'IN049 - Índice de perdas na distribuição']
df = df[colnames]

# rename columns
df.columns =  ['codigo_municipio', 'municipio', 'estado',
                'regiao', 'ano', 'IN049']

# remove NA
df['IN049'].isna().sum()
df['IN049'].dropna(inplace=True)

# create new column
df['index'] = list(np.arange(0,len(df)))

# make new column the new index
df.set_index('index', inplace=True)

# remove non integers
print((df['IN049'].apply(lambda x: isinstance(x, int)).sum() / len(df))*100,  '% of data are integers')
df = df[df['IN049'].apply(lambda x: isinstance(x, int))]

# remove negative and >100% values
df = df[(df['IN049'] <= 100) & (df['IN049'] >= 0)]

# select totals [non city data]
selector = df['codigo_municipio'].str.contains('TOTAL').fillna(False)
totais = df[selector]


#================================
# SELECT AND SAVE DATA
#===============================

''' function to extract name of territory
'''
def terrExtract(text):
    m = re.search('AMOSTRA (.+?):', text)
    if m:
        return m.group(1)
    else:
        return 'NA'

#----------------------- select city data

# select non-totals [city data]
citySNIS = df[selector == False]

# save data
citySNIS.to_csv('SNIS_IN049_serie_cidades.csv', index = False)
#citySNIS.to_parquet('SNIS_IN049_serie_cidades.parquet')
#citySNIS.to_excel('SNIS_IN049_serie_cidades.xls', index = False)

#----------------------- select national data

# select national level at 'total da amostra'
brSNIS = totais.copy()
brSNIS = brSNIS[brSNIS['codigo_municipio'] == 'TOTAL da AMOSTRA:']

# create territory and rename columns
brSNIS['territorio'] = 'Brasil'

# save data
brSNIS = brSNIS[['territorio','ano', 'IN049']]
brSNIS.to_csv('SNIS_IN049_serie_brasil.csv', index = False)
brSNIS.to_excel('SNIS_IN049_serie_brasil.xls', index = False)

#------------------------ select region data

# list of regions
regs = ['Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

# loop to identify and create selection booleans
select = [False]*len(totais)
for i in regs:
    select = select + totais['codigo_municipio'].str.contains(i)

# select region data
regSNIS = totais.copy()
regSNIS = regSNIS[select]

# append territory column
regSNIS['regiao'] = regSNIS['codigo_municipio'].apply(terrExtract)

# save data
regSNIS = regSNIS[['regiao', 'ano', 'IN049']]
regSNIS.to_csv('SNIS_IN049_serie_regioes.csv', index = False)
regSNIS.to_excel('SNIS_IN049_serie_regioes.xls', index = False)

#-------------------- select state data

# transform region in false and others in true
selection = select == False

# national value as False
nat_sel = totais['codigo_municipio'] != 'TOTAL da AMOSTRA:'

# build selector
selector = selection & nat_sel

# select cases
stateSNIS = totais[selector]

# append territory column
stateSNIS['estado'] = stateSNIS['codigo_municipio'].apply(terrExtract)

# save data
stateSNIS = stateSNIS[['estado', 'ano', 'IN049']]
stateSNIS.to_csv('SNIS_IN049_serie_estados.csv', index = False)
stateSNIS.to_excel('SNIS_IN049_serie_estados.xls', index = False)
