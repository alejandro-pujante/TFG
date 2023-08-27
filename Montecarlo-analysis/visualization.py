import meshio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
import json

with open('outputs/test/sensor_coordinates.json', 'r') as g:
  sensor = json.load(g)


# READ VTK FILE BY OUTPUT DIRECTORY

mesh = meshio.read('outputs/test/grid.vtk')

# READ CSV OF COORDINATES BY MESH FILE (EDIT)

data = pd.read_csv('outputs/test/coordinates.csv', sep=',')

df = pd.DataFrame(data)
df = df.iloc[:, 1:-1]
df.columns = ['x', 'y']
df['concentration'] = mesh.point_data['c']

plt.scatter(df.x, df.y, c= df.concentration, s = 6, cmap = 'turbo', marker='s')


plt.plot(list(sensor['x'].values()) , list(sensor['y'].values()) , 'ro' ,markersize=7, alpha = 0.7, label = 'Puntos de monitoreo')


cbar = plt.colorbar()

plt.tricontour(df.x, df.y, df.concentration, levels = np.linspace(0, 12 , 11), linewidths=0.5, colors='k')

# plt.text(-90, 80, '(d)', color = 'white', fontsize = 19)

# plt.title('$P_e = 840$', fontsize = 17) ; plt.xlabel('$x (m)$', fontsize = 13) ; plt.ylabel('$y (m)$', fontsize = 13)

cbar.set_label(f'Concentración ($g/m^{3}$)')
plt.legend(loc = 'upper left', fontsize = "9")

plt.savefig('heatmaps-images/heatmap_3sources.png', bbox_inches='tight')
plt.savefig('heatmaps-images/heatmap_3sources.pdf' , bbox_inches='tight')

