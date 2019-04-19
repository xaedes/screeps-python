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
    commands["constructionSite"] = {
        "required_body_parts": [],
        "loop": cmd_constructionSite
    };

def cmd_constructionSite(entity, command_stack, data_stack):
    if entity.type == STRUCTURE_TOWER:
        # create job posting for this
        job_cmd_stack = []
        job_data_stack = []
    return False

