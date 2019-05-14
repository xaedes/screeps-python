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
        path_init(mem, "logistic", {})
        path_init(mem, "logistic.range", {"storage":4,"assign":7})
        
        
        r = mem.logistic.range.storage
        entities_in_range = entity.room.lookAtArea(
            entity.pos.y-r,
            entity.pos.x-r,
            entity.pos.y+r,
            entity.pos.x+r, 
            True) # as flat array
        dropped_energy = _.filter(entities_in_range, lambda obj: obj.type == "energy")
        sources = _.filter(entities_in_range, lambda obj: obj.type == "source")
        sum_dropped_energy = _.sum(_.map(dropped_energy,lambda obj: obj.energy.amount))
        mem.logistic.storage = {"energy": sum_dropped_energy}

        # TODO
        #  - storage ids
        #  - storage targets
        #  - source slots
        #  - offer jobs
        #    - energy requesters
        #    - source slots
        #  - hire creeps

        # aggregate data from non flag entities assigned to this flag
        mem.logistic.request = {}
        mem.logistic.quest = {}
        mem.logistic.harvest = {}
        mem.logistic.job_postings = []

        for non_flag_id in path_get(mem,"logistic.non_flags",[]):
            non_flag = Game.getObjectById(non_flag_id)
            if non_flag:
                entity.room.visual.line(entity.pos, non_flag.pos, {'color': 'gray', 'style': 'dashed'})

                mem2 = memory_of_entity(non_flag)
                if not mem2: continue
                if not "logistic" in mem2: continue

                for job_posting in path_get(mem2,"logistic.job_postings",[]):
                    mem.logistic.job_postings.push(job_posting)

                for key in Object.keys(path_get(mem2,"logistic.request",{})):
                    if key not in mem.logistic.request:
                        mem.logistic.request[key] = mem2.logistic.request[key]
                    else:
                        mem.logistic.request[key] += mem2.logistic.request[key]

                for key in Object.keys(path_get(mem2,"logistic.quest",{})):
                    if key not in mem.logistic.quest:
                        mem.logistic.quest[key] = mem2.logistic.quest[key]
                    else:
                        mem.logistic.quest[key] += mem2.logistic.quest[key]

                for key in Object.keys(path_get(mem2,"logistic.harvest",{})):
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

        if mem.logistic.job_postings.length > 0:
            say.push("jobs: " + str(mem.logistic.job_postings.length))

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

        def visual_say(entity, say, size=0.5, padding=0):
            dy = -say.length*(size+padding)
            for line in say:
                entity.room.visual.text(line, entity.pos.x, entity.pos.y+dy, {
                        "font": "size"
                    })
                dy += size+padding
        visual_say(entity, say)

    # command_stack.js_pop()
    return False

