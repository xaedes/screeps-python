
from constants import *

def draw_costs(room, costs, max_alpha, color):
    h,w = costs.shape
    max_value = _.max(_.filter(costs.data, lambda cost: cost<BIG_VALUE))
    for y in range(h):
        for x in range(w):
            if costs.data[y*w+x]<BIG_VALUE:
                if room.visual.getSize() < 500000:
                    room.visual.rect(x-0.5,y-0.5,1,1,{
                        "opacity": max_alpha*costs.data[y*w+x] / max_value,
                        "fill": color
                        })

def draw_colors(room, color_idcs, colors, alpha):
        h,w = color_idcs.shape
        n = colors.length
        max_value = _.max(_.filter(color_idcs.data, lambda cost: cost<BIG_VALUE))
        for y in range(h):
            for x in range(w):
                idx = color_idcs.data[y*w+x]
                if 0 <= idx:
                    if room.visual.getSize() < 500000:
                        room.visual.rect(x-0.5,y-0.5,1,1,{
                            "opacity": alpha,
                            "fill": colors[idx % n]
                            })
