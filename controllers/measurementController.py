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
