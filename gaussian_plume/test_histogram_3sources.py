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

WIND_1 = {"condition": "constant", "speed": 10.0, "direction": 75.0}
WIND_2 = {"condition": "constant", "speed": 10.0, "direction": 60.0}
WIND_3 = {"condition": "constant", "speed": 10.0, "direction": 200.0}

STACKS_1 = [(30, 20, 2)] 
STACKS_2 = [(25, 29, 2)]
STACKS_3 = [(12, 0, 2)]

flux_1 = [100]
flux_2 = [80]
flux_3 = [60]

xlims = (0.01, 30.0)
ylims = xlims
zlims = (0.0, 1.0)
tlims = (0.0, 1.0)
deltas = {"dx": 0.5, "dy": 0.5, "dz": 1, "dt": 1.0}

solver = GaussianModel(xlims, ylims, zlims, tlims, runmode="plan", **deltas)
C = solver.solve(flux_1, STACKS_1, STABILITY, WIND_1) + solver.solve(flux_2, STACKS_2, STABILITY, WIND_2) + solver.solve(flux_3, STACKS_3, STABILITY, WIND_3)

dx = deltas['dx']
dy = deltas['dy']

p1 = [10,10]
p2 = [10,27]
p3 = [20,20]


ob1 = C[int(p1[1]/dx), int(p1[0]/dy), 0]
ob2 = C[int(p2[1]/dx), int(p2[0]/dy), 0]
ob3 = C[int(p3[1]/dx), int(p3[0]/dy), 0]

def gaus_3(q1, q2, q3):
        
    flux_1 = [q1]
    flux_2 = [q2]
    flux_3 = [q3]

    C = solver.solve(flux_1, STACKS_1, STABILITY, WIND_1) + solver.solve(flux_2, STACKS_2, STABILITY, WIND_2) + solver.solve(flux_3, STACKS_3, STABILITY, WIND_3)
        
    a = C[int(p1[1]/dx), int(p1[0]/dy), 0]
    b = ob1
    
    c = C[int(p2[1]/dx), int(p2[0]/dy), 0]
    d = ob2
    
    e = C[int(p3[1]/dx), int(p3[0]/dy), 0]
    f = ob3
    
    
    dif1 = (a-b)**2
    dif2 = (c-d)**2
    dif3 = (e-f)**2
    
    dif = dif1 + dif2 + dif3
    
    return q1, q2, q3, dif

inicio = time.time()

N = 4**4

q1 = []
q2 = []
q3 = []

for j in range(10_000):
    print(f'Comienza la simulación {j}')

    qs_1 = np.random.normal(80, 17, N)
    qs_2 = np.random.normal(80, 17, N)
    qs_3 = np.random.normal(80, 17, N)


    if __name__ == '__main__':
        num_processes = multiprocessing.cpu_count()
        num_iterations = N
        pool = multiprocessing.Pool(processes=num_processes)
        results = []
        for i in range(len(qs_1)):

            result = pool.apply_async(gaus_3, args=(qs_1[i], qs_2[i], qs_3[i]))
            results.append(result)
        pool.close()
        pool.join()
        output = [(result.get()[0], result.get()[1], result.get()[2],  result.get()[3]) for result in results]


        datos = pd.DataFrame(output, columns = ['q1' , 'q2' ,'q3','err' ])

        indice = datos['err'].idxmin()

        fin = time.time()

        tiempo_total = fin - inicio

        q1.append(datos.q1[indice])
        q2.append(datos.q2[indice])
        q3.append(datos.q3[indice])
        
tiempo_total = fin - inicio

print("Tiempo:", tiempo_total, "sec.")

print(np.mean(q1), np.mean(q2), np.mean(q3))
print(np.std(q1), np.std(q2), np.std(q3))
print(N)

values = [256, 1024, 4096]