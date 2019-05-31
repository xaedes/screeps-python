import numpy as np
import math

def rand_point(terrain):
    h,w = terrain.shape
    return np.floor(np.random.rand(2) * (w,h)).astype("int")

def rand_points(terrain, num_points):
    points = []
    while len(points) < num_points:
        point = rand_point(terrain)
        if terrain[point[1],point[0]] > 0:
            points.append(point)
    points = np.array(points)
    return points

def distance(A,B):
    x0,y0=A
    x1,y1=B
    dx,dy=x0-x1,y0-y1
    return math.sqrt(dx*dx+dy*dy)

def neighborhood():
    return np.array([
        [dx,dy] 
        for dx in [-1,0,1]
        for dy in [-1,0,1]
        if not ((dx == 0) and (dy == 0))
    ])

def compute_cost_map(terrain_costs, point):
    h,w = terrain_costs.shape
    cost = np.zeros(terrain_costs.shape, dtype=float)
    cost[:,:] = np.infty
    visited = np.zeros(terrain_costs.shape, dtype=bool)
    stack = [point]
    cost[point[1],point[0]] = 0

    #print(neighbor_offsets)
    k=0
    while len(stack)>0:
        #plt.imshow(cost)
        #plt.plot(np.array(stack)[:,0],np.array(stack)[:,1],"o")
        stack = sorted(stack,key=lambda xy:-cost[xy[1],xy[0]])
        x,y = stack.pop()
        if visited[y,x]: continue
        visited[y,x] = True
        neighbors = [
            [x+dx,y+dy]
            for dx,dy in neighborhood()
            if 0 <= x+dx < w 
            and 0 <= y+dy < h
            and terrain_costs[y+dy,x+dx] < np.infty
        ]
        for nx,ny in neighbors:
            stack.append((nx,ny))
            if cost[y,x] + terrain_costs[ny,nx] < cost[ny,nx]:
                
                cost[ny,nx] = cost[y,x] + terrain_costs[ny,nx]
                
    return cost

def compute_voronoi(cost_maps):
    idcs = np.argmin(cost_maps,axis=0)
    idcs[cost_maps.min(axis=0) == np.infty] = -1
    return idcs

def comute_voronoi_neighbors(indices):
    h,w = indices.shape
    neighbors = dict()
    for k in range(0,indices.max()+1):
        neighbors[k] = set()
    for y in range(0,h):
        for x in range(0,w):
            if indices[y,x] < 0: continue
            for dx,dy in neighborhood():
                if ((0 <= x+dx < w)
                    and (0 <= y+dy < h)
                    and (indices[y+dy,x+dx] >= 0)
                    and (indices[y+dy,x+dx] != indices[y,x])):
                    
                    neighbors[indices[y,x]].add(indices[y+dy,x+dx])
    return neighbors

def map_terrain_costs(terrain, mapping={128:2, 255:1}):
    terrain_costs = np.zeros(terrain.shape, float)
    terrain_costs[:,:] = np.infty
    terrain_costs[terrain == 0] = np.infty
    for key,val in mapping.items():
        terrain_costs[terrain == key] = val
    return terrain_costs

def path_to(cost_map, start_pos, end_pos, maxit = 200, debug=False,w_eucl_cost=0.1,w_future_cost=1.0):
    tx,ty = end_pos
    x,y = start_pos
    neighbors = neighborhood()
    k = 0
    path = [(x,y)]
    h,w = cost_map.shape
    while not((x == tx) and (y == ty)) and k<maxit:
        k+=1
        moves = np.array([
            (x+dx,y+dy)
            for dx,dy in neighbors 
            if ((0 <= x+dx < w)
            and (0 <= y+dy < h)
               )])
            #and (cost_map[y+dy,x+dx] <= cost_map[y,x]))]
        costs = np.array([cost_map[y_,x_] for x_,y_ in moves])
        eucl_costs = np.sqrt(np.sum(np.square(moves-(x,y)),axis=1))
        future_costs = np.sqrt(np.sum(np.square(moves-(tx,ty)),axis=1))
        total_costs = costs+w_eucl_cost*eucl_costs+w_future_cost*future_costs
        if debug: print("#", k, list(zip(moves,total_costs)))
        best_move = np.argmin(total_costs)
        if debug: print("best_move", best_move)
        if debug: print("total_costs[best_move]", total_costs[best_move])
        sel_best_moves = total_costs == total_costs[best_move]
        if np.sum(sel_best_moves)>1:
            best_moves = moves[sel_best_moves]
            x,y = best_moves[np.random.randint(0,len(best_moves))]
        else:
            x,y = moves[best_move]
        path.append((x,y))
    return path

