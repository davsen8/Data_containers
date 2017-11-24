#!/usr/bin/env python

'''
Created on 2017-10-26 by Dave Senciall
@author: DSenciall

NOTES:
coded for python 3.x    the panda's to_xx functions dont seem to be present in the anancoda 2.7 for some
bizzare reason even though the they are part o\pandas since pandas 0.17

'''

#NOTE THIS COPY HAS PIPE_TIME SET TO FALSE TO HANDLE THE CTD TEST FILE
#
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


        self.hdrdict["ODF_HEADER"] = OrderedDict()    # OBLIGATORY

        self.hdrdict["CRUISE_HEADER"] = OrderedDict()  # OBLIGATORY

        self.hdrdict["EVENT_HEADER"] = OrderedDict()   # OBLIGATORY

        self.hdrdict["METRO_HEADER"] = OrderedDict()

        self.hdrdict["INSTRUMENT_HEADER"] = OrderedDict()

        self.hdrdict["QUALITY_HEADER"] = OrderedDict()          # single but sub-elements can repeat

        self.hdrdict["GENERAL_CAL_HEADER"] = OrderedDict()      # multi
        self.hdrdict["GENERAL_CAL_HEADER"]["COUNT"]=0


        self.hdrdict["POLYNOMIAL_CAL_HEADER"] = OrderedDict()   # multi
        self.hdrdict["POLYNOMIAL_CAL_HEADER"]["COUNT"]=0

        self.hdrdict["COMPASS_CAL_HEADER"] = OrderedDict()      # multi
        self.hdrdict["COMPASS_CAL_HEADER"]["COUNT"]=0

        self.hdrdict["HISTORY_HEADER"] = OrderedDict()          # multi
        self.hdrdict["HISTORY_HEADER"]["COUNT"] = 0

        self.hdrdict["PARAMETER_HEADER"] = OrderedDict()        # multi  OBLIGATORY
        self.hdrdict["PARAMETER_HEADER"]["COUNT"]=0

        self.hdrdict["RECORD_HEADER"] = OrderedDict()           # OBLIGATORY
        self.hdrdict["DATA"] = list()                           # -- DATA --   OBLIGATORY

        self.time_channel = -1
        self.channels = list()

        self.parse_text()

#        self.print_text()


# please don't 'judge' this code,, it is a proof of concept test to get the data read in..
    def parse_text(self):
        linelist = list()
        with open(self.filename) as fp:

            self.endrow = 0
            current_dict = ''
            buf =""
            line = ''
            # parse through the HEADER blccks
            while True:

                try:
                    line = fp.readline()
                except:
                    break

                # if we've reached the data block
                # else we are still crawkling over headers
                if "-- DATA --" in line:
                    n = 0
                    # this is a bit of jam in to handle the issue of the pipe time stamp getting split on its
                    # enbedded blank and the 2 resultant date time elements have dangling quotes... ugg
                    if "SYTM_01" in self.channels :
                        self.time_channel = self.channels.index("'SYTM_01'")
                        Pipe_time = True
                        print ("time detected")
                    else :
                        Pipe_time = False

                    while True:
                        try:
                            line = fp.readline()
                            line = line.rstrip()

                            if (Pipe_time):
                                line = line.replace ('\'',' ') #BIO VMS timestamp gets split, but the quote cases an issue
                                linelist = line.split()
                                dt = linelist[self.time_channel]+' '+linelist[self.time_channel+1]
                                del linelist[self.time_channel]
                                linelist[self.time_channel] = dt

                            else:
                                linelist = line.split()
                        except:
                            return

                        if line =='':
#                            print "BUG OUT EOF"
                            return

                        n=n+1
                        for index,item in enumerate(linelist):
                            if index != self.time_channel:
                                linelist[index] = float(item)

                        self.hdrdict["DATA"].append(linelist)


                line = line.rstrip()
                line = line.rstrip(',')

                if line in self.hdrdict:
                    current_dict = line

                else:
                    if current_dict == "HISTORY_HEADER":
                        self.hdrdict["HISTORY_HEADER"][self.hdrdict["HISTORY_HEADER"]["COUNT"]] = OrderedDict()
                        line = line.rstrip()

                        self.hdrdict["HISTORY_HEADER"][self.hdrdict["HISTORY_HEADER"]["COUNT"]][0] = line.lstrip()
                        n=1
                        line = fp.readline()
                        line = line.rstrip()
                        while line[-1:] ==',':

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

                        self.channels.append (self.hdrdict["PARAMETER_HEADER"][self.hdrdict["PARAMETER_HEADER"]["COUNT"]]["CODE"])

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


    def write_JSON(self):
        with open('CTD_BCD2016666_001_01_DN_test.json', 'w') as fp:
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



    datafile = "JSON_test\BIO\CTD_BCD2016666_001_01_DN.ODF"
#    datafile = "JSON_test\BIO\MCM_HUD2013021_1841_0563_3600.ODF"
#    datafile = "JSON_test\BIO\CTD_BCD20155666_007_01_UP.ODF"

    hdr = ODF_reader(datafile)

    print (hdr.channels)

    hdr.write_JSON()

    data = hdr.hdrdict["DATA"]

    pd_data = pd.DataFrame(data)

#    pd_data.columns=['cntrl','cntr-f','Pres','Press_f','Temp','Temp_f']
#    pd_data['DateTime']= pd.to_datetime(pd_data['DateTime'],format='%d-%b-%Y %H:%M:%S.00')



    pd_data["PRES"] = pd.to_numeric(pd_data[hdr.channels.index("'PRES_01'")])
    pd_data.loc[:,"PRES"] *=-1
    pd_data["TEMP"] = pd.to_numeric(pd_data[hdr.channels.index("'TEMP_01'")])
#    print (pd_data)
    pd_data.plot(x='TEMP',y='PRES',title='BIO CTD demo')
    pyplot.show()


if __name__ == "__main__":
    main()