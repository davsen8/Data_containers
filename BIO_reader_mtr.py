#!/usr/bin/env python


'''
Created on 2017-10-26 by Dave Senciall
@author: DSenciall

NOTES:
coded for python 3.x    the panda's to_xx functions dont seem to be present in the anancoda 2.7 for some
bizzare reason even though the they are part o\pandas since pandas 0.17

'''

#NOTE THIS COPY HAS PIPE_TIME SET TO TRUE TO HANDLE THE HOBO MTR TEST FILE
####################################################################################
#import the necessary modules
####################################################################################

import datetime

from collections import OrderedDict
import json
import pandas as pd
import matplotlib.pyplot as pyplot

class ODF_reader():


    def __init__(self, filename):
        self.filename = filename

        # i'm pre declaring the dictionaies to ensure they are ordered dicts..
        # this is only to ensure things stay in original order...
        # I havent decided if this is raelly needed yet
        # also the ones that a multile like HSITORY need to have an hierachy

        # this is not a complete list of posible ODF heders...

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
        self.hdrdict["DATA"] = list()

        self.parse_text()

#        self.print_text()



# please don't 'judge' this code,, it is a proof of concept test to get the data read in..
    def parse_text(self):

        linelist = list()

        with open(self.filename) as fp:

#            self.endrow = 0
            current_dict = ''
            buf =""
            line = ''
            # parse through the HEADER blccks ; blocks terminate by NOT have a trailing comma
            while True:


                try:
                    line = fp.readline()
                except:
                    break

                # if we've reached the data block
                # else we are still crawling over headers
                if "-- DATA --" in line:
                    n = 0
                    while True:
                        try:
                            line = fp.readline()
                            line = line.rstrip()
                            Pipe_time = True

                            # this is a bit of jam in to handle the issue of the pipe time stamp getting split on its
                            # enbedded blank and the 2 resultant date time elements have dangling quotes... ugg
                            if (Pipe_time):

                                line = line.replace ('\'',' ') #BIO VMS timestamp gets splip, but the quote cases an issue
                                linelist = line.split()
                                dt = linelist[0]+' '+linelist[1]
                                del linelist[1]
                                linelist[0] = dt


                        except:
                            return

                        if line =='':
#                            print "BUG OUT EOF"
                            return

                        n=n+1


# if we want to write the numbers without the quotes... R seems to have an issue picking that up
# at the moment so for now I'm letting the outn as strings..
#                        for index,item in enumerate(linelist):
#                            if not (Pipe_time and index ==0):
#                                  linelist[index] = float(item)

                        self.hdrdict["DATA"].append(linelist)


                line = line.rstrip()
                line = line.rstrip(',')

                # a new header block start found
                if line in self.hdrdict:
                    current_dict = line

                else:   # HISTORY AND PARAMETERS  and POLYNOMIAL are multi occurent
                    if current_dict == "HISTORY_HEADER":
                        self.hdrdict["HISTORY_HEADER"][self.hdrdict["HISTORY_HEADER"]["COUNT"]] = OrderedDict()
                        line = line.rstrip()

                        self.hdrdict["HISTORY_HEADER"][self.hdrdict["HISTORY_HEADER"]["COUNT"]][0] = line.lstrip()
                        n=1
                        line = fp.readline()
                        line = line.rstrip()
                        while line[-1:] ==',':    # a missing comma means end of block

                            self.hdrdict["HISTORY_HEADER"][self.hdrdict["HISTORY_HEADER"]["COUNT"]][n] = line.lstrip()
                            n = n +1
                            try:
                                line = fp.readline()
                                line = line.rstrip()
                            except:
                                break

                        self.hdrdict["HISTORY_HEADER"][self.hdrdict["HISTORY_HEADER"]["COUNT"]][n] = line.lstrip()
                        self.hdrdict["HISTORY_HEADER"]["COUNT"] = self.hdrdict["HISTORY_HEADER"]["COUNT"] + 1

                        current_dict = ''

                    elif current_dict == "PARAMETER_HEADER":

                        self.hdrdict["PARAMETER_HEADER"][self.hdrdict["PARAMETER_HEADER"]["COUNT"]] = OrderedDict()
                        line = line.rstrip()
                        sub_parms = line.split("=")

                        self.hdrdict["PARAMETER_HEADER"][self.hdrdict["PARAMETER_HEADER"]["COUNT"]][sub_parms[0].lstrip()] = sub_parms[1]

                        line = fp.readline()
                        line = line.rstrip()
                        print ("LINES=", line[-1:])
                        while line[-1:] == ',':
                            line = line.rstrip(',')
                            sub_parms = line.split("=")
                            self.hdrdict["PARAMETER_HEADER"][self.hdrdict["PARAMETER_HEADER"]["COUNT"]][sub_parms[0].lstrip()] = sub_parms[1]

                            try:
                                line = fp.readline()
                                line = line.rstrip()
                            except:
                                break

                        line = line.rstrip(',')
                        sub_parms = line.split("=")
                        self.hdrdict["PARAMETER_HEADER"][self.hdrdict["PARAMETER_HEADER"]["COUNT"]][sub_parms[0].lstrip()] = sub_parms[1]
                        self.hdrdict["PARAMETER_HEADER"]["COUNT"] = self.hdrdict["PARAMETER_HEADER"]["COUNT"] + 1
                        current_dict = ''
                    else:
                        sub_parms = line.split("=")
                        self.hdrdict[current_dict][sub_parms[0].lstrip()] = sub_parms[1]

        def print_text(adict):
            for i in adict:
                for j in adict[i]:
                    if not isinstance(j, list):
                        print(i, j, adict[i][j])
                    else:
                        #                    for k  in j:
                        print(j)


    def write_JSON(self,afile):
        with open(afile, 'w') as fp:
            json.dump(self.hdrdict,fp,indent=4)
        fp.close()



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

    hdr.write_JSON('MTR_HUD2015030_1898_10588081_1800_ODF.json')

# and lets do a quick plot to show that we can get the  data from the dictionaries
    data = hdr.hdrdict["DATA"]

    pd_data = pd.DataFrame(data)
    pd_data.columns=['DateTime','Temp']
    pd_data['DateTime']= pd.to_datetime(pd_data['DateTime'],format='%d-%b-%Y %H:%M:%S.00')
    pd_data["Temp"] = pd.to_numeric(pd_data["Temp"])
    print (pd_data)
    pd_data.plot(x='DateTime',y='Temp',title='BIO HOBO demo')
    pyplot.show()


if __name__ == "__main__":
    main()