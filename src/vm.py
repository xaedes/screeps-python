from defs import *
from .entity import *
from .commands import commands
from .utils import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

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

def init_vm(entity):
    memory = memory_of_entity(entity)
    if "vm" not in memory:
        # init vm
        console.log("init vm on ", id_of_entity(entity))
        memory.vm = {"cmd": [], "dta": []}

def process_vm(entity):
    memory = memory_of_entity(entity)

    max_iter = path_get(memory, "vm.max_iter", 10)
    k = 0
    while process_vm_step(entity, memory.vm.cmd, memory.vm.dta) and k < max_iter:
        k+=1

# returns whether to continue vm processing or not
def process_vm_step(entity, command_stack, data_stack):
    if len(command_stack) > 0:
        cmd = command_stack[command_stack.length-1]
        if cmd in commands:
            name_ = name_of_entity(entity)
            id_ = id_of_entity(entity)
            # if name_ == "Emily":
                # console.log("[",name_,"]","execute", cmd)
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
