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
    commands["findEnergySource"] = {
        "required_body_parts": [],
        "loop": cmd_findEnergySource
    };
    commands["findEnergySourceWithFreeSlot"] = {
        "required_body_parts": [],
        "loop": cmd_findEnergySourceWithFreeSlot
    };
    commands["findEnergyDeposit"] = {
        "required_body_parts": [],
        "loop": cmd_findEnergyDeposit
    };
    commands["findDroppedEnergy"] = {
        "required_body_parts": [],
        "loop": cmd_findDroppedEnergy
    };
    commands["findController"] = {
        "required_body_parts": [],
        "loop": cmd_findController
    };
    commands["findConstructionSite"] = {
        "required_body_parts": [],
        "loop": cmd_findConstructionSite
    };
    commands["findRepairable"] = {
        "required_body_parts": [],
        "loop": cmd_findRepairable
    };
    commands["findTransportSourcePos"] = {
        "required_body_parts": [],
        "loop": cmd_findTransportSourcePos
    };
    commands["findTransportTargetPos"] = {
        "required_body_parts": [],
        "loop": cmd_findTransportTargetPos
    };
    commands["findEnergyRequester"] = {
        "required_body_parts": [],
        "loop": cmd_findEnergyRequester
    };


def energySourceSlots(entity):
    terrain = entity.room.getTerrain()
    slots = []
    for x in range(entity.pos.x-1,entity.pos.x+2):
        for y in range(entity.pos.y-1,entity.pos.y+2):
            tile = terrain.get(x,y)
            if tile != TERRAIN_MASK_WALL:
                slots.push(entity.room.getPositionAt(x,y))
    return slots

def energySourcesSlots(entities):
    slots = []
    for entity in entities:
        slots_ = energySourceSlots(entity)
        for slot in slots_:
            slots.push(slot)
    return slots

def filterFindInRange(entity, objects):
    mem = memory_of_entity(entity)
    if "range" in mem and "find" in mem.range:
        find_range = mem.range.find
        return _.filter(objects,
            lambda obj: entity.pos.inRangeTo(obj, find_range))
    else:
        return objects

def cmd_findEnergySourceWithFreeSlot(entity, command_stack, data_stack):
    # Get a random new source and save it
    sources = filterFindInRange(entity, entity.room.find(FIND_SOURCES).filter(lambda s: s.energy>0))
    if sources.length == 0:
        return False
    else:
        # source = entity.pos.findClosestByPath(sources)

        free_slots = _.filter(energySourcesSlots(sources),
            lambda pos: (pos.x == entity.pos.x and pos.y == entity.pos.y) 
                       or _.filter(entity.room.lookAt(pos), lambda obj: obj.type == "creep").length == 0)
        if free_slots.length == 0:
            return False
        else:
            free_slot = entity.pos.findClosestByRange(free_slots)
            source = free_slot.findClosestByRange(sources)
            # source = _.sample(sources)
            data_stack.push(source.id)
            command_stack.js_pop()
            return True

def cmd_findEnergySource(entity, command_stack, data_stack):
    # Get a random new source and save it
    sources = filterFindInRange(entity, entity.room.find(FIND_SOURCES).filter(lambda s: s.energy>0))
    if sources.length == 0:
        return False
    else:
        # source = entity.pos.findClosestByPath(sources)
        
        source = entity.pos.findClosestByRange(sources)
        # source = _.sample(sources)
        data_stack.push(source.id)
        command_stack.js_pop()
        return True

def cmd_findDroppedEnergy(entity, command_stack, data_stack):
    # Get a random new source and save it
    sources = filterFindInRange(entity, entity.room.find(FIND_DROPPED_RESOURCES).filter(lambda s: s.resourceType==RESOURCE_ENERGY))
    if sources.length == 0:
        return False
    else:
        # source = entity.pos.findClosestByPath(sources)
        source = entity.pos.findClosestByRange(sources)
        # source = _.sample(sources)
        data_stack.push(source.id)
        command_stack.js_pop()
        return True

def cmd_findRepairable(entity, command_stack, data_stack):
    repairables = filterFindInRange(entity, entity.room.find(FIND_STRUCTURES).filter(lambda s: s.hits < s.hitsMax))
    if repairables.length == 0:
        return False
    else:
        # source = entity.pos.findClosestByPath(repairables)
        repairable = entity.pos.findClosestByRange(repairables)
        # repairable = _.sample(repairables)
        data_stack.push(repairable.id)
        command_stack.js_pop()
        return True

