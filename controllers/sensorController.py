# Import library
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.sensor import Sensor

class SensorController(ConnectionController):
        
    def getList(self):
        try:
            query_api = self.client.query_api()

            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start:-30d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["domain"] == "sensor" or r["domain"] == "binary_sensor")\
                |> distinct(column: "entity_id")\
                |> yield(name: "mean")'

            try:
                sensors = query_api.query_data_frame(org=self.org, query=query)

                data = []

                for index, sensor in sensors.iterrows():
                    item = Sensor(sensor['entity_id'], sensor['_measurement'], sensor['entity_id'].split('_')[0])
                    data.append(item)

                return data
            except Exception as e:
                print(f"Erreur requête flux : {e}")
        except:
            print("Erreur connexion à InfluxDB")


    def getByName(self, name):
            try:
                query_api = self.client.query_api()

                query = 'from(bucket: "' + self.bucket +'")\
                    |> range(start:-30d)\
                    |> filter(fn: (r) => r["_field"] == "value")\
                    |> filter(fn: (r) => r["entity_id"] == "' + name + '")\
                    |> distinct(column: "entity_id")\
                    |> yield(name: "mean")'

                try:
                    sensors = query_api.query_data_frame(org=self.org, query=query)

                    data = []

                    for index, sensor in sensors.iterrows():
                        item = Sensor(sensor['entity_id'], sensor['_measurement'], sensor['entity_id'].split('_')[0])
                        data.append(item)

                    return data
                except Exception as e:
                    print(f"Erreur requête flux : {e}")
            except:
                print("Erreur connexion à InfluxDB")


    def getListByRoom(self, room):
            try:
                query_api = self.client.query_api()

                query = 'from(bucket: "' + self.bucket +'")\
                    |> range(start:-30d)\
                    |> filter(fn: (r) => r["_field"] == "value")\
                    |> filter(fn: (r) => r["entity_id"] =~ /^' + room + '/)\
                    |> distinct(column: "entity_id")\
                    |> yield(name: "mean")'

                try:
                    sensors = query_api.query_data_frame(org=self.org, query=query)

                    data = []

                    for index, sensor in sensors.iterrows():
                        item = Sensor(sensor['entity_id'], sensor['_measurement'], sensor['entity_id'].split('_')[0])
                        data.append(item)

                    return data
                except Exception as e:
                    print(f"Erreur requête flux : {e}")
            except:
                print("Erreur connexion à InfluxDB")
