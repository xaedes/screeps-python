from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def repair_creep_memory(entity):
    mem = entity.memory
    if "score" in mem:
        if mem.score == None:
            mem.score = 0
            
    if "vm" in mem:
        if "dta" in mem.vm:
            if mem.vm.dta.length > 500:
                mem.vm.cmd = []
                mem.vm.dta = []
        if "cmd" in mem.vm:
            if mem.vm.cmd.length > 500:
                mem.vm.cmd = []
                mem.vm.dta = []

def cleanup_memory():

    if Memory.creeps:
        for name in Object.keys(Memory.creeps):
            if name not in Game.creeps:
                del Memory.creeps[name]

    if Memory.entities and Object.keys(Memory.entities).length > 10:
        for id_ in Object.keys(Memory.entities):
            obj = Game.getObjectById(id_)
            if not obj:
                del Memory.entities[id_]

