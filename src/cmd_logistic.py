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
    commands["requestEnergy"] = {
        "required_body_parts": [],
        "loop": cmd_requestEnergy
    };

    commands["flag"] = {
        "required_body_parts": [],
        "loop": cmd_flag
    };



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
        
        path_set(mem, "logistic.request.energy", 
            1 + path_get(mem, "logistic.request.energy", 0))

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
                            lambda obj: obj and "name" in obj and obj.name in Game.creeps)
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

