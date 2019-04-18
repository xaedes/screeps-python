from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

# def task_collect_energy(creep):
#     sum_carry = _.sum(creep.carry)
#     if sum_carry < creep.carryCapacity:
#         # If we dont have a saved source, find one
#         if not creep.memory.task.state.source:
#             # Get a random new source and save it
#             sources = creep.room.find(FIND_SOURCES).filter(lambda s: s.energy>0)
#             source = _.sample(sources)
#             if sources.length == 0:
#                 return False
#             creep.memory.task.state.source = source.id

#         source = Game.getObjectById(creep.memory.task.state.source)
#         if not source: return False
#         creep.room.visual.line(creep.pos, source.pos, {'color': 'red', 'style': 'dashed'})

#         # If we're near the source, harvest it - otherwise, move to it.
#         if creep.pos.isNearTo(source):
#             result = creep.harvest(source)
#             if result != OK:
#                 console.log("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
#         else:
#             creep.moveTo(source)
#         return False
#     else:
#         # creep.memory.task.results.push({"name":"carry_energy"})
#         return True

# def task_deposit_energy(creep):
#     sum_carry = _.sum(creep.carry)
#     if sum_carry > 0:
#         # If we dont have a saved target, find one
#         if not creep.memory.task.state.target:
#             deposit_targets = _.filter(creep.room.find(FIND_STRUCTURES),
#                 lambda s: (s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION)
#                            and s.energy < s.energyCapacity)
#             if deposit_targets.length ==  0:
#                 return False
#             target = _.sample(deposit_targets)
#             creep.memory.task.state.target = target.id

#         target = Game.getObjectById(creep.memory.task.state.target)

#         if not target: return False

#         creep.room.visual.line(creep.pos, target.pos)

#         is_close = creep.pos.isNearTo(target)
#         if is_close:
#             if target.energyCapacity:
#                 result = creep.transfer(target, RESOURCE_ENERGY)
#                 if result == OK or result == ERR_FULL:
#                     del creep.memory.task.state.target
#                 else:
#                     console.log("[{}] Unknown result from creep.transfer({}, {}): {}".format(
#                         creep.name, target, RESOURCE_ENERGY, result))
#         else:
#             creep.moveTo(target)
#         return False
#     else:
#         # creep.memory.task.results.push({"name":"carry_energy"})
#         return True

# def task_upgrade_controller(creep):
#     sum_carry = _.sum(creep.carry)
#     if sum_carry > 0:
#         # If we dont have a saved target, find one
#         if not creep.memory.task.state.target:
#             controllers = _.filter(creep.room.find(FIND_STRUCTURES),
#                                    lambda s: s.structureType == STRUCTURE_CONTROLLER)
#             if controllers.length ==  0:
#                 return False
#             target = _.sample(controllers)
#             creep.memory.task.state.target = target.id
        
#         target = Game.getObjectById(creep.memory.task.state.target)

#         if not target: return False

#         creep.room.visual.line(creep.pos, target.pos)

#         # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
#         is_close = creep.pos.inRangeTo(target, 3)
#         if is_close:
#             if target.structureType == STRUCTURE_CONTROLLER:
#                 result = creep.upgradeController(target)
#                 if result != OK:
#                     console.log("[{}] Unknown result from creep.upgradeController({}): {}".format(
#                         creep.name, target, result))
#                 # Let the creeps get a little bit closer than required to the controller, to make room for other creeps.
#                 if not creep.pos.inRangeTo(target, 2):
#                     creep.moveTo(target)
#         else:
#             creep.moveTo(target)

#         return False
#     else:
#         return True

# def task_build(creep):
#     sum_carry = _.sum(creep.carry)
#     # console.log("task_build")
#     # console.log("sum_carry", sum_carry)
#     if sum_carry > 0:
#         # creep.memory.tasks.
#         # If we dont have a saved target, find one
#         if not creep.memory.task.state.target:
#             construction_sites = _.filter(creep.room.find(FIND_CONSTRUCTION_SITES),
#                                           lambda s: s.progress < s.progressTotal)
#             if construction_sites.length ==  0:
#                 return False
#             target = _.sample(construction_sites)
#             creep.memory.task.state.target = target.id

#         target = Game.getObjectById(creep.memory.task.state.target)

#         # Target invalid or complete, find a new one
#         if not target or "progressTotal" not in target or target.progress >= target.progressTotal:
#             construction_sites = _.filter(creep.room.find(FIND_CONSTRUCTION_SITES),
#                                           lambda s: s.progress < s.progressTotal)
#             if construction_sites.length ==  0:
#                 return False
#             while not target or "progressTotal" not in target or target.progress >= target.progressTotal:
#                 target = _.sample(construction_sites)
#                 creep.memory.task.state.target = target.id

#         target = Game.getObjectById(creep.memory.task.state.target)
        # console.log("target", target)
        # console.log("creep.memory.task.state.target", creep.memory.task.state.target)

#         if not target: return False

#         creep.room.visual.line(creep.pos, target.pos)

#         is_close = creep.pos.inRangeTo(target, 3)
#         if is_close:
#             if target.progressTotal:
#                 result = creep.build(target)
#                 if result != OK:
#                     console.log("[{}] Unknown result from creep.build({}): {}".format(
#                         creep.name, target, result))
#                 # Let the creeps get a little bit closer than required, to make room for other creeps.
#                 if not creep.pos.inRangeTo(target, 2):
#                     creep.moveTo(target)
#         else:
#             creep.moveTo(target)
#         return False
#     else:
#         return True

