from defs import *
from .utils import *
from .entity import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def register_commands(commands):
    commands["tower"] = {
        "required_body_parts": [],
        "loop": cmd_tower
    };



def cmd_tower(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    # mem = entity.room.memory
    if mem and entity.structureType != STRUCTURE_TOWER:
        command_stack.js_pop()
        return True

    # create job posting for this
    path_set(mem, "logistic.request.energy", 0)
    if entity.energy / entity.energyCapacity < 0.25:
        mem.logistic.request.energy = 1
    elif entity.energy / entity.energyCapacity < 0.50:
        mem.logistic.request.energy = 1
    elif entity.energy / entity.energyCapacity < 0.75:
        mem.logistic.request.energy = 0
    else:
        mem.logistic.request.energy = 0

    enemies = _.sortBy(entity.room.find(FIND_HOSTILE_CREEPS), lambda enemy: enemy.hits)
    if enemies.length > 0:
        enemy = enemies[0]
        entity.attack(enemy)

    else:
        repairables = entity.room.find(FIND_STRUCTURES).filter(lambda s: s.hits < s.hitsMax)
        non_infrastructure = _.filter(repairable, lambda s:(s.structureType != STRUCTURE_ROAD) and (s.structureType != STRUCTURE_WALL))
        containers = _.filter(repairables, lambda s:s.structureType == STRUCTURE_CONTAINER)
        ramparts = _.filter(repairables, lambda s:s.structureType == STRUCTURE_RAMPART)

        if containers.length > 0:
            repairable = _.sortBy(containers, lambda s:s.hits / s.hitsMax)[0]
            #repairable = _.sample(repairables)
            entity.repair(repairable)
        elif ramparts.length > 0:
            repairable = _.sortBy(ramparts, lambda s:s.hits / s.hitsMax)[0]
            #repairable = _.sample(repairables)
            entity.repair(repairable)
        elif non_infrastructure.length > 0:
            repairable = _.sortBy(non_infrastructure, lambda s:s.hits / s.hitsMax)[0]
            # repairable = _.sample(repairables)
            entity.repair(repairable)
        # elif repairables.length > 0:
        #     # repairable = _.sortBy(repairables, lambda s:s.hits / s.hitsMax)[0]
        #     repairable = _.sample(repairables)
        #     entity.repair(repairable)

    # create job posting for this
    mem = memory_of_entity(entity)
    flag_name = path_get(mem, "logistic.flag", None)
    if flag_name:
        job_posting = {
            "name": "upgrader",
            "stacks": [
                ["stationaryQuesterJob"],
                [entity.id, flag_name]]
        }
        job_postings = [job_posting]
        path_set(mem, "logistic.job_postings", job_postings)

    return False


