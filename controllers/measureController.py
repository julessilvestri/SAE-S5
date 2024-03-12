import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Import controllers
from controllers.connectionController import ConnectionController

# Import models
from models.measure import Measure

class MeasureController(ConnectionController):
    RECOMMENDATIONS = {
        "°C": lambda value: "La température est trop basse" if value < 18 else ("La température est trop haute" if value > 22 else "Aucun problème de température"),
        "lx": lambda value: "La luminosité est trop faible" if value < 300 else ("La luminosité est trop élevée" if value > 500 else "Aucun problème de luminosité"),
        "ppm": lambda value: "La quantité de CO2 est trop élevée" if value > 1000 else "Aucun problème de quantité de CO2",
        "%": lambda value: "L'humidité est trop basse" if value < 40 else ("L'humidité est trop élevée" if value > 60 else "Aucun problème d'humidité"),
        "µg/m³": lambda value: "La quantité de fumée est trop élevée" if value > 10 else "Aucun problème de fumée",
        "default": "Aucune message disponible pour ce capteur"
    }

    def getRoomState(self, room):
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

                measurment = average_data['_measurement'][i]
                value = average_data['_value'][i]

                if measurment in self.RECOMMENDATIONS:
                    recommendation = self.RECOMMENDATIONS[measurment](value)
                else:
                    recommendation = self.RECOMMENDATIONS["default"]

                data.append(Measure(value, measurment, recommendation))

            return data
        
        except Exception as e:
            print("An unexpected error occurred:", e)
    
    def getMeasure(self, room, sensor):
        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start: -2d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["entity_id"] =~/^' + room + '/)\
                |> filter(fn: (r) => r["_measurement"] =~/^' + sensor + '/)\
                |> group(columns: ["_measurement", "entity_id"])\
                |> last(column: "_value")\
                |> yield(name: "mean")'
            
            roomData = self.query_api.query_data_frame(org=self.org, query=query)

            average_data = roomData.groupby('_measurement')['_value'].mean().reset_index()

            for i in range(len(average_data['_measurement'])):
                measurment = average_data['_measurement'][i]
                value = average_data['_value'][i]

                if measurment in self.RECOMMENDATIONS:
                    recommendation = self.RECOMMENDATIONS[measurment](value)
                else:
                    recommendation = self.RECOMMENDATIONS["default"]
            return Measure(value, measurment, recommendation)
        
        except Exception as e:
            print("An unexpected error occurred:", e)

    def getMeasuresByRoomName(self, room):
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

                measurement = average_data['_measurement'][i]
                value = average_data['_value'][i]

                if measurement in self.RECOMMENDATIONS:
                    recommendation = self.RECOMMENDATIONS[measurement](value)
                else:
                    recommendation = self.RECOMMENDATIONS["default"]

                data.append(Measure(value, measurement, recommendation))
                
            return data
        
        except Exception as e:
            print("An unexpected error occurred:", e)
    
    def getRoomPresence(self, room):
        try:
            query = 'from(bucket: "' + self.bucket +'")\
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_field"] == "value")\
                |> filter(fn: (r) => r["entity_id"] =~/^' + room + '/)\
                |> group(columns: ["_measurement", "entity_id"])\
                |> last(column: "_value")\
                |> yield(name: "mean")'
            
            roomData = self.query_api.query_data_frame(org=self.org, query=query)

            average_data = roomData.groupby('_measurement')['_value'].mean().reset_index()
            data = []

            for i in range(len(average_data['_measurement'])):
                measurment = average_data['_measurement'][i]
                value = average_data['_value'][i]

                if measurment in self.RECOMMENDATIONS:
                    recommendation = self.RECOMMENDATIONS[measurment](value)
                else:
                    recommendation = self.RECOMMENDATIONS["default"]

                data.append(Measure(value, measurment, recommendation))
            
            def intervale_min(measurement):
                return {"lx": 0, "dB": 20, "ppm": 10}.get(measurement, None)    

            def intervale_max(measurement):
                return {"lx": 700, "dB": 90, "ppm": 1000}.get(measurement, None)

            def normalize_value(value, min_val, max_val):
                return (value - min_val) / max_val if min_val is not None and max_val is not None else 0

            coefficients = {"lx": 10, "dB": 85, "ppm": 5}

            norm_values = {mesure.measurement: normalize_value(mesure.value, intervale_min(mesure.measurement), intervale_max(mesure.measurement)) * coefficients.get(mesure.measurement, 0) for mesure in data if mesure.measurement in ["lx", "dB", "ppm"]}

            presence_percentage = sum(norm_values.values())

            return f"{round(presence_percentage, 0)}% de chance de présence dans la salle"
        
        except Exception as e:
            print("An unexpected error occurred:", e)   

