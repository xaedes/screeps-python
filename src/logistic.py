from defs import *
from .entity import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

from cmd_find import energySourceSlots
from cmd_find import energySourcesSlots
from cmd_find import filterFindInRange

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

def process_logistic():
    assign_flags()

