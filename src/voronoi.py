
from utils import *
from constants import *

def compute_voronoi(cost_maps):
    n = cost_maps.length
    if n == 0:
        return None

    h,w = cost_maps[0].shape
    
    nearest_idcs = arr2d_create(w,h,0)
    for y in range(h):
        for x in range(w):
            idx = y*w+x
            nearest_idcs.data[idx] = \
                arr_argmin([cost_maps[k].data[idx] for k in range(n)])
            
            if cost_maps[nearest_idcs.data[idx]].data[idx] == BIG_VALUE:
                nearest_idcs.data[idx] = -1
    
    return nearest_idcs

def compute_voronoi_neighbors(nearest_idcs):
    h,w = nearest_idcs.shape
    neighbors = {}
    neighborhood_ = neighborhood()
    for y in range(0,h):
        for x in range(0,w):
            k = y*w+x
            if nearest_idcs.data[k] < 0: continue
            if nearest_idcs.data[k] not in neighbors:
                neighbors[nearest_idcs.data[k]] = {}
            for dx,dy in neighborhood_:
                dk = dy*w+dx
                if ((0 <= x+dx < w)
                    and (0 <= y+dy < h)
                    and (nearest_idcs.data[k+dk] >= 0)
                    and (nearest_idcs.data[k+dk] != nearest_idcs.data[k])):
                    neighbor = nearest_idcs.data[k+dk]
                    neighbors[nearest_idcs.data[k]][neighbor] = neighbor

    return neighbors
