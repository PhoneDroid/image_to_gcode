
from __future__ import  \
    unicode_literals ,  \
    absolute_import ,   \
    print_function ,    \
    division 

import termcolor
import copy
import cv2
import os



White = ( 255 , 255 , 255 )

ignore_color = White


#+- this color to be registered - might be needed due to compression alg

color_threshold = 10



class ImageToGcode():
    def __init__(self,
                 img,
                 spread,
                 nozzles,
                 area,
                 feedrate,
                 offsets,
                 verbose=False):
        self.img = cv2.imread(img)
        self.output = ""
        self.outFile = os.path.splitext(os.path.abspath(img))[0] + ".gco"
        self.spread = spread
        self.nozzles = int(nozzles)
        self.increment = spread/nozzles
        self.printArea = area
        self.feedrate = feedrate
        #change colors to sauces here
        self.red = (0, 0, 255)
        self.orange = (0, 152, 255)
        self.white = (255, 255, 255)
        self.black =(0, 0, 0)
        self.green = (0, 255, 0)
        self.offsets = offsets
        self.debug_to_terminal()
        self.make_gcode()

    def make_gcode(self):
        self.output = "M106\n"  # Start Fan
        nozzleFirings = [0 for x in range(0, self.img.shape[1])]
        nozzleFirings = [copy.copy(nozzleFirings) for x in range(0, self.nozzles)]
        scan = range(0, self.img.shape[0])
        scan = reversed(scan)
        for y in scan:
            for x in range(0, self.img.shape[1]):
                color = tuple(self.img[y, x])
               
                if color == ignore_color:
                    pass
                elif color == self.red:
                    nozzleFirings[0][x] += 1 << y % self.nozzles
                elif color == self.orange:
                    nozzleFirings[1][x] += 1 << y % self.nozzles
                elif color == self.green:
                    nozzleFirings[2][x] += 1 << y % self.nozzles
                elif color == self.black:
                    nozzleFirings[3][x] += 1 << y % self.nozzles
                else:
                    pass
            if y % self.nozzles == 0 and y > 0:
                for headNumber, headVals in enumerate(nozzleFirings):
                    for column, firingVal in enumerate(headVals):
                        if firingVal:
                            currentOffset = self.offsets[headNumber]
                            self.output += "G1 X"+str(self.increment*column-currentOffset[0])+" Y"+str(y/12*self.spread-currentOffset[1])+" F"+str(self.feedrate)+"\n"
                            self.output += "M400\n"
                            self.output += "M700 P"+str(headNumber)+" S"+str(firingVal)+"\n"
                #print(str(nozzleFirings))
                nozzleFirings = [0 for x in range(0, self.img.shape[1])]
                nozzleFirings = [copy.copy(nozzleFirings) for x in range(0, 4)]
        f = open(self.outFile, 'w')
        f.write(self.output)
        f.close()
        #print(self.output)

    def debug_to_terminal(self):
        print("Rows: "+str(self.img.shape[0]))
        print("Cols: "+str(self.img.shape[1]))
        print("Spread: "+str(self.spread)+"mm")
        print("Nozzles: "+str(self.nozzles))
        print("Print Area: "+str(self.printArea)+"mm")
        rowStr = ""
        for y in range(0, self.img.shape[0]):
            rowStr = ""
            for x in range(0, self.img.shape[1]):
                color = tuple(self.img[y, x])
                #print(color)
                #print(self.red)
                if color == self.red:
                    rowStr += termcolor.colored(" ", 'red', 'on_red')
                if color == self.green:
                    rowStr += termcolor.colored(" ", 'green', 'on_green')
                elif color == self.white:
                    rowStr += termcolor.colored(" ", 'white', 'on_white')
                elif color == self.orange:
                    rowStr += termcolor.colored(" ", 'yellow', 'on_yellow')
                elif color == self.black:
                    rowStr += " "
                else:
                    # print(color)
                    rowStr += termcolor.colored(" ", 'white', 'on_white')
            # print(rowStr)