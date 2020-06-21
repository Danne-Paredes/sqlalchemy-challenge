from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import date, timedelta, datetime
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables
measurement = Base.classes.measurement
station = Base.classes.station

date = dt.datetime(2016, 8, 23)



app = Flask(__name__)



@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print('Loaded: Precipitation')
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()
    precip = {date:prcp for date, prcp in results}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    print('Loaded: stations')
    session = Session(engine)
    results = session.query(station.station,station.name).all()
    session.close()
    stations = {station:name for station, name in results}
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print('Loaded: tobs')
    session = Session(engine)
    results = session.query(measurement.date,measurement.tobs).\
    filter(measurement.date >= date).\
    filter(measurement.station == 'USC00519397').all()
    session.close()
    precip = {date:tobs for date, tobs in results}
    return jsonify(precip)

@app.route("/api/v1.0/<start>")
def start(start):
    print('Loaded: <start>')
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    tobs_results = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_results.append(tobs_dict)
    return jsonify(tobs_results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    print('Loaded: <start>/<end>')
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    tobs_results = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_results.append(tobs_dict)
    return jsonify(tobs_results)



if __name__ == "__main__":
    app.run(debug=True)
