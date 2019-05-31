from constants import *
from utils import *





def terrain_costs(room):
    terrain = room.getTerrain()
    w = ROOM_WIDTH
    h = ROOM_HEIGHT
    costs = arr2d_create(w,h,BIG_VALUE)
    for y in range(h):
        for x in range(w):
            terrain_at = terrain.js_get(x,y)
            if terrain_at == TERRAIN_MASK_WALL:
                costs.data[y*w+x] = BIG_VALUE
            elif terrain_at == TERRAIN_MASK_SWAMP:
                costs.data[y*w+x] = 2
            elif terrain_at == 0:
                costs.data[y*w+x] = 1
    return costs


def pathcost_transform(costs, point):
    h,w = costs.shape
    pathcost = arr2d_create(h,w,BIG_VALUE)
    visited = arr2d_create(h,w,False)
    x,y = point
    x = int(x)
    y = int(y)
    priority_list = [[x,y]]
    pathcost.data[y*w+x] = 0
    neighborhood_ = neighborhood()
    k = 0
    while priority_list.length > 0:
        priority_list = _.sortBy(priority_list, lambda xy:-pathcost.data[xy[1]*w+xy[0]])
        x,y = priority_list.pop()
        if visited.data[y*w+x]: continue
        visited.data[y*w+x] = True
        for dx,dy in neighborhood_:
            nx = x+dx
            ny = y+dy
            in_bounds = 0 <= nx < w and 0 <= ny < h
            walkable = costs.data[ny*w+nx] < BIG_VALUE
            improvement = pathcost.data[y*w+x] + costs.data[ny*w+nx] < pathcost.data[ny*w+nx]

            if (in_bounds and walkable and improvement):
                priority_list.push([nx,ny])
                pathcost.data[ny*w+nx] = pathcost.data[y*w+x] + costs.data[ny*w+nx]

    return pathcost