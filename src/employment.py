from defs import *
from .entity import *
from .utils import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

jobs = {
    "harvester": { "command_stack": ["employ","collectEnergyJob","collectEnergyJob"], 
                   "data_stack": [] },
    "stationaryHarvester": { "command_stack": ["stationaryHarvesterJob", "repeatCommand"], 
                             "data_stack": [] },
    "energyPickupDeposit": { "command_stack": ["energyPickupDepositJob", "repeatCommand"], 
                             "data_stack": [] },
    "upgrader": { "command_stack": ["employ","upgradeControllerJob","upgradeControllerJob","upgradeControllerJob"], 
                  "data_stack": [] },
    "repairer": { "command_stack": ["employ","repairerJob","repairerJob","repairerJob"], 
                 "data_stack": [] },
    "builder": { "command_stack": ["employ","buildStructureJob","buildStructureJob","buildStructureJob"], 
                 "data_stack": [] },
    "constructionSite": { "command_stack": ["storeMemory"], 
                          "data_stack": [1, "logistic.request.energy"] },
    "structure": { "command_stack": [], 
                   "data_stack": [] },
    "flag": { "command_stack": ["flag"], 
              "data_stack": [] },
    "controller": { "command_stack": ["controller"], 
                    "data_stack": [] },
    "transporter": { "command_stack": ["transporterJob", "repeatCommand"], 
                     "data_stack": [] },
    "energyRequestResponse": { "command_stack": ["energyRequestResponseJob", "repeatCommand"], 
                     "data_stack": [] },
    "tower": { "command_stack": ["tower", "repeatCommand"], 
               "data_stack": [] },
}

job_say = {
    "stationaryHarvester": "🏭⚡",
    "energyPickupDeposit": "🚛⚡",
    "harvester": "⚡",
    "upgrader": "⭐",
    "builder": "🛠",
    "repairer": "🔧",
    "transporter": "🚛🚩",
    "energyRequestResponse": "🚩⚡",
}

def job_requirements(job_tasks):
    return list(set([commands[task_name] for task_name in job_tasks]))

def meets_job_requirements(creep, job_tasks):
    for task_name in job_tasks:
        if "required_body_parts" in commands[task_name]:
            body_parts = [body_part.type for body_part in creep.body]
            for part in commands[task_name].required_body_parts:
                if not body_parts.includes(part):
                    # console.log("meets_job_requirements")
                    # console.log("creep.body", creep.body)
                    # console.log("part", part)
                    return False
    return True

def employ(creep):
    console.log("employ")

    creep_jobs = {
        "harvester":             {"priority": 5, "minimum": 2, "maximum": 2},
        "builder":               {"priority": 5, "minimum": 1, "maximum": 1},
        "stationaryHarvester":   {"priority": 4, "minimum": 4, "maximum": 4},
        "energyPickupDeposit":   {"priority": 3, "minimum": 3, "maximum": 4},
        "energyRequestResponse": {"priority": 3, "minimum": 4, "maximum": 5},
        "transporter":           {"priority": 2, "minimum": 3, "maximum": 5},
        "repairer":              {"priority": 1, "minimum": 1},
        "upgrader":              {"priority": 0, "minimum": 2},
    }
    current_job = path_get(creep.memory, "job", None)
    available_jobs = _.filter(Object.keys(creep_jobs),
                               lambda job_name: meets_job_requirements(creep, jobs[job_name]))
    if available_jobs.length == 0:
        return False
    else:

        if "employment_statistics" in Memory:
            sources = creep.room.find(FIND_DROPPED_RESOURCES).filter(lambda s: s.resourceType==RESOURCE_ENERGY)
            if Memory.employment_statistics.energyPickupDeposit <= 0:
                roomDroppedEnergy = _.sum(_.map(sources, lambda s:s.amount))
                if roomDroppedEnergy > 250:
                    creep_jobs["harvester"].minimum = 0
                    creep_jobs["harvester"].maximum = 0
                    creep_jobs["harvester"].priority = 3
                    creep_jobs["energyPickupDeposit"].priority = 5

            if Memory.employment_statistics.energyPickupDeposit > 0:
                creep_jobs["harvester"].minimum = 0
                creep_jobs["harvester"].maximum = 0

            for job_name in _.sortBy(Object.keys(creep_jobs), lambda job_name: -creep_jobs[job_name].priority):
                is_my_job = current_job == job_name
                offset_is_my_job = 1 if is_my_job else 0
                if not available_jobs.includes(job_name): continue
                if "maximum" in creep_jobs[job_name] and Memory.employment_statistics[job_name]-offset_is_my_job >= creep_jobs[job_name].maximum:
                    console.log("remove job", job_name)
                    available_jobs.splice( available_jobs.indexOf(job_name), 1)
                    continue
                elif Memory.employment_statistics[job_name]-offset_is_my_job < creep_jobs[job_name].minimum:
                    creep.memory.job = job_name
                    Memory.employment_statistics[job_name] += 1-offset_is_my_job
                    console.log("assign job", creep.memory.job, "to", creep.name)
                    return True

        console.log("available_jobs", available_jobs)
        creep.memory.job = _.sample(available_jobs)
        console.log("assign job", creep.memory.job, "to", creep.name)
        return True

def employment_statistics():
    sum_employes = dict()
    sum_employes["unemployed"] = 0
    for job_name in Object.keys(jobs):
        sum_employes[job_name] = 0
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if "job" in creep.memory:
            sum_employes[creep.memory.job] += 1
        else:
            sum_employes["unemployed"] += 1
    return sum_employes
