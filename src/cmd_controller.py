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
    commands["controller"] = {
        "required_body_parts": [],
        "loop": cmd_controller
    };

def cmd_controller(entity, command_stack, data_stack):
    # console.log("cmd_controller")
    # console.log("entity.structureType", entity.structureType)
    # console.log("STRUCTURE_CONTROLLER", STRUCTURE_CONTROLLER)
    if entity.structureType != STRUCTURE_CONTROLLER:
        command_stack.js_pop()
        return True

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
    
    path_set(mem, "logistic.request.energy", 2)

    return False

