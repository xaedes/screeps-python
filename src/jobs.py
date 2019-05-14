from defs import *
from .vm import *
from .entity import *
from .employment import employ, employment_statistics, jobs, job_say

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def process_job(entity):
    memory = memory_of_entity(entity)
    if "job" not in memory: return False
    if memory.job not in jobs: return False
    job_description = jobs[memory.job]

    init_vm(entity)

    if memory.vm.cmd.length == 0:
        # populate vm with job
        # console.log("populate vm on", id_of_entity(entity), "with job", memory.job)
        push_cmd_data(
            entity, 
            job_description.command_stack, 
            job_description.data_stack)

    if "say" in entity and memory.job in job_say:
        say = job_say[memory.job]
        # if memory.vm.cmd.length > 0:
            # say = job_say[memory.job] + " " + memory.vm.cmd[memory.vm.cmd.length-1] + say
        # else:
        if "score" in memory:
            say += " " + str(memory.score)
        entity.say(say)

    last_num_iter = path_get(Memory, "vm.last_num_iter", 0)
    last_num_iter += process_vm(entity)
    path_set(Memory, "vm.last_num_iter", last_num_iter)

    return True

def process_jobs():
    path_set(Memory, "vm.last_num_iter", 0)

    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if not process_job(creep):
            employ(creep)

    for name in Object.keys(Game.rooms):
        room = Game.rooms[name]
        if not process_job(room.controller):
            memory_of_entity(room.controller).job = "controller"

    for name in Object.keys(Game.flags):
        flag = Game.flags[name]
        if not process_job(flag):
            memory_of_entity(flag).job = "flag"

    for name in Object.keys(Game.constructionSites):
        constructionSite = Game.constructionSites[name]
        if not process_job(constructionSite):
            memory_of_entity(constructionSite).job = "constructionSite"

    for name in Object.keys(Game.structures):
        structure = Game.structures[name]
        if structure.structureType == STRUCTURE_TOWER and not process_job(structure):
            memory_of_entity(structure).job = "tower"

    Memory.employment_statistics = employment_statistics()
