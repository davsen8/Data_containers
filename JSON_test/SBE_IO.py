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

import datetime
import re
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width',1000)

#parse the file
class SBEIO:

    def __init__(self,filename):
        self.filename = filename
        self.parse_text()
        self.parse_xml()
#        self.parse_data()

    #read each header line. If it's in the first part add it to a dictionary.
    #When it hits the <sensors> part, add it to a string. Parse this part later with xml parser if necessary
    def parse_text(self):

        with open(self.filename) as fp:
            self.hdrdict = {}
            xmlstr = []
            self.endrow = 0
            for line in fp:
                #stop once you hit the end of the header block
                if "*END*" in line:
                    self.endrow += 1
                    break
                #put the non-xml stuff into a dictionary
                elif "<" not in line:
                    self.endrow += 1
                    dictsplit = re.split('[=:]',line,1)
                    #If there's two entries, add them to a dictionary. If there's just one, ignore it.
                    if len(dictsplit)>1:
                        #remove the leading characters, \n, and trailing whitespace
                        if dictsplit[0].startswith('**'):
							front = dictsplit[0].split()
							dictsplit[0] = front[1]
                        ent1 = dictsplit[0].replace('# ','').replace('** ','').replace('* ','').rstrip()
                        ent1 = re.sub(' \(S[0-9][0-9][0-9][0-9]\)','', ent1)
                        ent1 = re.sub(' \( S[0-9][0-9][0-9][0-9] \)', '', ent1)
                        ent2 = dictsplit[1].replace('\n','').rstrip()
                        self.hdrdict[ent1] = ent2.lstrip();
                #the xml part will go into a string to be parsed later
                elif "<" in line:
                    self.endrow += 1
                    #xmlstr.append(re.sub(r"PROCESS='#([^']*)',", r'\1', line)) #eventually something like this for ODF
                    xmlstr.append(line.replace('# ',''))
            self.xmlstr = ''.join(xmlstr)
            #convert the date/time format

            for1 = '%b %d %Y %H:%M:%S'
            for2 = '%Y-%m-%d %H:%M:%S'
	    self.hdrdict['System UpLoad Time'] = datetime.datetime.strptime(self.hdrdict['System UpLoad Time'], for1).strftime(for2)
	    self.hdrdict['Deploy Time'] = datetime.datetime.strptime(self.hdrdict['System UpLoad Time'], for2)
#	    print int (self.hdrdict['span 0'].split(',')[1])/24
	    self.hdrdict['Recovered Time'] = self.hdrdict['Deploy Time'] +  datetime.timedelta(seconds= (int (self.hdrdict['span 0'].split(',')[1])/24))
		#		self.hdrdict['Recovered Time'] = self.hdrdict['Deploy Time'] +  datetime.timedelta(seconds= int(self.hdrdict['span 0'].split(',')[1])/24)))

    def print_pfile_hdr(self):
        #fix self.hdrdict['System UpLoad Time'] so that the format is '2016-07-17 02:26:04'
        #probe type needs to use a regular expression
        print " "
        print self.hdrdict['VESSEL/TRIP/SEQ'], self.hdrdict['LATITUDE'], ''.join(['-',(self.hdrdict['LONGITUDE']).lstrip()]), \
            self.hdrdict['System UpLoad Time'], self.hdrdict['SOUNDING'], self.hdrdict['PROBE'], \
            self.hdrdict['CTD'], "FORMAT?", self.hdrdict['COMMENTS']
        print " "


    def parse_xml(self):
        import xml.etree.ElementTree as ET
        root = ET.fromstring(self.xmlstr)
        #These are the main entries
        self.channum = []; self.channame = []; self.sernum = []; self.caldate = [];
        self.totnumsens = root.attrib['count']
        for channel in root.findall('sensor'):
            if len(channel) == 0:
                self.channum.append(channel.attrib['Channel'])
                self.channame.append("None")
                self.sernum.append("None")
                self.caldate.append("None")
            else:
                self.channum.append(channel.attrib['Channel'])
                for sensor in channel:
                    self.channame.append(sensor.tag)
                    self.sernum.append(sensor.findall('SerialNumber')[0].text)
                    self.caldate.append(sensor.findall('CalibrationDate')[0].text)

        '''
        #EXAMPLE: get the oxygen calibration constants
        self.oxy1 = {'placement': 'primary', 'type': 'oxygen'}
        self.oxy2 = {'placement': 'secondary', 'type': 'oxygen'}; cou = 0
        for channel in root.findall('sensor/OxygenSensor'):
            for sensor1 in channel.findall('CalibrationDate'):
                cou = cou+1
                if cou == 1:
                    self.oxy1[sensor1.tag] = sensor1.text
                else:
                    self.oxy2[sensor1.tag] = sensor1.text
            for sensor in channel.findall('SerialNumber'):
                #cou = cou+1
                if cou == 1:
                    self.oxy1[sensor.tag] = sensor.text
                else:
                    self.oxy2[sensor.tag] = sensor.text
            for sensor in channel.findall('CalibrationCoefficients'):
                if sensor.attrib['equation'] == '1':
                    for parameter in sensor:
                        if cou == 1:
                            self.oxy1[parameter.tag] = parameter.text
                        else:
                            self.oxy2[parameter.tag] = parameter.text
        '''


    #function to add data to variables
    #the data contains: Sal00, Par, Upoly0, Scan, Sbeox0V, Sbeox1V, FlECO-AFL, Sal11, Sbeox1ML/L,
    #PrDM, OxsatML/L, Sigma-t11, C1S/m, T090C, T190C, Ph, Sbeox0ML/L, C0S/m, Sigma-t00
    def parse_data(self):
        self.df = pd.read_csv(self.filename, header=self.endrow, na_values=[-999], delim_whitespace=True)


#test = SBEIO('C:/ctd/QualityControlSampleData/39160073.sbe')
#test.print_pfile_hdr()

#print test.df.head()
