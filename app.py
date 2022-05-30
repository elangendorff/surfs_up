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

measurement = Base.classes.measurement
station = Base.classes.station

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
        Welcome to the Climate Analysis API!
        Available Routes:
        {version_prefix}/precipitation
        {version_prefix}/stations
        {version_prefix}/tobs
        {version_prefix}/temp/start/end
        '''
    )

