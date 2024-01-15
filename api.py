# Import library
from flask import Flask, jsonify
from flasgger import Swagger
from flask_cors import CORS

# Import controllers
from controllers.roomController import RoomController
from controllers.sensorController import SensorController

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/rooms", methods=["GET"])
def getRoomList():

    """
    Get room list.

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
        rooms = RoomController().getRoomList()
        if rooms :
            data = [{"label": room.label} for room in rooms]
        else :
            data = {"error": "Rooms not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500

@app.route("/rooms/<string:name>", methods=["GET"])
def getRoomById(name):

    """
    Get room by name.

    ---
    tags:
      - GET
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: ID of the room
    responses:
      200:
        description: Information for room
      500:
        description: Internal server error
    """

    try:
        room = RoomController().getById(name)
        if room :
            data = {"label": room.label}
        else :
            data = {"error": "Room not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500
    
@app.route("/sensors", methods=["GET"])
def getSensorsList():

    """
    Get sensors list.

    ---
    tags:
      - GET
    responses:
      200:
        description: Information for room
      500:
        description: Internal server error
    """

    try:
        sensors = SensorController().getSensorsList()
        if sensors :
            data = [{"label": sensor.label} for sensor in sensors]
        else :
            data = {"error": "Sensors not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500
    


@app.route("/sensors/<string:name>", methods=["GET"])
def getNameSensorsByName(name):

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
        description: ID of the room
    responses:
      200:
        description: Information for room
      500:
        description: Internal server error
    """

    try:
        sensor = SensorController().getNameSensorsByName(name)
        if sensor :
            data = {"label": sensor}
        else :
            data = {"error": "Room not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500
    

@app.route("/room/<string:room>/sensors", methods=["GET"])
def getListSensorByRoom(room):

    """
    Get sensors list by room.

    ---
    tags:
      - GET
    parameters:
      - name: room
        in: path
        type: string
        required: true
        description: ID of the room
    responses:
      200:
        description: Information for room
      500:
        description: Internal server error
    """

    try:
        sensors = SensorController().getListSensorByRoom(room)
        if sensors :
            data = [{"label": sensor} for sensor in sensors]
        else :
            data = {"error": "Sensors not found"}, 404
        return jsonify(data)
    except Exception as e:
            return f"Erreur interne du serveur : {str(e)}", 500
     
                
# un capteur par id
# tous les types capteurs (température, humidity, co2 etc...)
# tous les types capteurs par salle

# mesures
    