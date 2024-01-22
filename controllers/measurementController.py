# Import library
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import models
from models.measurement import Measurement

class MeasurementController:
    def __init__(self):
        self.bucket = "IUT_BUCKET"
        self.org = "INFO"
        self.token = "q4jqYhdgRHuhGwldILZ2Ek1WzGPhyctQ3UgvOII-bcjEkxqqrIIacgePte33CEjekqsymMqWlXnO0ndRhLx19g=="
        self.url = "http://51.83.36.122:8086/"

    def getList(self):
        try:
            client = influxdb_client.InfluxDBClient(
                self.url,
                self.token,
                self.org
            )

            if client.health().status == 'pass':
                print("Connexion à la base de données réussie")
            else:
                print("Échec de la connexion à la base de données")

            query_api = client.query_api()

            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start: 2023-01-01T00:00:00Z, stop: 2024-01-11T23:59:59Z)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> distinct(column: "_measurement")\
                |> yield(name: "mean")'


            try:
                measurements = query_api.query_data_frame(org=self.org, query=query)

                data = []

                for measurement_name in measurements['_measurement']:
                    item = Measurement(measurement_name)
                    data.append(item)

                return data
            except Exception as e:
                print(f"Erreur requête flux : {e}")
        except:
            print("Erreur connexion à InfluxDB")
