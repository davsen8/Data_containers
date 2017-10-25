#!/usr/bin/env python

'''
Created on 2017-04-12 by Jennifer Holden
@author: holdenje

NOTES:
Parses the seabird data files for header information and data

'''

####################################################################################
#import the necessary modules
####################################################################################

#import datetime
#import re
from collections import OrderedDict
import json
#import pandas as pd

class ODF_reader:
    def __init__(self, filename):
        self.filename = filename

        self.hdrdict = OrderedDict()
        self.hdrdict["ODF_HEADER"] = OrderedDict()
        self.hdrdict["CRUISE_HEADER"] = OrderedDict()
        self.hdrdict["EVENT_HEADER"] = OrderedDict()
        self.hdrdict["INSTRUMENT_HEADER"] = OrderedDict()
        self.hdrdict["QUALITY_HEADER"] = OrderedDict()
        self.hdrdict["HISTORY_HEADER"] = OrderedDict()
        self.hdrdict["HISTORY_HEADER"]["COUNT"] = 0
        self.hdrdict["PARAMETER_HEADER"] = OrderedDict()
        self.hdrdict["PARAMETER_HEADER"]["COUNT"]=0
        self.hdrdict["RECORD_HEADER"] = OrderedDict()

        self.DATA = OrderedDict()



        self.parse_text()

        self.print_text()

        self.write_JSON()


    def parse_text(self):
        with open(self.filename) as fp:

            self.endrow = 0
            current_dict = ''

            # parse through the HEADER blccks
            for line in fp:
                # stop once you hit the end of the header block
                line = line.rstrip()
                line = line.rstrip(',')
                if "-- DATA --" in line:
                    self.endrow += 1
                    break
                if line in self.hdrdict:
                    current_dict = line
#                    print "current dict = ",current_dict
                else:
#                    print "line = ",line
                    sub_parms = line.split("=")
#                    print sub_parms[0], sub_parms[1]
                    self.hdrdict[current_dict][sub_parms[0]] = sub_parms[1]


    def print_text(self):
        for i in self.hdrdict :
            for j in self.hdrdict[i]:
                    print i,j, self.hdrdict[i][j]


    def write_JSON(self):
        with open('test.JSON', 'w') as fp:
            json.dump(self.hdrdict,fp,indent=4)
#            fp.write(json.dumps(self.hdrdict),indent=4,seperators=(',',':'))
        fp.close()

    def read_JSON(self):
            try:
                with open('test.JSON', 'r') as fp:
                    testdict = json.load(fp)

                fp.close()
            except:
                pass


def main():
    #	if len(sys.argv) != 2:
    #		print "supply data file name"
    #		quit()
    #	print sys.argv , len(sys.argv)
    #	print sys.argv[0], sys.argv[1]

    #	for i in range (1 , len(sys.argv)) :
    #		datafile = sys.argv[i]
    datafile = "JSON_test\BIO\MTR_HUD2015030_1898_10588081_1800.ODF"
    hdr = ODF_reader(datafile)
    #		hdr.print_pfile_hdr()



if __name__ == "__main__":
    main()