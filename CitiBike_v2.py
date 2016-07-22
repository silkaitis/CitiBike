
# coding: utf-8

# In[6]:

#Import needed modules
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 as lite
from datetime import datetime
from dateutil.parser import parse
import collections
get_ipython().magic('matplotlib inline')


# In[2]:

#Pull JSON data from CitiBike website
r = requests.get('http://www.citibikenyc.com/stations/json')

#Pull JSON data into Pandas DataFrame
bikedata=pd.io.json.json_normalize(r.json()['stationBeanList'])


# In[3]:

#Build SQLite database with reference table and bike data table
con = lite.connect('citibike.db')
cur = con.cursor()

sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
idList=bikedata['id'].tolist()
idList=['_'+str(x)+' INT' for x in idList]
with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT)')
    for station in r.json()['stationBeanList']:
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))
    
    cur.execute("CREATE TABLE available_bikes (execution_time INT, " + ", ".join(idList)+");")


# In[4]:

bikeid=collections.defaultdict(int)

for itr in range(0,60):
    print('Iteration: %d' % itr)
    #Pull JSON data from CitiBike website
    r = requests.get('http://www.citibikenyc.com/stations/json')
    
    #Pull execution time
    exec_time = parse(r.json()['executionTime'])

    #Create dictionary for available bikes per station
    for station in r.json()['stationBeanList']:
        bikeid[station['id']] = station['availableBikes']

    with con:
        #Insert execution time into database
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime("%Y%m%d_%H%M%S"),))

        #Insert available bikes per station into database
        for key,value in bikeid.items():
            cur.execute('UPDATE available_bikes SET _' + str(key) + ' = ' + str(value) + " WHERE execution_time = " + "'"+exec_time.strftime("%Y%m%d_%H%M%S")+"'"+";")
    
    #Pause for 60 seconds till next iteration
    time.sleep(60)


# In[7]:

#Pull bike data from database
bikedata = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

#Find station activity over an hour
hourdelta=collections.defaultdict(int)
for key,val in bikedata.iteritems():      
    hourdelta[int(key.replace("_",""))] = sum([abs(val[i]-val[i-1]) for i in range(1,len(val))])

#Pull specific station data from database
data=cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max(hourdelta, key=hourdelta.get),)).fetchone()

print('The most active station is station id %s at %s (latitude: %s longitude: %s)\n' % data)
print('With %d bicycles coming and going in the hour between %s and %s' % (hourdelta[data[0]],datetime.strptime(bikedata.index[0],"%Y%m%d_%H%M%S"),datetime.strptime(bikedata.index[1],"%Y%m%d_%H%M%S")))

plt.bar(hourdelta.keys(),hourdelta.values())
plt.title('Station Activity')
plt.xlabel('Station Number')
plt.ylabel('Number of Bikes')

