# import harvester
# import behaviours
import jobs
import logistic
import roads
import repair
# import ecs
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *
from .entity import *
from .utils import *

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

MAX_ROAD_CONSTRUCTIONS_PER_ROOM = 2

def main():
    """
    Main game logic loop.
    """

    for creep in Object.js_values(Game.creeps):
        repair.repair_creep_memory(creep)

    jobs.process_jobs()
    logistic.process_logistic()




    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            # Get the number of our creeps in the room.
            num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName)
            console.log("num_creeps: {}".format(num_creeps))
            # If there are no creeps, spawn a creep once energy is at 250 or more
            if num_creeps <= 0 and spawn.room.energyAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE, MOVE])

            elif ((num_creeps < 10 and spawn.room.energyAvailable >= 500)
                    or (num_creeps < 20 and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable*0.8)):

                recipes = [
                    [WORK, CARRY, MOVE, MOVE],
                    [WORK, CARRY, CARRY, MOVE],
                    # [CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, CARRY, MOVE],
                    # [WORK, WORK, WORK, MOVE],
                    [WORK, WORK, CARRY, CARRY, MOVE],
                    # [WORK, WORK, WORK, WORK, MOVE],
                    [WORK, WORK, WORK, CARRY, MOVE],
                    [WORK, CARRY, CARRY, CARRY, MOVE],
                    # [CARRY, CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, WORK, WORK, CARRY, CARRY, MOVE],
                    [WORK, WORK, CARRY, CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE],
                    [WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE],
                ]
                recipe = _.sample(recipes)
                if spawn.room.energyCapacityAvailable >= 50+recipe.length*50:
                    spawn.createCreep(recipe,{})

    roads.update_heatmap()
    num_road_constructions = roads.num_road_constructions()
    for name in Object.keys(Game.rooms):
        room = Game.rooms[name]
        # roads.display_heatmap(room)
        path_set(room.memory, "roads.proposed", roads.propose_roads(room))

        if room.memory.roads.proposed and \
                num_road_constructions[room.name] < MAX_ROAD_CONSTRUCTIONS_PER_ROOM:

            for proposal in room.memory.roads.proposed[:MAX_ROAD_CONSTRUCTIONS_PER_ROOM]:
                if proposal:
                    room.createConstructionSite(proposal.x, proposal.y, STRUCTURE_ROAD)

        if "mori" not in Memory:
            Memory.mori = {}

        tomb_stones = _.filter(room.find(FIND_TOMBSTONES),lambda ts:ts.creep.my)
        for tomb_stone in tomb_stones:
            if tomb_stone.creep.id not in Memory.mori:
                Memory.mori[tomb_stone.creep.id] = {
                    "name": tomb_stone.creep.name,
                    "body": tomb_stone.creep.body,
                    "score": path_get(tomb_stone.creep.memory,"score",0),
                    "job": path_get(tomb_stone.creep.memory,"job","")
                }

    # report best past creeps
    # mori = _.sortBy(Object.js_values(Memory.mori), lambda mori: -mori.score)
    # for m in mori[:50]:
    #     body = dict()
    #     for part in m.body:
    #         if part.type in body:
    #             body[part.type] += 1
    #         else:
    #             body[part.type] = 1
    #     body = _.map(
    #         _.sortBy(Object.keys(body), lambda part_type: body[part_type]),
    #         lambda part_type: part_type + ":" + str(body[part_type])).join(", ")
    #     console.log("score:", m.score, "job:", m.job, "body:", body)

    # if controller level >= 4 : 
    # construct container near flags
    repair.cleanup_memory()

module.exports.loop = main
