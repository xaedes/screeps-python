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
    commands["dropn_if"] = {
        "required_body_parts": [],
        "loop": cmd_dropn_if
    };
    commands["drop_if"] = {
        "required_body_parts": [],
        "loop": cmd_drop_if
    };

    commands["duplicateData"] = {
        "required_body_parts": [],
        "loop": cmd_duplicateData
    };
    commands["pushData_0"] = {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 0)
    };
    commands["pushData_1"] = {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 1)
    };
    commands["pushData_2"] = {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 2)
    };
    commands["pushData_3"] = {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 3)
    };
    commands["pushData_4"] = {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 4)
    };
    commands["pushData_5"] = {
        "required_body_parts": [],
        "loop": lambda entity, command_stack, data_stack: cmd_pushData(entity, command_stack, data_stack, 5)
    };
    commands["repeatCommand"] = {
        "required_body_parts": [],
        "loop": cmd_repeatCommand
    };
    commands["logData"] = {
        "required_body_parts": [],
        "loop": cmd_logData
    };
    commands["loadMemory"] = {
        "required_body_parts": [],
        "loop": cmd_loadMemory
    };
    commands["storeMemory"] = {
        "required_body_parts": [],
        "loop": cmd_storeMemory
    };
    commands["loadEntityAttr"] = {
        "required_body_parts": [],
        "loop": cmd_loadEntityAttr
    };
    commands["storeEntityAttr"] = {
        "required_body_parts": [],
        "loop": cmd_storeEntityAttr
    };
    commands["loadData"] = {
        "required_body_parts": [],
        "loop": cmd_loadData
    };
    commands["loadRelData"] = {
        "required_body_parts": [],
        "loop": cmd_loadRelData
    };
    commands["loadArgument"] = {
        "required_body_parts": [],
        "loop": cmd_loadArgument
    };
    commands["loadBasePointer"] = {
        "required_body_parts": [],
        "loop": cmd_loadBasePointer
    };
    commands["storeBasePointer"] = {
        "required_body_parts": [],
        "loop": cmd_storeBasePointer
    };
    commands["add"] = {
        "required_body_parts": [],
        "loop": cmd_add
    };
    commands["sub"] = {
        "required_body_parts": [],
        "loop": cmd_sub
    };
    commands["mul"] = {
        "required_body_parts": [],
        "loop": cmd_mul
    };
    commands["div"] = {
        "required_body_parts": [],
        "loop": cmd_div
    };

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


def cmd_logData(entity, command_stack, data_stack):
    console.log(data_stack[-1])
    command_stack.js_pop()
    data_stack.js_pop()
    return True

def cmd_add(entity, command_stack, data_stack):
    if data_stack.length<2: 
        command_stack.js_pop()
        return True
    try:
        a = float(data_stack[data_stack.length-2])
        b = float(data_stack[data_stack.length-1])
        c = a+b
        # console.log("add(",a,",",b,") =",c)
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(c)
    except:
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(None)
    return True

def cmd_sub(entity, command_stack, data_stack):
    if data_stack.length<2: 
        command_stack.js_pop()
        return True
    # console.log("data_stack.length               ", data_stack.length)
    # console.log("data_stack[data_stack.length-2] ", data_stack[data_stack.length-2])
    # console.log("data_stack[data_stack.length-1] ", data_stack[data_stack.length-1])
    try:
        a = float(data_stack[data_stack.length-2])
        b = float(data_stack[data_stack.length-1])
        c = a-b
        # console.log("sub(",a,",",b,") =",c)
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(c)
    except:
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(None)
    return True

def cmd_mul(entity, command_stack, data_stack):
    if data_stack.length<2: 
        command_stack.js_pop()
        return True

    try:
        a = float(data_stack[data_stack.length-2])
        b = float(data_stack[data_stack.length-1])
        c = a*b
        # console.log("mul(",a,",",b,") =",c)
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(c)
    except:
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(None)
    return True

def cmd_div(entity, command_stack, data_stack):
    if data_stack.length<2: 
        command_stack.js_pop()
        return True
    try:
        a = float(data_stack[data_stack.length-2])
        b = float(data_stack[data_stack.length-1])
        c = a/b
        # console.log("div(",a,",",b,") =",c)
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(c)
    except:
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(None)
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
    data_stack.js_pop()
    return True

def cmd_loadData(entity, command_stack, data_stack):
    if data_stack.length < 1: 
        command_stack.js_pop()
        return True

    idx = data_stack[data_stack.length-1]
    while idx < 0:
        idx += data_stack.length
    while idx >= data_stack.length:
        idx -= data_stack.length
    command_stack.js_pop()
    data_stack.js_pop()
    if 0 <= idx < data_stack.length:
        data_stack.push(data_stack[idx])
    return True

def cmd_loadRelData(entity, command_stack, data_stack):
    if data_stack.length < 2: 
        command_stack.js_pop()
        data_stack.js_pop()
        if data_stack.length > 0:
            data_stack.js_pop()
        return True

    idx = data_stack[data_stack.length-2]
    offset = data_stack[data_stack.length-1]
    while idx+offset < 0:
        offset += data_stack.length
    while idx+offset >= data_stack.length:
        offset -= data_stack.length
    command_stack.js_pop()
    data_stack.js_pop()
    if 0 <= idx+offset < data_stack.length:
        data_stack.push(data_stack[idx+offset])
    return True

def cmd_loadArgument(entity, command_stack, data_stack):
    if data_stack.length < 1: 
        command_stack.js_pop()
        return True
    mem = memory_of_entity(entity)
    bp = path_get(mem, "bp", None)
    if bp:
        idx = bp-data_stack[data_stack.length-1]
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(data_stack[idx])
        return True
    else:
        command_stack.js_pop()
        data_stack.js_pop()
        data_stack.push(None)
        return True

def cmd_loadBasePointer(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    command_stack.js_pop()
    data_stack.push(path_get(mem, "bp", None))
    return True

def cmd_storeBasePointer(entity, command_stack, data_stack):
    mem = memory_of_entity(entity)
    path_set(mem, "bp", data_stack.length-1)
    command_stack.js_pop()
    return True

