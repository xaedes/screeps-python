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
    commands["moveTo"] = {
        "required_body_parts": [MOVE],
        "loop": cmd_moveTo
    };
    commands["moveToPos"] = {
        "required_body_parts": [MOVE],
        "loop": cmd_moveToPos
    };
    commands["harvestEnergy"] = {
        "required_body_parts": [WORK, CARRY, MOVE],
        "loop": cmd_harvestEnergy
    };
    commands["pickup"] = {
        "required_body_parts": [CARRY, MOVE],
        "loop": cmd_pickup
    };
    commands["dropEnergy"] = {
        "required_body_parts": [CARRY],
        "loop": cmd_dropEnergy
    };
    commands["withdraw"] = {
        "required_body_parts": [CARRY, MOVE],
        "loop": cmd_withdraw
    };
    commands["repair"] = {
        "required_body_parts": [WORK, CARRY, MOVE],
        "loop": cmd_repair
    };
    commands["transferEnergy"] = {
        "required_body_parts": [WORK, CARRY],
        "loop": cmd_transferEnergy
    };
    commands["upgradeController"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_upgradeController
    };
    commands["buildStructure"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_buildStructure
    };
    commands["useEnergyOnTarget"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_useEnergyOnTarget
    };

    commands["isCarryEmpty"] = {
        "required_body_parts": [],
        "loop": cmd_isCarryEmpty
    };
    commands["isCarryFull"] = {
        "required_body_parts": [],
        "loop": cmd_isCarryFull
    };
    commands["carriedEnergy"] = {
        "required_body_parts": [],
        "loop": cmd_carriedEnergy
    };

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
    # else:
        # command_stack.push("scoreNUp")
        # data_stack.push(sum_carry)

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

        # command_stack.push("scoreNUp")
        # data_stack.push(_.sum(entity.carry) - sum_carry)
        # data_stack.push(1)
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

        # command_stack.push("scoreNUp")
        # data_stack.push(_.sum(entity.carry) - sum_carry)
        # data_stack.push(1)
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
            # command_stack.push("scoreNUp")
            # data_stack.push(sum_carry)
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
            # command_stack.push("scoreNUp")
            # data_stack.push(_.sum(entity.carry) - sum_carry)
            # data_stack.push(1)
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
            # command_stack.push("scoreNUp")
            # data_stack.push(_.sum(entity.carry) - sum_carry)
            # data_stack.push(1)
            return False
        else:
            console.log("[{}] Unknown result from entity.build({}): {}".format(
                entity.name, target, result))
            data_stack.js_pop()
            command_stack.js_pop()
            return True

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
    carried_energy = entity.carry[RESOURCE_ENERGY]
    # console.log("cmd_carriedEnergy", carried_energy)
    data_stack.push(carried_energy)
    return True
