from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def task_collect_energy(creep):
    sum_carry = _.sum(creep.carry)
    if sum_carry < creep.carryCapacity:
        # If we dont have a saved source, find one
        if not creep.memory.task.state.source:
            # Get a random new source and save it
            sources = creep.room.find(FIND_SOURCES).filter(lambda s: s.energy>0)
            source = _.sample(sources)
            if sources.length == 0:
                return False
            creep.memory.task.state.source = source.id

        source = Game.getObjectById(creep.memory.task.state.source)
        if not source: return False
        creep.room.visual.line(creep.pos, source.pos, {'color': 'red', 'style': 'dashed'})

        # If we're near the source, harvest it - otherwise, move to it.
        if creep.pos.isNearTo(source):
            result = creep.harvest(source)
            if result != OK:
                console.log("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
        else:
            creep.moveTo(source)
        return False
    else:
        # creep.memory.task.results.push({"name":"carry_energy"})
        return True

def task_deposit_energy(creep):
    sum_carry = _.sum(creep.carry)
    if sum_carry > 0:
        # If we dont have a saved target, find one
        if not creep.memory.task.state.target:
            deposit_targets = _.filter(creep.room.find(FIND_STRUCTURES),
                lambda s: (s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION)
                           and s.energy < s.energyCapacity)
            if deposit_targets.length ==  0:
                return False
            target = _.sample(deposit_targets)
            creep.memory.task.state.target = target.id

        target = Game.getObjectById(creep.memory.task.state.target)

        if not target: return False

        creep.room.visual.line(creep.pos, target.pos)

        is_close = creep.pos.isNearTo(target)
        if is_close:
            if target.energyCapacity:
                result = creep.transfer(target, RESOURCE_ENERGY)
                if result == OK or result == ERR_FULL:
                    del creep.memory.task.state.target
                else:
                    console.log("[{}] Unknown result from creep.transfer({}, {}): {}".format(
                        creep.name, target, RESOURCE_ENERGY, result))
        else:
            creep.moveTo(target)
        return False
    else:
        # creep.memory.task.results.push({"name":"carry_energy"})
        return True

def task_upgrade_controller(creep):
    sum_carry = _.sum(creep.carry)
    if sum_carry > 0:
        # If we dont have a saved target, find one
        if not creep.memory.task.state.target:
            controllers = _.filter(creep.room.find(FIND_STRUCTURES),
                                   lambda s: s.structureType == STRUCTURE_CONTROLLER)
            if controllers.length ==  0:
                return False
            target = _.sample(controllers)
            creep.memory.task.state.target = target.id
        
        target = Game.getObjectById(creep.memory.task.state.target)

        if not target: return False

        creep.room.visual.line(creep.pos, target.pos)

        # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
        is_close = creep.pos.inRangeTo(target, 3)
        if is_close:
            if target.structureType == STRUCTURE_CONTROLLER:
                result = creep.upgradeController(target)
                if result != OK:
                    console.log("[{}] Unknown result from creep.upgradeController({}): {}".format(
                        creep.name, target, result))
                # Let the creeps get a little bit closer than required to the controller, to make room for other creeps.
                if not creep.pos.inRangeTo(target, 2):
                    creep.moveTo(target)
        else:
            creep.moveTo(target)

        return False
    else:
        return True

def task_build(creep):
    sum_carry = _.sum(creep.carry)
    # console.log("task_build")
    # console.log("sum_carry", sum_carry)
    if sum_carry > 0:
        # creep.memory.tasks.
        # If we dont have a saved target, find one
        if not creep.memory.task.state.target:
            construction_sites = _.filter(creep.room.find(FIND_CONSTRUCTION_SITES),
                                          lambda s: s.progress < s.progressTotal)
            if construction_sites.length ==  0:
                return False
            target = _.sample(construction_sites)
            creep.memory.task.state.target = target.id

        target = Game.getObjectById(creep.memory.task.state.target)

        # Target invalid or complete, find a new one
        if not target or "progressTotal" not in target or target.progress >= target.progressTotal:
            construction_sites = _.filter(creep.room.find(FIND_CONSTRUCTION_SITES),
                                          lambda s: s.progress < s.progressTotal)
            if construction_sites.length ==  0:
                return False
            while not target or "progressTotal" not in target or target.progress >= target.progressTotal:
                target = _.sample(construction_sites)
                creep.memory.task.state.target = target.id

        target = Game.getObjectById(creep.memory.task.state.target)
        # console.log("target", target)
        # console.log("creep.memory.task.state.target", creep.memory.task.state.target)

        if not target: return False

        creep.room.visual.line(creep.pos, target.pos)

        is_close = creep.pos.inRangeTo(target, 3)
        if is_close:
            if target.progressTotal:
                result = creep.build(target)
                if result != OK:
                    console.log("[{}] Unknown result from creep.build({}): {}".format(
                        creep.name, target, result))
                # Let the creeps get a little bit closer than required, to make room for other creeps.
                if not creep.pos.inRangeTo(target, 2):
                    creep.moveTo(target)
        else:
            creep.moveTo(target)
        return False
    else:
        return True

# def task_moveTo(creep):
#     if not creep.memory.task.state.target:
#         if creep.memory.task.stack.length < 2:
#             return True

#         creep.memory.task.state.distance_threshold = creep.memory.task.stack.pop()
#         creep.memory.task.state.target = creep.memory.task.stack.pop()

#     target = Game.getObjectById(creep.memory.task.state.target)
#     if not target:
#         return True

#     creep.room.visual.line(creep.pos, target.pos)
#     is_close = creep.pos.inRangeTo(target, creep.memory.task.state.distance_threshold)
    
#     if is_close:
#         return True
#     else:
#         return False

# def task_findEnergySource(creep):
#     # Get a random new source and save it
#     sources = creep.room.find(FIND_SOURCES).filter(lambda s: s.energy>0)
#     if sources.length == 0:
#         return False

#     source = _.sample(sources)

#     creep.memory.task.stack.push(source.id)

#     return True

# def task_findEnergyDeposit(creep):
#     # Get a random new source and save it
#     deposit_targets = _.filter(creep.room.find(FIND_STRUCTURES),
#         lambda s: (s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION)
#                    and s.energy < s.energyCapacity)
#     if deposit_targets.length == 0:
#         return False

#     deposit_target = _.sample(deposit_targets)

#     creep.memory.task.stack.push(deposit_target.id)

#     return True

# def task_harvestEnergy(creep):
#     if not creep.memory.task.state.target:
#         if creep.memory.task.stack.length < 1:
#             return True
#         creep.memory.task.state.target = creep.memory.task.stack.pop()

#     sum_carry = _.sum(creep.carry)
#     if sum_carry == creep.carryCapacity:
#         return True

#     target = Game.getObjectById(creep.memory.task.state.target)
#     result = creep.harvest(target)
#     if result != OK:
#         console.log("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
#         return True

#     return False

# def task_depositEnergy(creep):
#     if not creep.memory.task.state.target:
#         if creep.memory.task.stack.length < 1:
#             return True
#         creep.memory.task.state.target = creep.memory.task.stack.pop()

#     sum_carry = _.sum(creep.carry)
#     if sum_carry == 0:
#         return True

#     target = Game.getObjectById(creep.memory.task.state.target)

#     if target.energyCapacity:
#         result = creep.transfer(target, RESOURCE_ENERGY)
#         if result == OK:
#             return False
#         elif result == ERR_FULL or result == ERR_NOT_ENOUGH_RESOURCES:
#             return True
#         else:
#             return True
#             console.log("[{}] Unknown result from creep.transfer({}, {}): {}".format(
#                 creep.name, target, RESOURCE_ENERGY, result))
#     else:
#         return True



tasks = {
    "collect_energy": {
        "required_body_parts": [MOVE,WORK,CARRY],
        "loop": task_collect_energy,
    },
    "deposit_energy": {
        "required_body_parts": [MOVE,WORK,CARRY],
        "loop": task_deposit_energy
    },
    "upgrade_controller": {
        "required_body_parts": [MOVE,WORK,CARRY],
        "loop": task_upgrade_controller
    },
    "build": {
        "required_body_parts": [MOVE,WORK,CARRY],
        "loop": task_build
    },
    # "move_to": {
    #     "required_body_parts": [MOVE],
    #     "loop": task_moveTo
    # },
    # "find_energy_source": {
    #     "required_body_parts": [MOVE],
    #     "loop": task_findEnergySource
    # },
    # "find_energy_deposit": {
    #     "required_body_parts": [MOVE],
    #     "loop": task_findEnergyDeposit
    # },
    # "harvest_energy": {
    #     "required_body_parts": [MOVE],
    #     "loop": task_harvestEnergy
    # },
    # "deposit_energy_": {
    #     "required_body_parts": [MOVE],
    #     "loop": task_depositEnergy
    # },
}

jobs = {
    "harvester": ["collect_energy", "deposit_energy"],
    "upgrader": ["collect_energy", "upgrade_controller"],
    "builder": ["collect_energy", "build"],
}

job_say = {
    "harvester": "⚡",
    "upgrader": "⭐",
    "builder": "🔧",
}

def distance(a,b):
    return a.pos.getRangeTo(b.pos)

def process_job(creep):
    if "job" not in creep.memory: return False
    if creep.memory.job not in jobs: return False
    job_tasks = jobs[creep.memory.job]
    if job_tasks.length == 0: return False
    
    if "task" not in creep.memory:
        creep.memory.task = {}

    if "idx" not in creep.memory.task:
        creep.memory.task.idx = 0
        creep.memory.task.name = job_tasks[0]
        creep.memory.task.state = {}
        creep.memory.task.stack = []

    if creep.memory.job in job_say:
        creep.say(job_say[creep.memory.job])

    if process_task(creep):
        creep.memory.task.idx = (creep.memory.task.idx+1) % job_tasks.length
        creep.memory.task.name = job_tasks[creep.memory.task.idx]
        creep.memory.task.state = {}
        creep.memory.task.stack = []

    return True

def process_task(creep):
    if "task" not in creep.memory: return False
    if "name" not in creep.memory.task: return False
    if creep.memory.task.name not in tasks: return True
    return tasks[creep.memory.task.name].loop(creep)


def process_jobs():
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if not process_job(creep):
            employ(creep)
    # console.log("employment_statistics()", employment_statistics())
    Memory.employment_statistics = employment_statistics()

def job_requirements(job_tasks):
    return list(set([tasks[task_name] for task_name in job_tasks]))

def meets_job_requirements(creep, job_tasks):
    for task_name in job_tasks:
        if "required_body_parts" in tasks[task_name]:
            body_parts = [body_part.type for body_part in creep.body]
            for part in tasks[task_name].required_body_parts:
                if not body_parts.includes(part):
                    # console.log("meets_job_requirements")
                    # console.log("creep.body", creep.body)
                    # console.log("part", part)
                    return False
    return True

def sample_weighted(seq, weights):
    r = Math.random()
    wsum = _.sum(weights)
    k = 0
    cumsum = 0
    for w in weights:
        cumsum = cumsum+(w/wsum)
        if r < cumsum:
            return seq[k]
        k+=1
    return seq[-1]


def employ(creep):
    console.log("employ")
    available_jobs = _.filter(Object.keys(jobs),
                               lambda job_name: meets_job_requirements(creep, jobs[job_name]))
    console.log("available_jobs", available_jobs)
    if available_jobs.length == 0:
        return False
    else:

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
