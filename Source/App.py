#! /usr/bin/env python3

from Rasterize import rasterize

import argparse
import sys



if __name__ == '__main__' :
    
    #Setup Command line arguments
    
    parser = argparse.ArgumentParser(
        description = 'Convert bitmaps to gcode.' ,
        usage = '%(prog)s [options] input...' ,
        prog = 'image_to_gcode.py'
    )
    
    parser.add_argument(
        '-o' , '--output' ,
        default = sys.stdout ,
        help = 'Output file, defaults to stdout'
    )
    
    parser.add_argument(
        '-s' , '--spread' ,
        default = '3.175' ,
        help = 'Nozzle spread (mm). Default: %(default)s'
    )
                        
    parser.add_argument(
        '-n' , '--nozzles' ,
        default = '12' ,
        help = 'Nozzle count. Default: %(default)s'
    )
                        
    parser.add_argument(
        '-a' , '--area' ,
        default = '[200,200]' ,
        help = 'Print area in millimeters. Default: %(default)s'
    )
                        
    parser.add_argument(
        '-f' , '--feedrate' ,
        default = '1000' ,
        help = 'Print feedrate. Default: %(default)s'
    )
                        
    parser.add_argument(
        'input' ,
        help = 'input file, defaults to stdin'
    )
                        
    parser.add_argument(
        '--version' ,
        version = '%(prog)s 0.0.1-dev' ,
        action = 'version'
    )
                        
    parser.add_argument(
        '-r' , '--red' ,
        default = '[0,0]' ,
        help = 'Head offset in millimeters. Default: %(default)s'
    )
                        
    parser.add_argument(
        '-g' , '--green' ,
        default = '[30.5,0.1]' ,
        help = 'Head offset in millimeters. Default: %(default)s'
    )
                        
    parser.add_argument(
        '-b' , '--blue' ,
        default = '[0,0]' ,
        help = 'Head offset in millimeters. Default: %(default)s'
    )
                        
    parser.add_argument(
        '-k' , '--black' ,
        default = '[0,0]' ,
        help = 'Head offset in millimeters. Default: %(default)s'
    )

    
    #   Display help page by default
    
    if len(sys.argv) == 1 :
        parser.print_help()
        sys.exit(0)
        
        
    options = parser \
        .parse_args()
        
    rasterize(options)
