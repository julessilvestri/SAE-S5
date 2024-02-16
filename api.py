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
    return NotFoundException() 
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
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)

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
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)

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
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)

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
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)

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
    if measures:
      return jsonify([{"measurement": measure.measurement, "value" : measure.value, "recommendation" : measure.recommendation} for measure in measures])
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)

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
    return NotFoundException()    
  except Exception as e:
    return InternalServerError(e)

@app.route("/rooms/sensors", methods=["GET"])
def getRoomsSensorsList():

  """
    Retrieve a list of sensors grouped by rooms.

    This endpoint fetches a list of sensors grouped by rooms along with their respective measurements and recommendations.

    ---
    tags:
      - GET
    responses:
      200:
        description: List of rooms with associated sensor data
      404:
        description: No rooms found
      500:
        description: Internal server error
  """

  try:
      rooms = RoomController().getRooms()
      if not rooms:
          return jsonify({"error": "Rooms not found"}), 404

      rooms_sensors = []
      for room in rooms:
          sensors_data = MeasureController().getMeasuresByRoomName(room.name)
          sensors_data_dicts = [{
              "value": sensor.value,
              "measurement": sensor.measurement
          } for sensor in sensors_data] if sensors_data else "Sensors data not found"

          room_info = {
              "name": room.name,
              "locate": room.locate,
              "sensors": sensors_data_dicts
          }
          rooms_sensors.append(room_info)

      return jsonify(rooms_sensors), 200
  except Exception as e:
      return jsonify({"error": f"Internal server error: {str(e)}"}), 500

def delete_pycache(root_dir):

  """
    Delete all __pycache__ directories within the specified root directory.

    This function recursively walks through the directory tree starting from the root directory.
    If a __pycache__ directory is found within any directory, it is deleted along with its contents.

    Parameters:
        root_dir (str): The root directory from which to start searching for __pycache__ directories.

    Returns:
        None
  """

  for root, dirs, files in os.walk(root_dir):
    if "__pycache__" in dirs:
      pycache_dir = os.path.join(root, "__pycache__")
      shutil.rmtree(pycache_dir)
      dirs.remove("__pycache__")

if __name__ == "__main__":
  delete_pycache(os.getcwd())
  app.run(host='0.0.0.0', port=5000, debug=True)

