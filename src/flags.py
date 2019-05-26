
from utils import *

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
                    found_flag = True
                    break

            if not found_flag:
                could_not_assign.push(site_id)

    # otherwise add flags
    positions = positionsByIds(could_not_assign)
    clusters = clusterPositionsGreedy(positions, rangeThreshold)
    clusters = _.map(clusters, lambda cluster: _.map(cluster, lambda idx:could_not_assign[idx]))
    for cluster in clusters:
        flag_id = nextFlagId(room)
        room.memory.flags[flag_id] = {
            "flag_id": flag_id,
            "sites": cluster,
            "pos": meanPositionOfIds(cluster),
            "range": rangeThreshold
        }
        for site_id in cluster:
            room.memory.sites[site_id].flag = flag_id




def updateFlags(room):
    initFlags(room)
    # unassigned_sites = _.filter(_.js_values(room.memory.sites), lambda site: site.flag == False)
    # console.log("unassigned_sites",JSON.stringify( unassigned_sites))
    unassigned_sites = _.map(_.filter(_.js_values(room.memory.sites), lambda site: site.flag < 0),"id")
    if unassigned_sites.length > 0:
        # console.log("unassigned_sites", unassigned_sites)
        processUnassignedSites(room, unassigned_sites, 5)

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
