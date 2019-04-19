from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def id_of_entity(entity):
    if "id" in entity and entity.id:
        return entity.id
    elif "name" in entity and entity.name:
        return entity.name
    else:
        return entity

def name_of_entity(entity):
    if "name" in entity and entity.name:
        return entity.name
    elif "id" in entity and entity.id:
        return entity.id
    else:
        return str(entity)

def memory_of_entity(entity):
    if "memory" in entity:
        return entity.memory
    else:
        if "entities" not in Memory:
            Memory.entities = {}

        id_ = id_of_entity(entity)
        if id_ not in Memory.entities:
            Memory.entities[id_] = {}

        return Memory.entities[id_]

def all_entities():
    entities = []
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        entities.push(creep)

    for name in Object.keys(Game.rooms):
        room = Game.rooms[name]
        entities.push(room.controller)

    for name in Object.keys(Game.flags):
        flag = Game.flags[name]
        entities.push(flag)

    for name in Object.keys(Game.constructionSites):
        constructionSite = Game.constructionSites[name]
        entities.push(constructionSite)

    for name in Object.keys(Game.structures):
        structure = Game.structures[name]
        if  structure.structureType == STRUCTURE_TOWER:
            entities.push(structure)

    return entities