def cmd_findEnergyDeposit(entity, command_stack, data_stack):
    # Get a random new source and save it
    test_1 = lambda s: ( ((s.structureType == STRUCTURE_SPAWN) or (s.structureType == STRUCTURE_EXTENSION))
                        and (s.energy < s.energyCapacity)
                        and (s.my))
    test_2 = lambda s: ( (s.structureType == STRUCTURE_CONTAINER)
                        and (_.sum(s.store) < s.storeCapacity))
    deposit_targets = filterFindInRange(entity, _.filter(entity.room.find(FIND_STRUCTURES),
        test_1
        # lambda s: (test_1(s) or test_2(s))
        ))
    if deposit_targets.length == 0:
        return False
    else:
        deposit_target = entity.pos.findClosestByRange(deposit_targets)
        # deposit_target = _.sample(deposit_targets)
        data_stack.push(deposit_target.id)
        command_stack.js_pop()
        return True

def cmd_findController(entity, command_stack, data_stack):
    # Get a random new source and save it
    controllers = filterFindInRange(entity, _.filter(entity.room.find(FIND_STRUCTURES),
                           lambda s: s.structureType == STRUCTURE_CONTROLLER))
    if controllers.length == 0:
        return False
    else:
        controller = _.sample(controllers)
        data_stack.push(controller.id)
        command_stack.js_pop()
        return True

def cmd_findConstructionSite(entity, command_stack, data_stack):
    # Get a random new source and save it
    construction_sites = filterFindInRange(entity, _.filter(entity.room.find(FIND_CONSTRUCTION_SITES),
                                  lambda s: s.progress < s.progressTotal))
    if construction_sites.length == 0:
        return False
    else:
        construction_site = entity.pos.findClosestByRange(construction_sites)
        # construction_site = _.sample(construction_sites)
        data_stack.push(construction_site.id)
        command_stack.js_pop()
        return True



def cmd_findTransportSourcePos(entity, command_stack, data_stack):
    positions = []
    for name in Object.keys(Game.flags):
        flag = Game.flags[name]
        flag_mem = memory_of_entity(flag)
        flag_storage=path_get(flag_mem,"logistic.storage.energy",0)
        flag_harvest=path_get(flag_mem,"logistic.harvest.energy",0)
        if flag_harvest > 0 and flag_storage > 0:
            positions.push(flag.pos)

    positions = filterFindInRange(entity, positions)
    if positions.length == 0:
        return False
    else:
        position = entity.pos.findClosestByRange(positions)
        pos = {
                    "x":position.x,
                    "y":position.y,
                    "roomName":position.roomName
                    }
        # position = _.sample(positions)
        data_stack.push(pos)
        command_stack.js_pop()
        return True

def cmd_findTransportTargetPos(entity, command_stack, data_stack):
    positions = []
    for name in Object.keys(Game.flags):
        flag = Game.flags[name]
        flag_mem = memory_of_entity(flag)
        flag_harvest=path_get(flag_mem,"logistic.harvest.energy",0)
        flag_request=path_get(flag_mem,"logistic.request.energy",0)
        if flag_request > 0 and flag_harvest <= 0:
            positions.push(flag.pos)

    positions = filterFindInRange(entity, positions)

    if positions.length == 0:
        return False
    else:
        position = entity.pos.findClosestByRange(positions)
        pos = {
                    "x":position.x,
                    "y":position.y,
                    "roomName":position.roomName
                    }
        # position = _.sample(positions)
        data_stack.push(pos)
        command_stack.js_pop()
        return True


def cmd_findEnergyRequester(entity, command_stack, data_stack):
    energyRequesters = []
    mem = memory_of_entity(entity)
    entity_flag = path_get(mem, "logistic.flag", None)
    for flag_name in Object.keys(Game.flags):
        flag = Game.flags[flag_name]
        flag_mem = memory_of_entity(flag)
        if "logistic" in flag_mem:
            is_entity_flag = entity_flag == flag_name
            flag_quest = path_get(flag_mem, "logistic.quest.energy", None)
            flag_request = path_get(flag_mem, "logistic.request.energy", None)
            if flag_quest and flag_request:
                if flag_quest-(1 if is_entity_flag else 0) > flag_request:
                    continue

            if "non_flags" in flag_mem.logistic:
                non_flags = _.map(flag_mem.logistic.non_flags, lambda id_: Game.getObjectById(id_))
                # other_flag_creeps = _.filter(non_flags, lambda obj: obj.id != entity.id and "name" in obj and obj.name in Game.creeps)
                # num_other_flag_creeps = other_flag_creeps.length

                for non_flag in non_flags:
                    if not non_flag: continue
                    non_flag_mem = memory_of_entity(non_flag)
                    non_flag_mem_request_energy = path_get(non_flag_mem, "logistic.request.energy", 0)
                    if non_flag_mem_request_energy > 0:
                        energyRequesters.push(non_flag)

    energyRequesters = filterFindInRange(entity, energyRequesters)

    # console.log("cmd_findEnergyRequester ", energyRequesters)   
    if energyRequesters.length == 0:
        return False
    else:
        energyRequester = entity.pos.findClosestByRange(energyRequesters)
        # position = _.sample(energyRequesters)
        data_stack.push(energyRequester.id)
        command_stack.js_pop()
        return True
