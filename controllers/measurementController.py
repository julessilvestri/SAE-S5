# Import library
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.measurement import Measurement

class MeasurementController(ConnectionController):

    def getList(self):
        try:
            query_api = self.client.query_api()

            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start:-30d)\
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
