#1 import Flask, jasonify
from flask import Flask, jsonify

import numpy as np
import pandas as pd

#Importing the dependancies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


#2 create an app, being sure to pass __name__
app = Flask(__name__)

#Define route
@app.route("/")
def home():
	print("server received a requet for 'Home' page")
	return (f"Surfs Up!"
			f"Available Routes:<br/>"
			f"/api/v1.0/precipitation<br/>"
			f"/api/v1.0/stations<br/>"
			f"/api/v1.0/tobs"
			)

@app.route("/api/v1.0/precipitation")
def prcp():

	session=Session(engine)
	result_prcp=session.query(Measurement.date, Measurement.prcp)
	returned={}
	for x in result_prcp:
		date=x[0]
		prcp=x[1]
		returned[date]=prcp
	#print (returned)
	return jsonify(returned)
	session.close()

@app.route("/api/v1.0/stations")
def stations():
	
	session=Session(engine)

	result_station=session.query(Station.station).all()
	session.close()
	all_stations=list(np.ravel(result_station))
	
	return jsonify(all_stations)
	
	session.close()

@app.route("/api/v1.0/tobs")
def temp():

	session=Session(engine)

	most_active_station='USC00519281'
	prev_year=dt.date(2017,8,23) - dt.timedelta(days=365)
	sel=[Measurement.station, Measurement.date, Measurement.tobs]
	results=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=prev_year).\
	filter(Measurement.station==most_active_station).all()
	most_active=list(np.ravel(results))

	
	return jsonify(most_active)

	session.close()

@app.route("/api/v1.0/<start>")
#@app.route("/api/v1.0/<start>/<end>")
def start(start):

	session=Session(engine)

	#date_string="2017-08-23"
	#start_date=datetime.strptime(date_string, "%Y-%m-%d").date()
	temp_calc=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs))\
		.filter(Measurement.date>=start).all()
	
	results_temp=list(np.ravel(temp_calc))

	min_temp=results_temp[0]
	max_temp=results_temp[1]
	avg_temp=results_temp[2]

	#temp_data=[]

	temp_dict={"Start Date": start,
	"Minimum temperature": min_temp,
	"Average temperature": avg_temp,
	"Maximum temperature": max_temp
	}

	return jsonify(temp_dict)

	session.close()

@app.route("/api/v1.0/<start>/<end>")
def end (start, end):	

	session=Session(engine)

	temp_calc_v2=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs))\
		.filter(Measurement.date>=start).filter(Measurement.date<=end).all()
	
	results_temp_v2=list(np.ravel(temp_calc_v2))

	min_temp_v2=results_temp_v2[0]
	avg_temp_v2=results_temp_v2[2]
	max_temp_v2=results_temp_v2[1]

	#temp_data=[]

	temp_dict_v2={"Start Date": start,
	"End Date": end,
	"Minimum temperature": min_temp_v2,
	"Average temperature": avg_temp_v2,
	"Maximum temperature": max_temp_v2
	}

	return jsonify(temp_dict_v2)

	session.close()

if __name__=="__main__":
	app.run(debug=True)