# from https://www.r-bloggers.com/an-introduction-to-time-series-with-json-data/

#Install package
install.packages("rjson")
library(rjson)
jsonfile <- "C:\\sources\\GitHub\\Data_containers\\ref_material\\losangelesrevenue.json" 


rev <- fromJSON(file = jsonfile)

datalength <- length(rev$data)


yeardata <- {}
monthdata <- {}
department <- {}
revenue <- {}
fiscalperiod <- {}

for (x in 1:datalength) {
  yeardata <- c(yeardata,as.integer(noquote(rev$data[[x]][9]))) 
  monthdata <- c(monthdata,toString(noquote(rev$data[[x]][10])))
  department <- c(department,toString(noquote(rev$data[[x]][12])))
  revenue <- c(revenue,as.double(noquote(rev$data[[x]][13])))
  fiscalperiod <- c(fiscalperiod,toString(noquote(rev$data[[x]][19])))
}
  
#Bind columns and convert it to dataframe
revdata <- as.data.frame(cbind(department, yeardata, monthdata, revenue,fiscalperiod))
revdata[,4] <- as.double(revenue)
head(revdata)

install.packages("plyr")
library(plyr)
revtotal <- ddply(revdata,.(fiscalperiod,monthdata), summarize, 
     monthly_revenue = sum(revenue))
head(revtotal)

install.packages('forecast')
library(forecast)
mts <- ts(revtotal$monthly_revenue, 
     start=c(2012,1),end=c(2016,6),frequency=12) 
fit <- stl(mts, s.window="period")
plot(fit)

