
from GCode import ImageToGcode
from Input import pairFrom


def rasterize ( options ):

    offsets = [pairFrom(options.red),
               pairFrom(options.green),
               pairFrom(options.blue),
               pairFrom(options.black)
               ]

    imageProcessor = ImageToGcode(img=options.input,
                                  spread=float(options.spread),
                                  nozzles=float(options.nozzles),
                                  area=pairFrom(options.area),
                                  feedrate=float(options.feedrate),
                                  offsets=offsets
                                  )