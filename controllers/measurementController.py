# -----=====|  |=====-----
# Create by Jules - 12/2023
# -----=====|  |=====-----

# Import library
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.measurement import Measurement

class MeasurementController(ConnectionController):
    
    def getMeasurements(self):
        """
            Récupère une liste de mesures distinctes depuis InfluxDB pour le seau spécifié dans les 30 derniers jours.

            Args:
                self (objet): Instance de la classe.
                
            Returns:
                list: Une liste d'objets Measurement représentant des mesures distinctes.
                
            Raises:
                RuntimeError: S'il y a une erreur lors de la requête de données depuis InfluxDB.
                Exception: S'il y a une erreur inattendue pendant l'exécution.
        """

        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> group()\
                |> distinct(column: "_measurement")\
                |> keep(columns: ["_value"])'

            try:
                measurements = self.query_api.query_data_frame(org=self.org, query=query)

                data = []                

                for measurement in measurements["_value"]:
                    item = Measurement(measurement)
                    data.append(item)

                return data
            except Exception as e:
                print(f"Erreur requête flux : {e}")
        except:
            print("Erreur connexion à InfluxDB")
