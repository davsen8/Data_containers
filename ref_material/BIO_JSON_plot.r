# from https://www.r-bloggers.com/an-introduction-to-time-series-with-json-data/
# http://neondataskills.org/R/time-series-plot-ggplot/

#Install package
#install.packages("rjson")  only needed if not already on yo8r machine

library(rjson)



jsonfile <- "C:\\sources\\GitHub\\Data_containers\\MTR_HUD2015030_1898_10588081_1800_ODF.json" 
#jsonfile <- "C:\\sources\\GitHub\\Data_containers\\MTR_HUD2015030_1898_10588081_1800_ODF_test.json"


# have an issue load unquoted  numbers as asre in the _test file

rev <- fromJSON(file = jsonfile)

datalength <- length(rev$DATA)

datalength


#attributes (rev)
rev$RECORD_HEADER$NUM_CYCLE


#str(rev$DATA)
#rev$DATA[]
#rev$DATA[][[2]]

#str(rev$DATA[0])
#rev$DATA[1] <-  as.numeric(paste(rev$DATA[1]))
# convert it to dataframe

revdata= as.data.frame(t(as.data.frame(rev$DATA))) # transposed to get cols and rows right

#revdata= as.data.frame(rev$DATA) # transposed to get cols and rows right
str(revdata)


colnames(revdata) <- c('date','temp')


# conver to a date ;convert temp from a 'factor' to a numeric
revdata['date'] <-  as.POSIXct(revdata[,'date'],format = "%d-%b-%Y %H:%M:%S.00", tz="")
revdata['temp'] <-  as.numeric(paste(revdata[,'temp']))


library(scales)
require(ggplot2)


str(revdata)

#  for the aes call do not put variable names in quotes
aplot<- ggplot(revdata, aes(x =date, y = temp))+ geom_line() +
  scale_y_continuous(name='temp',limits=c(-2,6))


aplot


