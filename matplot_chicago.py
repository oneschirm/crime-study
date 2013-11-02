import matplotlib.pyplot as plt
import shapefile
import matplotlib.patches as patches
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import csv

LONG_COLUMN = 20
LAT_COLUMN = 19
CRIMES_FILE_NAME = 'Crimes_-_2001_to_present.csv'
BUILDINGS_FILE_NAME = 'Building_Footprints/Building_Revised'
STREETS_FILE_NAME = 'streets/street_lines'
VIOLENT_TYPES = ['02','03','04A','04B','08A','08B','09','17','20']
MURDER_TYPES = ['01A','01B']

AREA = 'Cabrini_Green'
small_long = -87.64433311462402
big_long = -87.63287544250487
small_lat = 41.89433914769623
big_lat = 41.904704529604835

#AREA = 'Hyde_Park'
#small_long = -87.61322021484375
#big_long = -87.57030487060547
#small_lat = 41.777456667491066
#big_lat = 41.79963133506506

#padding bounds
safety_small_long = small_long - 0.02
safety_big_long = big_long + 0.02
safety_small_lat = small_lat - 0.02
safety_big_lat = big_lat + 0.02

#reads large footprint shapefile, plots patches inside of bounds
def plot_buildings(m):
    buildings = shapefile.Reader(BUILDINGS_FILE_NAME)
    building_shapes = buildings.shapes()
    for thing in building_shapes:
        shape = thing.points
        verts = []
        for set in shape:
            lon, lat = set[0], set[1]
            x, y = m(lon, lat)
            verts.append([x,y])
        # checks to see if the first point is within the bounds. others not checked. 
        lon, lat = shape[0][0], shape[0][1]
        if ((lat > small_lat and lat <big_lat) and (lon > small_long and lon < big_long)):
            poly = Polygon(verts, facecolor='#595959',alpha=float(0.5))
            plt.gca().add_patch(poly)

#reads crime data, finds by year, then sorts as nonviolent, violent, murder or n/a            
def get_crimes(YEAR,m,unusable_data):
    file = csv.reader(open(CRIMES_FILE_NAME))
    file.next()
    crime_dictionary = {'nonviolent':[],'violent':[],'murder':[]}
    for index, row in enumerate(file):
        if str(YEAR) in row[2]:
            try:
                lat = float(row[LAT_COLUMN])
                long = float(row[LONG_COLUMN])
                if ((lat > small_lat and lat <big_lat) and (long > small_long and long < big_long)):
                    x, y = m(long, lat)
                    if row[14] in VIOLENT_TYPES:
                        new_violent = crime_dictionary['violent']
                        new_violent.append([x,y])
                        crime_dictionary['violent'] = new_violent
                    elif row[14] in MURDER_TYPES:
                        new_murder = crime_dictionary['murder']
                        new_murder.append([x,y])
                        crime_dictionary['murder'] = new_murder
                    else:
                        nonviolent = crime_dictionary['nonviolent']
                        nonviolent.append([x,y])
                        crime_dictionary['nonviolent'] = nonviolent
            except ValueError:
                try:
                    unusable_data.writerow(row)
                except:
                    unusable_data.writerow('null') 
    return crime_dictionary
    
#plot nonviolent crimes in purple, scale with density   
def plot_crimes(crime_locations,m):
    #plot 'normal' crimes
    unique_locations = []
    for item in crime_locations:
        if item in unique_locations:
            pass
        else:
            unique_locations.append(item)
    for item in unique_locations:
        display_alpha = 0.25
        calculated_alpha = (0.15*crime_locations.count(item)/20)
        if calculated_alpha > display_alpha:
            display_alpha = calculated_alpha
        if calculated_alpha >=1:
            display_alpha = 1
        m.plot(item[0], item[1], 'o', markersize=7, color='#CC33FF', alpha=float(display_alpha))
        
