from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

from .constants import *

def zero_map():
    return [[0 for i in range(ROOM_WIDTH)]
            for j in range(ROOM_HEIGHT)]


blur_kernel = [
    [0.25, 0.50, 0.25],
    [0.50, 0.75, 0.50],
    [0.25, 0.50, 0.25],
]
def blur_map(map):
    new_map = zero_map()
    for j in range(ROOM_HEIGHT):
        for i in range(ROOM_WIDTH):
            wsum = 0
            vsum = 0
            for jj in range(max(0,j-1), min(ROOM_HEIGHT,j+2)):
                for ii in range(max(0,i-1), min(ROOM_WIDTH,i+2)):
                    w=blur_kernel[jj][ii]
                    wsum += w
                    vsum += map[j+jj][i+ii]*w
            if wsum == 0:
                new_map[j][i] = vsum / wsum
            else:
                new_map[j][i] = vsum
    return new_map

def init_heatmap(room):
    if "roads" not in room.memory: room.memory.roads = {}
    if "heatmaps" not in room.memory.roads:
        room.memory.roads.heatmaps = {}
    if "walk" not in room.memory.roads.heatmaps:
        room.memory.roads.heatmaps.walk = zero_map()
    if "energy" not in room.memory.roads.heatmaps:
        room.memory.roads.heatmaps.energy = zero_map()

def update_heatmap():
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        init_heatmap(creep.room)
        if can_build_road(creep.room, creep.pos.x, creep.pos.y):
            creep.room.memory.roads.heatmaps.walk[creep.pos.y][creep.pos.x] += 1


    roads = _.filter(Game.structures, lambda structure:
        structure.structureType == STRUCTURE_ROAD)
    for road in roads:
        road.room.memory.roads.heatmaps.walk[road.pos.y][road.pos.x] = 0

    road_constructions = _.filter(Game.constructionSites, lambda constructionSite:
        constructionSite.structureType == STRUCTURE_ROAD)
    for road in road_constructions:
        road.room.memory.roads.heatmaps.walk[road.pos.y][road.pos.x] = 0


def display_heatmap(room):
    if "roads" not in room.memory: return
    if "heatmap" not in room.memory.roads: return

    # heatmap_sum = _.sum([_.sum(row) for row in room.memory.roads.heatmap])
    heatmap_max = _.max([_.max(row) for row in room.memory.roads.heatmaps.walk])
    if heatmap_max == 0: return
    for j in range(ROOM_HEIGHT):
        for i in range(ROOM_WIDTH):
            room.visual.rect(i-0.5,j-0.5,1,1,{
                "opacity": room.memory.roads.heatmaps.walk[j][i] / heatmap_max
                })

def can_build_road(room, x, y):
    not_allowed_types = ["constructionSite", "structure"]
    conflicting_objects = _.filter(room.lookAt(x, y), (lambda obj:
        (obj.type == "terrain" and obj.terrain == "wall") 
        or (not_allowed_types.includes(obj.type))
        ))
    return conflicting_objects.length == 0

def propose_roads(room):
    if "roads" not in room.memory: return
    if "heatmaps" not in room.memory.roads: return
    if "walk" not in room.memory.roads.heatmaps: return

    # heatmap_sum = _.sum([_.sum(row) for row in room.memory.roads.heatmap])
    heatmap_max = _.max([_.max(row) for row in room.memory.roads.heatmaps.walk])
    if heatmap_max == 0: return

    proposed = []

    for j in range(ROOM_HEIGHT):
        for i in range(ROOM_WIDTH):
            norm = room.memory.roads.heatmaps.walk[j][i] / heatmap_max
            if norm > 0.1 and can_build_road(room, i, j):
                proposed.push({"x": i, "y": j, "norm": norm})
    proposed = _.sortBy(proposed, lambda proposal: -proposal.norm)
    return proposed

def num_road_constructions():
    num = dict()
    for name in Object.keys(Game.rooms):
        room = Game.rooms[name]
        num[name] = _.filter(Game.constructionSites, lambda constructionSite:
            constructionSite.structureType == STRUCTURE_ROAD and constructionSite.room.name == room.name
            ).length

    return num
