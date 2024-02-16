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

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

@app.route("/rooms", methods=["GET"])
def getRoomList():

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
        rooms = RoomController().getAll()
        if rooms :
            data = [{"name": room.name, "locate": room.locate} for room in rooms]
        else :
            data = {"error": "Rooms not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500

@app.route("/sensors", methods=["GET"])
def getSensorsList():

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
        sensors = SensorController().getList()
        if sensors:
            data = [{"name": sensor.name, "measurements": sensor.measurements, "room": sensor.room} for sensor in sensors]
        else:
            data = {"error": "Sensors not found"}

        return jsonify(data), 200  # Set the status code explicitly to 200 for success
    except Exception as e:
        error_message = f"Erreur interne du serveur : {str(e)}"
        return make_response(jsonify({"error": error_message}), 500)

@app.route("/sensors/<string:name>", methods=["GET"])
def getSensorsByName(name):

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
        sensors = SensorController().getByName(name)
        if sensors :
            data = [{"name": sensor.name, "measurements": sensor.measurements, "room": sensor.room} for sensor in sensors]
        else :
            data = {"error": "Sensor not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500

@app.route("/rooms/<string:room>/sensors", methods=["GET"])
def getListSensorByRoom(room):

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
        sensors = SensorController().getListByRoom(room)
        if sensors :
            data = [{"name": sensor.name, "measurements": sensor.measurements, "room": sensor.room} for sensor in sensors]
        else :
            data = {"error": "Sensors not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500

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
        measurements = MeasurementController().getList()
        if measurements:
            data = [{"measurement": measurement.name} for measurement in measurements]
            return jsonify(data), 200
        else:
            return make_response(jsonify({"error": "Measurements not found"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"Internal server error: {str(e)}"}), 500)
    




@app.route("/rooms/<string:room>/state", methods=["GET"])
def getRoomState(room):

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
      measures = MeasureController().getRoomState(room)

      if measures:
        data = [{"measurment": measure.measurment, "value" : measure.value, "recommendation" : measure.recommendation} for measure in measures]
        return jsonify(data), 200
      else:
        return make_response(jsonify({"error": "Measurements not found"}), 200)
    except Exception as e:
      return make_response(jsonify({"error": f"Internal server error: {str(e)}"}), 500, {"Content-Type": "application/json; charset=utf-8"})



@app.route("/rooms/<string:room>/state/<string:sensor>", methods=["GET"])
def getMeasure(room, sensor):

    """
    Get measure of one sensor in room.

    ---
    tags:
      - GET
    parameters:
      - name: room
        in: path
        type: string
        required: true
        description: Name of the room
      - name: sensor
        in: path
        type: string
        required: true
        description: Name of the sensor
    responses:
      200:
        description: Room informations
      500:
        description: Internal server error
    """

    try:
      measure = MeasureController().getMeasure(room, sensor)

      if measure :
        return jsonify({"measurment": measure.measurment, "value" : measure.value, "recommendation" : measure.recommendation}), 200
      return make_response(jsonify({"error": "Measurements not found"}), 200)
    
    except Exception as e:
      return make_response(jsonify({"error": f"Internal server error: {str(e)}"}), 500, {"Content-Type": "application/json; charset=utf-8"})


def delete_pycache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in dirs:
            pycache_dir = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_dir)
            print(f"Deleted {pycache_dir}")
            dirs.remove("__pycache__")

if __name__ == "__main__":
    delete_pycache(os.getcwd())
    app.run(host='0.0.0.0', port=5000, debug=False)

