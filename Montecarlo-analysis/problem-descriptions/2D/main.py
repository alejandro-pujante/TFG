import numpy as np
import csv
import json

with open('meshes/2D/mesh_limits.json', 'r') as f:
  limits = json.load(f)

with open('outputs/test/sources_coordinates.json', 'r') as g:
  sources = json.load(g)


filename_mesh = "../../meshes/2D/grid.mesh"


delta = 0.001
x_left = limits['x_axis']['left'] + delta
x_right = limits['x_axis']['right'] - delta
y_up = limits['y_axis']['up'] - delta
y_down = limits['y_axis']['down'] + delta



options = {
    'nls' : 'newton', # Nonlinear solver
    'ls' : 'ls', # Linear solver
    'output_format': 'vtk',
    'output_dir': './outputs/test',
    'ts' : 'ts',
    'save_times' : 'all', 
}

regions = {
    'Omega': 'cells of group 1',

    # Vertices corresponding to wall 
    'g_b1': (f'vertices in (x < {x_left})', 'facet'),
    'g_b2': (f'vertices in (x > {x_right})', 'facet'),
    'g_b3': (f'vertices in (y < {y_down})', 'facet'),
    'g_b4': (f'vertices in (y > {y_up})', 'facet'),

    'Gamma_build': ('r.g_b1 +v r.g_b2 +v r.g_b3 +v r.g_b4', 'facet'),

    # Sources
    'Omega_1': 'vertices by get_source_cells_1',
    'Omega_2': 'vertices by get_source_cells_2',
    'Omega_3': 'vertices by get_source_cells_3',

}

fields = {
    'concentration': ('real', 1, 'Omega', 1),
}

variables = {
    'c': ('unknown field', 'concentration', 0, 1),
    's': ('test field', 'concentration', 'c'),
}

ebcs = {
    'c_build': ('Gamma_build', {'c.0': 0.01}),
}

q1 = np.random.normal(30,20,1)[0]
q2 = np.random.normal(30,20,1)[0]
q3 = np.random.normal(30,20,1)[0]


materials = {
    'diff': ({'val': 1}, ),
    'source_1': ({'val': 10}, ),
    'source_2': ({'val': 25}, ),
    'source_3': ({'val': 25}, ),


    'wind': ({'val':  [[0.15], [0]]}, ),
}


integrals = {
    'i': 2
}

equations = {
    'Diffusion': """  dw_advect_div_free.i.Omega( wind.val, s, c ) + dw_laplace.i.Omega( diff.val, s, c )
                    = dw_volume_lvf.i.Omega_1( source_1.val, s )
                     + dw_volume_lvf.i.Omega_2( source_2.val, s ) 
                     + dw_volume_lvf.i.Omega_3( source_3.val, s )"""
}

solvers = {
    'ls' : ('ls.scipy_direct', {}),
    'newton' : ('nls.newton',
                {'i_max'      : 1,
                 'eps_a'      : 1e-10,
    }),
}


functions = {
    'get_source_cells_1': (lambda coors, domain=None:
                         get_source_cells_1(coors[:, 0], coors[:, 1], 0), ),

    'get_source_cells_2': (lambda coors, domain=None:
                         get_source_cells_2(coors[:, 0], coors[:, 1], 0), ),     

    'get_source_cells_3': (lambda coors, domain=None:
                         get_source_cells_3(coors[:, 0], coors[:, 1], 0), ),                 
}

def get_source_cells_1(x, y, z, center=(sources['x']['x1'], sources['y']['y1'], 0.0), radius= 2):
    x0, y0, _ = center 
    r = np.sqrt( (x - x0)**2 + (y - y0)**2 )
    indx = np.where(r < radius)[0]

    n = indx.shape[0]
    if n <= 1:
        raise ValueError(f'Too few cells selected ({n})')

    return indx


def get_source_cells_2(x, y, z, center=(sources['x']['x2'], sources['y']['y2'], 0.0), radius= 2):
    x0, y0, _ = center 
    r = np.sqrt( (x - x0)**2 + (y - y0)**2 )
    indx = np.where(r < radius)[0]

    n = indx.shape[0]
    if n <= 1:
        raise ValueError(f'Too few cells selected ({n})')

    return indx

def get_source_cells_3(x, y, z, center=(sources['x']['x3'], sources['y']['y3'], 0.0), radius= 2):
    x0, y0, _ = center 
    r = np.sqrt( (x - x0)**2 + (y - y0)**2 )
    indx = np.where(r < radius)[0]

    n = indx.shape[0]
    if n <= 1:
        raise ValueError(f'Too few cells selected ({n})')

    return indx



with open('./outputs/test/q_values.csv', mode='a') as q_file:
    q_writer = csv.writer(q_file)
    q_writer.writerow([q1, q2])


print('PECLET NUMBER = ', 12*(materials['wind'][0]['val'][0][0] / materials['diff'][0]['val']) )