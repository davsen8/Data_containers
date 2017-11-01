

import datetime
#import re
from collections import OrderedDict
import json
import pandas as pd
import matplotlib.pyplot as pyplot


def read_JSON(afile):
    testdict = OrderedDict()
    try:
        with open(afile, 'r') as fp:
            testdict = json.load(fp)

        fp.close()
    except:
        pass
    return (testdict)

def print_text(adict):
        for i in adict :
            for j in adict[i]:
                if not isinstance(j, list):
                    print (i,j, adict[i][j])
                else:
#                    for k  in j:
                        print (j)


def main():
    #	if len(sys.argv) != 2:
    #		print "supply data file name"
    #		quit()
    #	print sys.argv , len(sys.argv)
    #	print sys.argv[0], sys.argv[1]

    #	for i in range (1 , len(sys.argv)) :
    #		datafile = sys.argv[i]
#    datafile = "JSON_test\BIO\MTR_HUD2015030_1898_10588081_1800.ODF"
#    datafile = "JSON_test\BIO\MTR_HUD2015030_1898_10588081_1800.ODF"
#    hdr = ODF_reader(datafile)

    hdr = read_JSON("MTR_HUD2015030_1898_10588081_1800_ODF.json")
    data = hdr["DATA"]

    pd_data = pd.DataFrame(data)
    pd_data.columns=['DateTime','Temp']
    pd_data['DateTime']= pd.to_datetime(pd_data['DateTime'],format='%d-%b-%Y %H:%M:%S.00')
    pd_data["Temp"] = pd.to_numeric(pd_data["Temp"])

#    print (pd_data)             # print the data fran\me contents

    pd_data.plot(x='DateTime',y='Temp',title='BIO HOBO demo')
    pyplot.show()

#    print_text(hdr)             # print dictionary returned from JSON file

#    print (pd_data.head(2))    # print first 2 rows

    #		hdr.print_pfile_hdr()

    print (hdr["RECORD_HEADER"],hdr["RECORD_HEADER"]["NUM_CYCLE"])



if __name__ == "__main__":
    main()