# Import dependencies
import datetime as dt
import numpy as np
# import pandas as pd
# import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set Up Database
filepath = ''
engine = create_engine(
    f"sqlite://{filepath}/hawaii.sqlite",
    connect_args={'check_same_thread': False}   # Make the engine multi-threaded
)                                               # https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#using-a-memory-database-in-multiple-threads

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Set Up Flask
app = Flask(__name__)

version_prefix = '/api/v1.0'

route = {
    'precipitation': f'<a href = "{version_prefix}/precipitation">Precipitation</a>',
    'stations': f'<a href = "{version_prefix}/stations">Stations</a>',
    'tobs': f'<a href = "{version_prefix}/tobs">Temperature Observations</a>',
    # 'stats': f'<a href = "{version_prefix}/temp/start/end">Statistics</a>'
    'stats': f'<a href = "{version_prefix}/temp/">Statistics</a>'
}

prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)   # Leap years?

# 9.5.2 Create the Welcome Route
@app.route("/") # The @ sign is a "listener" decoration.
                # When a user goes to the URL shown in the argument of the `route` method,
                # `@` causes the Flask object it's attached to (`app`)
                # to call the function that's defined immediately below it.

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

def welcome():
    return(
        f'''
        Welcome to the Climate Analysis API!<br>
        Available Routes:<br>
        {route["precipitation"]}<br>
        {route["stations"]}<br>
        {route["tobs"]}<br>
        {route["stats"]}
        '''
    )

# 9.5.3 Precipitation Route
@app.route(f"{version_prefix}/precipitation")

def precipitation():
    # prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)   # Leap years?
                                                                # `prev_year` (with the same definition) gets used again in a later function,
                                                                # so moved this definition up and outside the functions (see above), instead.
    precipitation = (
        session.query(Measurement.date, Measurement.prcp)   # '''SELECT date, prcp FROM Measurement
        .filter(prev_year <= Measurement.date)              # WHERE prev_year <= Measurement.date'''
        .all()
    )
    
    precip = {date: prcp for date, prcp in precipitation}   # Convert the 2-tuples from precipitation into key-value dictionary pairs
    
    return jsonify(precip)

# 9.5.4 Stations Route
@app.route(f"{version_prefix}/stations")

def stations():
    results = session.query(Station.station).all()  # 'SELECT station from Station' (outputs a list of tuples)
    station_list = list(np.ravel(results))          # np.ravel "flattens" the above list of tuples into a single array
                                                    # whose elements are the elements of each of the tuples, in sequence
    
    return jsonify(stations=station_list)           # The `=` causes `jsonify` to make a dictionary-like entry
                                                    # with 'stations' as the entry's key and `station_list` as its value

# 9.5.5 Monthly Temperature Route
@app.route(f"{version_prefix}/tobs")

def temp_monthly():
    the_station = 'USC00519281'
    results = (
        session.query(Measurement.tobs)                 # '''SELECT tobs FROM Measurement
        .filter(Measurement.station == the_station)     # WHERE station == 'USC00519281'
        .filter(prev_year <= Measurement.date)          # AND prev_year <= date'''
        .all()
    )
    temps = list(np.ravel(results))
    
    return jsonify(
        station=the_station,        # See the `jsonify()` function inside the `stations()` function above.
        temperatures_recorded=temps # Same.
    )

# 9.5.6 Statistics Route
@app.route(f"{version_prefix}/temp/")
@app.route(f"{version_prefix}/temp/<start>")
@app.route(f"{version_prefix}/temp/<start>/")
@app.route(f"{version_prefix}/temp/<start>/<end>")
@app.route(f"{version_prefix}/temp/<start>/<end>/")

def stats(start=None, end=None):
    # The list elements in `sel` will be used as columns in later SQL queries
    sel = [
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ]
    
    # If the `start` parameter has no value (or is `False`; note: `not None` evaluates to `True`), then…
    if not start:
        return f'''
            Instructions: Enter &ltstart&gt or &ltstart&gt/&ltend&gt dates at the end of the URL in the address bar.<br>
            Dates should be in yyyy-mm-dd format.<br>
            Example: …{version_prefix}/temp/2017-06-01/2017-06-30
            '''
    
    # If the `end` parameter has no value (or is `False`; note: `not None` evaluates to `True`), then…
    if not end:
        results = (
            # See <https://docs.python.org/3.10/reference/expressions.html#calls>
            # for an explanation of the `*` on the line that follows
            session.query(*sel)
            .filter(start <= Measurement.date)
            .all()
        )
        temps = list(np.ravel(results))
    
        # return jsonify(min_avg_max_temps=temps) # See the `jsonify()` function inside the `stations()` function above.
        return jsonify(
            minimum_temperature=temps[0],   # See the `jsonify()` function inside the `stations()` function above.
            average_temperature=temps[1],   # Same.
            maximum_temperature=temps[2]    # Same.
        )
    
    # Otherwise (they both have values)…
    results = (
        session.query(*sel)
        .filter(start <= Measurement.date)
        .filter(Measurement.date <= end)
        .all()
    )
    temps = list(np.ravel(results))
    
    # return jsonify(min_avg_max_temps=temps)     # See the `jsonify()` function inside the `stations()` function above.
    return jsonify(
        minimum_temperature=temps[0],   # See the `jsonify()` function inside the `stations()` function above.
        average_temperature=temps[1],   # Same.
        maximum_temperature=temps[2]    # Same.
    )