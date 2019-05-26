

from utils import *
import flags
import sites

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


def handleReset():
    for room in _.js_values(Game.rooms):
        room.memory["reset"] = False

    for spawn in _.js_values(Game.spawns):
        mem = spawn.room.memory
        if "spawn_id" not in mem or mem.spawn_id != spawn.id:
            spawn.room.memory = {
                "spawn_id" : spawn.id,
                "reset" : True
            }

def drawStats(room):
    room.visual.text(
        "cpu: {} / {}".format(
            roundN(Game.cpu.getUsed(),2), 
            Game.cpu.tickLimit), 
        0, 0, {"align": "left"})


def main():
    handleReset()
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
        sites.updateSites(room)
        flags.updateFlags(room)
        drawStats(room)


module.exports.loop = main
