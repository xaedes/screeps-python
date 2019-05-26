
def idsOf(seq):
    return _.map(seq, lambda item: item.id)

def gameObjectsByIds(ids):
    return _.map(ids, lambda id_: Game.getObjectById(id_))

def distanceTo(x1,y1,x2,y2):
    dx=x1-x2
    dy=y1-y2
    return Math.sqrt(dx*dx+dy*dy)

def arr_replace(arr, arr2):
    arr.splice(0, arr.length)
    if arr2 == js_undefined: return
    for item in arr2:
        arr.push(item)

def positionsOf(objs):
    return _.map(objs, lambda obj: obj.pos)

def positionsByIds(ids):
    return positionsOf(gameObjectsByIds(ids))

def meanPosition(positions):
    sumx = 0.0
    sumy = 0.0
    count = 0
    for pos in positions:
        sumx += pos.x
        sumy += pos.y
        count += 1
    
    if count == 0:
        return 25,25
    else:
        return sumx/count,sumy/count

def meanPositionOfIds(ids):
    positions = positionsByIds(ids)
    return meanPosition(positions)

def roundN(number, num_digits):
    tenPow = 10 ** num_digits
    return Math.round(number*tenPow)/tenPow

def arr_iloc(arr, idx_seq):
    return [arr[idx] for idx in idx_seq]
