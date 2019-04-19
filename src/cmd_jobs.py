from defs import *
from .utils import *
from .entity import *
import employment

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def register_commands(commands):
    commands["employ"] = {
        "required_body_parts": [],
        "loop": cmd_employ
    };
    commands["harvestEnergyJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_harvestEnergyJob
    };
    commands["energyPickupJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_energyPickupJob
    };
    commands["depositEnergyJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_depositEnergyJob
    };
    commands["stationaryHarvesterJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_stationaryHarvesterJob
    };
    commands["energyPickupDepositJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_energyPickupDepositJob
    };
    commands["collectEnergyJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_collectEnergyJob
    };
    commands["upgradeControllerJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_upgradeControllerJob
    };
    commands["repairerJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_repairerJob
    };
    commands["buildStructureJob"] = {
        "required_body_parts": [MOVE, WORK, CARRY],
        "loop": cmd_buildStructureJob
    };
    commands["transporterJob"] = {
        "required_body_parts": [MOVE, CARRY],
        "loop": cmd_transporterJob
    };
    commands["energyRequestResponseJob"] = {
        "required_body_parts": [WORK, MOVE, CARRY],
        "loop": cmd_energyRequestResponseJob
    };

def cmd_employ(entity, command_stack, data_stack):
    employment.employ(entity)
    command_stack.js_pop()
    return True

def cmd_stationaryQuesterJob(entity, command_stack, data_stack):
    command_stack.js_pop()
    # inputs target, flag

    command_stack.push("useEnergyOnTarget")
    command_stack.push("getEnergyFromFlag")

    command_stack.push("storeMemory")
    data_stack.push(1)
    data_stack.push("logistic.quest.energy")

    command_stack.push("storeMemory")
    data_stack.push(5)
    data_stack.push("range.find")

    return True

def cmd_stationaryHarvesterJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    command_stack.push("dropEnergy")
    command_stack.push("scoreNUp") # += carriedEnergyNow - carriedEnergyBefore
    data_stack.push(-1)
    command_stack.push("mul")
    command_stack.push("sub")
    command_stack.push("carriedEnergy")

    command_stack.push("harvestEnergy")
    command_stack.push("moveTo")
    command_stack.push("pushData_1")
    command_stack.push("duplicateData")
    command_stack.push("findEnergySourceWithFreeSlot")
    
    command_stack.push("carriedEnergy")

    command_stack.push("storeMemory")
    data_stack.push(1)
    data_stack.push("logistic.harvest.energy")

    return True

def cmd_energyPickupJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    sum_carry = _.sum(entity.carry) # TODO filter for energy
    if sum_carry < entity.carryCapacity:
        command_stack.push("scoreNUp") # += carriedEnergyNow - carriedEnergyBefore
        data_stack.push(-1)
        command_stack.push("mul")
        command_stack.push("sub")
        command_stack.push("carriedEnergy")
        command_stack.push("pickup")
        command_stack.push("moveTo")
        command_stack.push("pushData_1")
        command_stack.push("duplicateData")
        command_stack.push("findDroppedEnergy")
        command_stack.push("carriedEnergy")

    return True

def cmd_harvestEnergyJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    sum_carry = _.sum(entity.carry) # TODO filter for energy
    if sum_carry < entity.carryCapacity:
        command_stack.push("scoreNUp") # += carriedEnergyNow - carriedEnergyBefore
        data_stack.push(-1)
        command_stack.push("mul")
        command_stack.push("sub")
        command_stack.push("carriedEnergy")
        command_stack.push("harvestEnergy")
        command_stack.push("moveTo")
        command_stack.push("pushData_1")
        command_stack.push("duplicateData")
        command_stack.push("findEnergySourceWithFreeSlot")
        command_stack.push("carriedEnergy")

    return True

def cmd_depositEnergyJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    sum_carry = _.sum(entity.carry) # TODO filter for energy
    if sum_carry > 0:
        command_stack.push("depositEnergyJob")
        command_stack.push("scoreNUp") # += carriedEnergyBefore - carriedEnergyNow
        command_stack.push("sub")
        command_stack.push("carriedEnergy")
        command_stack.push("transferEnergy")
        command_stack.push("moveTo")
        command_stack.push("pushData_1")
        command_stack.push("duplicateData")
        command_stack.push("findEnergyDeposit")
        command_stack.push("carriedEnergy")

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
    command_stack.push("scoreNUp") # += carriedEnergyBefore - carriedEnergyNow
    command_stack.push("sub")
    command_stack.push("carriedEnergy")
    command_stack.push("upgradeController")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findController")
    command_stack.push("carriedEnergy")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_5")

    command_stack.push("energyPickupJob")
    return True

def cmd_repairerJob(entity, command_stack, data_stack):
    command_stack.js_pop()
    command_stack.push("scoreNUp") # += carriedEnergyBefore - carriedEnergyNow
    command_stack.push("sub")
    command_stack.push("carriedEnergy")
    command_stack.push("repair")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findRepairable")
    command_stack.push("carriedEnergy")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_5")

    command_stack.push("energyPickupJob")
    return True

def cmd_buildStructureJob(entity, command_stack, data_stack):
    command_stack.js_pop()
    command_stack.push("scoreNUp") # += carriedEnergyBefore - carriedEnergyNow
    command_stack.push("sub")
    command_stack.push("carriedEnergy")
    command_stack.push("buildStructure")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findConstructionSite")
    command_stack.push("carriedEnergy")

    command_stack.push("dropn_if")
    command_stack.push("isCarryEmpty")
    command_stack.push("pushData_5")

    command_stack.push("energyPickupJob")
    return True

def cmd_energyRequestResponseJob(entity, command_stack, data_stack):
    command_stack.js_pop()

    command_stack.push("scoreNUp") # += carriedEnergyBefore - carriedEnergyNow
    command_stack.push("sub")
    command_stack.push("carriedEnergy")

    command_stack.push("useEnergyOnTarget")
    command_stack.push("moveTo")
    command_stack.push("pushData_2")
    command_stack.push("duplicateData")
    command_stack.push("findEnergyRequester")
    
    command_stack.push("carriedEnergy")

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

    command_stack.push("scoreNUp") # += carriedEnergyBefore - carriedEnergyNow
    command_stack.push("sub")
    command_stack.push("carriedEnergy")
    command_stack.push("dropEnergy")
    command_stack.push("moveToPos")
    command_stack.push("pushData_2")
    command_stack.push("findTransportTargetPos")
    command_stack.push("carriedEnergy")

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


