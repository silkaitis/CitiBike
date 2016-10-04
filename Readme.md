# CitiBike Usage Investigation

**Purpose**

Citi Bike is a privately owned public bicycle sharing system that serves parts of New York City. It is the largest bike sharing program in the United States. This is an exploratory data analysis on the busiest CitiBike station.

**Method**

Station status was queried every minute for a given hour using the CitiBike [API](https://feeds.citibikenyc.com/stations/stations.json).  Station data was originally queried July 22nd, 2016 at 6 PM Eastern and stored in a SQLite3 database.

**Results**

* The most active station is station id 490 at 8 Ave & W 33 St (latitude: 40.751551 longitude: -73.993934)
* There were 281 bicycles coming and going in the hour between 2016-07-22 17:55:45 and 2016-07-22 19:00:58

![alt text](https://raw.githubusercontent.com/silkaitis/CitiBike/master/CitiBike_Usage.png)

**Interpretation**

Station 490 is located near several major factilities; Moynihan Station, Madison Sqaure Garden and Penn Station. There were no events at Madison Square Garden or Moynihan Station on July 22nd. There are other event spaces in the area, such as a movie theater, but it's hard to imagine these smaller venues drawing enough people to generate this level of activity. Penn Station is the main railroad station for NYC and serves 600,000 commuters a day [[1]](https://en.wikipedia.org/wiki/Pennsylvania_Station_(New_York_City)). Data was pulled at 6 PM on a Friday which is most likely the (or near the) peak hour for commuters in a given day.
There are 25,000 commuters per hour assuming the commuter volume is evenly distributed. Therefore, only 1.1% of commuters in that hour need to rent or return a bike to make this station the most active. Realistically, commuter volume won't be evenly distributed but this assumption is sufficient for now. This simple assessment doesn't account for other factors that could impact station usage.

**Code**

* CitiBike_datascrape.ipynb ~ API query and data storage
* CitiBike_v2.ipynb ~ Analysis of station data
