# -----=====|  |=====-----
# Create by Jules - 12/2023
# -----=====|  |=====-----

# Import library
from flask import Flask, jsonify, make_response, Response
from flasgger import Swagger
from flask_cors import CORS
import json, os, shutil

# Import controllers
from controllers.roomController import RoomController
from controllers.sensorController import SensorController
from controllers.measurementController import MeasurementController
from controllers.measureController import MeasureController

# Import files
from helpers.exceptions import *

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

@app.route("/rooms", methods=["GET"])
def getRooms():
    
  """
    Get all rooms.

  ---
  tags:
    - GET
  responses:
    200:
      description: Information for all rooms
    500:
      description: Internal server error
  """

  try:
    rooms = RoomController().getRooms()
    if rooms:
      return jsonify([{"name": room.name, "locate": room.locate} for room in rooms])
    NotFoundException() 
  except Exception as e:
    return InternalServerError(e)

@app.route("/sensors", methods=["GET"])
def getSensors():

  """
  Get all sensors.

  ---
  tags:
    - GET
  responses:
    200:
      description: Information for all sensors
    500:
      description: Internal server error
  """

  try:
    sensors = SensorController().getSensors()
    if sensors:
      return jsonify([{"name": sensor.name, "measurement": sensor.measurement, "room": sensor.room} for sensor in sensors])
    NotFoundException()
  except Exception as e:
    InternalServerError(e)

@app.route("/sensors/<string:name>", methods=["GET"])
def getSensor(name):

  """
  Get sensor by name.

  ---
  tags:
    - GET
  parameters:
    - name: name
      in: path
      type: string
      required: true
      description: Name of the sensor
  responses:
    200:
      description: Information for sensor
    500:
      description: Internal server error
  """

  try:
    sensors = SensorController().getSensor(name)
    if sensors :
      return jsonify([{"name": sensor.name, "measurement": sensor.measurement, "room": sensor.room} for sensor in sensors])
    NotFoundException()
  except Exception as e:
    InternalServerError(e)

@app.route("/rooms/<string:room>/sensors", methods=["GET"])
def getSensorsByRoom(room):

  """
  Get all sensors by room.

  ---
  tags:
    - GET
  parameters:
    - name: room
      in: path
      type: string
      required: true
      description: Name of the room
  responses:
    200:
      description: Information for room
    500:
      description: Internal server error
  """

  try:
    sensors = SensorController().getSensorsByRoom(room)
    if sensors :
      return jsonify([{"name": sensor.name, "measurement": sensor.measurement, "room": sensor.room} for sensor in sensors])
    NotFoundException()
  except Exception as e:
    InternalServerError(e)

@app.route("/measurements", methods=["GET"])
def getListMeasurements():

  """
  Get all measurements.

  ---
  tags:
    - GET
  responses:
    200:
      description: Information for measurements
    500:
      description: Internal server error
  """

  try:
    measurements = MeasurementController().getMeasurements()
    if measurements:
        return jsonify([{"measurement": measurement.name} for measurement in measurements])
    NotFoundException()
  except Exception as e:
    InternalServerError(e)

@app.route("/rooms/<string:room>/state", methods=["GET"])
def getMeasuresByRoomName(room):

  """
  Get state of room.

  ---
  tags:
    - GET
  parameters:
    - name: room
      in: path
      type: string
      required: true
      description: Name of the room
  responses:
    200:
      description: Room informations
    500:
      description: Internal server error
  """

  try:
    measures = MeasureController().getMeasuresByRoomName(room)
    print("===========================")
    print(measures)
    print("===========================")
    if measures:
      return jsonify([{"measurement": measure.measurement, "value" : measure.value, "recommendation" : measure.recommendation} for measure in measures])
    NotFoundException()
  except Exception as e:
    InternalServerError(e)

@app.route("/rooms/<string:room>/state/<string:measurement>", methods=["GET"])
def getMeasuresByRoomAndMeasurement(room, measurement):

  """
  Get measure of one measurement in room.

  ---
  tags:
    - GET
  parameters:
    - name: room
      in: path
      type: string
      required: true
      description: Name of the room
    - name: measurement
      in: path
      type: string
      required: true
      description: Name of the measurement
  responses:
    200:
      description: Room informations
    500:
      description: Internal server error
  """

  try:
    measure = MeasureController().getMeasuresByRoomAndMeasurement(room, measurement)
    if measure :
      return jsonify({"measurement": measure.measurement, "value" : measure.value, "recommendation" : measure.recommendation})
    NotFoundException()    
  except Exception as e:
    InternalServerError(e)

def delete_pycache(root_dir):
  for root, dirs, files in os.walk(root_dir):
    if "__pycache__" in dirs:
      pycache_dir = os.path.join(root, "__pycache__")
      shutil.rmtree(pycache_dir)
      dirs.remove("__pycache__")

if __name__ == "__main__":
  delete_pycache(os.getcwd())
  app.run(host='0.0.0.0', port=5000, debug=True)

