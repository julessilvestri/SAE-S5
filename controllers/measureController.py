import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.measure import Measure

class MeasureController(ConnectionController):
     
    def getState(self, room):
        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start: -2d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["entity_id"] =~/^' + room + '/)\
                |> group(columns: ["_measurement", "entity_id"])\
                |> last(column: "_value")\
                |> yield(name: "mean")'
            
            roomData = self.query_api.query_data_frame(org=self.org, query=query)

            average_data = roomData.groupby('_measurement')['_value'].mean().reset_index()
            data = []

            for i in range(len(average_data['_measurement'])):
                data.append(Measure(average_data['_value'][i], average_data['_measurement'][i]))

            return data
        
        except:
            print("Error connecting to InfluxDB")