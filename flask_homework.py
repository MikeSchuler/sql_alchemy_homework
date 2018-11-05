from flask import Flask, jsonify
import pandas as pd


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation(): 

    session = Session(engine)

    prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2017-01-01').all()
    
    prcp_df = pd.DataFrame(prcp)
    dic1 = prcp.to_dict()

    return jsonify(dic1)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    stations = session.query(Measurement.station).group_by(Measurement.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    past_year_tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-24').\
    order_by(Measurement.date.asc()).all()    
    
    return jsonify(past_year_tobs)

@app.route("/api/v1.0/<start>")
def start_date():
    
    session = Session(engine)
    
    start = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= '2016-08-24').all()    
    
    return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def range_date():
    
    session = Session(engine)
    
    start_end = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23' and Measurement.Date <= '2017-08-23').all
    
    return jsonify(start_end)

if __name__ == "__main__":
    app.run(debug=True)

