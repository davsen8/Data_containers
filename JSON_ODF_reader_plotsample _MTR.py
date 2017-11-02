'''
Created on 2017-10-26 by Dave Senciall
@author: DSenciall

NOTES:
coded for python 3.x : the panda's to_xx functions dont seem to be present in the anancoda 2.7 for some
bizzare reason even though they are part of pandas since pandas 0.17

'''

import datetime
#import re
from collections import OrderedDict
import json
import pandas as pd
import matplotlib.pyplot as pyplot


def read_JSON(afile):
    jdict = OrderedDict()
    try:
        with open(afile, 'r') as fp:
            jdict = json.load(fp)

        fp.close()
    except:
        pass
    return (jdict)

def print_text(adict):
        for i in adict :
            for j in adict[i]:
                if not isinstance(j, list):
                    print (i,j, adict[i][j])
                else:
#                    for k  in j:
                        print (j)


def main():

# reasd JSON file that has encode ODF

    hdr = read_JSON("MTR_HUD2015030_1898_10588081_1800_ODF.json")


# demo of accessing a header element value
    print (hdr["RECORD_HEADER"],hdr["RECORD_HEADER"]["NUM_CYCLE"])

# get the data block (list of lists)	
    data = hdr["DATA"]

# coerce it to a pandas data frame
    pd_data = pd.DataFrame(data)

# label the channels (technicall you could pull the channel ids fromt he parameters blocks)	
    pd_data.columns=['DateTime','Temp']

# set the data types for the columns
    pd_data['DateTime']= pd.to_datetime(pd_data['DateTime'],format='%d-%b-%Y %H:%M:%S.00')
    pd_data["Temp"] = pd.to_numeric(pd_data["Temp"])

#plot the data
    pd_data.plot(x='DateTime',y='Temp',title='BIO HOBO demo')
    pyplot.show()




if __name__ == "__main__":
    main()