def move_creep_close(entity, target, distance_threshold):
    # console.log("target.pos", target.pos)
    # console.log("entity.pos", entity.pos)
    # console.log("range", entity.pos.getRangeTo(target))
    # console.log("distance_threshold", distance_threshold)
    is_close = entity.pos.inRangeTo(target, distance_threshold)
    if is_close:
        return True
    else:
        # pathFinding = Game.cpu.getUsed() / Game.cpu.tickLimit < 0.5
        # pathFinding = False
        pathFinding = Math.random() < 0.1
        if pathFinding:
            entity.moveTo(target)
            # console.log("moveTo")
        else:
            result = entity.moveTo(target, {"opts": {"noPathFinding": True}})
            # console.log("moveTo cached")
            if result == ERR_NO_PATH:
                entity.moveTo(target)
                # console.log("moveTo")

        is_close = entity.pos.inRangeTo(target, distance_threshold)
        return is_close


def cmd_moveTo(entity, command_stack, data_stack):
    target_id, threshold = data_stack[data_stack.length-2:]

    target = Game.getObjectById(target_id)

    mem = memory_of_entity(entity)
    if mem and "range" in mem and "walk" in mem.range:
        if not entity.pos.inRangeTo(target, mem.range.walk):
            data_stack.js_pop()
            data_stack.js_pop()
            command_stack.js_pop()
            return True

    if target and "pos" in target:
        entity.room.visual.line(entity.pos, target.pos)

    if not target or move_creep_close(entity, target, threshold):
        data_stack.js_pop()
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        return False

def cmd_moveToPos(entity, command_stack, data_stack):
    target_pos, threshold = data_stack[data_stack.length-2:]

    if Game.getObjectById(target_pos) or not (("roomName" in target_pos) and ("x" in target_pos) and ("y" in target_pos)):
        data_stack.js_pop()
        data_stack.js_pop()
        command_stack.js_pop()
        return True

    target_pos = Game.rooms[target_pos.roomName].getPositionAt(target_pos.x, target_pos.y)

    mem = memory_of_entity(entity)
    if mem and "range" in mem and "walk" in mem.range:
        if not entity.pos.inRangeTo(target_pos, mem.range.walk):
            data_stack.js_pop()
            data_stack.js_pop()
            command_stack.js_pop()
            return True

    if target_pos:
        entity.room.visual.line(entity.pos,  target_pos)

    if not target_pos or move_creep_close(entity, target_pos, threshold):
        data_stack.js_pop()
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        return False


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
    deposit_targets = filterFindInRange(entity, _.filter(entity.room.find(FIND_STRUCTURES),
        lambda s: (s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION)
                   and s.energy < s.energyCapacity))
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
        if "logistic" in flag_mem:
            if "storage" in flag_mem.logistic \
                    and "energy" in flag_mem.logistic.storage \
                    and flag_mem.logistic.storage.energy > 0 \
                    and ("request" not in flag_mem.logistic \
                         or ("energy" not in flag_mem.logistic.request \
                             or flag_mem.logistic.request.energy <= 0)):

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
        if "logistic" in flag_mem:
            if "request" in flag_mem.logistic \
                    and "energy" in flag_mem.logistic.request \
                    and flag_mem.logistic.request.energy > 0 \
                    and ("storage" not in flag_mem.logistic \
                         or ("energy" not in flag_mem.logistic.storage \
                             or flag_mem.logistic.storage.energy <= 0)):

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
    for name in Object.keys(Game.flags):
        flag = Game.flags[name]
        flag_mem = memory_of_entity(flag)
        if "logistic" in flag_mem:
            if "non_flags" in flag_mem.logistic:
                non_flags = _.map(flag_mem.logistic.non_flags, lambda id_: Game.getObjectById(id_))
                other_flag_creeps = _.filter(non_flags, lambda obj: obj.id != entity.id and "name" in obj and obj.name in Game.creeps)
                num_other_flag_creeps = other_flag_creeps.length

                for non_flag in non_flags:
                    non_flag_mem = memory_of_entity(non_flag)
                    if "logistic" in non_flag_mem \
                            and "request" in non_flag_mem.logistic \
                            and "energy" in non_flag_mem.logistic.request \
                            and non_flag_mem.logistic.request.energy > num_other_flag_creeps:

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



