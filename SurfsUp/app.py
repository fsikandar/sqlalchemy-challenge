# Import the dependencies.
#import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///C:/Users/sikan/CHALLENGES/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
@app.route("/api/v1.0/precipitation")

def precipitation():
   
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   session.close()
   return jsonify(precip)
   
@app.route("/api/v1.0/stations")

def stations():
    
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    session.close()
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    
     
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
     filter(Measurement.station == 'USC00519281').\
     filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    session.close()
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start= None, end=None):
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end:
       start = dt.datetime.strptime(start,"%m%d%Y")
       results = session.query(*sel).filter(Measurement.date <= start).all()
       session.close()
       temps = list(np.ravel(results))
       return jsonify(temps)
    start = dt.datetime.strptime(start,"%m%d%Y")
    end = dt.datetime.strptime(end,"%m%d%Y")
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
if __name__ == '__main__':
    app.run(debug=True)
    