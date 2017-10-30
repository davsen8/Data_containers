# from https://www.r-bloggers.com/an-introduction-to-time-series-with-json-data/
# http://neondataskills.org/R/time-series-plot-ggplot/

#Install package
#install.packages("rjson")
library(rjson)
jsonfile <- "C:\\sources\\GitHub\\Data_containers\\test.JSON" 


rev <- fromJSON(file = jsonfile)

datalength <- length(rev$DATA)

datalength
#rev$DATA[1]
#rev$DATA[[1]][1]
#rev$DATA[[1]][2]


#attributes (rev)

#str(rev$DATA)

# as.POSIXct
timedate = {}
temp = {}

for (x in 1:datalength) {
#  timedate <-  c(timedate,toString(rev$DATA[[x]][1]))
  timedate <-  c(timedate,strptime(rev$DATA[[x]][1],format = "%d-%b-%Y %H:%M:%S.00", tz=""))
  temp <- c(temp,as.double(noquote(rev$DATA[[x]][2]))) 
}
  
#Bind columns and convert it to dataframe
revdata <- as.data.frame(cbind(timedate,temp))

head(revdata)
#str(revdata)

library(scales)
require(ggplot2)
qplot(x =timedate, y = temp, data = revdata)


