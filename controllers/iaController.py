import joblib
from datetime import datetime, timedelta
import numpy as np

class IaController() :
    def getPredictTemperature(self, year, month, day) :
        loaded_model = joblib.load('ressources/ia/model.pkl')

        def normalizeInputModel(timestamp):
            year = datetime.fromtimestamp(timestamp).year
            start = datetime(year, 1, 1).timestamp()
            end = datetime(year+1, 1, 1).timestamp()
            return (timestamp-start)/(end-start)

        def KelvinToCelsius(temperature):
            return temperature - 273.15

        input_timestamp = int(datetime(year, month, day).timestamp())
        current_timestamp = int(datetime.now().timestamp())

        inputs = np.array([
            current_timestamp,
            input_timestamp
        ])

        inputs = list(map(lambda input: [normalizeInputModel(input)], inputs))
        results = loaded_model.predict(inputs)
        results = list(map(lambda temperature: KelvinToCelsius(temperature[0]), results))

        return results