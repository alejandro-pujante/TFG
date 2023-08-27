import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import json

q_values = pd.read_csv('q_values.csv' , sep = ',', header = None)
q_values = q_values.iloc[1::2]

error_values = pd.read_csv('error_values.csv' , header = None)

q_values = q_values.reset_index(drop=True)
error_values = error_values.reset_index(drop=True)

datos = pd.concat(  [q_values, error_values.iloc[:,0]] , axis = 1)

index = datos.iloc[:, -1].idxmin()

results = []

for i in q_values.iloc[index]:
    results.append(i)

emi = dict()

for i in range(len(results)):
    emi[f'{i+1}'] = results[i]


with open('emissions_results.json', 'w') as archivo_json:
    json.dump(emi, archivo_json)
