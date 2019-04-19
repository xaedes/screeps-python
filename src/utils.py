from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def path_arr(path):
    if type(path) == str:
        return path.split(".")
    else:
        return path

def path_get(obj, path, default_value):
    path_arr_ = path_arr(path)
    # wrapped with object, so inner loop accesses wont be transpiled to local variables
    current = {"obj":obj}
    for item in path_arr_:
        if item in current.obj:
            current.obj = current.obj[item]
        else:
            return default_value
    return current.obj

            
def path_set(obj, path, value):
    path_arr_ = path_arr(path)
    # wrapped with object, so inner loop accesses wont be transpiled to local variables
    current = {"obj":obj}
    for item in path_arr_[:path_arr_.length-1]:
        if item not in current.obj:
            current.obj[item] = {}
        current.obj = current.obj[item]
    item = path_arr_[path_arr_.length-1]
    current.obj[item] = value

def distance(a,b):
    return a.pos.getRangeTo(b.pos)


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
    return seq[seq.length-1]
