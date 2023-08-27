import numpy as np
import pandas as pd
import meshio
import json

mesh = meshio.read('grid.mesh')

data = pd.DataFrame(mesh.points)
data.to_csv('../../outputs/test/coordinates.csv')
data.columns = ['x' , 'y' , 'z']

x_left = min(data.x)
x_right = max(data.x)
y_up = max(data.y)
y_down = min(data.y)

limits = {
    "x_axis": {
        "left": x_left,
        "right": x_right 
    } ,

    "y_axis": {
        "up": y_up,
        "down": y_down
    }
}

with open("mesh_limits.json", "w") as file:
    json.dump(limits, file)