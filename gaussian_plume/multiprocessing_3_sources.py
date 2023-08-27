from gaussian_plume_model import GaussianModel
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
import multiprocessing
import pandas as pd
import time

inicio = time.time()

RUNMODE = "plan"  # Generate the x-y view at z=0
STABILITY = {"condition": "constant", "value": 1}

WIND_1 = {"condition": "constant", "speed": 10.0, "direction": 90.0}
WIND_2 = {"condition": "constant", "speed": 10.0, "direction": 60.0}
WIND_3 = {"condition": "constant", "speed": 10.0, "direction": 200.0}

STACKS_1 = [(10, 0.0, 2)] 
STACKS_2 = [(5, 9.0, 2)]
STACKS_3 = [(-8, -20, 2)]

flux_1 = [100]
flux_2 = [60]
flux_3 = [10]

xlims = (-20.0, 20.0)
ylims = xlims
zlims = (0.0, 10.0)
tlims = (0.0, 1.0)
deltas = {"dx": 0.2, "dy": 0.2, "dz": 0.5, "dt": 1.0}

solver = GaussianModel(xlims, ylims, zlims, tlims, runmode="plan", **deltas)
C = solver.solve(flux_1, STACKS_1, STABILITY, WIND_1) + solver.solve(flux_2, STACKS_2, STABILITY, WIND_2) + solver.solve(flux_3, STACKS_3, STABILITY, WIND_3)

plt.imshow(C)
plt.scatter(60,50, color = 'black', s =10)
plt.scatter(50,130, color = 'black', s =10)
plt.scatter(100,100, color = 'black', s =10)
plt.savefig('3_sources.png')

ob1 = C[50,60,0]
ob2 = C[130,50,0]
ob3 = C[100,100,0]


def gaus_3(q1, q2, q3):
        
    flux_1 = [q1]
    flux_2 = [q2]
    flux_3 = [q3]

    C = solver.solve(flux_1, STACKS_1, STABILITY, WIND_1) + solver.solve(flux_2, STACKS_2, STABILITY, WIND_2) + solver.solve(flux_3, STACKS_3, STABILITY, WIND_3)
        
    a = C[50,60,0]
    b = ob1
    
    c = C[130,50,0]
    d = ob2
    
    e = C[100,100,0]
    f = ob3
    
    
    dif1 = (a-b)**2
    dif2 = (c-d)**2
    dif3 = (e-f)**2
    
    dif = dif1 + dif2 + dif3
    
    return q1, q2, q3, dif



inicio = time.time()

N = 100

qs_1 = np.random.normal(75, 20, N)
qs_2 = np.random.normal(75, 20, N)
qs_3 = np.random.normal(75, 20, N)

if __name__ == '__main__':
    num_processes = multiprocessing.cpu_count()
    num_iterations = N
    pool = multiprocessing.Pool(processes=num_processes)
    results = []
    for i in range(len(qs_1)):
        a = qs_1[i]
        b = qs_2[i]
        c = qs_3[i]
        result = pool.apply_async(gaus_3, args=(a, b, c))
        results.append(result)
    pool.close()
    pool.join()
    output = [(result.get()[0], result.get()[1], result.get()[2],  result.get()[3]) for result in results]
    

    datos = pd.DataFrame(output, columns = ['q1' , 'q2' ,'q3' , 'err' ])

    indice = datos['err'].idxmin()

    fin = time.time()

    tiempo_total = fin - inicio

    print(datos.q1[indice])
    print(datos.q2[indice])
    print(datos.q3[indice])


    print("Tiempo:", tiempo_total, "sec.")
