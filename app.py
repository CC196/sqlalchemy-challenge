import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def Home():
    return(
        f"Climate<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2012-03-05<br/>"
        f"/api/v1.0/2012-02-28/2012-03-05"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_prec = list(np.ravel(results))
    return jsonify(all_prec)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    station = list(np.ravel(results))
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    data = session.query(Measurement.tobs).filter(Measurement.date >= "2016/8/23").filter(Measurement.station=="USC00519281").all()
    session.close()
    tobs = list(np.ravel(data))
    return jsonify(tobs)
    

@app.route("/api/v1.0/<start>")
def startday(start):
    session = Session(engine)
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    result = list(np.ravel(data))
    return jsonify(result)

@app.route("/api/v1.0/<start>/<end>")
def endday(start, end):
    session = Session(engine)
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    result = list(np.ravel(data))
    return jsonify(result)

if __name__=='__main__':
    app.run(debug=True)