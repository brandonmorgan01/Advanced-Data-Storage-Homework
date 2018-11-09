#import dependencies
import pandas as pd
import datetime as dt
import os
from flask import Flask, jsonify 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#create engine
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurements = Base.classes.measurements
Stations = Base.classes.stations
session = Session(bind=engine)

#initiate Flask app
app = Flask(__name__)

@app.route('/')
def home:
    return (
         "Avalable Routes:<br/>"
         "/api/v1.0/precipitation"
         "/api/v1.0/stations"
         "/api/v1.0/tobs"
         "/api/v1.0/<start>"
         "/api/v1.0/<start>/<end>"
     )

@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago= dt.date.today() - dt.timedelta(365)
    start_date = dt.date.today()
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(year_ago, start_date)).all()
    return jsonify(prcp_query)

@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(Station.station).all()
    return jsonify(station_query)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    year_ago= dt.date.today() - dt.timedelta(365)
    start_date = dt.date.today()
    temp_year = session.query(Measurement.date, Measurement.tobs)..filter(Measurement.date.between(year_ago, start_date)).all()
    return jasonify(temp_year)

@app.route("/api/v1.0/temp/<start>")
def stats(start=None):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    return jsonify(temp_data)

@app.route("/api/v1.0/temp-range/<start>/<end>")
def stat_range(start=None, end=None):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(and_(Measurement.date >= start, Measurement.date <= today)).all()
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)