# from https://www.r-bloggers.com/an-introduction-to-time-series-with-json-data/
# http://neondataskills.org/R/time-series-plot-ggplot/

#Install package
#install.packages("rjson")  only needed if not already on yo8r machine

library(rjson)

#jsonfile <- "C:\\sources\\GitHub\\Data_containers\\CTD_BCD2016666_001_01_DN_ODF_test.json" 
jsonfile <- "C:\\sources\\GitHub\\Data_containers\\MTR_HUD2015030_1898_10588081_1800_ODF.json" 

rev <- fromJSON(file = jsonfile)

datalength <- length(rev$DATA)

datalength


#attributes (rev)

#str(rev$DATA)

  
# convert it to dataframe

revdata= as.data.frame(t(as.data.frame(rev$DATA))) # transposed to get cols and rows right

colnames(revdata) <- c('contr','contr_f','Pres','pres_f','Temp','temp_f')
revdata['Pemp'] <-  as.numeric(paste(revdata[,'Pres']))
revdata['Temp'] <-  as.numeric(paste(revdata[,'Temp']))

#col_headings <- c('date','temp')
#names(revdata) <- col_headings


str(revdata)

# conver to a date ;convert temp from a 'factor' to a numeric
#revdata['date'] <-  as.POSIXct(revdata[,'date'],format = "%d-%b-%Y %H:%M:%S.00", tz="")
#revdata <-  as.numeric(paste(revdata))


#head(revdata,n=1)


library(scales)
require(ggplot2)



aplot<- ggplot(revdata, aes(x ='Pres', y = 'Temp'))+ geom_line() +
  scale_y_continuous(name="pres",limits=c(0,200)) +
  scale_x_continuous(name="temp",limits=c(-2,8))


#aplot<- ggplot(revdata, aes(x =date, y = temp))+ geom_line() 


aplot