def cmd_harvestEnergy(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry)
    if sum_carry == entity.carryCapacity:
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        target_id = data_stack[data_stack.length-1]
        target = Game.getObjectById(target_id)

        result = entity.harvest(target)
        if result == ERR_NOT_IN_RANGE:
            command_stack.push("moveTo")
            command_stack.push("pushData_1")
            command_stack.push("duplicateData")
            return True

        elif result != OK:
            console.log("[{}] Unknown result from entity.harvest({}): {}".format(entity.name, target, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

        # command_stack.push("scoreNUp")
        # data_stack.push(_.sum(entity.carry) - sum_carry)
        # data_stack.push(1)
        return False

def cmd_pickup(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry)
    if sum_carry == entity.carryCapacity:
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        target_id = data_stack[data_stack.length-1]
        target = Game.getObjectById(target_id)

        result = entity.pickup(target)
        if result == ERR_NOT_IN_RANGE:
            command_stack.push("moveTo")
            command_stack.push("pushData_1")
            command_stack.push("duplicateData")
            return True

        elif result != OK:
            console.log("[{}] Unknown result from entity.pickup({}): {}".format(entity.name, target, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

        # command_stack.push("scoreNUp")
        # data_stack.push(_.sum(entity.carry) - sum_carry)
        # data_stack.push(1)
        return False

def cmd_dropEnergy(entity, command_stack, data_stack):
    command_stack.js_pop()
    sum_carry = _.sum(entity.carry)
    result = entity.drop(RESOURCE_ENERGY)
    if result != OK:
        console.log("[{}] Unknown result from entity.drop(RESOURCE_ENERGY): {}".format(entity.name, result))
    else:
        command_stack.push("scoreNUp")
        data_stack.push(sum_carry)

    return True

def cmd_withdraw(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry)
    if sum_carry == entity.carryCapacity:
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        target_id = data_stack[data_stack.length-1]
        target = Game.getObjectById(target_id)

        result = entity.withdraw(target)
        if result == ERR_NOT_IN_RANGE:
            command_stack.push("moveTo")
            command_stack.push("pushData_1")
            command_stack.push("duplicateData")
            return True

        elif result != OK:
            console.log("[{}] Unknown result from entity.withdraw({}): {}".format(entity.name, target, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

        command_stack.push("scoreNUp")
        # data_stack.push(_.sum(entity.carry) - sum_carry)
        data_stack.push(1)
        return False

def cmd_repair(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry)
    if sum_carry == entity.carryCapacity:
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        target_id = data_stack[data_stack.length-1]
        target = Game.getObjectById(target_id)

        if not target or target.hits == target.hitsMax:
            data_stack.js_pop()
            command_stack.js_pop()
            # command_stack.push("findRepairable")
            return True

        result = entity.repair(target)
        if result == ERR_NOT_IN_RANGE:
            command_stack.push("moveTo")
            command_stack.push("pushData_1")
            command_stack.push("duplicateData")
            return True

        elif result != OK:
            console.log("[{}] Unknown result from entity.repair({}): {}".format(entity.name, target, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

        command_stack.push("scoreNUp")
        # data_stack.push(_.sum(entity.carry) - sum_carry)
        data_stack.push(1)
        return False


def cmd_transferEnergy(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry)
    if sum_carry == 0:
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        target_id = data_stack[data_stack.length-1]
        target = Game.getObjectById(target_id)

        result = entity.transfer(target, RESOURCE_ENERGY)
        if result == OK:
            command_stack.push("scoreNUp")
            data_stack.push(sum_carry)
            return False
        elif result == ERR_NOT_IN_RANGE:
            command_stack.push("moveTo")
            command_stack.push("pushData_1")
            command_stack.push("duplicateData")

            return True
        elif result == ERR_FULL or result == ERR_NOT_ENOUGH_RESOURCES:
            data_stack.js_pop()
            command_stack.js_pop()
            return True
        else:
            console.log("[{}] Unknown result from entity.transfer({}, {}): {}".format(
                entity.name, target, RESOURCE_ENERGY, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

def cmd_upgradeController(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry)
    if sum_carry == 0:
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        target_id = data_stack[data_stack.length-1]
        target = Game.getObjectById(target_id)

        result = entity.upgradeController(target)
        if result == OK:
            # Let the entitys get a little bit closer than required to the controller, to make room for other entities.
            if not entity.pos.inRangeTo(target, 1):
                entity.moveTo(target)
            command_stack.push("scoreNUp")
            # data_stack.push(_.sum(entity.carry) - sum_carry)
            data_stack.push(1)
            return False
        else:
            console.log("[{}] Unknown result from entity.upgradeController({}): {}".format(
                entity.name, target, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

def cmd_buildStructure(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry)
    if sum_carry == 0:
        data_stack.js_pop()
        command_stack.js_pop()
        return True
    else:
        target_id = data_stack[data_stack.length-1]
        target = Game.getObjectById(target_id)

        result = entity.build(target)
        if result == OK:
            # Let the entitys get a little bit closer than required, to make room for other entitys.
            if not entity.pos.inRangeTo(target, 1):
                entity.moveTo(target)
            command_stack.push("scoreNUp")
            # data_stack.push(_.sum(entity.carry) - sum_carry)
            data_stack.push(1)
            return False
        else:
            console.log("[{}] Unknown result from entity.build({}): {}".format(
                entity.name, target, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

def cmd_isCarryEmpty(entity, command_stack, data_stack):
    command_stack.js_pop()
    sum_carry = _.sum(entity.carry)
    data_stack.push(sum_carry == 0)
    return True

def cmd_isCarryFull(entity, command_stack, data_stack):
    command_stack.js_pop()
    sum_carry = _.sum(entity.carry)
    data_stack.push(sum_carry == entity.carryCapacity)
    return True

def cmd_carriedEnergy(entity, command_stack, data_stack):
    command_stack.js_pop()
    sum_carry = _.sum(entity.carry) # TODO filter for energy
    data_stack.push(sum_carry)
    return True

def cmd_stationaryHarvesterJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    command_stack.push("dropEnergy")
    command_stack.push("scoreNUp")
    command_stack.push("carriedEnergy")

    command_stack.push("harvestEnergy")
    command_stack.push("moveTo")
    command_stack.push("pushData_1")
    command_stack.push("duplicateData")
    command_stack.push("findEnergySourceWithFreeSlot")

    command_stack.push("storeMemory")
    data_stack.push(1)
    data_stack.push("logistic.harvest.energy")

    return True

def cmd_energyPickupJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    sum_carry = _.sum(entity.carry) # TODO filter for energy
    if sum_carry < entity.carryCapacity:
        command_stack.push("scoreNUp")
        data_stack.push(entity.carryCapacity-sum_carry)
        command_stack.push("pickup")
        command_stack.push("moveTo")
        command_stack.push("pushData_1")
        command_stack.push("duplicateData")
        command_stack.push("findDroppedEnergy")

    return True

def cmd_harvestEnergyJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    sum_carry = _.sum(entity.carry) # TODO filter for energy
    if sum_carry < entity.carryCapacity:
        command_stack.push("scoreNUp")
        data_stack.push(entity.carryCapacity-sum_carry)
        command_stack.push("harvestEnergy")
        command_stack.push("moveTo")
        command_stack.push("pushData_1")
        command_stack.push("duplicateData")
        command_stack.push("findEnergySourceWithFreeSlot")

    return True

def cmd_depositEnergyJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    sum_carry = _.sum(entity.carry) # TODO filter for energy
    if sum_carry > 0:
        command_stack.push("depositEnergyJob")
        command_stack.push("transferEnergy")
        command_stack.push("moveTo")
        command_stack.push("pushData_1")
        command_stack.push("duplicateData")
        command_stack.push("findEnergyDeposit")

    return True

def cmd_collectEnergyJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    command_stack.push("depositEnergyJob")
    command_stack.push("harvestEnergyJob")

    return True

def cmd_energyPickupDepositJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    command_stack.push("depositEnergyJob")
    command_stack.push("energyPickupJob")

    return True

def cmd_upgradeControllerJob(entity, command_stack, data_stack):
    command_stack.js_pop()
    command_stack.push("upgradeController")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findController")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_5")

    command_stack.push("energyPickupJob")
    return True

def cmd_repairerJob(entity, command_stack, data_stack):
    command_stack.js_pop()
    command_stack.push("repair")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findRepairable")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_5")

    command_stack.push("energyPickupJob")
    return True

def cmd_buildStructureJob(entity, command_stack, data_stack):
    command_stack.js_pop()
    command_stack.push("buildStructure")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findConstructionSite")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_5")

    command_stack.push("energyPickupJob")
    return True

def cmd_employ(entity, command_stack, data_stack):
    employ(entity)
    command_stack.js_pop()
    return True

def cmd_duplicateData(entity, command_stack, data_stack):
    command_stack.js_pop()
    data_stack.push(data_stack[data_stack.length-1])
    return True

def cmd_repeatCommand(entity, command_stack, data_stack):
    command_stack.push(command_stack[command_stack.length-2])
    return True

def cmd_pushData(entity, command_stack, data_stack, data):
    command_stack.js_pop()
    data_stack.push(data)
    return True

def cmd_dropn_if(entity, command_stack, data_stack):
    n, pred = data_stack[data_stack.length-2:]
    command_stack.js_pop()
    data_stack.js_pop()
    data_stack.js_pop()
    if pred:
        for k in range(n):
            command_stack.js_pop()
    return True

def cmd_drop_if(entity, command_stack, data_stack):
    pred = data_stack[data_stack.length-1]
    data_stack.js_pop()
    command_stack.js_pop()
    if pred:
        command_stack.js_pop()
    return True

def path_arr(path):
    if type(path) == str:
        return path.split(".")
    else:
        return path

def path_get(obj, path, default):
    path_arr_ = path_arr(path)
    current_obj = obj
    for item in path_arr_:
        if item in obj:
            current_obj = current_obj[item]
        else:
            return default
    return current_obj
            
def path_set(obj, path, value):
    path_arr_ = path_arr(path)
    current_obj = obj
    for item in path_arr_[:path_arr_.length-1]:
        if item not in obj:
            current_obj[item] = {}
        current_obj = current_obj[item] 
    item = path_arr_[path_arr_.length-1]
    current_obj[item] = value

            
def cmd_logData(entity, command_stack, data_stack):
    console.log(data_stack[-1])
    command_stack.js_pop()
    data_stack.js_pop()
    return True

def cmd_loadMemory(entity, command_stack, data_stack):
    memory_path = data_stack[data_stack.length-1]
    mem = memory_of_entity(entity)

    command_stack.js_pop()
    data_stack.js_pop()
    data_stack.push(path_get(mem, memory_path, None))
    return True

def cmd_storeMemory(entity, command_stack, data_stack):
    value = data_stack[data_stack.length-2]
    memory_path = data_stack[data_stack.length-1]
    mem = memory_of_entity(entity)
    path_set(mem, memory_path, value)

    command_stack.js_pop()
    data_stack.js_pop()
    return True

def cmd_loadEntityAttr(entity, command_stack, data_stack):
    path = data_stack[data_stack.length-1]
    command_stack.js_pop()
    data_stack.js_pop()
    data_stack.push(path_get(entity, path, None))
    return True

def cmd_storeEntityAttr(entity, command_stack, data_stack):
    value = data_stack[data_stack.length-2]
    path = data_stack[data_stack.length-1]
    path_set(entity, path, value)

    command_stack.js_pop()
    data_stack.js_pop()
    return True

def cmd_constructionSite(entity, command_stack, data_stack):
    if entity.type == STRUCTURE_TOWER:
        # create job posting for this
        job_cmd_stack = []
        job_data_stack = []
    return False

def cmd_scoreUp(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score += 1
    command_stack.js_pop()

def cmd_scoreDown(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score -= 1
    command_stack.js_pop()

def cmd_scoreNUp(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score += data_stack[data_stack.length-1]
    command_stack.js_pop()
    data_stack.js_pop()

def cmd_scoreNDown(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score -= data_stack[data_stack.length-1]
    command_stack.js_pop()
    data_stack.js_pop()

def cmd_tower(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    # mem = entity.room.memory
    if mem:
        if "logistic" not in mem:
            mem.logistic = {}
        if "request" not in mem.logistic:
            mem.logistic.request = {}
        if "energy" not in mem.logistic.request:
            mem.logistic.request.energy = 0


    if entity.structureType == STRUCTURE_TOWER:
        # create job posting for this
        if entity.energy / entity.energyCapacity < 0.5:
            mem.logistic.request.energy = 1
        else:
            mem.logistic.request.energy = 0

        repairables = entity.room.find(FIND_STRUCTURES).filter(lambda s: s.hits < s.hitsMax)
        non_infrastructure = _.filter(repairable, lambda s:(s.structureType != STRUCTURE_ROAD) and (s.structureType != STRUCTURE_WALL))
        ramparts = _.filter(repairables, lambda s:s.structureType == STRUCTURE_RAMPART)
        if ramparts.length > 0:
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

    # command_stack.js_pop()
    return False


def cmd_useEnergyOnTarget(entity, command_stack, data_stack):
    sum_carry = _.sum(entity.carry) # TODO filter for energy
    if sum_carry == 0:
        command_stack.js_pop()
        data_stack.js_pop()
    else:
        # try different methods to use energy
        command_stack.js_pop()
        command_stack.push("transferEnergy")
        command_stack.push("repair")
        command_stack.push("buildStructure")
        command_stack.push("upgradeController")
        command_stack.push("duplicateData")
        command_stack.push("duplicateData")
        command_stack.push("duplicateData")
    
    return True



def cmd_energyRequestResponseJob(entity, command_stack, data_stack):
    command_stack.js_pop()


    command_stack.push("useEnergyOnTarget")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findEnergyRequester")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_5")

    command_stack.push("energyPickupJob")

    command_stack.push("storeMemory")
    data_stack.push(1)
    data_stack.push("logistic.quest.energy")

    return True

def cmd_transporterJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    command_stack.push("dropEnergy")
    command_stack.push("moveToPos")
    command_stack.push("pushData_2")
    command_stack.push("findTransportTargetPos")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_4")

    command_stack.push("energyPickupJob")
    command_stack.push("moveToPos")
    command_stack.push("pushData_2")
    command_stack.push("findTransportSourcePos")

    command_stack.push("dropn_if")
    command_stack.push("isCarryFull")
    command_stack.push("pushData_4")
    return True

def cmd_requestEnergy(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    # mem = entity.room.memory
    if mem:
        if "logistic" not in mem:
            mem.logistic = {}
        if "request" not in mem.logistic:
            mem.logistic.request = {}
        if "energy" not in mem.logistic.request:
            mem.logistic.request.energy = 0

        mem.logistic.request.energy = 1

    command_stack.js_pop()
    return True


def cmd_flag(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "logistic" not in mem:
            mem.logistic = {}

        if "range" not in mem.logistic:
            mem.logistic.range = {"storage":4,"assign":7}
        
        r = mem.logistic.range.storage
        stored_energy = _.map(
            _.filter(
                entity.room.lookAtArea(entity.pos.y-r,entity.pos.x-r,entity.pos.y+r,entity.pos.x+r, True),
                lambda obj: obj.type == "energy"),
            lambda obj: obj.energy.amount)
        sum_stored_energy = _.sum(stored_energy)

        mem.logistic.storage = {"energy": sum_stored_energy}


        mem.logistic.request = {}
        mem.logistic.quest = {}
        mem.logistic.harvest = {}

        if "non_flags" in mem.logistic:
            for non_flag_id in mem.logistic.non_flags:
                non_flag = Game.getObjectById(non_flag_id)
                if non_flag:

                    entity.room.visual.line(entity.pos, non_flag.pos, {'color': 'gray', 'style': 'dashed'})

                    mem2 = memory_of_entity(non_flag)
                    if "request" in mem2.logistic:
                        if "request" not in mem.logistic:
                            mem.logistic.request = mem2.logistic.request
                        else:
                            for key in Object.keys(mem2.logistic.request):
                                if key not in mem.logistic.request:
                                    mem.logistic.request[key] = mem2.logistic.request[key]
                                else:
                                    mem.logistic.request[key] += mem2.logistic.request[key]

                    if "quest" in mem2.logistic:
                        if "quest" not in mem.logistic:
                            mem.logistic.quest = mem2.logistic.quest
                        else:
                            for key in Object.keys(mem2.logistic.quest):
                                if key not in mem.logistic.quest:
                                    mem.logistic.quest[key] = mem2.logistic.quest[key]
                                else:
                                    mem.logistic.quest[key] += mem2.logistic.quest[key]

                    if "harvest" in mem2.logistic:
                        if "harvest" not in mem.logistic:
                            mem.logistic.harvest = mem2.logistic.harvest
                        else:
                            for key in Object.keys(mem2.logistic.harvest):
                                if key not in mem.logistic.harvest:
                                    mem.logistic.harvest[key] = mem2.logistic.harvest[key]
                                else:
                                    mem.logistic.harvest[key] += mem2.logistic.harvest[key]

                                # mem2.logistic.request[key] = mem2.logistic.request[key] // 2

        # say = "request:" + "\n"

        say = []
        if "non_flags" in mem.logistic:
            flag_creeps = _.filter(_.map(mem.logistic.non_flags,Game.getObjectById), 
                            lambda obj: "name" in obj and obj.name in Game.creeps)
            num_flag_creeps = flag_creeps.length
            if num_flag_creeps > 0:
                say.push("creeps: " + str(num_flag_creeps))

        if Object.keys(mem.logistic.request).length > 0:
            say.push("requests:")
            for key in Object.keys(mem.logistic.request):
                say.push(key + " " + str(mem.logistic.request[key]))
        
        if Object.keys(mem.logistic.quest).length > 0:
            say.push("quests:")
            for key in Object.keys(mem.logistic.quest):
                say.push(key + " " + str(mem.logistic.quest[key]))
        
        if Object.keys(mem.logistic.harvest).length > 0:
            say.push("harvesters:")
            for key in Object.keys(mem.logistic.harvest):
                say.push(key + " " + str(mem.logistic.harvest[key]))
        
        # say += "storage:" + "\n"
        if Object.keys(mem.logistic.storage).length > 0:
            say.push("storage:")
            for key in Object.keys(mem.logistic.storage):
                say.push(key + " " + str(mem.logistic.storage[key]))

        dy = -say.length*0.5
        for line in say:
            entity.room.visual.text(line, entity.pos.x, entity.pos.y+dy, {
                    "font": "0.5"
                })
            dy += 0.5


    # command_stack.js_pop()
    return False

def assign_flags():
    logistic_entities = _.filter(all_entities(), 
        lambda entity: "logistic" in memory_of_entity(entity))
    flags = _.filter(logistic_entities, 
        lambda entity: "secondaryColor" in entity)
    non_flags = _.filter(logistic_entities, 
        lambda entity: "secondaryColor" not in entity)
    if flags.length == 0: return
    for flag in flags:

        mem = memory_of_entity(flag)
        mem.logistic.non_flags = []

    for non_flag in non_flags:
        mem = memory_of_entity(non_flag)
        closest_flag = non_flag.pos.findClosestByRange(_.filter(flags, lambda flag: flag.room.name == non_flag.room.name))
        threshold = mem.logistic.range.assign if ("range" in mem.logistic and "assign" in mem.logistic.range) else 5
        if non_flag.pos.getRangeTo(closest_flag) < threshold:
            mem.logistic.flag = id_of_entity(closest_flag)
            memory_of_entity(closest_flag).logistic.non_flags.push(id_of_entity(non_flag))
        else:
            del mem.logistic.flag

commands = {
    # "collect_energy": {
    #     "required_body_parts": [MOVE,WORK,CARRY],
    #     "loop": task_collect_energy,
    # },
    # "deposit_energy": {
    #     "required_body_parts": [MOVE,WORK,CARRY],
    #     "loop": task_deposit_energy
    # },
    # "upgrade_controller": {
    #     "required_body_parts": [MOVE,WORK,CARRY],
    #     "loop": task_upgrade_controller
    # },
    # "build": {
    #     "required_body_parts": [MOVE,WORK,CARRY],
    #     "loop": task_build
    # },
    
    "requestEnergy": {
        "required_body_parts": [],
        "loop": cmd_requestEnergy
    },
    "scoreUp": {
        "required_body_parts": [],
        "loop": cmd_scoreUp
    },
    "scoreDown": {
        "required_body_parts": [],
        "loop": cmd_scoreDown
    },
    "scoreNUp": {
        "required_body_parts": [],
        "loop": cmd_scoreNUp
    },
    "scoreNDown": {
        "required_body_parts": [],
        "loop": cmd_scoreNDown
    },
    "flag": {
        "required_body_parts": [],
        "loop": cmd_flag
    },
    "tower": {
        "required_body_parts": [],
        "loop": cmd_tower
    },
    "employ": {
        "required_body_parts": [],
        "loop": cmd_employ
    },
    "harvestEnergyJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_harvestEnergyJob
    },
    "energyPickupJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_energyPickupJob
    },
    "depositEnergyJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_depositEnergyJob
    },
    "stationaryHarvesterJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_stationaryHarvesterJob
    },
    "energyPickupDepositJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_energyPickupDepositJob
    },
    "collectEnergyJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_collectEnergyJob
    },
    "upgradeControllerJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_upgradeControllerJob
    },
    "repairerJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_repairerJob
    },
    "buildStructureJob": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_buildStructureJob
    },
    "transporterJob": {
        "required_body_parts": [MOVE, CARRY],
        "loop": cmd_transporterJob
    },
    "energyRequestResponseJob": {
        "required_body_parts": [WORK, MOVE, CARRY],
        "loop": cmd_energyRequestResponseJob
    },
    "isCarryEmpty": {
        "required_body_parts": [],
        "loop": cmd_isCarryEmpty
    },
    "isCarryFull": {
        "required_body_parts": [],
        "loop": cmd_isCarryFull
    },
    "carriedEnergy": {
        "required_body_parts": [],
        "loop": cmd_carriedEnergy
    },
    "dropn_if": {
        "required_body_parts": [],
        "loop": cmd_dropn_if
    },
    "drop_if": {
        "required_body_parts": [],
        "loop": cmd_drop_if
    },
    "moveTo": {
        "required_body_parts": [MOVE],
        "loop": cmd_moveTo
    },
    "moveToPos": {
        "required_body_parts": [MOVE],
        "loop": cmd_moveToPos
    },
    "findEnergySource": {
        "required_body_parts": [],
        "loop": cmd_findEnergySource
    },
    "findEnergySourceWithFreeSlot": {
        "required_body_parts": [],
        "loop": cmd_findEnergySourceWithFreeSlot
    },
    "findEnergyDeposit": {
        "required_body_parts": [],
        "loop": cmd_findEnergyDeposit
    },
    "findDroppedEnergy": {
        "required_body_parts": [],
        "loop": cmd_findDroppedEnergy
    },
    "findController": {
        "required_body_parts": [],
        "loop": cmd_findController
    },
    "findConstructionSite": {
        "required_body_parts": [],
        "loop": cmd_findConstructionSite
    },
    "findRepairable": {
        "required_body_parts": [],
        "loop": cmd_findRepairable
    },
    "findTransportSourcePos": {
        "required_body_parts": [],
        "loop": cmd_findTransportSourcePos
    },
    "findTransportTargetPos": {
        "required_body_parts": [],
        "loop": cmd_findTransportTargetPos
    },
    "findEnergyRequester": {
        "required_body_parts": [],
        "loop": cmd_findEnergyRequester
    },
    "harvestEnergy": {
        "required_body_parts": [WORK, CARRY, MOVE],
        "loop": cmd_harvestEnergy
    },
    "pickup": {
        "required_body_parts": [CARRY, MOVE],
        "loop": cmd_pickup
    },
    "dropEnergy": {
        "required_body_parts": [CARRY],
        "loop": cmd_dropEnergy
    },
    "withdraw": {
        "required_body_parts": [CARRY, MOVE],
        "loop": cmd_withdraw
    },
    "repair": {
        "required_body_parts": [WORK, CARRY, MOVE],
        "loop": cmd_repair
    },
    "transferEnergy": {
        "required_body_parts": [WORK, CARRY],
        "loop": cmd_transferEnergy
    },
    "upgradeController": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_upgradeController
    },
    "buildStructure": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_buildStructure
    },
    "useEnergyOnTarget": {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_useEnergyOnTarget
    },
    "duplicateData": {
        "required_body_parts": [],
        "loop": cmd_duplicateData
    },
    "pushData_0": {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 0)
    },
    "pushData_1": {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 1)
    },
    "pushData_2": {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 2)
    },
    "pushData_3": {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 3)
    },
    "pushData_4": {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 4)
    },
    "pushData_5": {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 5)
    },
    "repeatCommand": {
        "required_body_parts": [],
        "loop": cmd_repeatCommand
    },
    "logData": {
        "required_body_parts": [],
        "loop": cmd_logData
    },
    "loadMemory": {
        "required_body_parts": [],
        "loop": cmd_loadMemory
    },
    "storeMemory": {
        "required_body_parts": [],
        "loop": cmd_storeMemory
    },
    "loadEntityAttr": {
        "required_body_parts": [],
        "loop": cmd_loadEntityAttr
    },
    "storeEntityAttr": {
        "required_body_parts": [],
        "loop": cmd_storeEntityAttr
    },
}

