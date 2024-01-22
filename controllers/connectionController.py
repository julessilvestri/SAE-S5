# Import library
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

class ConnectionController:
    def __init__(self):
        try:
            self.bucket = "IUT_BUCKET"
            self.org = "INFO"
            self.token = "q4jqYhdgRHuhGwldILZ2Ek1WzGPhyctQ3UgvOII-bcjEkxqqrIIacgePte33CEjekqsymMqWlXnO0ndRhLx19g=="
            self.url = "http://51.83.36.122:8086/"

            self.client = influxdb_client.InfluxDBClient(
                self.url,
                self.token,
                self.org
            )

            if self.client.health().status != 'pass':
                raise Exception()
        except Exception as e:
           return f"Erreur connexion à influxDB : {e}"
