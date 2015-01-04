# Open the image given its path and store it in the variable 'image'
import sys
import os
import argparse

from ij import IJ
from util import RGB_to_Luminance
from ini.trakem2.imaging.filters import CLAHE
from ij.io import FileSaver

def action(filename, outname, fast=1, blocksize=70, grad=3):
        sys.stdout.write(str(filename))
        if verbose:
                print " "
                print "(fast, blocksize, grad) "+str((fast,blocksize,grad))

        if verbose:
                print "Opening image.."
        image = IJ.openImage(filename)
        if verbose:
                print "..done"
	
        if verbose:
                print "Converting to Luminance"
        im_lum = RGB_to_Luminance.convertToLuminance(image)
        #im_lum.show()
        if verbose:
                print "..done"
        
        if verbose:
                print "Obtaining ip.."
        ip = im_lum.getProcessor()
        if verbose:
                print "..done"
        
        if verbose:
                print "Applying CLAHE.."
        ip2=CLAHE(fast,blocksize,256, grad).process(ip)
        if verbose:
                print "..done"
        
        #im_lum.updateAndDraw()
        
        if verbose:
                print "Saving file "+outname+"  .."
        fs=FileSaver(im_lum)
        fs.saveAsTiff(outname)

        print "  ..done"
                

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("workdir", help="path of a directory containing the files that will be processed")
        parser.add_argument("-f", "--fast", help="Performa a fast CLAHE (less precise)", action="store_true")
        parser.add_argument("-b", "--blocksize", help="local block size (default:70)", default=70,type=int)
        parser.add_argument("-g", "--gradientlim", help="local contrast gradient limit (default:3)", default=3,type=float)
        parser.add_argument("-v", "--verbose", help="Increase verbosity", action="store_true")
        if len(sys.argv)==1:
                parser.print_help()
                sys.exit(1)
        args = parser.parse_args()
        
        workdir=args.workdir
        fast=int(args.fast)
        blocksize=args.blocksize
        grad=args.gradientlim
        verbose=args.verbose
        if verbose:
                print "Working directory: "+workdir

        for filename in sorted(os.listdir(workdir)):
                
                outname="CLAHE-"+str(fast)+"_"+str(blocksize)+"_"+str(grad)+"-"+filename+".tif"                
                action(workdir+"/"+filename, workdir+"/"+outname, fast, blocksize, grad)

        

				
	# then display it.
	#image.show()
 
 
