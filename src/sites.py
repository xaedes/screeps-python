
from utils import *

def findSites(room):
    # sites include spawn, controller, sources, energy consuming structures
    spawns = idsOf(room.find(FIND_MY_SPAWNS))
    controller = idsOf([room.controller])
    sources = idsOf(room.find(FIND_SOURCES))
    construction_sites = idsOf(room.find(FIND_MY_CONSTRUCTION_SITES))
    extensions = idsOf(room.find(FIND_MY_STRUCTURES, { "filter": { "structureType" : STRUCTURE_EXTENSION } }))
    towers = idsOf(room.find(FIND_MY_STRUCTURES, { "filter": { "structureType" : STRUCTURE_TOWER } }))
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

def initSite(site_id):
    return {
        "id": site_id,
        "pos": Game.getObjectById(site_id).pos,
        "flag" : -1
    }

def resetSites(room):
    room.memory.sites = {}

def initSites(room):
    sites = findSites(room)
    if "sites" not in room.memory: 
        room.memory.sites = {}
    for site_id in sites:
        if site_id not in room.memory.sites:
            room.memory.sites[site_id] = initSite(site_id)

def updateSites(room):
    # resetSites(room)
    initSites(room)

    for k,(site_id,site_mem) in enumerate(_.pairs(room.memory.sites)):
        # console.log(k,site_id)
        # console.log(site_mem)
        site = Game.getObjectById(site_id)
        room.visual.text("site {}".format(k), site.pos)

    # if True or "clusters" not in room.memory:
    #     rangeThreshold = 10
    #     clusters = clusterSites(room.memory.sites, rangeThreshold)
    #     room.memory.clusters = []
    #     for k,cluster in enumerate(clusters):
    #         cluster_name = room.name + "_" + String(k)
    #         room.memory.clusters.push({
    #             "id": cluster_name,
    #             "ids": cluster,
    #             "pos": findWalkablePosition(room, meanPositionOfIds(cluster), rangeThreshold),
    #             "range": rangeThreshold,
    #             "paths": {}
    #             })

    #     # console.log("clusters", JSON.stringify(clusters))


    # for k in range(room.memory.clusters.length or 0):
    #     cluster_k = room.memory.clusters[k]
    #     x,y = cluster_k.pos
    #     r = cluster_k.range
    #     room.visual.text("🏴",x,y)
    #     room.visual.circle(x,y,{"radius": r, "opacity": 0.1})
    #     for i in range(k+1,room.memory.clusters.length or 0):
    #         cluster_i = room.memory.clusters[i]
    #         x2,y2 = cluster_i.pos
    #         room.visual.line(x,y,x2,y2,{"color":"#112AA7"})

    #         # see if we computed one side of the path already
    #         path_ki = cluster_k.paths[cluster_i.id] or findPath(
    #             room.getPositionAt(x,y),
    #             room.getPositionAt(x2,y2)
    #         )

    #         if  not cluster_k.paths[cluster_i.id] and path_ki:
    #             cluster_k.paths[cluster_i.id] = path_ki
    #         if not cluster_i.paths[cluster_k.id] and path_ki:
    #             cluster_i.paths[cluster_k.id] = path_ki.reverse()
            
    #         if path_ki:
    #             drawPath(path_ki)
    #         # PathFinder.
    #             room.visual.text(String(path_ki.length),(x+x2)/2,(y+y2)/2)
    #             room.visual.text(String(path_ki.length),path_ki[path_ki.length//2].x,path_ki[path_ki.length//2].y)

    #             # for item in path_ki:
    #                 # room.createConstructionSite(item.x, item.y, STRUCTURE_ROAD)
