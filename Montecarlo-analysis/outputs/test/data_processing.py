import meshio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
import csv
import json

def dif2(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Las listas de datos/sensores y datos/simulados deben tener la misma longitud")
    return np.sum((np.array(list1) - np.array(list2)) ** 2)


# READ VTK FILE BY OUTPUT DIRECTORY

mesh = meshio.read('grid.vtk')

# READ CSV OF COORDINATES BY MESH FILE (EDIT)

df = pd.read_csv('coordinates.csv', sep = ',', index_col = None)
df.columns = ['index','x', 'y', 'z']
df['concentration'] = mesh.point_data['c']

# READ CSV OF SENSOR DATA

sensor_data = pd.read_csv('sensor_data.csv')

# READ COORDINATES OF SENSORS 

with open('sensor_coordinates.json', 'r') as f:
  data = json.load(f)


data_obs = sensor_data.iloc[0].values
data_sim = []


for x, y in zip(data['x'].values(), data['y'].values()):
    idx = cdist(df[['x', 'y']].values, np.array([(x, y)]), metric='euclidean').argmin()
    data_sim.append(df.loc[idx, 'concentration'])  

with open('error_values.csv', mode='a', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow([ dif2(data_obs, data_sim)] )