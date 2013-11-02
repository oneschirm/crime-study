A simple Python program to plot crime data using matplotlib and shapefile. 

![2008](https://raw.github.com/oneschirm/crime-study/master/Cabrini_Green/Cabrini_Green_2008.png)

More info:
http://oneschirm.github.io/crime-study/

### Data Sources
[Crime Data](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2)

[Buildings Shapefile](https://data.cityofchicago.org/Buildings/Building-Footprints/6mpq-sfwi) 

[Streets Shapefile](https://data.cityofchicago.org/Transportation/Street-Center-Lines/6imu-meau)

The Chicago Police Department uses a modified form of the FBI's Uniform Crime Reporting codes. The FBI details this system [here.](www2.fbi.gov/ucr/handbook/ucrhandbook04.pdf)

Note: You may have issues using the shapefiles if you do not convert x/y pairs to WGS84 before use in Python. 
