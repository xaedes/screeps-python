from defs import *
import cmd_vm
import cmd_construction
import cmd_creep
import cmd_find
import cmd_logistic
import cmd_jobs
import cmd_tower
import cmd_score
import cmd_controller

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

commands = {}
cmd_vm.register_commands(commands)
cmd_construction.register_commands(commands)
cmd_creep.register_commands(commands)
cmd_find.register_commands(commands)
cmd_logistic.register_commands(commands)
cmd_jobs.register_commands(commands)
cmd_tower.register_commands(commands)
cmd_score.register_commands(commands)
cmd_controller.register_commands(commands)
