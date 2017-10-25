
import sys
import datetime
from SBE_IO import SBEIO 

'''
 print a elog block based on an NAFC header insert stored in an SBEIO object
 needs to look like this

$@MID@$: 1
Date: Sun, 20 Sep 2015 13:00:24 -0300
Reply to: 2
Event: 001
Station: HL_00
Instrument: CTD
Attached: Par | SBE35 | pH
Flowmeter Start: 
Flowmeter End: 
Action: Deployed
Sounding: 75
Sample ID: 0
End_Sample_ID: 24
Wire out: 
Wire Angle: 
Depth: 
Author: HebertD
IMEI_No: 
S/N: 
Wind Speed and Direction: 
Name: 
Comment: 
Time|Position: 2015-09-20 | 160021.00 | 44 41.6318 N | 63 38.4466 W
Cruise: HUD2015030
PI: D. Hebert
Protocol: AZMP
Platform: CCGS Hudson
Revisions: 
Attachment: 
Encoding: plain
========================================
'''
class Write_elog:
	def __init__(self,PI):
		self.elogdict = {}
		self.MID=1
		self.elogdict["PI"] =PI

	def __call__ (self,hdr,event):
		self.hdr = hdr
		self.event = event
		Action = "DEPLOYED"
		self.make_elog(Action)
		self.print_elog()
		self.MID+=1

		Action = "RECOVERED"
		self.make_elog(Action)
		self.print_elog()
		self.MID+=1
		
		print '|'+self.hdr.hdrdict['VNET']+'|'
		if self.hdr.hdrdict['VNET']  == 'Y':
			print 'net tow as well'


	def ship_is(self,x):
		return {
			'39': 'CCGS TELEOST',
			'20': 'CGGS HUDSON',
			'10': 'CCGS WIFRED TEMPLEMAN',
			'12': 'CCGS ALFRED NEEDLER',
		}[x]
			
		
	def make_elog(self,Action):
				self.elogdict["MID"] = self.MID
				if Action == 'DEPLOYED':
					self.elogdict["Date"] =self.hdr.hdrdict['Deploy Time'].strftime('%a, %d %b %Y %H:%M:%S -0000')
				else:
					self.elogdict["Date"] =self.hdr.hdrdict['Recovered Time'].strftime('%a, %d %b %Y %H:%M:%S -0000')
				self.elogdict["Reply"] = "000"
				self.elogdict["Event"] = self.event
				self.elogdict["Station"] = self.hdr.hdrdict["COMMENTS"].split()[0]
				self.elogdict["Instrument"] = "CTD"
				self.elogdict["Attached"] = "Par | SBE35 | pH"
				self.elogdict["Flow S"] = ""
				self.elogdict["Flow E"] = ""
				self.elogdict["Action"] = Action
				self.elogdict["Sounding"] = self.hdr.hdrdict["SOUNDING"]
				self.elogdict["Sample ID"] = self.hdr.hdrdict["STICKERS"].split()[0]
				self.elogdict["End_Sample_ID"] = self.hdr.hdrdict["STICKERS"].split()[2]
				self.elogdict["Wire out"] = ""
				self.elogdict["Wire Angle"] = ""
				self.elogdict["Depth"] = ""
				self.elogdict["Author"] = "unspecified"
				self.elogdict["IMEI_No"] = ""
				self.elogdict["S/N"] = self.hdr.hdrdict["PROBE"]
				self.elogdict["Wind"] = ""
				self.elogdict["Name"] = ""
				self.elogdict["Comments"] = self.hdr.hdrdict["COMMENTS"]
				if (Action == 'DEPLOYED`'):
					tp = self.hdr.hdrdict['System UpLoad Time'].strftime("%Y-%m-%d | %H%M%S.00") +' | ' \
				+ self.hdr.hdrdict["LATITUDE"] +' | '+ self.hdr.hdrdict["LONGITUDE"]
				else:
					tp = self.hdr.hdrdict['Recovered Time'].strftime("%Y-%m-%d | %H%M%S.00") +' | ' \
				+ self.hdr.hdrdict["LATITUDE"] +' | '+ self.hdr.hdrdict["LONGITUDE"]
				
				self.elogdict["Time|Position"] = tp
				self.elogdict["Cruise"] = self.hdr.hdrdict["VESSEL/TRIP/SEQ"]
				self.elogdict["Protocol"] = "NL-AZMP"
				self.elogdict["Platform"] =self.ship_is(self.hdr.hdrdict["VESSEL/TRIP/SEQ"].lstrip()[:2])
				
	def print_elog(self):
			print "$@MID@$:",self.MID
			print "Date:",self.elogdict["Date"]
			print "Reply to:",self.elogdict["Reply"] 
			print "Event:",self.elogdict["Event"] 
			print "Station:",self.elogdict["Station"]
			print "Instrument:","CTD"
			print "Attached:",self.elogdict["Attached"]
			print "Flowmeter Start:"
			print "Flowmeter End: "
			print "Action:","Deployed"
			print "Sounding: ",self.elogdict["Sounding"]
			print "Sample ID:",self.elogdict["Sample ID"]
			print "End_Sample_ID: ",self.elogdict["End_Sample_ID"] 
			print "Wire out:"
			print "Wire Angle:" 
			print "Depth:"
			print "Author:",self.elogdict["Author"]
			print "IMEI_No:"
			print "S/N:",self.elogdict["S/N"]
			print "Wind Speed and Direction:"
			print "Name:"
			print "Comment:",self.elogdict["Comments"]
			print "Time|Position:",self.elogdict["Time|Position"] 
			print "Cruise:",self.elogdict["Cruise"]
			print "PI:",self.elogdict["PI"]
			print "Protocol:",self.elogdict["Protocol"]
			print "Platform:",self.elogdict["Platform"]
			print "Revisions:"
			print "Attachment:"
			print "Encoding: plain"
			print "========================================\n"

def main():
#	if len(sys.argv) != 2:
#		print "supply data file name"
#		quit()
#	print sys.argv , len(sys.argv)
#	print sys.argv[0], sys.argv[1]
 	Welog=Write_elog('ColbourneE')
	event = 1
#	for i in range (1 , len(sys.argv)) :
#		datafile = sys.argv[i]
	datafile = "39173001.hdr"
	hdr = SBEIO(datafile)
#		hdr.print_pfile_hdr()
	Welog(hdr,event)
	event+=1
	
	
	
if __name__ == "__main__":
    main()
