# Import library
from flask import Flask, jsonify, make_response
from flasgger import Swagger
from flask_cors import CORS

# Import controllers
from controllers.roomController import RoomController
from controllers.sensorController import SensorController
from controllers.measurementController import MeasurementController

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)

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
        print("Rooms : ")
        print(rooms)
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
            data = [{"name": sensor.name, "measurements": sensor.measurements, "room": sensor.room} for sensor in sensors], 200
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