# for k in range(10):
#     commands["pushData_" + str(k)] = {
#         "required_body_parts": [],
#         "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, k)
#     }

jobs = {
    "harvester": { "command_stack": ["employ","collectEnergyJob","collectEnergyJob"], 
                   "data_stack": [] },
    "stationaryHarvester": { "command_stack": ["stationaryHarvesterJob", "repeatCommand"], 
                             "data_stack": [] },
    "energyPickupDeposit": { "command_stack": ["energyPickupDepositJob", "repeatCommand"], 
                             "data_stack": [] },
    "upgrader": { "command_stack": ["employ","upgradeControllerJob","upgradeControllerJob","upgradeControllerJob"], 
                  "data_stack": [] },
    "repairer": { "command_stack": ["employ","repairerJob","repairerJob","repairerJob"], 
                 "data_stack": [] },
    "builder": { "command_stack": ["employ","buildStructureJob","buildStructureJob","buildStructureJob"], 
                 "data_stack": [] },
    "constructionSite": { "command_stack": ["requestEnergy", "repeatCommand"], 
                          "data_stack": [] },
    "structure": { "command_stack": [], 
                   "data_stack": [] },
    "flag": { "command_stack": ["flag"], 
              "data_stack": [] },
    "controller": { "command_stack": ["requestEnergy", "repeatCommand"], 
                    "data_stack": [] },
    "transporter": { "command_stack": ["transporterJob", "repeatCommand"], 
                     "data_stack": [] },
    "energyRequestResponse": { "command_stack": ["energyRequestResponseJob", "repeatCommand"], 
                     "data_stack": [] },
    "tower": { "command_stack": ["tower", "repeatCommand"], 
               "data_stack": [] },
}

