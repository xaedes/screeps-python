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
    commands["scoreUp"] = {
        "required_body_parts": [],
        "loop": cmd_scoreUp
    };
    commands["scoreDown"] = {
        "required_body_parts": [],
        "loop": cmd_scoreDown
    };
    commands["scoreNUp"] = {
        "required_body_parts": [],
        "loop": cmd_scoreNUp
    };
    commands["scoreNDown"] = {
        "required_body_parts": [],
        "loop": cmd_scoreNDown
    };



def cmd_scoreUp(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score += 1
    command_stack.js_pop()
    return True

def cmd_scoreDown(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score -= 1
    command_stack.js_pop()
    return True

def cmd_scoreNUp(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score += data_stack[data_stack.length-1]
    command_stack.js_pop()
    data_stack.js_pop()
    return True

def cmd_scoreNDown(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    if mem:
        if "score" not in mem:
            mem.score = 0
        mem.score -= data_stack[data_stack.length-1]
    command_stack.js_pop()
    data_stack.js_pop()

