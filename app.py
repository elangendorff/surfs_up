# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set Up Database
filepath = ''
engine = create_engine(f"sqlite://{filepath}/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Set Up Flask
app = Flask(__name__)

version_prefix = '/api/v1.0'

# 9.5.2 Create the Welcome Route
@app.route("/")

# def welcome():
#     return(
#     '''
#     Welcome to the Climate Analysis API!
#     Available Routes:
#     /api/v1.0/precipitation
#     /api/v1.0/stations
#     /api/v1.0/tobs
#     /api/v1.0/temp/start/end
#     ''')

# def welcome():
#     return(
#         '''
#         Welcome to the Climate Analysis API!
#         Available Routes:
#         /api/v1.0/precipitation
#         /api/v1.0/stations
#         /api/v1.0/tobs
#         /api/v1.0/temp/start/end
#         '''
#     )

def welcome():
    return(
        f'''
        Welcome to the Climate Analysis API!<BR>
        Available Routes:<BR>
        {version_prefix}/precipitation<BR>
        {version_prefix}/stations<BR>
        {version_prefix}/tobs<BR>
        {version_prefix}/temp/start/end
        '''
    )

@app.route(f"{version_prefix}/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)  # More precisely: 365.2425
    precipitation = (
        session.query(Measurement.date, Measurement.prcp)   # '''SELECT date, prcp FROM Measurement
        .filter(prev_year <= Measurement.date)              # WHERE prev_year <= Measurement.date'''
        .all()
    )

    precip = {date: prcp for date, prcp in precipitation}   # Convert the 2-tuples from precip into key-value dictionary pairs
    
    return jsonify(precip)

@app.route(f"{version_prefix}/stations")

def stations():
    results = session.query(Station.station).all()  # 'SELECT station from Station' (outputs a list of tuples)
    stations = list(np.ravel(results))              # np.ravel "flattens" the above into a single list of each element of the tuples in sequence

    return jsonify(stations=stations)               # Even after consulting the documentation, I don't know what 'stations=stations' is doing