job_say = {
    "stationaryHarvester": "🏭⚡",
    "energyPickupDeposit": "🚛⚡",
    "harvester": "⚡",
    "upgrader": "⭐",
    "builder": "🛠",
    "repairer": "🔧",
    "transporter": "🚛🚩",
    "energyRequestResponse": "🚩⚡",
}

def distance(a,b):
    return a.pos.getRangeTo(b.pos)

def push_cmd_data(entity, command_stack_to_push, data_stack_to_push):
    # console.log("push_cmd_data")
    # console.log("entity.name", entity.name)
    # console.log("command_stack_to_push", command_stack_to_push)
    # console.log("data_stack_to_push", data_stack_to_push)
    mem = memory_of_entity(entity)
    for cmd in command_stack_to_push:
        mem.vm.cmd.push(cmd)
    for dta in data_stack_to_push:
        mem.vm.dta.push(dta)
    # console.log("entity.memory.vm.cmd", entity.memory.vm.cmd)
    # console.log("entity.memory.vm.dta", entity.memory.vm.dta)

def id_of_entity(entity):
    if "id" in entity and entity.id:
        return entity.id
    elif "name" in entity and entity.name:
        return entity.name
    else:
        return entity

def name_of_entity(entity):
    if "name" in entity and entity.name:
        return entity.name
    elif "id" in entity and entity.id:
        return entity.id
    else:
        return str(entity)

