# Import library
import influxdb_client, os
from dotenv import load_dotenv
from influxdb_client.client.write_api import SYNCHRONOUS

class ConnectionController:
    def __init__(self):
        try:
            load_dotenv()

            self.bucket = os.getenv("INFLUX_BUCKET")
            self.org = os.getenv("INFLUX_ORG")
            self.token = os.getenv("INFLUX_TOKEN")
            self.url = os.getenv("INFLUX_URL")

            self.client = influxdb_client.InfluxDBClient(
                self.url,
                self.token,
                self.org
            )

            if self.client.health().status != 'pass':
                raise Exception()

            self.query_api = self.client.query_api()

        except Exception as e:
           return f"Erreur connexion à influxDB : {e}"
