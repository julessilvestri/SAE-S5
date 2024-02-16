# -----=====|  |=====-----
# Create by Jules - 12/2023
# -----=====|  |=====-----

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.measure import Measure

class MeasureController(ConnectionController):
    RECOMMENDATIONS = {
        "°C": lambda value: "La température est trop basse" if value < 18 else ("La température est trop haute" if value > 22 else "Aucun problème de température"),
        "lx": lambda value: "La luminosité est trop faible" if value < 300 else ("La luminosité est trop élevée" if value > 500 else "Aucun problème de luminosité"),
        "ppm": lambda value: "La quantité de CO2 est trop élevée" if value > 1000 else "Aucun problème de quantité de CO2",
        "%": lambda value: "L'humidité est trop basse" if value < 40 else ("L'humidité est trop élevée" if value > 60 else "Aucun problème d'humidité"),
        "µg/m³": lambda value: "La quantité de fumée est trop élevée" if value > 10 else "Aucun problème de fumée",
        "default": "Aucune message disponible pour ce capteur"
    }

    def getMeasuresByRoomName(self, room):
        """
            Récupère l'état d'une pièce spécifique depuis InfluxDB pour les 48 dernières heures.

            Args:
                self (object): Instance de la classe.
                room (str): Nom de la pièce à interroger dans InfluxDB.

            Returns:
                list: Une liste d'objets Measure représentant les valeurs moyennes des mesures de la pièce spécifiée.

            Raises:
                Exception: Si une erreur inattendue se produit lors de la récupération des données.
        """

        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start: -2d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["entity_id"] =~/^' + room + '/)\
                |> group(columns: ["_measurement", "entity_id"])\
                |> last(column: "_value")\
                |> yield(name: "mean")'
            
            roomData = self.query_api.query_data_frame(org=self.org, query=query)

            print(roomData)

            average_data = roomData.groupby('_measurement')['_value'].mean().reset_index()
            data = []

            for i in range(len(average_data['_measurement'])):

                measurement = average_data['_measurement'][i]
                value = average_data['_value'][i]
                time = average_data['_time'][i]

                # print("===================")
                # print(time)
                # print("===================")

                if measurement in self.RECOMMENDATIONS:
                    recommendation = self.RECOMMENDATIONS[measurement](value)
                else:
                    recommendation = self.RECOMMENDATIONS["default"]

                data.append(Measure(value, measurement, recommendation, time))
                
            return data
        
        except Exception as e:
            print("An unexpected error occurred:", e)
    
    def getMeasuresByRoomAndMeasurement(self, room, measurement):
        """
            Récupère la dernière mesure d'un capteur spécifique dans une pièce donnée depuis InfluxDB pour les 48 dernières heures.

            Args:
                self (object): Instance de la classe.
                room (str): Nom de la pièce à interroger dans la base de données.
                sensor (str): Nom du capteur à interroger dans la base de données.

            Returns:
                Measure: Un objet Measure représentant la dernière mesure du capteur spécifié dans la pièce donnée.

            Raises:
                Exception: Si une erreur inattendue se produit lors de la récupération des données.
        """

        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start: -2d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["entity_id"] =~/^' + room + '/)\
                |> filter(fn: (r) => r["_measurement"] =~/^' + measurement + '/)\
                |> group(columns: ["_measurement", "entity_id"])\
                |> last(column: "_value")\
                |> yield(name: "mean")'
            
            roomData = self.query_api.query_data_frame(org=self.org, query=query)

            average_data = roomData.groupby('_measurement')['_value'].mean().reset_index()

            for i in range(len(average_data['_measurement'])):
                measurement = average_data['_measurement'][i]
                value = average_data['_value'][i]

                if measurement in self.RECOMMENDATIONS:
                    recommendation = self.RECOMMENDATIONS[measurement](value)
                else:
                    recommendation = self.RECOMMENDATIONS["default"]

            return Measure(value, measurement, recommendation)
        
        except Exception as e:
            print("An unexpected error occurred:", e)