def memory_of_entity(entity):
    if "memory" in entity:
        return entity.memory
    else:
        if "entities" not in Memory:
            Memory.entities = {}

        id_ = id_of_entity(entity)
        if id_ not in Memory.entities:
            Memory.entities[id_] = {}

        return Memory.entities[id_]

def process_job(entity):
    memory = memory_of_entity(entity)
    if "job" not in memory: return False
    if memory.job not in jobs: return False
    job_description = jobs[memory.job]

    if "vm" not in memory:
        # init vm
        console.log("init vm on ", id_of_entity(entity))
        memory.vm = {"cmd": [], "dta": []}

    if memory.vm.cmd.length == 0:
        # populate vm with job
        console.log("populate vm on", id_of_entity(entity), "with job", memory.job)
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

    k, max_iter = 0, 5
    while process_vm(entity, memory.vm.cmd, memory.vm.dta) and k < max_iter:
        k+=1

    return True


def process_vm(entity, command_stack, data_stack):
    if len(command_stack) > 0:
        cmd = command_stack[command_stack.length-1]
        if cmd in commands:
            name_ = name_of_entity(entity)
            id_ = id_of_entity(entity)
            if name_ == "Sophia":
                console.log("[",name_,"]","execute", cmd)
            # console.log("[",name_,"]","execute", cmd)
            res = commands[cmd].loop(entity, command_stack, data_stack)
            # if name_ == "Ella":
                # console.log("[",name_,"]","  command_stack ", command_stack)
                # console.log("[",name_,"]","  data_stack    ", data_stack)
            return res
        else:
            console.log("drop unknown cmd", cmd)
            command_stack.js_pop()
            return True
    else:
        return False

