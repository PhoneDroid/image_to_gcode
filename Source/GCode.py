
from __future__ import  \
    unicode_literals ,  \
    absolute_import ,   \
    print_function ,    \
    division 

import termcolor
import copy
import cv2
import os


Orange = ( 0 , 152 , 255 )
White = ( 255 , 255 , 255 )
Green = ( 0 , 255 , 0 )
Black = ( 0 , 0 , 0 )
Red = ( 0 , 0 , 255 )


ignore_color = White


class ImageToGcode () :
    
    def __init__(
        self , img , spread , nozzles , area ,
        feedrate , offsets , verbose = False
    ):
        
        self.increment = spread / nozzles
        self.printArea = area
        self.feedrate = feedrate
        self.outFile = os.path.splitext(os.path.abspath(img))[0] + '.gco'
        self.nozzles = int(nozzles)
        self.output = ''
        self.spread = spread
        self.img = cv2.imread(img)
        
        self.orange = Orange
        self.white = White
        self.black = Black
        self.green = Green
        self.red = Red
        
        self.offsets = offsets
        
        self.debug_to_terminal()
        self.make_gcode()
        

    def make_gcode ( self ):
        
        # Start Fan
        
        self.output = 'M106\n'
        
        shape = self.img.shape
        
        nozzleFirings = [ 0 for x in range(0,shape[1]) ]
        nozzleFirings = [ copy.copy(nozzleFirings) for x in range(0,self.nozzles) ]
        
        scan = range(0,shape[0])
        scan = reversed(scan)
        
        colors = [ self.red , self.orange , self.green , self.black ]
        
        for y in scan :
            
            for x in range(0,self.img.shape[1]) :
                
                color = tuple(self.img[y,x])
               
                if color == ignore_color:
                    continue
                    
                try:
                    
                    nozzle = colors.index(color)
                    
                    nozzleFirings[nozzle][x] \
                        += 1 << y % self.nozzles
                        
                except:
                    continue
                    
                    
            if ( y % self.nozzles != 0 ) or ( y < 1 ) :
                continue
                
            for head , fires in enumerate(nozzleFirings) :
                for column , fire in enumerate(fires) :
                    
                    if not fire :
                        continue
                    
                    offset = self.offsets[head]
                    
                    X = str( self.increment * column - offset[0] )
                    Y = str( y / 12 * self.spread - offset[1] )
                    
                    self.output +=                                                  \
                        'G1 X' + X + ' Y' + Y + ' F' + str(self.feedrate) + '\n' +  \
                        'M400\n' +                                                  \
                        'M700 P' + str(head) + ' S' + str(fire) + '\n'

            nozzleFirings = [ 0 for x in range(0,shape[1]) ]
            nozzleFirings = [ copy.copy(nozzleFirings) for x in range(0,4) ]

        file = open(self.outFile,'w')
        file.write(self.output)
        file.close()


    def debug_to_terminal ( self ):
        
        shape = self.img.shape
        
        print('Rows: ' + str(shape[0]))
        print('Cols: ' + str(shape[1]))
        print('Spread: ' + str(self.spread) + 'mm')
        print('Nozzles: ' + str(self.nozzles))
        print('Print Area: ' + str(self.printArea) + 'mm')
        
        rowStr = ''
        
        for y in range(0,shape[0]) :
            
            rowStr = ''
            
            for x in range(0,shape[1]) :
                
                color = tuple(self.img[y,x])
                
                if color == self.red:
                    rowStr += termcolor.colored(' ','red','on_red')
                if color == self.green:
                    rowStr += termcolor.colored(' ','green','on_green')
                elif color == self.white:
                    rowStr += termcolor.colored(' ','white','on_white')
                elif color == self.orange:
                    rowStr += termcolor.colored(' ','yellow','on_yellow')
                elif color == self.black:
                    rowStr += ' '
                else:
                    rowStr += termcolor.colored(' ','white','on_white')
                    
            # print(rowStr)