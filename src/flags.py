
from utils import *
from constants import *
from defs.constants import *
import distance_transform
import voronoi
import draw

def clusterPositionsGreedy(positions, rangeThreshold):
    if positions.length == 0: return []

    remaining = range(positions.length-1,-1,-1)
    clusters = []

    def clusterPosition(cluster):
        clusterPositions = arr_iloc(positions, cluster)
        return meanPosition(clusterPositions)   


    while remaining.length > 0:
        # add cluster consisting of one of the remaining positions
        # and fill it with positions in range of mean position
        idx = remaining.js_pop()
        cluster = [idx]
        posx,posy = clusterPosition(cluster)
        if remaining.length > 0:
            remainingInRange = _.groupBy(remaining, lambda idx: positions[idx].inRangeTo(posx, posy, rangeThreshold))
            arr_replace(remaining, remainingInRange[False] or [])
            arr_replace(cluster, cluster.concat(remainingInRange[True] or []))
        clusters.push(cluster)

    return clusters

def clusterSites(sites, rangeThreshold = 5):
    positions = _.map(sites, lambda id_: Game.getObjectById(id_).pos)
    clusters = clusterPositionsGreedy(positions, rangeThreshold)
    return _.map(clusters, lambda cluster: _.map(cluster, lambda idx:sites[idx]))



def initFlags(room):
    if "flags" not in room.memory: 
        room.memory.flags = {}

    if "next_flag_id" not in room.memory: 
        room.memory.next_flag_id = 0

def nextFlagId(room):
    res = room.memory.next_flag_id
    room.memory.next_flag_id += 1
    return res

def canAssignFlag(flag, site_id):
    pos = Game.getObjectById(site_id).pos
    fx = flag.pos[0]
    fy = flag.pos[1]
    x=pos.x
    y=pos.y
    dist = distanceTo(fx,fy,x,y) 
    if dist < flag.range:
        # can only assign if no site will be 
        # out of range due to new mean position
        
        n = flag.sites.length
        mx = (fx*n+x)/(n+1)
        my = (fy*n+y)/(n+1)
        sites_not_inRange = _.filter(flag.sites, 
            lambda site_id:
                not Game.getObjectById(site_id)
                    .pos.inRangeTo(mx,my,flag.range))
        return (sites_not_inRange.length == 0)
    else:
        return False

def create_flag(room,site_idcs,flagRange):
    flag_id = nextFlagId(room)
    room.memory.flags[flag_id] = {
        "flag_id": flag_id,
        "sites": site_idcs,
        "pos": meanPositionOfIds(site_idcs),
        "range": flagRange,
        "update_distances": True,
        "distances": False,
    }
    for site_id in site_idcs:
        room.memory.sites[site_id].flag = flag_id

    return room.memory.flags[flag_id]

def processUnassignedSites(room, unassigned_site_ids, rangeThreshold = 5):
    # assign site_id to existing flag if possible
    could_not_assign = []
    for site_id in unassigned_site_ids:
        flag_ids = _.js_keys(room.memory.flags)
        if flag_ids.length == 0:
            could_not_assign.push(site_id)
        else:
            found_flag = False
            for flag_id in flag_ids:
                if canAssignFlag(room.memory.flags[flag_id], site_id):
                    # console.log("assigning site", site_id, "to flag", flag_id)
                    room.memory.sites[site_id].flag = flag_id
                    room.memory.flags[flag_id].sites.push(site_id)
                    room.memory.flags[flag_id].pos = meanPositionOfIds(room.memory.flags[flag_id].sites)
                    room.memory.flags[flag_id].update_distances = True
                    found_flag = True
                    break

            if not found_flag:
                could_not_assign.push(site_id)

    # otherwise add flags
    positions = positionsByIds(could_not_assign)
    clusters = clusterPositionsGreedy(positions, rangeThreshold)
    clusters = _.map(clusters, lambda cluster: _.map(cluster, lambda idx:could_not_assign[idx]))
    for cluster in clusters:
        create_flag(room, cluster, rangeThreshold)