# def process_task(creep):
#     if "task" not in creep.memory: return False
#     if "name" not in creep.memory.task: return False
#     if creep.memory.task.name not in tasks: return True
#     return tasks[creep.memory.task.name].loop(creep)

def all_entities():
    entities = []
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        entities.push(creep)

    for name in Object.keys(Game.rooms):
        room = Game.rooms[name]
        entities.push(room.controller)

    for name in Object.keys(Game.flags):
        flag = Game.flags[name]
        entities.push(flag)

    for name in Object.keys(Game.constructionSites):
        constructionSite = Game.constructionSites[name]
        entities.push(constructionSite)

    for name in Object.keys(Game.structures):
        structure = Game.structures[name]
        if  structure.structureType == STRUCTURE_TOWER:
            entities.push(structure)

    return entities

def process_jobs():
    assign_flags()

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

    # console.log("employment_statistics()", employment_statistics())
    Memory.employment_statistics = employment_statistics()

def job_requirements(job_tasks):
    return list(set([commands[task_name] for task_name in job_tasks]))

def meets_job_requirements(creep, job_tasks):
    for task_name in job_tasks:
        if "required_body_parts" in commands[task_name]:
            body_parts = [body_part.type for body_part in creep.body]
            for part in commands[task_name].required_body_parts:
                if not body_parts.includes(part):
                    # console.log("meets_job_requirements")
                    # console.log("creep.body", creep.body)
                    # console.log("part", part)
                    return False
    return True

