# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask (__name__)

#################################################
# Flask Routes
#################################################
# Home page with list of APIs
@app.route("/")
def homepage():
    #list of all APIs
    return( f' -:Hawaii Weather Data:-<br/>'
            f' Last 12 months Precipitation:/api/v1.0/precipitation<br/>'
            f' List of Station:/api/v1.0/stations <br/>'
            f' List of temperature observation of previous year at station-USC00519281:/api/v1.0/tobs <br/>'
            f' Temperature summary:/api/v1.0/<start><br/>'
            f' Temperature summary:/api/v1.0/<start>/<end><br/>')
#Append precippitation data, zip into dictionary and jasonify it.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Find the most recent date in the data set.
    most_rec_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # by using max func
    most = session.query(func.max(Measurement.date)).all()
    print(most_rec_date)
    # Calculate the date one year from the last date in data set.
    last_dt = most_rec_date[0]
    last_date = dt.datetime.strptime(last_dt, '%Y-%m-%d')
    start_date = last_date - dt.timedelta(days=365)
    start_date_format = start_date.strftime('%Y-%m-%d')
    print(start_date_format)

# Perform a query to retrieve the data and precipitation scores
    data_list =[Measurement.date,func.sum(Measurement.prcp)]
    prcp_data = session.query(*data_list).\
    filter(func.strftime(Measurement.date)>= start_date_format).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    session.close()
    
    # store data for everyday
    dates_prcp = []
    total_prcp = []
    for date, daytotal in prcp_data:
        dates_prcp.append(date)
        total_prcp.append(daytotal)
    prcp_dict = dict(zip(dates_prcp,total_prcp))    
    return jsonify (prcp_dict)   

# list of stations and normlazied the list and jasonify it.

@app.route("/api/v1.0/stations")
def stations():
   session = Session(engine)
   stations_list = [Measurement.station]
   total_act_station = session.query(*stations_list).\
   group_by(Measurement.station).all()
   session.close()

   convert_into_list = list(np.ravel(total_act_station))
   return jsonify(convert_into_list)
# temperature data for previous year and jasonify.

@app.route("/api/v1.0/tobs")    
def tem_obervation():
    session = Session(engine)
    # Find the most recent date in the data set.
    most_rec_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # by using max func
    most = session.query(func.max(Measurement.date)).all()
    print(most_rec_date)
    # Calculate the date one year from the last date in data set.
    last_dt = most_rec_date[0]
    last_date = dt.datetime.strptime(last_dt, '%Y-%m-%d')
    start_date = last_date - dt.timedelta(days=365)
    start_date_format = start_date.strftime('%Y-%m-%d')
    print(start_date_format)

    # Perform a query to retrieve the data and precipitation scores
    data_list =[Measurement.date,func.sum(Measurement.tobs)]
    station_data = session.query(*data_list).\
    filter(func.strftime(Measurement.date)>= start_date_format, Measurement.station == 'USC00519281').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    
    obs_date_list = []
    tem_obs_list =[]
    for date, obs in station_data:
        obs_date_list.append(date)
        tem_obs_list.append(obs)
    session.close()    
    tem_obs_dict = dict(zip(obs_date_list,tem_obs_list))    
    return jsonify(tem_obs_dict)
# Temperature summary form any start date to latest date.
@app.route("/api/v1.0/<start>")
def tem_summary_one(start, end_date = func.max(Measurement.date)):
    session = Session(engine)
    temp_summary= [func.min(Measurement.tobs),
             func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    temp_data=session.query(*temp_summary).\
                filter(Measurement.date >= start).all()
    session.close() 
    list_trip_one = []
    for min,max,avg in temp_data:
        trip_one_dict = {}
        trip_one_dict['Min']= min
        trip_one_dict['Max']= max
        trip_one_dict['Average']= avg
        list_trip_one.append(trip_one_dict)
    if trip_one_dict['Min']:
        return jsonify(list_trip_one)
    else:
        return jsonify({"error": f'date format is YYYY-MM-DD'})
 # Teperature summary form any time frame  
@app.route("/api/v1.0/<start>/<end>")
def tem_summary_two(start, end):

    session = Session(engine)
    
    temp_summary= [func.min(Measurement.tobs),
             func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    temp_data=session.query(*temp_summary).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    session.close()

    list_trip_two = []
    for min,max,avg in temp_data:
        trip_one_dict = {}
        trip_one_dict['Min']= min
        trip_one_dict['Max']= max
        trip_one_dict['Average']= avg
        list_trip_two.append(trip_one_dict)
    if trip_one_dict['Min']:
        return jsonify(list_trip_two)
    else:
        return jsonify({"error": f'date format is YYYY-MM-DD'})                  

# Run the APIs.
if __name__ == "__main__":
    app.run(debug= True)