# sqlalchemy_challenge
# Import all dependecies
Import all dependencies
Part 1: Analyze and Explore the Climate Data
## Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 
# Calculate the date one year from the last date in data set. Find the most recent date in the data set.
# Plot the graph
Exploratory Station Analysis
# Design a query to calculate the total number of stations in the dataset
# Design a query to find the most active stations (i.e. which stations have the most rows?)
# List the stations and their counts in descending order.
# Calculate the lowest, highest, and average temperature Using the most active station id from the previous query.
#Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
Part 2: Design Your Climate App
1.	/
o	Start at the homepage.
o	List all the available routes.
2.	/api/v1.0/precipitation
o	Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
o	Return the JSON representation of your dictionary.
3.	/api/v1.0/stations
o	Return a JSON list of stations from the dataset.
4.	/api/v1.0/tobs
o	Query the dates and temperature observations of the most-active station for the previous year of data.
o	Return a JSON list of temperature observations for the previous year.
5.	/api/v1.0/<start> and /api/v1.0/<start>/<end>
o	Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.


