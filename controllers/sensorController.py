# Import library
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import models
from models.sensor import Sensor


class SensorController :
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
                    |> range(start:-2d)\
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
                    |> range(start:-2d)\
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
