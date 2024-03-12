# -----=====|  |=====-----
# Create by Jules - 12/2023
# -----=====|  |=====-----

# Import library
from flask import Flask, jsonify, make_response, Response
from flasgger import Swagger
from flask_cors import CORS
import os, shutil

# Import controllers
from controllers.roomController import RoomController
from controllers.sensorController import SensorController
from controllers.measurementController import MeasurementController
from controllers.measureController import MeasureController
from controllers.iaController import IaController

# Import files
from helpers.exceptions import *

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

@app.route("/rooms", methods=["GET"])
def getRooms():
    
  """
    Récupérer toutes les salles.

    ---
    tags:
      - GET
    responses:
      200:
        description: Informations concernant toutes les salles
      500:
        description: Erreur interne du serveur
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
    Récupérer tous les capteurs.

    ---
    tags:
      - GET
    responses:
      200:
        description: Informations concernant toutes les capteurs
      500:
        description: Erreur interne du serveur
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
    Récupérer un capteur par son nom.

    ---
    tags:
      - GET
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Nom du capteur
    responses:
      200:
        description: Information du capteur
      500:
        description: Erreur interne du serveur
  """

  try:
    sensors = SensorController().getSensor(name)
    print(sensors)
    if sensors :
      return jsonify([{"name": sensor.name, "measurement": sensor.measurement, "room": sensor.room} for sensor in sensors])
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)

@app.route("/rooms/<string:room>/sensors", methods=["GET"])
def getSensorsByRoom(room):

  """
  Récupérer tous les capteur d'une salle.

  ---
  tags:
    - GET
  parameters:
    - name: room
      in: path
      type: string
      required: true
      description: Nom de la salle
  responses:
    200:
      description: Information de la salle
    500:
      description: Erreur interne du serveur
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
  Récupérer tous les mesurements.

  ---
  tags:
    - GET
  responses:
    200:
      description: Information de tous les mesurements
    500:
      description: Erreur interne du serveur
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
  Récupérer l'état de la salle.

  ---
  tags:
    - GET
  parameters:
    - name: room
      in: path
      type: string
      required: true
      description: NNom de la salle
  responses:
    200:
      description: Informations de la salle
    500:
      description: Erreur interne du serveur
  """

  try:
    measures = MeasureController().getRoomState(room)
    if measures:
      return jsonify([{"measurement": measure.measurement, "value" : measure.value, "recommendation" : measure.recommendation} for measure in measures])
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)
  
@app.route("/rooms/<string:room>/presence", methods=["GET"])
def getPresenceByRoomName(room):

  """
  Récupérer les chances de présence d'une ou plusieurs personnes dans la salle.

  ---
  tags:
    - GET
  parameters:
    - name: room
      in: path
      type: string
      required: true
      description: Name de la salle
  responses:
    200:
      description:  Informations de présence
    500:
      description: Erreur interne du serveur
  """

  try:
    presence = MeasureController().getRoomPresence(room)
    if presence:
      return jsonify([{"result": presence}])
    return NotFoundException()
  except Exception as e:
    return InternalServerError(e)

@app.route("/rooms/<string:room>/state/<string:measurement>", methods=["GET"])
def getMeasuresByRoomAndMeasurement(room, measurement):

  """
  Récupérer la mesure d'un mesurement dans une salle.

  ---
  tags:
    - GET
  parameters:
    - name: room
      in: path
      type: string
      required: true
      description: Nom de la salle
    - name: measurement
      in: path
      type: string
      required: true
      description: Nom du mesurement
  responses:
    200:
      description: Informations de la salle
    500:
      description: Erreur interne du serveur 
  """

  try:
    measure = MeasureController().getMeasure(room, measurement)
    if measure :
      return jsonify({"measurement": measure.measurement, "value" : measure.value, "recommendation" : measure.recommendation})
    return NotFoundException()    
  except Exception as e:
    return InternalServerError(e)

@app.route("/rooms/sensors", methods=["GET"])
def getRoomsSensorsList():

  """
    Récupère la liste des capteurs disponible par salle.

    ---
    tags:
      - GET
    responses:
      200:
        description: Liste de toutes les salles avec leur capteur associés
      404:
        description: Aucune salle trouvée
      500:
        description: Erreur interne du serveur
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
             "measurement": sensor.measurement,
             "recommendation": sensor.recommendation,
             "date": sensor.date
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

@app.route("/predictTemperature/<int:year>/<int:month>/<int:day>", methods=["GET"])
def getPredictTemperature(year, month, day):

  """
    Récupérer la prédiction de température générale générée par apprentissage.

    ---
    tags:
      - GET
    parameters:
      - name: year
        in: path
        type: integer
        required: true
        description: Année
      - name: month
        in: path
        type: integer
        required: true
        description: Mois
      - name: day
        in: path
        type: integer
        required: true
        description: Jours
    responses:
      200:
        description: Température prédit en fonction de la date passée en paramètres
      404:
        description: Aucune prediction trouvée
      500:
        description: Erreur interne du serveur
  """

  try:
    return jsonify(IaController().getPredictTemperature(year, month, day))
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

