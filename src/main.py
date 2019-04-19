# import harvester
# import behaviours
import jobs
import roads
# import ecs
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

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

    # # Run each creep
    # for name in Object.keys(Game.creeps):
        # creep = Game.creeps[name]

        # harvester.run_harvester(creep)

    jobs.process_jobs()

    roads.update_heatmap()
    num_road_constructions = roads.num_road_constructions()
    for name in Object.keys(Game.rooms):
        room = Game.rooms[name]
        # roads.display_heatmap(room)
        jobs.path_set(room.memory, "roads.proposed", roads.propose_roads(room))

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
                    "score": jobs.path_get(tomb_stone.creep.memory,"score",0),
                    "job": jobs.path_get(tomb_stone.creep.memory,"job","")
                }

        # mori_by_job = 

    # ecs.run_systems()


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

            # If there are less than 15 creeps but at least one, wait until all spawns and extensions are full before
            # spawning.
            elif num_creeps < 20 and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable*0.8:
                # If we have more energy, spawn a bigger creep.
                # if spawn.room.energyCapacityAvailable >= 50+7*50:
                    # spawn.createCreep([WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE],{})
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
                ]
                recipe = _.sample(recipes)
                if spawn.room.energyCapacityAvailable >= 50+recipe.length*50:
                    spawn.createCreep(recipe,{})
                # spawn.createCreep([WORK, CARRY, CARRY, MOVE, MOVE, MOVE])
                # else:
                    # spawn.createCreep([WORK, CARRY, MOVE],{})


    if Memory.creeps:
        for name in Object.keys(Memory.creeps):
            if name not in Game.creeps:
                del Memory.creeps[name]

module.exports.loop = main