def updateFlagDistances(room, flag):
    console.log("updateFlagDistances")
    room.memory.flags[flag.flag_id].distances = distance_transform.pathcost_transform(
        room.memory.terrain_costs, 
        roundXY(flag.pos)
    )

def updateFlagNeighbors(room):
    if room.memory.nearest_flags:
        neighbors = voronoi.compute_voronoi_neighbors(room.memory.nearest_flags)
        flag_ids = _.js_keys(room.memory.flags)
        room.memory.flag_neighbors = {}
        for k in Object.js_keys(neighbors):
            flag_id1 = flag_ids[k]
            room.memory.flag_neighbors[flag_id1] = {}
            for i in Object.js_keys(neighbors[k]):
                flag_id2 = flag_ids[i]
                room.memory.flag_neighbors[flag_id1][flag_id2] = flag_id2

        return room.memory.flag_neighbors
    else:
        return None

def updateFlags(room):
    initFlags(room)

    for flag_id in Object.js_keys(room.memory.flags):
        num_sites_before = room.memory.flags[flag_id].sites.length
        room.memory.flags[flag_id].sites = _.filter(
            room.memory.flags[flag_id].sites,
            lambda site_id: site_id in room.memory.sites
            )
        num_sites = room.memory.flags[flag_id].sites.length
        if num_sites < num_sites_before:
            room.memory.flags[flag_id].pos = meanPositionOfIds(room.memory.flags[flag_id].sites)
            room.memory.update_voronoi = True
        if num_sites == 0:
            del room.memory.flags[flag_id]


    # unassigned_sites = _.filter(_.js_values(room.memory.sites), lambda site: site.flag == False)
    # console.log("unassigned_sites",JSON.stringify( unassigned_sites))
    unassigned_sites = _.map(_.filter(_.js_values(room.memory.sites), lambda site: site.flag < 0),"id")
    if unassigned_sites.length > 0:
        # console.log("unassigned_sites", unassigned_sites)
        processUnassignedSites(room, unassigned_sites, 5)


    for flag_id in Object.js_keys(room.memory.flags):
        flag = room.memory.flags[flag_id]
        if flag.update_distances:
            room.memory.update_voronoi = True
            updateFlagDistances(room, flag)
            flag.update_distances = False

    if room.memory.update_voronoi:
        cost_maps = [
            flag.distances 
            for flag 
            in Object.js_values(room.memory.flags)
            if flag.distances != False
        ]
        # console.log("cost_maps.length",cost_maps.length)
        # console.log("Object.js_keys(room.memory.flags)",Object.js_keys(room.memory.flags))
        if cost_maps.length == Object.js_keys(room.memory.flags).length:
            room.memory.nearest_flags = voronoi.compute_voronoi(cost_maps)
            room.memory.update_voronoi = False
            updateFlagNeighbors(room)

    drawFlags(room)

def drawFlags(room):
    for flag_id,flag in _.pairs(room.memory.flags):
        x = flag.pos[0]
        y = flag.pos[1]
        room.visual.text("🏴",x,y)
        room.visual.circle(x,y,{"radius": flag.range, "opacity": 0.1})
        for site_id in flag.sites:
            sx=room.memory.sites[site_id].pos.x
            sy=room.memory.sites[site_id].pos.y
            room.visual.line(x,y,sx,sy)

        # if flag.distances != False:
            # draw.draw_costs(room, flag.distances, 0.1, "#ff0000")

    if room.memory.nearest_flags:
        draw.draw_colors(room, room.memory.nearest_flags, WEBCOLORS, 0.5)
    
    if room.memory.flag_neighbors:
        for flag_id1 in Object.js_keys(room.memory.flag_neighbors):
            for flag_id2 in Object.js_keys(room.memory.flag_neighbors[flag_id1]):
                x1 = room.memory.flags[flag_id1].pos[0]
                y1 = room.memory.flags[flag_id1].pos[1]
                x2 = room.memory.flags[flag_id2].pos[0]
                y2 = room.memory.flags[flag_id2].pos[1]
                room.visual.line(x1,y1,x2,y2)