def sample_weighted(seq, weights):
    r = Math.random()
    wsum = _.sum(weights)
    k = 0
    cumsum = 0
    for w in weights:
        cumsum = cumsum+(w/wsum)
        if r < cumsum:
            return seq[k]
        k+=1
    return seq[seq.length-1]



def employ(creep):
    console.log("employ")

    creep_jobs = {
        "harvester":             {"priority": 5, "minimum": 2, "maximum": 2},
        "builder":               {"priority": 5, "minimum": 1, "maximum": 1},
        "stationaryHarvester":   {"priority": 4, "minimum": 4, "maximum": 4},
        "energyPickupDeposit":   {"priority": 3, "minimum": 2, "maximum": 4},
        "energyRequestResponse": {"priority": 3, "minimum": 4, "maximum": 5},
        "transporter":           {"priority": 2, "minimum": 3, "maximum": 5},
        "repairer":              {"priority": 1, "minimum": 1},
        "upgrader":              {"priority": 0, "minimum": 2},
    }

    available_jobs = _.filter(Object.keys(creep_jobs),
                               lambda job_name: meets_job_requirements(creep, jobs[job_name]))
    if available_jobs.length == 0:
        return False
    else:

        if "employment_statistics" in Memory:
            sources = creep.room.find(FIND_DROPPED_RESOURCES).filter(lambda s: s.resourceType==RESOURCE_ENERGY)
            if Memory.employment_statistics.energyPickupDeposit <= 0:
                roomDroppedEnergy = _.sum(_.map(sources, lambda s:s.amount))
                if roomDroppedEnergy > 250:
                    creep_jobs["harvester"].minimum = 0
                    creep_jobs["harvester"].maximum = 0
                    creep_jobs["harvester"].priority = 3
                    creep_jobs["energyPickupDeposit"].priority = 5

            if Memory.employment_statistics.energyPickupDeposit > 0:
                creep_jobs["harvester"].minimum = 0
                creep_jobs["harvester"].maximum = 0

            for job_name in _.sortBy(Object.keys(creep_jobs), lambda job_name: -creep_jobs[job_name].priority):
                if not available_jobs.includes(job_name): continue
                if "maximum" in creep_jobs[job_name] and Memory.employment_statistics[job_name] >= creep_jobs[job_name].maximum:
                    console.log("remove job", job_name)
                    available_jobs.splice( available_jobs.indexOf(job_name), 1)
                    continue
                elif Memory.employment_statistics[job_name] < creep_jobs[job_name].minimum:
                    creep.memory.job = job_name
                    Memory.employment_statistics[job_name] += 1
                    console.log("assign job", creep.memory.job, "to", creep.name)
                    return True

        console.log("available_jobs", available_jobs)
        creep.memory.job = _.sample(available_jobs)
        console.log("assign job", creep.memory.job, "to", creep.name)
        return True

def employment_statistics():
    sum_employes = dict()
    sum_employes["unemployed"] = 0
    for job_name in Object.keys(jobs):
        sum_employes[job_name] = 0
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if "job" in creep.memory:
            sum_employes[creep.memory.job] += 1
        else:
            sum_employes["unemployed"] += 1
    return sum_employes
