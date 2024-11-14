#!/usr/bin/env python

# ****************************
# palfa_single_pulse_viewer.py
# ****************************
#
# Original code written by Anne Archibald (McGill University) 
# Modified by Patrick Lazarus (McGill University) to work with PALFA data
# 20090215: Modified and commented by Matthew Jaffee (F&M '10) and Froney Crawford
# 20090518: Modified by M. Jaffee to include uppercase 'P' project name (P2030)
#
# The following is a python script to call up singlepulse.ps.gz files,
# display them one by one, and allow the user to assign a rating
# through the command line
#
# Rating scheme:
# 1 - indicates an excellent candidate
# 2 - indicates a possible candidate (interesting, worth keeping)
# 3 - indicates junk or nothing of interest
#
# Two files are created in the results directory in which the singlepulse file resides:
# singlepulse-viewed(username) is an empty file which indicates that file was viewed
# rating(username) is a file which contains a number (1,2, or 3) which indicates the rating
# username in each of the preceding lines is the string obtained from os.getlogin()
# if the user who rated a file was called pulsar, the rating file would be called rating(pulsar)
#


import os 
import glob 
import sys

from PALFA_config import *

viewed = 0      # keeps track of the total number of files viewed by this script
this_time = 0   # keeps track of the total number of files viewed in this session
username = os.getlogin()  # gets the username for use in creation of rating and viewed files

# beams is a list of all directories which may contain single pulse files
beams = sorted(glob.glob(os.path.join(final_dir, "../*/*/p1944*G*/*/*/"))+glob.glob(os.path.join(final_dir, "../*/*/p2030*G*/*/*/"))+glob.glob(os.path.join(final_dir, "../*/*/P1944*G*/*/*/"))+glob.glob(os.path.join(final_dir, "../*/*/P2030*G*/*/*/")))

# print out the total number of directories (the number of elements in beams)
print "Total beams:\t%d" % len(beams)

# the remainder of the code looks at each directory in beams succesively
for d in beams: 
    try:
        vfn = os.path.join(d,"singlepulse-viewed(%s)" % username)
        # if there is a file called singlepulse-viewed(username) in the directory, it will be skipped over and counted as viewed
        if os.path.exists(vfn):
            print "singlepulse file at %s already viewed" % d
            viewed += 1
        else:
            # spf is a list of all the singlepulse files in the current directory in beams
            spf = glob.glob(os.path.join(d,"*singlepulse.ps.gz"))
            if not spf: # if there are no singlepulse files in the current directory
                print "WARNING: singlepulse ps files missing from %s" % d
                continue
            # looking at each of the single pulse files one by one (there should only be one)
            for f in spf:
                print "\nNow viewing... %s" % f
                print "Enter a rating, 'q' to quit, or '?' to leave unviewed"
                os.system("gv -geometry +0+0 %s" % f) # pulls up the plot
                r = sys.stdin.readline() # prompts the user for input
                try:
                    n = int(r) # if r is not a number this will go straight to except
                    h = open(os.path.join(d,"rating(%s)" % username),"wt") # creates a file called rating(username)
                    h.write("%s\n" % r) # writes the rating entered by the user into the rating file
                    h.close()
                    g = open(vfn,"wt") # creates the file called singlepulse-viewed(username) to denote that this directory has been viewed
                    g.close()
                    this_time += 1
                    print "marked %s interesting, rating %d" % (d,n)
                except ValueError:# this block is executed if the value entered above is not a number
                    if 'q' in r: # entering a 'q' will quit the program
                        print "Quitting."
                        sys.exit(0)# throws an exception kicking us to the outer except block where sys.exit(0) is called again
                    else: # anything other than a number or q entered for r just leaves the file "unviewed"
                        pass

    except SystemExit:
        sys.exit(0)
 
    except:
	print "Error with %s" % d # any other exception thrown in the above try block will print this error message containing the directory where the error was encountered
	
    print "Total:\t%d\tPrevious:\t%d\tViewed:\t%d" % (len(beams),viewed,this_time) # prints the total number of beams, the total number viewed, and the number viewed this session
    



