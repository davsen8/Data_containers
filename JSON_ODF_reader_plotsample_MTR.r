#Created on 2017-11-01 by Dave Senciall
#@author: DSenciall

#Install package
#install.packages("rjson")  only needed if not already on yo8r machine

library(rjson)


jsonfile <- "C:\\sources\\GitHub\\Data_containers\\MTR_HUD2015030_1898_10588081_1800_ODF.json" 



 hdr<- fromJSON(file = jsonfile)

datalength <- length(hdr$DATA)

# see how many lines you got of data
datalength


#atributes (hdr)

# and a demo of accessing a header element value
hdr$RECORD_HEADER$NUM_CYCLE


# convert it to dataframe
# unlike in python for R need to transposed to get cols and rows right
hdrdata= as.data.frame(t(as.data.frame(hdr$DATA))) 

#hdrdata= as.data.frame(hdr$DATA) # transposed to get cols and rows right


# check the attributes
#str(hdrdata)

# label the channels (technicall you could pull the channel ids fromt he parameters blocks)	 
colnames(hdrdata) <- c('date','temp')


# conver to a date ;convert temp from an R 'factor' to a numeric
hdrdata['date'] <-  as.POSIXct(hdrdata[,'date'],format = "%d-%b-%Y %H:%M:%S.00", tz="")
hdrdata['temp'] <-  as.numeric(paste(hdrdata[,'temp']))


# plot the data
library(scales)
require(ggplot2)


# note : for the aes call do not put variable names in quotes
aplot<- ggplot(hdrdata, aes(x =date, y = temp)) +
        geom_line() +
        scale_y_continuous(name='temp',limits=c(-2,6))

aplot

                     
