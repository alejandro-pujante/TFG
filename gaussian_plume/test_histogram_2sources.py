from gaussian_plume_model import GaussianModel
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
import multiprocessing
import pandas as pd
import time
import csv

inicio = time.time()

RUNMODE = "plan"  # Generate the x-y view at z=0
STABILITY = {"condition": "constant", "value": 1}

WIND_1 = {"condition": "constant", "speed": 10.0, "direction": 75.0}
WIND_2 = {"condition": "constant", "speed": 10.0, "direction": 60.0}

STACKS_1 = [(30, 20, 2)] 
STACKS_2 = [(25, 29, 2)]

flux_1 = [100]
flux_2 = [60]

xlims = (0.01, 30.0)
ylims = xlims
zlims = (0.0, 1.0)
tlims = (0.0, 1.0)
deltas = {"dx": 0.7, "dy": 0.7, "dz": 1, "dt": 1.0}

solver = GaussianModel(xlims, ylims, zlims, tlims, runmode="plan", **deltas)
C = solver.solve(flux_1, STACKS_1, STABILITY, WIND_1) + solver.solve(flux_2, STACKS_2, STABILITY, WIND_2) 

dx = deltas['dx']
dy = deltas['dy']

p1 = [12,18]
p2 = [15,25]

ob1 = C[int(p1[1]/dx), int(p1[0]/dy), 0]
ob2 = C[int(p2[1]/dx), int(p2[0]/dy), 0]

def gaus_3(q1, q2):
        
    flux_1 = [q1]
    flux_2 = [q2]

    C = solver.solve(flux_1, STACKS_1, STABILITY, WIND_1) + solver.solve(flux_2, STACKS_2, STABILITY, WIND_2) 
        
    a = C[int(p1[1]/dx), int(p1[0]/dy), 0]
    
    b = C[int(p2[1]/dx), int(p2[0]/dy), 0]
        
    
    dif1 = (a-ob1)**2
    dif2 = (b-ob2)**2
    
    dif = dif1 + dif2 
    
    sim = [a, b]
    real = [ob1, ob2]
    

    return q1, q2, dif

inicio = time.time()

N = 4**8

q1 = []
q2 = []

for j in range(1000):
    print(f'Comienza la simulación {j}')

    qs_1 = np.random.normal(80, 20, N)
    qs_2 = np.random.normal(80, 20, N)

    if __name__ == '__main__':
        num_processes = multiprocessing.cpu_count()
        num_iterations = N
        pool = multiprocessing.Pool(processes=num_processes)
        results = []
        for i in range(len(qs_1)):

            result = pool.apply_async(gaus_3, args=(qs_1[i], qs_2[i]))
            results.append(result)
        pool.close()
        pool.join()
        output = [(result.get()[0], result.get()[1], result.get()[2]) for result in results]


        datos = pd.DataFrame(output, columns = ['q1' , 'q2' ,'err' ])

        indx_dif = datos['err'].idxmin()
        
        fin = time.time()

        tiempo_total = fin - inicio

        q1.append(datos.q1[indx_dif])
        q2.append(datos.q2[indx_dif])
        
tiempo_total = fin - inicio

print("Tiempo:", tiempo_total, "sec.")

print(np.mean(q1), np.mean(q2))
print(np.std(q1), np.std(q2))


with open('data-outputs/hist-q1-6.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(q1)

with open('data-outputs/hist-q2-6.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(q2)


with open('data-outputs/q1-n-stats.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([N, np.mean(q1), np.std(q1)])

with open('data-outputs/q2-n-stats.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([N, np.mean(q2) , np.std(q2)])