#plot violent crimes in red, scale with density        
def plot_crimes_violent(crime_locations_violent,m):
    #plot violent crimes  
    unique_locations_violent = []
    for item in crime_locations_violent:
        if item in unique_locations_violent:
            pass
        else:
            unique_locations_violent.append(item)
    for item in unique_locations_violent:
        display_alpha = 0.25
        calculated_alpha = (0.15*crime_locations_violent.count(item)/20)
        if calculated_alpha > display_alpha:
            display_alpha = calculated_alpha
        if calculated_alpha >=1:
            display_alpha = 1
        m.plot(item[0], item[1], 'o', markersize=7, color='#FF0000',alpha=float(display_alpha)) 
        
#plot murders in bright white. no scaling        
def plot_crimes_murder(crime_locations_murder,m):
    #plot murders 
    for item in crime_locations_murder:
        display_alpha = 0.9
        m.plot(item[0], item[1], 'o', markersize=7, color='white',alpha=float(display_alpha))

#plot street center lines from shapefile        
def plot_streets(m):
    street_lines = shapefile.Reader(STREETS_FILE_NAME)
    street_lines_shapes = street_lines.shapes()
    for thing in street_lines_shapes:
        shape = thing.points
        x_s = []
        y_s = []
        for set in shape:
            lon, lat = set[0], set[1]
            x, y = m(lon, lat)
            x_s.append(x)
            y_s.append(y)
        lon, lat = shape[0][0], shape[0][1]
        if ((lat > safety_small_lat and lat <safety_big_lat) and (lon > \
        safety_small_long and lon < safety_big_long)):
            m.plot(x_s,y_s, '-', color='white',alpha=float(0.35))

# add labels manually for viewer context            
def label_streets():
    #street names    
    cabrini_green_streets = [{'x':525,'y':295,'name':'West Chicago Avenue',\
    'rotation':'horizontal'},
    {'x':140,'y':1240,'name':'North Larrabee Street','rotation':'vertical'},\
    {'x':1110,'y':1375,'name':'North LaSalle Street','rotation':'vertical'},\
    {'x':525,'y':1380,'name':'West Division Street','rotation':'horizontal'}]    
    hyde_park_streets = [{'x':3020,'y':2185,'name':'South Stony Island Avenue',\
    'rotation':'vertical'},
    {'x':630,'y':2550,'name':'South Cottage Grove Avenue','rotation':'vertical'},\
    {'x':1390,'y':400,'name':'East 63rd Street','rotation':'horizontal'},\
    {'x':1420,'y':2710,'name':'East 55th Street','rotation':'horizontal'}]   
    
    if AREA == 'Cabrini_Green':
        streets = cabrini_green_streets
    elif AREA == 'Hyde_Park':
        streets = hyde_park_streets
        
    for street in streets:
        plt.text(street['x'],street['y'],street['name'], color='white',fontsize=14,\
         rotation=street['rotation'],alpha=float(0.35))
    
def main():
    unusable_name = 'unusable_%s.csv' % AREA
    unusable_data = csv.writer(open(unusable_name,'wb'))

    for i in range(2004,2013):
        m = Basemap(projection='merc',resolution=None,llcrnrlat=small_lat, \
        urcrnrlon=big_long,urcrnrlat=big_lat,llcrnrlon=small_long)
        fig = plt.figure(figsize=(11,11))
        ax = plt.subplot(111)
        m.drawmapboundary(fill_color='#1B1B1B')
    
        crime_dictionary = get_crimes(i,m,unusable_data)
        plot_crimes(crime_dictionary['nonviolent'],m)
        plot_crimes_violent(crime_dictionary['violent'],m) 
        plot_crimes_murder(crime_dictionary['murder'],m)
    
        plot_buildings(m)
        plot_streets(m)
        label_streets()

        output_file_name = '%s/%s_%s.png' % (AREA,AREA,str(i))
        ax.text(0.01,0.01,'https://github.com/oneschirm',color='white',\
        fontsize=12,transform=ax.transAxes)
        ax.text(0.9, 0.01, str(i),color='white', fontsize=20,transform=ax.transAxes)
        plt.savefig(output_file_name, dpi=150,bbox_inches='tight')

if __name__ == '__main__':
    main()