
from GCode import ImageToGcode
from Input import pairFrom


def rasterize ( options ):

    offsets = [
        options.red ,
        options.green ,
        options.blue ,
        options.black        
    ]
    
    offsets = list(map(pairFrom,offsets))

    ImageToGcode (
        feedrate = float(options.feedrate) ,
        nozzles = float(options.nozzles) ,
        offsets = offsets ,
        spread = float(options.spread) ,
        area = pairFrom(options.area) ,
        img = options.input
    )