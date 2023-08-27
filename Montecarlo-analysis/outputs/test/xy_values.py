import meshio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

# READ VTK FILE BY OUTPUT DIRECTORY

mesh = meshio.read('grid.vtk')

# READ CSV OF COORDINATES BY MESH FILE (EDIT)

data = pd.read_csv('coordinates.csv', sep=',')

df = pd.DataFrame(data)
df = df.iloc[:, 1:-1]
df.columns = ['x', 'y']
df['concentration'] = mesh.point_data['c']

x_1 = -25
y_1 = -15

x_2 = 0
y_2 = 20

x_3 = 50
y_3 = -10

c1 = df.iloc[cdist(df[['x', 'y']], [(x_1, y_1)], metric='euclidean').argmin()]['concentration']
c2 = df.iloc[cdist(df[['x', 'y']], [(x_2, y_2)], metric='euclidean').argmin()]['concentration']
c3 = df.iloc[cdist(df[['x', 'y']], [(x_3, y_3)], metric='euclidean').argmin()]['concentration']


print(c1, c2, c3)