def compute_paths(cost_maps, points, voronoi_neighbors, w_eucl_cost=0.2, w_future_cost=0.3):
    num_points = points.shape[0]
    def compute_point_path(k,i):
        if k==i:
            return []
        elif i in voronoi_neighbors[k]:
            return path_to(
                cost_maps[i], points[k], points[i], 
                w_eucl_cost=w_eucl_cost, 
                w_future_cost=w_future_cost
            )
        else:
            return None        
    paths = np.array([
        [compute_point_path(k,i) 
         for i in range(num_points)]
        for k in range(num_points)
    ])
    return paths

def compute_path_distance_matrix(paths, points):
    num_points = points.shape[0]
    distance_matrix = np.array([
        [
            len(paths[k,i]) 
            if paths[k,i] is not None 
            else np.infty
            
            for i in range(num_points)
        ]
        for k in range(num_points)
    ])
    return distance_matrix

def compute_floyd(distance_matrix):
    result = distance_matrix.copy()
    h,w = result.shape
    assert(h==w)
    n=w
    goto = np.empty_like(result,dtype=int)
    for j in range(n):
        for i in range(n):
            if distance_matrix[i,j] < np.infty:
                goto[i,j] = j
            else:
                goto[i,j] = -1
    for k in range(n):
        for j in range(n):
            for i in range(n):
                if result[i,k]+result[k,j] < result[i,j]:
                    goto[i,j] = k
                    result[i,j] = result[i,k]+result[k,j]
    return result, goto

def relevant_transportation_costs(transportation_costs, sending_idx, receiving_idx):
    return np.array([[transportation_costs[i,k] 
                      for k in receiving_idx]
                      for i in sending_idx])

def zero_transport(sending, receiving):
    return np.zeros(shape=(len(sending),len(receiving)))

def greedy_transport(transport, cost, sending, receiving):
    
    received = transport.sum(axis=0)
    sent = transport.sum(axis=1)
    missing = receiving - received
    available = sending - sent
    #print("missing", missing)
    #print("available", available)
    sel_valid_available = available>0
    sel_valid_missing = missing>0
    idx_valid_available = np.arange(len(sel_valid_available))[sel_valid_available]
    idx_valid_missing = np.arange(len(sel_valid_missing))[sel_valid_missing]
    #print("idx_valid_available", idx_valid_available)
    #print("idx_valid_missing", idx_valid_missing)
    if len(idx_valid_available) > 0 and len(idx_valid_missing) > 0:
        costs = np.array([
            [
                relevant_transportation_costs[i,k]
                for k in idx_valid_missing
            ]
            for i in idx_valid_available
        ])
        #print("costs")
        #print(costs)
        best_idx_valid = np.argmin(costs)
        best_idx_valid_missing = best_idx_valid % len(idx_valid_missing)
        best_idx_valid_available = best_idx_valid // len(idx_valid_missing)
        #print("best_idx_valid_available", best_idx_valid_available)
        #print("best_idx_valid_missing", best_idx_valid_missing)
        amount = min(available[idx_valid_available[best_idx_valid_available]], missing[idx_valid_missing[best_idx_valid_missing]])
        #print("amount", amount)
        #print("idx_valid_available[best_idx_valid_available]", idx_valid_available[best_idx_valid_available])
        #print("idx_valid_missing[best_idx_valid_missing]", idx_valid_missing[best_idx_valid_missing])
        new_transport = np.zeros_like(transport)
        new_transport[idx_valid_available[best_idx_valid_available],idx_valid_missing[best_idx_valid_missing]] = amount
        #print("new_transport")
        #print(new_transport)
        return new_transport
    else:
        return np.zeros_like(transport)
    
def greedy_transport_iterative(transport, cost, sending, receiving):
    result = transport.copy()
    ntransport = greedy_transport(result, cost, sending, receiving)
    while np.sum(ntransport) > 0:
        result += ntransport
        ntransport = greedy_transport(result, cost, sending, receiving)
    return result