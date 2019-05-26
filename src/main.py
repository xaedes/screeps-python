
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
# from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def processRoom(room):
    pass

def processCreep(creep):
    pass

def ids_of(seq):
    return _.map(seq, lambda item: item.id)

def findSites(room):
    # sites include spawn, controller, sources, energy consuming structures
    spawns = ids_of(room.find(FIND_MY_SPAWNS))
    controller = ids_of([room.controller])
    sources = ids_of(room.find(FIND_SOURCES))
    construction_sites = ids_of(room.find(FIND_MY_CONSTRUCTION_SITES))
    extensions = ids_of(room.find(FIND_MY_STRUCTURES, { "filter": { "structureType" : STRUCTURE_EXTENSION } }))
    towers = ids_of(room.find(FIND_MY_STRUCTURES, { "filter": { "structureType" : STRUCTURE_TOWER } }))
    # for site_id in spawns:
        # console.log(site_id)
    
    sites = [].concat(
        spawns, controller, sources, construction_sites, extensions, towers
    )

    return sites

def findPath(pos1,pos2):
    res = PathFinder.search(pos1,{"pos":pos2,"range":0})
    if res.incomplete:
        return None
    else:
        return res.path

def drawPath(path):
    n = path.length or 0
    if n == 0: return
    for k in range(n-1):
        if path[k].roomName != path[k+1].roomName: continue
        room = Game.rooms[path[k].roomName]
        if room:
            room.visual.line(
                path[k].x, path[k].y,
                path[k+1].x, path[k+1].y)

def findWalkablePosition(room, xy, range):
    x,y = xy
    x0 = int(x-range) # round down
    y0 = int(y-range) # round down
    x1 = int(x+range+1) # round up
    y1 = int(y+range+1) # round up
    terrain = room.lookForAtArea(LOOK_TERRAIN, y0,x0,y1,x1,True)
    walkable = _.filter(terrain, lambda item: item.terrain != "wall")
    # console.log(walkable)
    if walkable.length == 0:
        console.log("!")
        return None,None
    else:
        closest = _.sortBy(walkable, lambda item: distanceTo(x,y,item.x,item.y))
        return closest[0].x, closest[0].y

def updateSites(room):
    if True or "sites" not in room.memory:
        sites = findSites(room)
        room.memory.sites = sites

    for k,site_id in enumerate(room.memory.sites):
        site = Game.getObjectById(site_id)
        # room.visual.text("site {}".format(k), site.pos)

    if True or "clusters" not in room.memory:
        rangeThreshold = 10
        clusters = clusterSites(room.memory.sites, rangeThreshold)
        room.memory.clusters = []
        for k,cluster in enumerate(clusters):
            cluster_name = room.name + "_" + String(k)
            room.memory.clusters.push({
                "id": cluster_name,
                "ids": cluster,
                "pos": findWalkablePosition(room, meanPosition(cluster), rangeThreshold),
                "range": rangeThreshold,
                "paths": {}
                })

        # console.log("clusters", JSON.stringify(clusters))


    for k in range(room.memory.clusters.length or 0):
        cluster_k = room.memory.clusters[k]
        x,y = cluster_k.pos
        r = cluster_k.range
        room.visual.text("🏴",x,y)
        room.visual.circle(x,y,{"radius": r, "opacity": 0.1})
        for i in range(k+1,room.memory.clusters.length or 0):
            cluster_i = room.memory.clusters[i]
            x2,y2 = cluster_i.pos
            room.visual.line(x,y,x2,y2,{"color":"#112AA7"})

            # see if we computed one side of the path already
            path_ki = cluster_k.paths[cluster_i.id] or findPath(
                room.getPositionAt(x,y),
                room.getPositionAt(x2,y2)
            )

            if  not cluster_k.paths[cluster_i.id] and path_ki:
                cluster_k.paths[cluster_i.id] = path_ki
            if not cluster_i.paths[cluster_k.id] and path_ki:
                cluster_i.paths[cluster_k.id] = path_ki.reverse()
            
            if path_ki:
                drawPath(path_ki)
            # PathFinder.
                room.visual.text(String(path_ki.length),(x+x2)/2,(y+y2)/2)
                room.visual.text(String(path_ki.length),path_ki[path_ki.length//2].x,path_ki[path_ki.length//2].y)

                # for item in path_ki:
                    # room.createConstructionSite(item.x, item.y, STRUCTURE_ROAD)

def delaunay():
    pass
    # https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    # https://github.com/jmespadero/pyDelaunay2D

def distanceTo(x1,y1,x2,y2):
    dx=x1-x2
    dy=y1-y2
    return Math.sqrt(dx*dx+dy*dy)

def arr_replace(arr, arr2):
    arr.splice(0, arr.length)
    if arr2 == undefined: return
    for item in arr2:
        arr.push(item)

def meanPosition(ids):
    positions = _.map(ids, lambda id_: Game.getObjectById(id_).pos)
    sumx = 0.0
    sumy = 0.0
    count = 0
    for pos in positions:
        sumx += pos.x
        sumy += pos.y
        count += 1
    
    if count == 0:
        return 25,25
    else:
        return sumx/count,sumy/count

def clusterSites(sites, rangeThreshold = 5):
    positions = _.map(sites, lambda id_: Game.getObjectById(id_).pos)
    if positions.length == 0: return []

    def clusterPosition(cluster):
        sumx = 0.0
        sumy = 0.0
        count = 0
        for idx in cluster:
            sumx += positions[idx].x
            sumy += positions[idx].y
            count += 1
        
        if count == 0:
            return 25,25
        else:
            return sumx/count,sumy/count

    
    remaining = range(positions.length-1,-1,-1)
    # remaining = [3,2,1,0]
    # console.log(remaining)
    clusters = []
    while remaining.length > 0:
        # add cluster on one of the remaining positions
        idx = remaining.js_pop()
        cluster = [idx]
        posx,posy = clusterPosition(cluster)
        if remaining.length > 0:
            # console.log("remaining", remaining)
            remainingInRange = _.groupBy(remaining, lambda idx: positions[idx].inRangeTo(posx, posy, rangeThreshold))
            # console.log("remainingInRange[True]", remainingInRange[True])
            # console.log("remainingInRange[False]", remainingInRange[False])
            arr_replace(remaining, remainingInRange[False] or [])
            # console.log("remaining", remaining)
            arr_replace(cluster, cluster.concat(remainingInRange[True] or []))
        # console.log("cluster", cluster)
        clusters.push(cluster)
        #clusterInRange = _.groupBy(cluster, lambda idx: positions[idx].inRangeTo(posx, posy, rangeThreshold))
    # console.log("clusters", clusters)
    # console.log("clusters", JSON.stringify(clusters))

    return _.map(clusters, lambda cluster: _.map(cluster, lambda idx:sites[idx]))

def roundN(number, num_digits):
    tenPow = 10 ** num_digits
    return Math.round(number*tenPow)/tenPow

def drawStats(room):
    room.visual.text(
        "cpu: {} / {}".format(
            roundN(Game.cpu.getUsed(),2), 
            Game.cpu.tickLimit), 
        0, 0, {"align": "left"})


def main():
    # economy is organized with flags as
    # transportation nodes inspired by settlers2
    # 
    # - automatic flag placement
    # - assign sites to flags
    # - transportation network between flags
    # - creeps transport stuff between flags
    # - flags collect local jobs
    # - worker creeps are assigned to local jobs
    # 
    
    for room_name,room in _.pairs(Game.rooms):
        updateSites(room)
        drawStats(room)


module.exports.loop = main
