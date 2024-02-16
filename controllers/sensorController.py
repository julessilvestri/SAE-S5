# -----=====|  |=====-----
# Create by Jules - 12/2023
# -----=====|  |=====-----

# Import library
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.sensor import Sensor

class SensorController(ConnectionController):
        
    def getSensors(self):
        """
            Récupère une liste de tous les capteurs enregistrés dans la base de données InfluxDB au cours des 30 derniers jours.

            Args:
                self (object): Instance de la classe.

            Returns:
                list: Une liste d'objets Sensor représentant tous les capteurs enregistrés dans la base de données.

            Raises:
                RuntimeError: Si une erreur se produit lors de la requête de données depuis InfluxDB.
        """

        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start:-30d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["domain"] == "sensor" or r["domain"] == "binary_sensor")\
                |> distinct(column: "entity_id")\
                |> yield(name: "mean")'

            try:
                sensors = self.query_api.query_data_frame(org=self.org, query=query)

                data = []

                for index, sensor in sensors.iterrows():
                    item = Sensor(sensor['entity_id'], sensor['_measurement'], sensor['entity_id'].split('_')[0])
                    data.append(item)

                return data
            except Exception as e:
                print(f"Erreur requête flux : {e}")
        except:
            print("Erreur connexion à InfluxDB")


    def getSensor(self, name):
        """
            Récupère une liste de capteurs enregistrés dans la base de données InfluxDB qui ont un nom spécifique.

            Args:
                self (object): Instance de la classe.
                name (str): Nom du capteur à rechercher dans la base de données.

            Returns:
                list: Une liste d'objets Sensor représentant les capteurs trouvés avec le nom spécifié.

            Raises:
                RuntimeError: Si une erreur se produit lors de la requête de données depuis InfluxDB.
        """

        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start:-30d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["entity_id"] == "' + name + '")\
                |> distinct(column: "entity_id")\
                |> yield(name: "mean")'
            
            try:
                sensors = self.query_api.query_data_frame(org=self.org, query=query)

                data = []

                for index, sensor in sensors.iterrows():
                    item = Sensor(sensor['entity_id'], sensor['_measurement'], sensor['entity_id'].split('_')[0])
                    data.append(item)

                return data
            except Exception as e:
                print(f"Erreur requête flux : {e}")
        except:
            print("Erreur connexion à InfluxDB")

    def getSensorsByRoom(self, room):
        """
        Récupère une liste de capteurs enregistrés dans la base de données InfluxDB pour une pièce spécifique.

        Args:
            self (object): Instance de la classe.
            room (str): Nom de la pièce pour laquelle récupérer les capteurs.

        Returns:
            list: Une liste d'objets Sensor représentant les capteurs enregistrés dans la pièce spécifiée.

        Raises:
            RuntimeError: Si une erreur se produit lors de la requête de données depuis InfluxDB.
        """
        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start:-30d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["entity_id"] =~ /^' + room + '/)\
                |> distinct(column: "entity_id")\
                |> yield(name: "mean")'

            try:
                sensors = self.query_api.query_data_frame(org=self.org, query=query)

                data = []

                for index, sensor in sensors.iterrows():
                    if sensor['entity_id'] and sensor['_measurement'] and sensor['entity_id'].split('_')[0]:
                        data.append(Sensor(sensor['entity_id'], sensor['_measurement'], sensor['entity_id'].split('_')[0]))

                return data
            except Exception as e:
                print(f"Erreur requête flux : {e}")
                raise RuntimeError("Erreur lors de la requête des capteurs")
        except Exception as e:
            print("Erreur connexion à InfluxDB")
            raise RuntimeError("Erreur de connexion à InfluxDB")

