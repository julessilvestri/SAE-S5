import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.room import Room

class RoomController(ConnectionController):
        
    def getAll(self):
        try:
            query = 'from(bucket: "' + self.bucket +'")\
            |> range(start:-30d)\
            |> filter(fn: (r) => r["_field"] == "value")\
            |> distinct(column: "_measurement")\
            |> yield(name: "mean")'

            try:
                rooms_data = self.query_api.query_data_frame(org=self.org, query=query)

                data = []
                
                for index, room in rooms_data.iterrows():
                    entity_id = room["entity_id"].split("_")[0]
                    locate = "IUT" if entity_id.startswith("d") else "TETRAS"
                    currentRoom = Room(entity_id, locate)
                    exist = False
                    for room in data:
                        if currentRoom.name == room.name:
                            exist = True
                            break
                    if not exist:
                        data.append(currentRoom)

                return data
            except Exception as e:
                print(f"Query error: {e}")
        except:
            print("Error connecting to InfluxDB")
